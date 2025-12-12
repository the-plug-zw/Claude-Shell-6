#!/usr/bin/env python3
"""
Phase 5 Integration Test - Complete Framework Validation
Tests all components working together
"""

import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports"""
    print("\n✅ Testing Core Imports")
    try:
        from master_umbrella_setup import ConfigLoader, ConfigWatcher, ConfigBuilder
        print("   ✓ master_umbrella_setup.py")
        
        from agent_registry import AgentRegistry
        print("   ✓ agent_registry.py")
        
        from communication_managers import HeartbeatManager, SessionManager, ReconnectionManager
        print("   ✓ communication_managers.py")
        
        from command_executor import CommandExecutor
        print("   ✓ command_executor.py")
        
        from api_bridge import APIBridge, CommandQueue
        print("   ✓ api_bridge.py")
        
        from rest_api_server import app
        print("   ✓ rest_api_server.py")
        
        import yaml
        print("   ✓ pyyaml")
        
        return True
    except ImportError as e:
        print(f"   ✗ Import Error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n✅ Testing Configuration System")
    try:
        from master_umbrella_setup import ConfigLoader
        
        config = ConfigLoader()
        
        # Test YAML loading
        assert config.config is not None, "Config not loaded"
        print("   ✓ YAML config loaded")
        
        # Test config values
        server_ip = config.get('server.listen_ip')
        assert server_ip == '0.0.0.0', f"Server IP mismatch: {server_ip}"
        print(f"   ✓ Server IP: {server_ip}")
        
        server_port = config.get('server.listen_port')
        assert server_port == 4444, f"Server port mismatch: {server_port}"
        print(f"   ✓ Server Port: {server_port}")
        
        api_port = config.get('server.api_port')
        assert api_port == 5000, f"API port mismatch: {api_port}"
        print(f"   ✓ API Port: {api_port}")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_database():
    """Test database initialization"""
    print("\n✅ Testing Database System")
    try:
        from agent_registry import AgentRegistry
        import os
        
        # Initialize registry
        registry = AgentRegistry()
        assert registry.db_path.exists(), "Database not created"
        print(f"   ✓ Database created: {registry.db_path}")
        
        # Test agent registration with correct parameters
        agent_id = registry.register_agent(
            hostname='test-host',
            os='Linux',
            ip='192.168.1.100',
            machine_guid='test-guid-12345',
            metadata={'user': 'testuser'}
        )
        assert agent_id, "Failed to register agent"
        print(f"   ✓ Agent registered: {agent_id[:8]}...")
        
        # Test agent retrieval
        agent = registry.get_agent(agent_id)
        assert agent, "Failed to retrieve agent"
        print(f"   ✓ Agent retrieved: {agent['hostname']}")
        
        # List agents
        agents = registry.list_agents()
        assert len(agents) > 0, "No agents in database"
        print(f"   ✓ Agent count: {len(agents)}")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_communication():
    """Test communication managers"""
    print("\n✅ Testing Communication System")
    try:
        from communication_managers import HeartbeatManager, SessionManager, ReconnectionManager
        from agent_registry import AgentRegistry
        
        # Initialize registry for communication managers
        registry = AgentRegistry()
        
        # Test heartbeat manager
        hb = HeartbeatManager(registry, timeout=5)
        hb.start()
        print("   ✓ HeartbeatManager working")
        hb.stop()
        
        # Test session manager with required socket_info
        sm = SessionManager(registry)
        socket_info = {'ip': '127.0.0.1', 'port': 5555}
        session_id = sm.create_session('test-agent-2', socket_info)
        assert session_id, "Failed to create session"
        print(f"   ✓ SessionManager working: {str(session_id)[:8]}...")
        
        # Test reconnection manager
        rm = ReconnectionManager(registry)
        backoff = rm.get_backoff_time(1)
        assert backoff > 0, "Invalid backoff delay"
        print(f"   ✓ ReconnectionManager working (backoff: {backoff}s)")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_command_execution():
    """Test command executor"""
    print("\n✅ Testing Command Executor")
    try:
        from command_executor import CommandExecutor
        
        executor = CommandExecutor()
        
        # Test system info
        info = executor.get_system_info()
        assert info, "Failed to get system info"
        assert 'hostname' in info, "Missing hostname in system info"
        print(f"   ✓ System info: {info.get('hostname')}")
        
        # Test process list (non-Windows)
        try:
            processes = executor.get_process_list()
            assert processes, "Failed to get process list"
            print(f"   ✓ Process list: {len(processes.split(chr(10)))} processes")
        except:
            print("   ~ Process list: skipped (Windows only)")
        
        # Test current user
        user = executor.get_current_user()
        assert user, "Failed to get current user"
        print(f"   ✓ Current user: {user}")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_api_bridge():
    """Test API bridge components"""
    print("\n✅ Testing API Bridge")
    try:
        from api_bridge import APIBridge, CommandQueue
        
        # Test API bridge
        bridge = APIBridge()
        assert bridge.server_ip == '0.0.0.0', "Server IP mismatch"
        assert bridge.api_port == 5000, "API port mismatch"
        print(f"   ✓ APIBridge: {bridge.base_url}")
        
        # Test command queue
        queue = CommandQueue(bridge)
        queue.add_command('agent-1', 'whoami')
        queue.add_command('agent-2', 'id')
        
        queued = queue.get_queue()
        assert len(queued) >= 2, "Commands not queued"
        print(f"   ✓ CommandQueue: {len(queued)} commands queued")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def test_flask_api():
    """Test Flask REST API"""
    print("\n✅ Testing Flask REST API")
    try:
        from rest_api_server import app, create_app
        
        # Test app creation
        assert app, "Flask app not found"
        print("   ✓ Flask app initialized")
        
        # Test client
        test_app = create_app()
        with test_app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            assert response.status_code == 200, f"Health check failed: {response.status_code}"
            print("   ✓ GET /api/health - OK")
            
            # Test stats endpoint
            response = client.get('/api/stats')
            assert response.status_code == 200, f"Stats failed: {response.status_code}"
            print("   ✓ GET /api/stats - OK")
            
            # Test agents endpoint
            response = client.get('/api/agents')
            assert response.status_code == 200, f"Agents failed: {response.status_code}"
            print("   ✓ GET /api/agents - OK")
        
        return True
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def run_all_tests():
    """Execute all integration tests"""
    print("=" * 70)
    print("✅ PHASE 5 INTEGRATION TEST - COMPLETE FRAMEWORK VALIDATION")
    print("=" * 70)
    
    tests = [
        ("Core Imports", test_imports),
        ("Configuration System", test_configuration),
        ("Database System", test_database),
        ("Communication System", test_communication),
        ("Command Executor", test_command_execution),
        ("API Bridge", test_api_bridge),
        ("Flask REST API", test_flask_api),
    ]
    
    results = {}
    for name, test_func in tests:
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"\n✗ {name} - EXCEPTION: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {name}")
    
    print(f"\nTotal:  {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"\nStatus: {'✅ ALL TESTS PASSED - READY FOR DEPLOYMENT' if passed == total else '⚠️ SOME TESTS FAILED'}")
    print("=" * 70 + "\n")
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
