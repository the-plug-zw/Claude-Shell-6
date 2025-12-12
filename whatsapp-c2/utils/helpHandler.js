/**
 * Help Handler - Centralized help system
 * Handles /help, /help -command, /menu and displays formatted responses
 */

import { ResponseFormatter } from './formatter.js';
import { getCommand, getAllCategories, COMMAND_METADATA } from './commandMetadata.js';

export class HelpHandler {
  /**
   * Parse and handle help commands
   * /help - main menu
   * /help category - category menu
   * /help -command - detailed help
   * /menu - same as /help
   */
  static parseHelpCommand(input) {
    const parts = input.trim().split(/\s+/);
    const baseCmd = parts[0].toLowerCase();

    // Handle /menu and /help
    if (baseCmd === '/menu' || baseCmd === '/help' || baseCmd === 'help') {
      // /help or /menu alone = main menu
      if (parts.length === 1) {
        return { type: 'mainMenu' };
      }

      // /help -command = detailed help
      if (parts[1].startsWith('-')) {
        const cmdName = parts[1].substring(1);
        return { type: 'commandHelp', command: cmdName };
      }

      // /help category = category menu
      const category = parts[1].toLowerCase();
      return { type: 'categoryMenu', category };
    }

    return null;
  }

  /**
   * Process help request and return appropriate response
   */
  static processHelpRequest(helpRequest) {
    if (!helpRequest) return null;

    switch (helpRequest.type) {
      case 'mainMenu':
        return ResponseFormatter.mainMenu();

      case 'categoryMenu':
        return ResponseFormatter.categoryMenu(helpRequest.category);

      case 'commandHelp':
        return ResponseFormatter.commandHelp(helpRequest.command);

      default:
        return null;
    }
  }

  /**
   * Get help for terminal input
   */
  static getTerminalHelp(input) {
    const parts = input.trim().toLowerCase().split(/\s+/);

    // help -command
    if (parts[0] === 'help' && parts[1]?.startsWith('-')) {
      const cmdName = parts[1].substring(1);
      return ResponseFormatter.terminalCommandHelp(cmdName);
    }

    // help (all commands)
    if (parts[0] === 'help' || parts[0] === 'menu') {
      if (parts.length === 1) {
        return ResponseFormatter.allCommandsList();
      }

      // help category
      const category = parts[1];
      return ResponseFormatter.categoryMenu(category);
    }

    return null;
  }

  /**
   * Check if input is a help request
   */
  static isHelpRequest(input) {
    const cmd = input.trim().split(/\s+/)[0].toLowerCase();
    return cmd === '/help' || cmd === 'help' || cmd === '/menu' || cmd === 'menu' || cmd === '/?';
  }

  /**
   * Get all commands grouped by category
   */
  static getCommandsByCategory() {
    const grouped = {};

    Object.entries(COMMAND_METADATA).forEach(([key, category]) => {
      if (category.commands) {
        grouped[category.category] = {
          categoryName: category.categoryName,
          categoryEmoji: category.categoryEmoji,
          description: category.description,
          commands: Object.values(category.commands),
        };
      }
    });

    return grouped;
  }

  /**
   * Search for commands by keyword
   */
  static searchCommands(keyword) {
    const search = keyword.toLowerCase();
    const results = [];

    Object.values(COMMAND_METADATA).forEach((category) => {
      if (!category.commands) return;

      Object.values(category.commands).forEach((cmd) => {
        if (
          cmd.name.includes(search) ||
          cmd.shortDesc.toLowerCase().includes(search) ||
          cmd.fullDesc.toLowerCase().includes(search) ||
          (cmd.aliases && cmd.aliases.some(a => a.includes(search)))
        ) {
          results.push(cmd);
        }
      });
    });

    return results;
  }

  /**
   * Format search results
   */
  static formatSearchResults(keyword, results) {
    if (results.length === 0) {
      return ResponseFormatter.error(
        `No commands found matching "${keyword}"\n\nTry /help for full menu`
      );
    }

    let response = `╔═════════════════════════════════════════════════╗
║  🔍 SEARCH RESULTS for "${keyword}"
╚═════════════════════════════════════════════════╝\n`;

    response += `Found ${results.length} command(s):\n\n`;

    results.forEach((cmd) => {
      response += `${cmd.emoji} */${cmd.name}*`;
      if (cmd.aliases) {
        response += ` (${cmd.aliases.map(a => `/${a}`).join(', ')})`;
      }
      response += `\n   ${cmd.shortDesc}\n`;
      response += `   → /help -${cmd.name}\n\n`;
    });

    return response;
  }

  /**
   * Get quick reference card for a command
   */
  static getQuickReference(commandName) {
    const cmd = getCommand(commandName);

    if (!cmd) {
      return null;
    }

    return {
      name: cmd.name,
      emoji: cmd.emoji,
      aliases: cmd.aliases || [],
      shortDesc: cmd.shortDesc,
      usage: cmd.usage,
      example: cmd.example,
      danger: cmd.danger || false,
      category: cmd.category,
    };
  }
}
