# AI API MCP Server - Troubleshooting Guide

This guide helps you resolve common issues when using the AI API MCP Server.

## Table of Contents

1. [Installation Issues](#installation-issues)
2. [Configuration Problems](#configuration-problems)
3. [API Key Errors](#api-key-errors)
4. [Connection Issues](#connection-issues)
5. [Model-Specific Problems](#model-specific-problems)
6. [Performance Issues](#performance-issues)
7. [MCP Integration Issues](#mcp-integration-issues)
8. [Common Error Messages](#common-error-messages)

## Installation Issues

### Python Version Mismatch

**Problem**: Error message about Python version being too old

```
❌ Python 3.8 is installed, but version 3.10 or higher is required.
```

**Solution**:
1. Install Python 3.10 or higher from [python.org](https://www.python.org/downloads/)
2. On Windows, ensure Python is added to PATH
3. On macOS/Linux, you might need to use `python3` instead of `python`

### Dependency Installation Fails

**Problem**: `pip install` fails with permission errors

**Solution**:
```bash
# Option 1: Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .

# Option 2: Install for user only
pip install --user -e .

# Option 3: Use pipx for isolated installation
pipx install ai-api-mcp
```

### Docker Build Fails

**Problem**: Docker build fails with network errors

**Solution**:
```bash
# Clean Docker cache
docker system prune -a

# Build with no cache
docker build --no-cache -t ai-api-mcp .

# If behind proxy, set build args
docker build --build-arg HTTP_PROXY=http://proxy:port -t ai-api-mcp .
```

## Configuration Problems

### Environment File Not Found

**Problem**: Server can't find `.env` file

**Solution**:
1. Copy the example file:
   ```bash
   cp .env.example .env
   ```
2. Ensure file is in the project root directory
3. Check file permissions (readable by the user running the server)

### Invalid Environment Variables

**Problem**: Environment variables not being recognized

**Solution**:
1. Ensure no spaces around `=` in `.env` file:
   ```bash
   # Correct
   OPENAI_API_KEY=sk-...
   
   # Wrong
   OPENAI_API_KEY = sk-...
   ```

2. Don't use quotes unless they're part of the value:
   ```bash
   # Correct
   OPENAI_API_KEY=sk-abc123
   
   # Wrong (unless quotes are needed)
   OPENAI_API_KEY="sk-abc123"
   ```

## API Key Errors

### Invalid API Key

**Problem**: 
```
Error: OpenAI API error: Error code: 401 - Invalid API key
```

**Solution**:
1. Verify API key is correct and active
2. Check API key permissions on provider's dashboard
3. Ensure no extra spaces or characters in the key
4. Regenerate key if necessary

### API Key Not Set

**Problem**: Provider not initialized due to missing API key

**Solution**:
1. Add the required API key to `.env`:
   ```bash
   OPENAI_API_KEY=your_actual_key_here
   ANTHROPIC_API_KEY=your_actual_key_here
   GOOGLE_API_KEY=your_actual_key_here
   GROK_API_KEY=your_actual_key_here
   ```

2. Only add keys for providers you want to use

### Rate Limit Exceeded

**Problem**: 
```
Error: Rate limit exceeded. Please try again later.
```

**Solution**:
1. Check your API usage on the provider's dashboard
2. Implement request throttling:
   ```javascript
   // Add delay between requests
   await new Promise(resolve => setTimeout(resolve, 1000));
   ```
3. Use different API keys for development and production
4. Consider upgrading your API plan

## Connection Issues

### Network Timeout

**Problem**: Requests timing out

**Solution**:
1. Check internet connection
2. Verify firewall/proxy settings
3. Increase timeout in environment:
   ```bash
   # Add to .env
   REQUEST_TIMEOUT=60
   ```

### SSL Certificate Errors

**Problem**: SSL verification failures

**Solution**:
1. Update certificates:
   ```bash
   pip install --upgrade certifi
   ```

2. If behind corporate proxy, configure proxy settings:
   ```bash
   export HTTP_PROXY=http://proxy:port
   export HTTPS_PROXY=http://proxy:port
   ```

## Model-Specific Problems

### Model Not Found

**Problem**: 
```
Error: Model gpt-5 is not supported by openai
```

**Solution**:
1. Check available models:
   ```javascript
   const models = await mcp.list_models();
   console.log(models);
   ```

2. Use correct model names:
   - OpenAI: `gpt-4`, `gpt-3.5-turbo`
   - Anthropic: `claude-3-opus-20240229`
   - Google: `gemini-pro`
   - xAI: `grok-beta`

### Context Length Exceeded

**Problem**: 
```
Error: Maximum context length exceeded
```

**Solution**:
1. Reduce message history
2. Use model with larger context window
3. Implement message truncation:
   ```javascript
   const truncateMessages = (messages, maxTokens = 4000) => {
     // Keep system message and truncate from the middle
     return messages;
   };
   ```

## Performance Issues

### Slow Response Times

**Problem**: API calls taking too long

**Solution**:
1. Use faster models for simple tasks:
   - `gpt-3.5-turbo` instead of `gpt-4`
   - `claude-3-haiku` instead of `claude-3-opus`

2. Enable streaming for long responses
3. Implement caching for repeated queries

### High Token Usage

**Problem**: Excessive token consumption

**Solution**:
1. Set `max_tokens` limit:
   ```javascript
   await mcp.chat({
     messages: [...],
     model: "gpt-4",
     max_tokens: 500  // Limit response length
   });
   ```

2. Use concise prompts
3. Remove unnecessary conversation history

## MCP Integration Issues

### MCP Client Can't Find Server

**Problem**: MCP client fails to connect

**Solution**:
1. Verify MCP configuration:
   ```json
   {
     "mcpServers": {
       "ai-api": {
         "command": "python",
         "args": ["-m", "src.server"],
         "cwd": "/path/to/ai-api-mcp"
       }
     }
   }
   ```

2. Check path is absolute, not relative
3. Ensure Python is in PATH

### Permission Denied

**Problem**: Can't execute server

**Solution**:
```bash
# Make scripts executable
chmod +x run.sh install.sh

# Or run with explicit interpreter
python -m src.server
```

## Common Error Messages

### "No provider found for model"

**Cause**: Model name doesn't match any provider or provider not configured

**Fix**: 
- Check model name spelling
- Ensure provider API key is set
- Explicitly specify provider:
  ```javascript
  await mcp.chat({
    messages: [...],
    model: "gpt-4",
    provider: "openai"
  });
  ```

### "All models failed"

**Cause**: Multiple API failures in fallback chain

**Fix**:
- Check all API keys are valid
- Verify internet connection
- Check provider service status pages

### "JSON parsing error"

**Cause**: Model returned invalid JSON when JSON was expected

**Fix**:
- Lower temperature for more consistent output
- Add explicit JSON instructions to prompt
- Implement response validation

## Debugging Tips

### Enable Debug Logging

Add to your environment:
```bash
# .env
DEBUG=true
LOG_LEVEL=debug
```

### Test Individual Providers

Create a test script:
```python
# test_providers.py
import asyncio
from src.provider_manager import ProviderManager

async def test():
    manager = ProviderManager()
    providers = manager.get_available_providers()
    print(f"Available providers: {providers}")

asyncio.run(test())
```

### Check Server Health

```bash
# Test basic functionality
curl -X POST http://localhost:3000/health

# Or use the test script
python test_server.py
```

## Getting Help

If you're still experiencing issues:

1. Check the [GitHub Issues](https://github.com/yourusername/ai-api-mcp/issues)
2. Enable debug logging and collect error messages
3. Create a minimal reproduction example
4. Include your environment details:
   - OS and version
   - Python version
   - Node.js version (if using npm/npx)
   - Error messages and stack traces

## FAQ

**Q: Can I use only some providers?**
A: Yes, only configure API keys for the providers you want to use.

**Q: How do I update the server?**
A: 
```bash
# For pip installation
pip install --upgrade ai-api-mcp

# For npm
npm update @ai-api/mcp-server

# For development
git pull
pip install -e .
```

**Q: Can I add custom providers?**
A: Yes, create a new provider class inheriting from `AIProviderBase` and add it to the `ProviderManager`.

**Q: How do I monitor costs?**
A: Check the `usage` field in responses and track token consumption per provider.