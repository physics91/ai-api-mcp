# Complete MCP Installation Guide for AI API MCP Server

This guide provides comprehensive instructions for installing and configuring the AI API MCP Server with various MCP-supporting tools including Claude Code, Claude Desktop, Cursor, VS Code, and other compatible applications.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Claude Code (CLI)](#claude-code-cli)
- [Claude Desktop](#claude-desktop)
- [Cursor IDE](#cursor-ide)
- [VS Code with GitHub Copilot Chat](#vs-code-with-github-copilot-chat)
- [Other MCP-Supporting Tools](#other-mcp-supporting-tools)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing MCP servers, ensure you have:
1. **Node.js** (v16 or higher) - Required for running NPX
2. Administrator/root access to modify configuration files (for some tools)

## Quick Start

The AI API MCP Server can be run instantly using NPX without any installation:

```bash
# Run directly with NPX - no installation needed!
npx @ai-api/mcp-server
```

### Configure API Keys

Create a `.env` file in your current directory or set environment variables:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GROK_API_KEY=your_grok_api_key_here
```

## Claude Code (CLI)

Claude Code provides two ways to configure MCP servers: using configuration files or CLI commands.

### Method 1: Using CLI Commands (Recommended)

The easiest way to add an MCP server in Claude Code is using the built-in commands:

```bash
# Add MCP server with environment variables
claude mcp add ai-api \
  --command "npx" \
  --args "@ai-api/mcp-server" \
  --env OPENAI_API_KEY=your-openai-key \
  --env ANTHROPIC_API_KEY=your-anthropic-key \
  --env GOOGLE_API_KEY=your-google-key \
  --env GROK_API_KEY=your-grok-key

# List configured MCP servers
claude mcp list

# Remove an MCP server
claude mcp remove ai-api
```

### Method 2: Configuration File

Alternatively, you can manually create a configuration file in your project root:

1. **Create configuration file** in your project root:
   Create a file named `claude_mcp_config.json` in the root directory of your project.

2. **Add MCP server configuration**:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "npx",
         "args": ["@ai-api/mcp-server"],
         "env": {
           "OPENAI_API_KEY": "your-openai-key",
           "ANTHROPIC_API_KEY": "your-anthropic-key",
           "GOOGLE_API_KEY": "your-google-key",
           "GROK_API_KEY": "your-grok-key"
         }
       }
     }
   }
   ```

3. **Important notes**:
   - The configuration file must be named `claude_mcp_config.json` (not `.claude/settings.json`)
   - Place it in the project root directory
   - API keys can be set in the `env` section or in a `.env` file in the same directory
   - Using CLI commands is preferred as they handle file creation and formatting automatically

## Claude Desktop

Claude Desktop uses a dedicated configuration file for MCP servers.

### Configuration Steps

1. **Locate configuration file**:
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. **Create/Edit configuration file**:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "npx",
         "args": ["@ai-api/mcp-server"],
         "env": {
           "OPENAI_API_KEY": "your-openai-key",
           "ANTHROPIC_API_KEY": "your-anthropic-key",
           "GOOGLE_API_KEY": "your-google-key",
           "GROK_API_KEY": "your-grok-key"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to apply changes

### Using Desktop Extensions (2025 Update)

Navigate to **Settings > Extensions** within Claude Desktop for GUI-based MCP server management.

## Cursor IDE

Cursor IDE supports MCP servers through configuration files.

### Project-Specific Configuration

1. **Create configuration directory** in project root:
   ```bash
   mkdir -p .cursor
   ```

2. **Create MCP configuration** `.cursor/mcp.json`:
   ```json
   {
     "servers": [
       {
         "name": "ai-api-mcp",
         "command": ["npx"],
         "args": ["@ai-api/mcp-server"],
         "env": {
           "OPENAI_API_KEY": "your-openai-key",
           "ANTHROPIC_API_KEY": "your-anthropic-key",
           "GOOGLE_API_KEY": "your-google-key",
           "GROK_API_KEY": "your-grok-key"
         },
         "enabled": true
       }
     ]
   }
   ```

### Global Configuration

1. **Create global configuration**:
   - **Windows**: `%USERPROFILE%\.cursor\mcp.json`
   - **macOS/Linux**: `~/.cursor/mcp.json`

2. **Add the same configuration as above**

3. **Verify in Cursor**: Navigate to Settings > MCP to see server status

## VS Code with GitHub Copilot Chat

VS Code supports MCP servers through GitHub Copilot Chat with MCP extension capabilities.

### Method 1: Workspace Configuration

1. **Create workspace configuration**:
   ```bash
   mkdir -p .vscode
   ```

2. **Create MCP configuration** `.vscode/mcp.json`:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "npx",
         "args": ["@ai-api/mcp-server"],
         "env": {
           "OPENAI_API_KEY": "your-openai-key",
           "ANTHROPIC_API_KEY": "your-anthropic-key",
           "GOOGLE_API_KEY": "your-google-key",
           "GROK_API_KEY": "your-grok-key"
         }
       }
     }
   }
   ```

### Method 2: User Settings

1. **Open VS Code settings**: `Ctrl+Shift+P` > "Preferences: Open User Settings (JSON)"

2. **Add MCP configuration**:
   ```json
   {
     "chat.mcp.servers": {
       "ai-api": {
         "command": "npx",
         "args": ["@ai-api/mcp-server"]
       }
     }
   }
   ```

### Method 3: Automatic Discovery

Enable autodiscovery of MCP servers from other tools:
```json
{
  "chat.mcp.discovery.enabled": true
}
```

## Other MCP-Supporting Tools

### Continue Extension (VS Code)

Continue doesn't directly support MCP command execution but can connect to running MCP servers via API endpoints.

1. **Start AI API MCP Server**:
   ```bash
   npx @ai-api/mcp-server --port 8000
   ```

2. **Configure Continue** in `.continue/config.json`:
   ```json
   {
     "models": [
       {
         "title": "AI API MCP",
         "provider": "openai",
         "model": "gpt-4",
         "apiBase": "http://localhost:8000/v1",
         "apiKey": "your-api-key"
       }
     ]
   }
   ```

### Windsurf Editor

Similar to Cursor, Windsurf supports MCP through configuration files:

1. **Create configuration**: `.windsurf/mcp.json`
2. Use the same format as Cursor configuration

### Generic MCP Client Configuration

For any tool that supports MCP, the general pattern is:

```json
{
  "mcp" or "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["@ai-api/mcp-server"],
      "env": {
        "API_KEY": "value"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues and Solutions

1. **Server not starting**:
   - Verify Node.js is installed: `node --version`
   - Check NPX is available: `npx --version`
   - Ensure internet connection for NPX to download packages

2. **API key errors**:
   - Verify API keys are valid and properly formatted
   - Check environment variables or `.env` file
   - Ensure no extra spaces or quotes around keys

3. **Configuration not recognized**:
   - Restart the application after making changes
   - Check JSON syntax for errors
   - Verify configuration file is in the correct location

4. **Permission errors**:
   - On Windows, try running as administrator
   - Check file ownership and permissions
   - Ensure NPX can write to temporary directories

### Debug Mode

Enable debug logging in various tools:

- **Claude Desktop**: Settings > Advanced > Enable Debug Logging
- **VS Code**: Add `"chat.mcp.debug": true` to settings.json
- **Cursor**: Check logs in Settings > MCP > View Logs

### Verification Steps

1. **Test MCP server directly**:
   ```bash
   # Run with verbose output
   npx @ai-api/mcp-server --verbose
   ```

2. **Check health endpoint**:
   ```bash
   # If server exposes HTTP endpoint
   curl http://localhost:8000/health
   ```

3. **Verify in application**:
   - Look for MCP indicator in the UI
   - Try a simple command like "list models"
   - Check application logs for connection errors

## Security Best Practices

1. **API Key Management**:
   - Never commit API keys to version control
   - Use environment variables or `.env` files
   - Rotate keys regularly
   - Consider using a secrets management service

2. **Server Security**:
   - Only use official NPX packages
   - Review package permissions before running
   - Keep Node.js updated for security patches

3. **Network Security**:
   - MCP servers typically run locally
   - Avoid exposing to public networks
   - Use firewall rules if needed

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [AI API MCP Server Documentation](../README.md)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [Community MCP Servers](https://github.com/topics/mcp-server)

---

For updates and contributions, please visit the [AI API MCP GitHub repository](https://github.com/yourusername/ai-api-mcp).