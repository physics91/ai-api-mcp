# Complete MCP Installation Guide for AI API MCP Server

This guide provides comprehensive instructions for installing and configuring the AI API MCP Server with various MCP-supporting tools including Claude Code, Claude Desktop, Cursor, VS Code, and other compatible applications.

## Table of Contents
- [Prerequisites](#prerequisites)
- [AI API MCP Server Setup](#ai-api-mcp-server-setup)
- [Claude Code (CLI)](#claude-code-cli)
- [Claude Desktop](#claude-desktop)
- [Cursor IDE](#cursor-ide)
- [VS Code with GitHub Copilot Chat](#vs-code-with-github-copilot-chat)
- [Other MCP-Supporting Tools](#other-mcp-supporting-tools)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before installing MCP servers, ensure you have:
1. **Node.js** (v16 or higher) - Required for running MCP servers
2. **Python** (3.10 or higher) - Required for AI API MCP Server
3. **Git** - For cloning repositories
4. Administrator/root access to modify configuration files

## AI API MCP Server Setup

First, set up the AI API MCP Server that will be used by all tools:

### 1. Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-api-mcp.git
cd ai-api-mcp

# Install dependencies
chmod +x install.sh
./install.sh
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GROK_API_KEY=your_grok_api_key_here
```

### 3. Test the Server

```bash
# Run the server
./run.sh

# Or using Node.js
node run.js

# Or using Python
python -m src.server
```

## Claude Code (CLI)

Claude Code uses a dedicated configuration file for MCP servers in the project root directory.

### Configuration Steps

1. **Create configuration file** in your project root:
   Create a file named `claude_mcp_config.json` in the root directory of your project.

2. **Add MCP server configuration**:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "/path/to/ai-api-mcp",
         "env": {
           "PYTHONPATH": "/path/to/ai-api-mcp"
         }
       }
     }
   }
   ```

   **Windows example**:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "C:\\path\\to\\ai-api-mcp",
         "env": {
           "PYTHONPATH": "C:\\path\\to\\ai-api-mcp"
         }
       }
     }
   }
   ```

3. **Important notes**:
   - The configuration file must be named `claude_mcp_config.json` (not `.claude/settings.json`)
   - Place it in the project root directory
   - Use absolute paths for the `cwd` and `PYTHONPATH` values
   - On Windows, use double backslashes (`\\`) or forward slashes (`/`) in paths

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
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "/path/to/ai-api-mcp",
         "env": {
           "PYTHONPATH": "/path/to/ai-api-mcp"
         }
       }
     }
   }
   ```

3. **Alternative NPX configuration**:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "npx",
         "args": ["@ai-api/mcp-server"]
       }
     }
   }
   ```

4. **Restart Claude Desktop** to apply changes

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
         "command": ["python"],
         "args": ["-m", "src.server"],
         "cwd": "/path/to/ai-api-mcp",
         "env": {
           "PYTHONPATH": "/path/to/ai-api-mcp"
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
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "/path/to/ai-api-mcp",
         "env": {
           "PYTHONPATH": "/path/to/ai-api-mcp"
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
   cd /path/to/ai-api-mcp
   ./run.sh
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
      "command": "executable-path",
      "args": ["argument1", "argument2"],
      "cwd": "working-directory",
      "env": {
        "ENV_VAR": "value"
      }
    }
  }
}
```

## Troubleshooting

### Common Issues and Solutions

1. **Server not starting**:
   - Verify Python/Node.js is installed: `python --version` or `node --version`
   - Check file paths are absolute, not relative
   - Ensure all required dependencies are installed

2. **API key errors**:
   - Verify `.env` file exists in the AI API MCP directory
   - Check API keys are valid and properly formatted
   - Ensure no extra spaces or quotes around keys

3. **Configuration not recognized**:
   - Restart the application after making changes
   - Check JSON syntax for errors
   - Verify configuration file is in the correct location

4. **Permission errors**:
   - Run with appropriate permissions
   - Check file ownership and permissions
   - On Windows, try running as administrator

### Debug Mode

Enable debug logging in various tools:

- **Claude Desktop**: Settings > Advanced > Enable Debug Logging
- **VS Code**: Add `"chat.mcp.debug": true` to settings.json
- **Cursor**: Check logs in Settings > MCP > View Logs

### Verification Steps

1. **Test MCP server directly**:
   ```bash
   # Start server
   python -m src.server
   
   # In another terminal, test with curl
   curl http://localhost:8000/health
   ```

2. **Check MCP server logs**:
   ```bash
   tail -f ~/.ai-api-mcp/logs/server.log
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

2. **Server Security**:
   - Only install MCP servers from trusted sources
   - Review server code before installation
   - Limit network exposure (use localhost when possible)

3. **Permission Management**:
   - Run servers with minimal required permissions
   - Use separate user accounts for production
   - Audit server access logs regularly

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [AI API MCP Server Documentation](../README.md)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
- [Community MCP Servers](https://github.com/topics/mcp-server)

---

For updates and contributions, please visit the [AI API MCP GitHub repository](https://github.com/yourusername/ai-api-mcp).