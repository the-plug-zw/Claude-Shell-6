#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - Quick Launcher
    Single entry point that handles everything
═══════════════════════════════════════════════════════════════════════════════
"""

import subprocess
import sys
from pathlib import Path

def main():
    workspace = Path(__file__).parent
    
    # First, ensure environment is ready
    print("Checking environment...\n")
    result = subprocess.run([sys.executable, str(workspace / 'init_environment.py')])
    
    if result.returncode != 0:
        print("\n⚠️  Environment setup failed. Cannot continue.")
        sys.exit(1)
    
    # Now run the actual startup
    print("\n" + "=" * 70)
    print("Launching RAT Framework Control Console")
    print("=" * 70)
    
    subprocess.run([sys.executable, str(workspace / 'startup.py')])

if __name__ == '__main__':
    main()
