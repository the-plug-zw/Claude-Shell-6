"""
═══════════════════════════════════════════════════════════════════════════
REST API SERVER
FastAPI endpoint for Bot-Server communication
═══════════════════════════════════════════════════════════════════════════
"""

from flask import Flask, request, jsonify
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from master_umbrella_setup import config_get
from agent_registry import AgentRegistry
from communication_managers import SessionManager

app = Flask(__name__)

# Initialize managers
try:
    registry = AgentRegistry()
    session_manager = SessionManager(registry)
except Exception as e:
    print(f"Warning: Could not initialize managers: {e}")
    registry = None
    session_manager = None

# ═══════════════════════════════════════════════════════════════════════════
# HEALTH & STATUS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health():
    """Server health check"""
    return jsonify({
        'status': 'online',
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })

@app.route('/api/stats', methods=['GET'])
def stats():
    """Server statistics"""
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    stats_data = registry.get_statistics()
    return jsonify(stats_data)

# ═══════════════════════════════════════════════════════════════════════════
# AGENT MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all agents"""
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    status = request.args.get('status')
    agents = registry.list_agents(status=status)
    
    return jsonify({'agents': agents, 'count': len(agents)})

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    """Get agent details"""
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    agent = registry.get_agent(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    return jsonify(agent)

@app.route('/api/agents/<agent_id>/status', methods=['GET'])
def agent_status(agent_id):
    """Get agent status"""
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    agent = registry.get_agent(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    sessions = session_manager.get_agent_sessions(agent_id) if session_manager else {}
    
    return jsonify({
        'agent_id': agent_id,
        'status': agent['status'],
        'last_activity': agent['last_activity'],
        'active_sessions': len(sessions)
    })

# ═══════════════════════════════════════════════════════════════════════════
# COMMAND EXECUTION
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/command/execute', methods=['POST'])
def execute_command():
    """Execute command on agent"""
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    data = request.get_json()
    agent_id = data.get('agent_id')
    command = data.get('command')
    timeout = data.get('timeout', 30)
    
    if not agent_id or not command:
        return jsonify({'error': 'Missing agent_id or command'}), 400
    
    agent = registry.get_agent(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Log command
    session_id = next(iter(session_manager.get_agent_sessions(agent_id)), None) if session_manager else None
    if session_id:
        cmd_id = registry.log_command(session_id, agent_id, command)
    
    return jsonify({
        'status': 'queued',
        'agent_id': agent_id,
        'command': command,
        'message': f'Command queued for {agent["hostname"]}'
    })

@app.route('/api/agents/<agent_id>/history', methods=['GET'])
def command_history(agent_id):
    """Get command history for agent"""
    limit = request.args.get('limit', 50, type=int)
    
    if not registry:
        return jsonify({'error': 'Registry not initialized'}), 500
    
    agent = registry.get_agent(agent_id)
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    # Return history (simplified)
    return jsonify({
        'agent_id': agent_id,
        'commands': [],  # Would query database for real history
        'limit': limit
    })

# ═══════════════════════════════════════════════════════════════════════════
# ALERTS & NOTIFICATIONS
# ═══════════════════════════════════════════════════════════════════════════

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get server alerts"""
    alert_type = request.args.get('type')
    limit = request.args.get('limit', 50, type=int)
    
    # Would query alert database in real implementation
    return jsonify({
        'alerts': [],
        'count': 0,
        'type': alert_type,
        'limit': limit
    })

@app.route('/api/alerts', methods=['POST'])
def create_alert():
    """Create alert"""
    data = request.get_json()
    
    return jsonify({
        'status': 'created',
        'alert_id': 'alert_' + str(__import__('uuid').uuid4())[:8],
        'timestamp': __import__('datetime').datetime.now().isoformat()
    })

# ═══════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# ERROR HANDLERS
# ═══════════════════════════════════════════════════════════════════════════

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# ═══════════════════════════════════════════════════════════════════════════
# APP FACTORY
# ═══════════════════════════════════════════════════════════════════════════

def create_app():
    """Create and configure Flask app for testing"""
    return app

# ═══════════════════════════════════════════════════════════════════════════
# STARTUP
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    api_port = config_get('server.api_port', 5000)
    api_ip = config_get('server.listen_ip', '0.0.0.0')
    
    print(f"✅ Starting API Server on {api_ip}:{api_port}")
    app.run(host=api_ip, port=api_port, debug=False)
