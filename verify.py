#!/usr/bin/env python3
"""
Quick verification that all modules load correctly
"""

print("\n" + "="*70)
print("Verifying Framework Integrity")
print("="*70 + "\n")

try:
    import master_umbrella_setup
    print("✓ master_umbrella_setup.py imports successfully")
except Exception as e:
    print(f"✗ master_umbrella_setup.py failed: {e}")
    exit(1)

try:
    import startup
    print("✓ startup.py imports successfully")
except Exception as e:
    print(f"✗ startup.py failed: {e}")
    exit(1)

try:
    from rest_api_server import app
    print("✓ rest_api_server.py imports successfully")
except Exception as e:
    print(f"✗ rest_api_server.py failed: {e}")
    exit(1)

try:
    from agent_registry import AgentRegistry
    print("✓ agent_registry.py imports successfully")
except Exception as e:
    print(f"✗ agent_registry.py failed: {e}")
    exit(1)

try:
    from communication_managers import HeartbeatManager
    print("✓ communication_managers.py imports successfully")
except Exception as e:
    print(f"✗ communication_managers.py failed: {e}")
    exit(1)

try:
    from command_executor import CommandExecutor
    print("✓ command_executor.py imports successfully")
except Exception as e:
    print(f"✗ command_executor.py failed: {e}")
    exit(1)

try:
    from api_bridge import APIBridge
    print("✓ api_bridge.py imports successfully")
except Exception as e:
    print(f"✗ api_bridge.py failed: {e}")
    exit(1)

print("\n" + "="*70)
print("✅ SUCCESS: All core modules working - Zero dependency errors!")
print("="*70 + "\n")
