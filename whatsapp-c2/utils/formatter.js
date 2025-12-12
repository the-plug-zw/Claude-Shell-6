import chalk from 'chalk';
import moment from 'moment';
import { 
  COMMAND_METADATA, 
  getAllCategories, 
  getTotalCommandCount, 
  getCommand 
} from './commandMetadata.js';

/**
 * Response Formatter - Makes everything look beautiful
 */

export class ResponseFormatter {
  
  /**
   * Format header with emoji and title
   */
  static header(emoji, title) {
    return `╔═══════════════════════════════════════╗
║ ${emoji} *${title.toUpperCase()}* ${emoji}
╚═══════════════════════════════════════╝`;
  }

  /**
   * Format success message
   */
  static success(message) {
    return `✅ *SUCCESS*\n\n${message}`;
  }

  /**
   * Format error message
   */
  static error(message) {
    return `❌ *ERROR*\n\n${message}`;
  }

  /**
   * Format info message
   */
  static info(message) {
    return `ℹ️ *INFO*\n\n${message}`;
  }

  /**
   * Format warning message
   */
  static warning(message) {
    return `⚠️ *WARNING*\n\n${message}`;
  }

  /**
   * Format system info response
   */
  static systemInfo(data) {
    const lines = data.split('\n');
    let formatted = this.header('💻', 'SYSTEM INFORMATION');
    formatted += '\n\n';
    
    lines.forEach(line => {
      if (line.includes(':')) {
        const [key, value] = line.split(':');
        formatted += `▪️ *${key.trim()}:*\n   ${value.trim()}\n\n`;
      }
    });
    
    formatted += `⏰ _Retrieved: ${moment().format('HH:mm:ss')}_`;
    return formatted;
  }

  /**
   * Format process list
   */
  static processList(data) {
    const lines = data.split('\n').slice(0, 20); // First 20 processes
    let formatted = this.header('⚙️', 'RUNNING PROCESSES');
    formatted += '\n\n';
    
    lines.forEach((line, idx) => {
      if (line.trim()) {
        formatted += `${idx + 1}. \`${line.trim()}\`\n`;
      }
    });
    
    formatted += `\n_Showing top 20 processes_`;
    return formatted;
  }

  /**
   * Format credentials (passwords, wifi, etc)
   */
  static credentials(data, type) {
    let formatted = this.header('🔐', `${type.toUpperCase()} CREDENTIALS`);
    formatted += '\n\n';
    
    try {
      const parsed = JSON.parse(data);
      
      if (Array.isArray(parsed)) {
        parsed.forEach((item, idx) => {
          formatted += `\n*[${idx + 1}]*\n`;
          Object.keys(item).forEach(key => {
            formatted += `▪️ *${key}:* ${item[key]}\n`;
          });
        });
      } else {
        formatted += '```' + JSON.stringify(parsed, null, 2) + '```';
      }
    } catch {
      formatted += '```' + data + '```';
    }
    
    formatted += `\n\n💾 _Auto-saved to server_`;
    return formatted;
  }

  /**
   * Format network scan results
   */
  static networkScan(data) {
    const hosts = data.split('\n').filter(l => l.trim());
    let formatted = this.header('🌐', 'NETWORK SCAN RESULTS');
    formatted += '\n\n';
    
    formatted += `📊 *Found ${hosts.length} hosts*\n\n`;
    
    hosts.forEach((host, idx) => {
      formatted += `${idx + 1}. \`${host}\`\n`;
    });
    
    return formatted;
  }

