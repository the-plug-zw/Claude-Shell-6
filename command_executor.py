"""
═══════════════════════════════════════════════════════════════════════════
REAL COMMAND EXECUTOR
Execute actual commands instead of simulating them
═══════════════════════════════════════════════════════════════════════════
"""

import subprocess
import os
import sys
import base64
import json
from typing import Dict, Tuple, Optional
from pathlib import Path

class CommandExecutor:
    """Execute real commands and return results"""
    
    def __init__(self):
        """Initialize executor"""
        self.shell = 'cmd.exe' if sys.platform == 'win32' else '/bin/bash'
    
    def execute_command(self, command: str, timeout: int = 30) -> Dict:
        """Execute command and return result"""
        try:
            if sys.platform == 'win32':
                # Windows: use cmd.exe
                result = subprocess.run(
                    [self.shell, '/c', command],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            else:
                # Linux/Mac: use bash
                result = subprocess.run(
                    [self.shell, '-c', command],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            
            return {
                'status': 'success',
                'command': command,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode,
            }
        
        except subprocess.TimeoutExpired:
            return {
                'status': 'timeout',
                'command': command,
                'error': f'Command timed out after {timeout}s'
            }
        except Exception as e:
            return {
                'status': 'error',
                'command': command,
                'error': str(e)
            }
    
    def get_system_info(self) -> Dict:
        """Get system information"""
        try:
            info = {
                'hostname': subprocess.run(['hostname'], 
                                         capture_output=True, text=True).stdout.strip(),
                'username': os.getenv('USERNAME', 'UNKNOWN'),
                'platform': sys.platform,
            }
            
            if sys.platform == 'win32':
                # Windows
                info['os'] = self.execute_command('ver')['stdout']
            else:
                # Linux/Mac
                info['os'] = self.execute_command('uname -a')['stdout']
            
            return info
        except Exception as e:
            return {'error': str(e)}
    
    def read_file(self, filepath: str) -> Dict:
        """Read file contents"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            return {
                'status': 'success',
                'filepath': filepath,
                'content': content,
                'size': len(content)
            }
        except Exception as e:
            return {
                'status': 'error',
                'filepath': filepath,
                'error': str(e)
            }
    
    def write_file(self, filepath: str, content: str, append: bool = False) -> Dict:
        """Write file contents"""
        try:
            mode = 'a' if append else 'w'
            with open(filepath, mode, encoding='utf-8') as f:
                f.write(content)
            
            return {
                'status': 'success',
                'filepath': filepath,
                'size': len(content)
            }
        except Exception as e:
            return {
                'status': 'error',
                'filepath': filepath,
                'error': str(e)
            }
    
    def list_directory(self, path: str = '.') -> Dict:
        """List directory contents"""
        try:
            items = []
            for item in Path(path).iterdir():
                items.append({
                    'name': item.name,
                    'type': 'dir' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else 0,
                })
            
            return {
                'status': 'success',
                'path': path,
                'items': items,
                'count': len(items)
            }
        except Exception as e:
            return {
                'status': 'error',
                'path': path,
                'error': str(e)
            }
    
    def get_process_list(self) -> Dict:
        """Get list of running processes"""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    ['tasklist', '/v'],
                    capture_output=True,
                    text=True
                )
                return {
                    'status': 'success',
                    'processes': result.stdout.strip().split('\n')
                }
            else:
                result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True
                )
                return {
                    'status': 'success',
                    'processes': result.stdout.strip().split('\n')
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_network_info(self) -> Dict:
        """Get network configuration"""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(
                    ['ipconfig', '/all'],
                    capture_output=True,
                    text=True
                )
                return {
                    'status': 'success',
                    'config': result.stdout
                }
            else:
                result = subprocess.run(
                    ['ifconfig'],
                    capture_output=True,
                    text=True
                )
                return {
                    'status': 'success',
                    'config': result.stdout
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def kill_process(self, pid: int) -> Dict:
        """Kill a process"""
        try:
            if sys.platform == 'win32':
                subprocess.run(['taskkill', '/PID', str(pid), '/F'],
                             capture_output=True)
            else:
                subprocess.run(['kill', '-9', str(pid)],
                             capture_output=True)
            
            return {
                'status': 'success',
                'pid': pid,
                'message': 'Process killed'
            }
        except Exception as e:
            return {
                'status': 'error',
                'pid': pid,
                'error': str(e)
            }
    
    def get_current_user(self) -> Dict:
        """Get current user information"""
        try:
            username = os.getenv('USERNAME', 'UNKNOWN')
            
            if sys.platform == 'win32':
                domain = os.getenv('USERDOMAIN', 'LOCAL')
                user_full = f"{domain}\\{username}"
            else:
                user_full = username
            
            return {
                'status': 'success',
                'username': username,
                'user_full': user_full,
                'home_dir': str(Path.home()),
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }


if __name__ == '__main__':
    executor = CommandExecutor()
    
    # Test command execution
    print("✅ Testing CommandExecutor")
    print("═" * 50)
    
    # System info
    info = executor.get_system_info()
    print(f"✓ System Info: {info['hostname']}")
    
    # Process list
    procs = executor.get_process_list()
    print(f"✓ Process List: {len(procs['processes'])} processes")
    
    # Network info
    net = executor.get_network_info()
    print(f"✓ Network Info: {len(net['config'])} bytes")
    
    # Current user
    user = executor.get_current_user()
    print(f"✓ Current User: {user['username']}")
    
    # Execute test command
    result = executor.execute_command('echo "test"')
    print(f"✓ Command Execution: {result['status']}")
    
    print("\n✅ CommandExecutor ready for integration")
