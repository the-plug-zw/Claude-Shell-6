import yaml from 'js-yaml';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

/**
 * Configuration Loader for umbrella_config.yaml
 * Provides unified config access for WhatsApp Bot
 */
export class ConfigLoader {
  constructor(configPath = null) {
    this.configPath = configPath || path.join(__dirname, '../umbrella_config.yaml');
    this.config = null;
    this.load();
  }

  load() {
    try {
      const fileContents = fs.readFileSync(this.configPath, 'utf8');
      this.config = yaml.load(fileContents);
      console.log(`[Config] Loaded from ${this.configPath}`);
      return true;
    } catch (error) {
      console.error(`[Config] Failed to load: ${error.message}`);
      return false;
    }
  }

  get(keyPath, defaultValue = null) {
    const keys = keyPath.split('.');
    let value = this.config;

    for (const key of keys) {
      if (value && typeof value === 'object' && key in value) {
        value = value[key];
      } else {
        return defaultValue;
      }
    }
    return value;
  }

  getServer() {
    return this.config?.server || {};
  }

  getAgent() {
    return this.config?.agent || {};
  }

  getBot() {
    return this.config?.bot || {};
  }

  getSecurity() {
    return this.config?.security || {};
  }

  getStatus() {
    return {
      loaded: this.config !== null,
      path: this.configPath,
      server_ip: this.get('server.listen_ip'),
      server_port: this.get('server.listen_port'),
      api_port: this.get('server.api_port'),
      agent_callback: `${this.get('agent.callback_ip')}:${this.get('agent.callback_port')}`,
    };
  }
}

export default ConfigLoader;