  /**
   * Format metrics/stats
   */
  static metrics(data) {
    let formatted = this.header('📊', 'SYSTEM METRICS');
    formatted += '\n\n';
    
    try {
      const parsed = JSON.parse(data);
      
      // CPU
      formatted += `🖥️ *CPU*\n`;
      formatted += `   Usage: ${parsed.CPU.percent}%\n`;
      formatted += `   Cores: ${parsed.CPU.count}\n\n`;
      
      // Memory
      formatted += `💾 *MEMORY*\n`;
      formatted += `   Total: ${parsed.Memory.total_gb} GB\n`;
      formatted += `   Used: ${parsed.Memory.used_gb} GB (${parsed.Memory.percent}%)\n\n`;
      
      // Disk
      formatted += `💿 *DISK*\n`;
      formatted += `   Total: ${parsed.Disk.total_gb} GB\n`;
      formatted += `   Used: ${parsed.Disk.used_gb} GB (${parsed.Disk.percent}%)\n\n`;
      
      // Network
      formatted += `🌐 *NETWORK*\n`;
      formatted += `   Sent: ${(parsed.Network.bytes_sent / 1024 / 1024).toFixed(2)} MB\n`;
      formatted += `   Received: ${(parsed.Network.bytes_recv / 1024 / 1024).toFixed(2)} MB\n\n`;
      
      formatted += `⏱️ *Uptime:* ${parsed.Uptime_Hours} hours`;
      
    } catch {
      formatted += '```' + data + '```';
    }
    
    return formatted;
  }

  /**
   * Format command executing status
   */
  static executing(command) {
    return `⏳ *EXECUTING COMMAND*\n\n\`${command}\`\n\n_Please wait..._`;
  }

  /**
   * Format session list
   */
  static sessionList(sessions) {
    let formatted = this.header('🎯', 'ACTIVE SESSIONS');
    formatted += '\n\n';
    
    if (sessions.length === 0) {
      formatted += '❌ No active sessions';
      return formatted;
    }
    
    sessions.forEach((session, idx) => {
      formatted += `\n*[${session.id}]* ${session.active ? '🟢' : '🔴'}\n`;
      formatted += `▪️ *Host:* ${session.addr}\n`;
      formatted += `▪️ *Info:* ${session.info}\n`;
      formatted += `▪️ *Connected:* ${session.connected_at}\n`;
    });
    
    formatted += `\n_Use /use <id> to interact_`;
    return formatted;
  }

  /**
   * Format help menu
   */
  static helpMenu() {
    let help = this.header('📱', 'COMMAND MENU');
    help += '\n\n';
    
    help += `*🎯 SESSION MANAGEMENT*
/sessions - List all active sessions
/use <id> - Switch to session
/kill <id> - Kill session
/active - Show current session

*💻 SYSTEM INFO*
/sysinfo - System information
/processes - Running processes
/metrics - Performance metrics
/software - Installed software
/usb - USB devices

*📸 SURVEILLANCE*
/screenshot - Capture screen
/webcam - Capture webcam
/keylogs - Get keystrokes
/record <sec> - Record audio
/clipboard - Clipboard logs

*🔐 CREDENTIALS*
/passwords - Browser passwords
/wifi - WiFi passwords
/discord - Discord tokens
/history <browser> - Browser history

*⚙️ PROCESS CONTROL*
/killproc <pid> - Kill process

*🌐 NETWORK*
/netscan - Scan network
/locate - Geolocation

*💾 FILES*
/download <path> - Download file
/upload <path> - Upload file

*📷 ADVANCED CAPTURE*
/timelapse <count> <interval> - Screenshot timelapse
/photoburst <count> - Multiple webcam photos
/usblist - List USB devices

*🎮 FUN FEATURES*
/msgbox <msg> - Show message
/beep [freq] [dur] - Play beep
/lock - Lock screen
/shutdown - Shutdown system
/restart - Restart system

*🛡️ PERSISTENCE*
/persist - Add persistence
/elevate - Get admin
/defenderoff - Disable Defender

*💣 ADVANCED*
/ransom <path> - Ransomware demo
/spread - USB spreading
/selfdestruct - Remove traces

*ℹ️ OTHER*
/help - Show this menu
/ping - Check bot status`;
    
    return help;
  }

