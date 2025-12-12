#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - Environment Initializer
    Auto-installs dependencies, validates setup, and prepares framework
═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
import os
from pathlib import Path

class EnvironmentInitializer:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.success_count = 0
        self.failed_count = 0
    
    def print_header(self, text):
        """Print formatted header"""
        print(f"\n{'═' * 70}")
        print(f"  {text}")
        print(f"{'═' * 70}\n")
    
    def install_package(self, package_name, import_name=None):
        """Install a single package"""
        if import_name is None:
            import_name = package_name.lower()
        
        try:
            __import__(import_name.replace('-', '_'))
            print(f"  ✓ {package_name:.<40} already installed")
            self.success_count += 1
            return True
        except ImportError:
            try:
                print(f"  ↳ {package_name:.<40} installing...", end='', flush=True)
                subprocess.check_call(
                    [sys.executable, '-m', 'pip', 'install', '-q', package_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(" ✓")
                self.success_count += 1
                return True
            except Exception as e:
                print(f" ✗ failed")
                self.failed_count += 1
                return False
    
    def verify_core_dependencies(self):
        """Install core dependencies for framework"""
        self.print_header("Installing Core Dependencies")
        
        core_packages = [
            ('pyyaml', 'yaml'),
            ('cryptography', 'cryptography'),
            ('flask', 'flask'),
            ('requests', 'requests'),
        ]
        
        for package, import_name in core_packages:
            self.install_package(package, import_name)
    
    def verify_agent_dependencies(self):
        """Install optional agent dependencies"""
        self.print_header("Installing Agent Optional Dependencies")
        print("  (Some packages are Windows-only - skipping if platform doesn't support)\n")
        
        optional_packages = [
            'psutil',
            'pillow',
            'opencv-python',
            'pynput',
            'cryptography',
            'requests',
            'numpy',
        ]
        
        for package in optional_packages:
            try:
                self.install_package(package, package.replace('-', '_'))
            except:
                print(f"  ⊘ {package:.<40} skipped (optional)")
    
    def verify_bot_dependencies(self):
        """Install WhatsApp bot dependencies"""
        self.print_header("Installing WhatsApp Bot Dependencies")
        
        # Check if Node.js is installed
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
            print("  ✓ Node.js is installed\n")
            
            # Try to install npm packages
            bot_dir = self.workspace / 'whatsapp-c2'
            if bot_dir.exists():
                print("  ↳ Installing npm packages in whatsapp-c2/...", end='', flush=True)
                try:
                    subprocess.run(
                        ['npm', 'install'],
                        cwd=bot_dir,
                        capture_output=True,
                        timeout=60
                    )
                    print(" ✓")
                except Exception as e:
                    print(f" ✗ (run: cd whatsapp-c2 && npm install)")
        except FileNotFoundError:
            print("  ⊘ Node.js not installed")
            print("     Download from: https://nodejs.org/")
    
    def verify_configuration(self):
        """Check if configuration file exists"""
        self.print_header("Verifying Configuration")
        
        config_file = self.workspace / 'umbrella_config.yaml'
        if config_file.exists():
            print(f"  ✓ Configuration file found: {config_file}")
            return True
        else:
            print(f"  ✗ Configuration file missing: {config_file}")
            print("     This will be created on first run")
            return False
    
    def verify_database(self):
        """Check if database directory exists"""
        self.print_header("Verifying Database")
        
        data_dir = self.workspace / 'data'
        data_dir.mkdir(exist_ok=True)
        print(f"  ✓ Data directory ready: {data_dir}")
    
    def run_tests(self):
        """Run basic import tests"""
        self.print_header("Running Import Tests")
        
        test_imports = [
            ('master_umbrella_setup', 'ConfigLoader'),
            ('agent_registry', 'AgentRegistry'),
            ('communication_managers', 'HeartbeatManager'),
            ('command_executor', 'CommandExecutor'),
            ('api_bridge', 'APIBridge'),
            ('rest_api_server', 'app'),
        ]
        
        for module_name, class_name in test_imports:
            try:
                module = __import__(module_name)
                if hasattr(module, class_name):
                    print(f"  ✓ {module_name}.{class_name}")
                    self.success_count += 1
                else:
                    print(f"  ✗ {module_name}.{class_name} not found")
                    self.failed_count += 1
            except Exception as e:
                print(f"  ✗ {module_name} - {str(e)[:40]}")
                self.failed_count += 1
    
    def print_summary(self):
        """Print initialization summary"""
        self.print_header("Initialization Summary")
        
        print(f"  ✓ Successful: {self.success_count}")
        print(f"  ✗ Failed: {self.failed_count}")
        
        if self.failed_count == 0:
            print("\n  🎉 Framework is ready to use!")
            print("\n  Next steps:")
            print("    1. python startup.py server    # Start C2 server")
            print("    2. python startup.py bot       # Start WhatsApp bot")
            print("    3. python startup.py agent     # Build agent executable")
            return True
        else:
            print("\n  ⚠️  Some setup steps failed. See above for details.")
            return False
    
    def run(self):
        """Run complete initialization"""
        print("\n")
        print("╔" + "═" * 68 + "╗")
        print("║" + " " * 15 + "T0OL-B4S3-263 Environment Setup" + " " * 22 + "║")
        print("╚" + "═" * 68 + "╝")
        
        self.verify_core_dependencies()
        self.verify_agent_dependencies()
        self.verify_bot_dependencies()
        self.verify_configuration()
        self.verify_database()
        self.run_tests()
        
        return self.print_summary()

if __name__ == '__main__':
    initializer = EnvironmentInitializer()
    success = initializer.run()
    sys.exit(0 if success else 1)
