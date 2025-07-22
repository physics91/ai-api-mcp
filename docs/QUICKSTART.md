# AI API MCP Server - Quick Start Guide

Get up and running with AI API MCP Server in 5 minutes!

## 🚀 Fastest Setup (NPX)

```bash
# Run without installation
npx @physics91org/ai-api-mcp
```

That's it! The server will:
- ✅ Check for Python installation
- ✅ Install dependencies automatically
- ✅ Create `.env` file from template
- ✅ Start the MCP server

## 🔑 Add Your API Keys

Edit the generated `.env` file:

```env
# Add at least one API key
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
GROK_API_KEY=xai-...
```

## 🎯 Your First Request

### Using with Claude Desktop

1. Add to Claude's config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "ai-api": {
      "command": "npx",
      "args": ["@physics91org/ai-api-mcp"]
    }
  }
}
```

2. Restart Claude Desktop

3. Test it:
```
Use the AI API tool to ask GPT-4: "What is the meaning of life?"
```

### Using with MCP Inspector

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Connect to the server
mcp-inspector npx @physics91org/ai-api-mcp

# In the inspector, try:
# 1. Click "list_models" to see available models
# 2. Use "chat" with a simple prompt
```

## 🎨 Example Requests

### Simple Chat
```javascript
{
  "tool": "chat",
  "arguments": {
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "model": "gpt-3.5-turbo"
  }
}
```

### Compare Models
```javascript
{
  "tool": "compare",
  "arguments": {
    "prompt": "Write a haiku about coding",
    "models": ["gpt-4", "claude-3-haiku-20240307", "gemini-pro"]
  }
}
```

### Analyze Code
```javascript
{
  "tool": "analyze",
  "arguments": {
    "content": "def add(a, b): return a + b",
    "analysis_type": "code",
    "model": "gpt-4"
  }
}
```

## 🐳 Docker Quick Start

```bash
# One-liner with your keys
docker run -it --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  ghcr.io/yourusername/ai-api-mcp:latest
```

## 📦 NPM Global Install

```bash
# Install globally
npm install -g @physics91org/ai-api-mcp

# Run from anywhere
ai-api-mcp
```

## 🔧 Common Commands

```bash
# List available models
mcp-inspector npx @physics91org/ai-api-mcp
# Then call: list_models()

# Check server health
curl http://localhost:3000/health

# View logs
tail -f ~/.ai-api-mcp/logs/server.log
```

## ⚡ Pro Tips

1. **Start with GPT-3.5-Turbo** - It's fast and cheap for testing
2. **Use environment variables** - Never hardcode API keys
3. **Set rate limits** - Add `MAX_REQUESTS_PER_MINUTE=10` to `.env`
4. **Enable caching** - Add `ENABLE_CACHE=true` for repeated queries

## 🆘 Need Help?

- API key issues? → Check [Troubleshooting](TROUBLESHOOTING.md#api-key-errors)
- Want examples? → See [Usage Examples](EXAMPLES.md)
- Full API docs? → Read [API Reference](API.md)

## 🎉 What's Next?

1. **Try model comparison** - See which AI works best for your use case
2. **Explore analysis tools** - Analyze code, text, or security
3. **Build something cool** - Check our [examples](EXAMPLES.md) for inspiration

---

**Ready for more?** Check out the full [documentation](../README.md) or dive into [advanced examples](EXAMPLES.md#advanced-use-cases)!