  /**
   * Format network scan results
   */
  static networkScan(data) {
    let formatted = this.header('🌐', 'NETWORK SCAN RESULTS');
    formatted += '\n\n';
    
    try {
      const results = typeof data === 'string' ? data.split('\n') : data;
      const filtered = (Array.isArray(results) ? results : [results])
        .filter(r => r && r.trim())
        .slice(0, 20);
      
      if (filtered.length === 0) {
        formatted += '❌ No devices found on network';
      } else {
        formatted += `✅ Found ${filtered.length} active hosts:\n\n`;
        filtered.forEach((host, idx) => {
          formatted += `${idx + 1}. \`${host.trim()}\`\n`;
        });
      }
    } catch {
      formatted += '```' + data + '```';
    }
    
    return formatted;
  }

  /**
   * Console log with styling
   */
  static log(type, message) {
    const timestamp = moment().format('HH:mm:ss');
    
    switch(type) {
      case 'success':
        console.log(chalk.green(`[${timestamp}] ✓ ${message}`));
        break;
      case 'error':
        console.log(chalk.red(`[${timestamp}] ✗ ${message}`));
        break;
      case 'info':
        console.log(chalk.cyan(`[${timestamp}] ℹ ${message}`));
        break;
      case 'warning':
        console.log(chalk.yellow(`[${timestamp}] ⚠ ${message}`));
        break;
      default:
        console.log(chalk.white(`[${timestamp}] ${message}`));
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // ENHANCED HELP SYSTEM
  // ═══════════════════════════════════════════════════════════════

  /**
   * Main help menu with all commands and categories
   */
  static mainMenu() {
    const categories = getAllCategories();
    const totalCommands = getTotalCommandCount();
    
    let menu = `╔═════════════════════════════════════════════════╗
║         🎯 T0OL-B4S3-263 COMMAND HUB 🎯      ║
╚═════════════════════════════════════════════════╝

📊 *TOTAL COMMANDS:* ${totalCommands}

*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*
📁 *COMMAND CATEGORIES:*
*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*\n`;

    categories.forEach((cat) => {
      menu += `\n${cat.emoji} *${cat.displayName}*\n`;
      menu += `   ${cat.description}\n`;
      menu += `   📊 ${cat.commandCount} commands\n`;
      menu += `   → Send: /menu ${cat.name}\n`;
    });

    menu += `\n*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*
📖 *DETAILED HELP:*
*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*

/help <category>
Get all commands in a category

/help -command
Get detailed help for a specific command

Example: /help -screenshot`;

    return menu;
  }

  /**
   * Category menu with all commands in that category
   */
  static categoryMenu(categoryName) {
    const category = Object.values(COMMAND_METADATA).find(
      c => c.category === categoryName.toLowerCase()
    );

    if (!category || !category.commands) {
      return this.error(`Category "${categoryName}" not found`);
    }

    const commands = Object.values(category.commands);
    
    let menu = `╔═════════════════════════════════════════════════╗
║  ${category.categoryEmoji} ${category.categoryName.padEnd(40)} ║
╚═════════════════════════════════════════════════╝

${category.description}

*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*\n`;

    commands.forEach((cmd) => {
      menu += `\n${cmd.emoji} */${cmd.name}*`;
      
      if (cmd.aliases && cmd.aliases.length > 0) {
        menu += ` (${cmd.aliases.map(a => `/${a}`).join(', ')})`;
      }
      
      menu += `\n   ${cmd.shortDesc}\n`;
      menu += `   → /help -${cmd.name}\n`;
    });

    menu += `\n*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*`;
    menu += `\n\nℹ️ _Tap a command above for detailed help_`;

    return menu;
  }

  /**
   * Detailed help for a specific command
   */
  static commandHelp(commandName) {
    const command = getCommand(commandName);

    if (!command) {
      return this.error(`Command "${commandName}" not found. Try /help for menu.`);
    }

    let help = `╔═════════════════════════════════════════════════╗
║  ${command.emoji} ${command.name.toUpperCase().padEnd(40)} ║
╚═════════════════════════════════════════════════╝\n`;

    help += `*📝 Short Description:*
${command.shortDesc}\n`;

    help += `*📖 Full Description:*
${command.fullDesc}\n`;

    help += `*💻 Usage:*
\`${command.usage}\`\n`;

    help += `*📌 Example:*
\`${command.example}\`\n`;

    if (command.aliases && command.aliases.length > 0) {
      help += `*🔤 Aliases:*
${command.aliases.map(a => `• /${a}`).join('\n')}\n`;
    }

    if (command.danger) {
      help += `\n⚠️  *DANGEROUS COMMAND*
This command can cause system damage or data loss!
Use with caution on authorized targets only!\n`;
    }

    help += `*⏱️ Timeout:* ${command.timeout ? command.timeout + 'ms' : 'Dynamic'}\n`;

    help += `\n*━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━*`;
    help += `\n\n📚 _Back to main menu: /help_`;

    return help;
  }

  /**
   * All commands list for terminal
   */
  static allCommandsList() {
    const categories = getAllCategories();
    let list = `\n${'═'.repeat(70)}\n`;
    list += `${'T0OL-B4S3-263 COMMAND REFERENCE'.padStart(45)}\n`;
    list += `${'═'.repeat(70)}\n\n`;

    categories.forEach((cat) => {
      list += `${cat.emoji} ${cat.displayName} (${cat.commandCount} commands)\n`;
      list += `${'-'.repeat(70)}\n`;

      const commands = Object.values(COMMAND_METADATA[cat.name].commands);
      
      commands.forEach((cmd) => {
        const aliases = cmd.aliases ? `(${cmd.aliases.join(', ')})` : '';
        const danger = cmd.danger ? ' ⚠️ DANGER' : '';
        list += `  ${cmd.emoji} /${cmd.name.padEnd(15)} ${aliases.padEnd(25)} ${cmd.shortDesc}${danger}\n`;
      });

      list += '\n';
    });

    list += `${'═'.repeat(70)}\n`;
    list += `Use 'help -command' for detailed information\n`;
    list += `Example: help -screenshot\n`;
    list += `${'═'.repeat(70)}\n`;

    return list;
  }

  /**
   * Terminal-style detailed command help
   */
  static terminalCommandHelp(commandName) {
    const command = getCommand(commandName);

    if (!command) {
      return `Error: Command "${commandName}" not found`;
    }

    let help = `\n${'═'.repeat(70)}\n`;
    help += `${command.emoji} COMMAND: /${command.name}\n`;
    help += `${'═'.repeat(70)}\n\n`;

    help += `📝 SHORT DESC:\n`;
    help += `   ${command.shortDesc}\n\n`;

    help += `📖 FULL DESCRIPTION:\n`;
    const fullDescLines = command.fullDesc.split('\n');
    fullDescLines.forEach(line => {
      help += `   ${line}\n`;
    });
    help += '\n';

    help += `💻 USAGE:\n`;
    help += `   ${command.usage}\n\n`;

    help += `📌 EXAMPLE:\n`;
    help += `   ${command.example}\n\n`;

    if (command.aliases && command.aliases.length > 0) {
      help += `🔤 ALIASES:\n`;
      command.aliases.forEach(alias => {
        help += `   /${alias}\n`;
      });
      help += '\n';
    }

    if (command.danger) {
      help += `⚠️  DANGEROUS OPERATION:\n`;
      help += `   This command can cause system damage or data loss!\n`;
      help += `   Only use on authorized targets with proper authorization!\n\n`;
    }

    help += `⏱️  TIMEOUT: ${command.timeout ? command.timeout + 'ms' : 'Dynamic'}\n`;
    help += `📂 CATEGORY: ${command.category}\n`;

    help += `\n${'═'.repeat(70)}\n`;

    return help;
  }
}