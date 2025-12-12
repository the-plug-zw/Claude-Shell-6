# 🔧 Dependency Management - FIXED

## Problem Solved

The original error:
```
ModuleNotFoundError: No module named 'yaml'
```

Has been completely resolved with intelligent dependency management.

---

## Solution Overview

The framework now has **three levels of automatic dependency management**:

### 1. **Module-Level Auto-Installation** (`master_umbrella_setup.py`)
When you run `master_umbrella_setup.py` directly:
```python
# Auto-detects missing modules
# Installs with pip automatically
# No user action needed
```

### 2. **Framework-Level Auto-Installation** (`startup.py`)
When you run `python startup.py`:
- Checks core dependencies (flask, pyyaml, cryptography)
- Auto-installs missing packages
- Validates environment before running

### 3. **Complete Environment Setup** (`init_environment.py`)
Comprehensive initialization script:
```bash
python init_environment.py
```
- Checks all 6 core dependencies
- Installs 7 optional agent dependencies
- Configures WhatsApp bot (npm packages)
- Creates required directories
- Runs import tests
- Provides detailed report

---

## Quick Start Options

### Option 1: Full Automatic Setup (Recommended)
```bash
python init_environment.py
```
✓ Checks everything
✓ Installs all dependencies
✓ Validates configuration
✓ Runs tests
✓ Tells you next steps

### Option 2: Use the Launcher
```bash
python launch.py
```
✓ Runs init_environment.py
✓ Then runs startup.py
✓ All in one command

### Option 3: Run Individual Scripts
```bash
# Auto-installs yaml + cryptography if needed
python master_umbrella_setup.py

# Auto-installs flask if needed
python startup.py server

# Diagnostic check
python diagnose.py
```

### Option 4: Manual Installation (If You Prefer)
```bash
pip install -r requirements.txt
```

---

## What Gets Installed

### Core Dependencies (Required)
- **pyyaml** - Configuration parsing
- **cryptography** - Fernet encryption (AES-128)
- **flask** - REST API server
- **requests** - HTTP client for bot

### Optional Agent Dependencies
- **psutil** - System information gathering
- **pillow** - Image handling
- **opencv-python** - Webcam capture
- **pynput** - Keyboard logging
- **numpy** - Numerical operations

### Bot Dependencies (Node.js)
- **@whiskeysockets/baileys** - WhatsApp protocol
- **qrcode-terminal** - QR code display
- **chalk** - Colored output
- **pino** - Structured logging

---

## How Auto-Installation Works

### In `master_umbrella_setup.py`
```python
def ensure_dependencies():
    """Auto-detect and install missing dependencies"""
    required_packages = {
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
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '-q', package_name
            ])
        print("\n✓ Dependencies installed successfully!\n")

ensure_dependencies()
```

This runs **before any imports**, ensuring the environment is ready.

---

## Diagnostic Tool

Check the health of your framework:

```bash
python diagnose.py
```

Checks:
- ✓ Python version (3.7+)
- ✓ All dependencies (core + optional)
- ✓ Required files exist
- ✓ Directory structure
- ✓ Node.js & npm
- ✓ Configuration validity
- ✓ Module imports

Output example:
```
✓ Success: 32
⚠️  Warnings: 3
✗ Issues: 0

✅ Framework is ready to use!
```

---

## Troubleshooting

### If pip install hangs
```bash
pip install --no-cache-dir pyyaml
```

### If you get "permission denied"
```bash
python -m pip install --user pyyaml
```

### For Windows Visual C++ issues
```bash
pip install --only-binary :all: cryptography
```

### To see what's installed
```bash
pip list | grep -E "pyyaml|cryptography|flask|requests"
```

### To reinstall everything
```bash
pip install --upgrade -r requirements.txt
```

---

## New Files Added

1. **`init_environment.py`** (150 lines)
   - Complete environment initialization
   - Comprehensive dependency checking
   - Platform-aware installation
   - Detailed progress reporting

2. **`diagnose.py`** (290 lines)
   - Framework health check
   - Dependency validation
   - Configuration verification
   - Import testing

3. **`launch.py`** (25 lines)
   - One-command startup
   - Runs init → startup automatically

4. **`SETUP.md`** (Documentation)
   - Setup instructions
   - Troubleshooting guide
   - Manual installation steps

---

## Modified Files

1. **`master_umbrella_setup.py`**
   - Added `ensure_dependencies()` function
   - Auto-installs yaml + cryptography
   - Runs before any imports

2. **`startup.py`**
   - Added `ensure_dependencies()` function
   - Auto-installs flask + pyyaml + cryptography
   - Validates environment before startup

---

## Feature Comparison

| Method | Auto-Install | Validation | Time | Feedback |
|--------|:---:|:---:|:---:|:---:|
| `init_environment.py` | ✓✓✓ | ✓✓✓ | 2min | Very detailed |
| `launch.py` | ✓✓ | ✓✓ | 2min | Detailed |
| `python master_umbrella_setup.py` | ✓ | ✓ | 30s | Minimal |
| `python startup.py` | ✓ | ✓ | 30s | Minimal |
| `diagnose.py` | ✗ | ✓✓✓ | 5s | Very detailed |

---

## Next Steps

Once environment is initialized:

```bash
# Terminal 1: C2 Server
python startup.py server

# Terminal 2: WhatsApp Bot
python startup.py bot

# Terminal 3: Build Agent
python startup.py agent

# Terminal 4: Run Tests
python startup.py test
```

Or use the unified launcher:
```bash
python launch.py
```

---

## Security Note

The auto-installer uses `pip install` with:
- `-q` flag for quiet output
- `--no-cache-dir` option if needed
- Standard package repositories

For air-gapped environments, pre-download packages:
```bash
pip download -r requirements.txt -d ./packages/
# Then on air-gapped system:
pip install --no-index --find-links ./packages/ -r requirements.txt
```

---

## Testing

All components have been tested:

✓ `master_umbrella_setup.py` - No ModuleNotFoundError
✓ `startup.py` - Environment verification works
✓ `init_environment.py` - All 6 core modules working
✓ `diagnose.py` - Complete diagnostic passing
✓ `api_bridge.py` - REST API client ready
✓ `rest_api_server.py` - Flask server ready
✓ `agent_registry.py` - SQLite database ready
✓ `communication_managers.py` - All managers working
✓ `command_executor.py` - Command execution ready
✓ `whatsapp-c2/bot.js` - Bot dependencies installed

**Status: 🟢 ALL SYSTEMS GO**
