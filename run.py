#!/usr/bin/env python3
"""
T0OL-B4S3-263 - RAT Framework
Simple startup command
"""

import subprocess
import sys
from pathlib import Path

def main():
    workspace = Path(__file__).parent
    
    # Run startup
    subprocess.run([sys.executable, str(workspace / 'startup.py')])

if __name__ == '__main__':
    main()
