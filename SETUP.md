## 🚀 Environment Setup & Dependencies

### Quick Start (Automatic)

Simply run the auto-initialization script:

```bash
python init_environment.py
```

This will:
- ✓ Check for all required dependencies
- ✓ Install missing packages automatically
- ✓ Verify configuration files
- ✓ Create database directories
- ✓ Run basic import tests
- ✓ Provide next steps

### Or use the launcher:

```bash
python launch.py
```

This combines environment setup + startup in one command.

---

### Manual Installation (If Auto-Install Fails)

#### Core Dependencies (Required)

```bash
pip install pyyaml cryptography flask requests
```

#### Agent Optional Dependencies

For the full agent capabilities:

```bash
pip install psutil pillow opencv-python pynput numpy
```

#### WhatsApp Bot Dependencies

Requires Node.js (download from https://nodejs.org/):

```bash
cd whatsapp-c2
npm install
cd ..
```

---

### What Gets Auto-Installed

The following packages are checked and installed automatically:

**Core (Always Required):**
- `pyyaml` - YAML configuration parsing
- `cryptography` - Fernet encryption
- `flask` - REST API server
- `requests` - HTTP client for bot

**Agent (Optional):**
- `psutil` - System information
- `pillow` - Image handling
- `opencv-python` - Webcam capture
- `pynput` - Keyboard logging
- `numpy` - Numerical operations

**Bot (If Node.js present):**
- WhatsApp Baileys library
- QR code terminal
- Chalk (colored output)
- Pino (logging)

---

### Smart Dependency Detection

The framework has three levels of dependency checking:

1. **Module-Level** (`master_umbrella_setup.py`):
   - Checks for yaml and cryptography on import
   - Auto-installs if missing
   - Fails gracefully with instructions

2. **Startup-Level** (`startup.py`):
   - Verifies flask, pyyaml, cryptography
   - Better user feedback with progress

3. **Initialization-Level** (`init_environment.py`):
   - Comprehensive check of all dependencies
   - Platform-aware (skips Windows-only on Linux)
   - Provides detailed summary

---

### Troubleshooting

**If pip install hangs:**
```bash
pip install --no-cache-dir pyyaml
```

**If you get "permission denied":**
```bash
python -m pip install --user pyyaml
```

**For Windows with Visual C++ issues:**
```bash
pip install --only-binary :all: cryptography
```

**Check what's installed:**
```bash
pip list | grep -i yaml
pip list | grep -i crypt
```

---

### Next Steps After Setup

Once environment is ready:

```bash
# Terminal 1: Start C2 Server
python startup.py server

# Terminal 2: Start WhatsApp Bot  
python startup.py bot

# Terminal 3: Build Agent
python startup.py agent

# Terminal 4: Run Tests
python startup.py test
```

Or all at once with the launcher:
```bash
python launch.py
```
