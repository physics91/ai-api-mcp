# AI API MCP Server

A FastMCP-based Model Context Protocol (MCP) server that provides unified access to multiple AI APIs including OpenAI GPT, Google Gemini, Anthropic Claude, and xAI Grok.

## 📚 Documentation

- [**Quick Start**](docs/QUICKSTART.md) - Get started in 5 minutes
- [**MCP Installation Guide**](docs/MCP_INSTALLATION_GUIDE.md) - Setup for Claude Code, Claude Desktop, Cursor, VS Code, and more
- [**API Reference**](docs/API.md) - Detailed API documentation
- [**Usage Examples**](docs/EXAMPLES.md) - Practical examples and patterns
- [**Troubleshooting**](docs/TROUBLESHOOTING.md) - Common issues and solutions

## Features

- **Unified Interface**: Single MCP interface for multiple AI providers
- **Multiple Providers**: Support for OpenAI, Anthropic, Google, and xAI
- **Streaming Support**: Real-time streaming responses from all providers
- **Model Comparison**: Compare responses from multiple models simultaneously
- **Content Analysis**: Analyze code, text, security, and performance
- **Content Generation**: Generate code, documentation, and tests
- **Automatic Retry**: Built-in retry logic with exponential backoff
- **Error Handling**: Comprehensive error handling across all providers

## Installation

### Quick Install

Choose your preferred installation method:

#### Using NPX (Recommended)
```bash
npx @ai-api/mcp-server
```

#### Using Bun
```bash
bunx @ai-api/mcp-server
```

#### Using Docker
```bash
docker run -it --rm \
  -e OPENAI_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  -e GOOGLE_API_KEY=your_key \
  -e GROK_API_KEY=your_key \
  ai-api-mcp
```

#### Using Docker Compose
```bash
# Clone the repository first
git clone https://github.com/yourusername/ai-api-mcp.git
cd ai-api-mcp

# Copy and edit .env file
cp .env.example .env

# Run with docker-compose
docker-compose up
```

### Manual Installation

#### Prerequisites
- Python 3.10 or higher
- pip

#### Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-api-mcp.git
cd ai-api-mcp
```

2. Run the installation script:

**Linux/macOS:**
```bash
chmod +x install.sh
./install.sh
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -e .
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

### Development Installation

For development with hot-reload and editable installation:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Configuration

Add your API keys to the `.env` file:

```env
# AI API Keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
GROK_API_KEY=your_grok_api_key_here

# Optional: Custom API endpoints
# OPENAI_BASE_URL=https://api.openai.com/v1
# GROK_BASE_URL=https://api.x.ai/v1

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY=1.0
```

## Usage

### Running the Server

Choose your preferred method to run the server:

#### Using NPX/Bunx (No installation required)
```bash
# With npx
npx @ai-api/mcp-server

# With bunx  
bunx @ai-api/mcp-server
```

#### Using Node.js
```bash
npm start
# or
node run.js
```

#### Using Python
```bash
python -m src.server
```

#### Using Shell Script
```bash
./run.sh
```

#### Using Docker
```bash
# Build and run
docker build -t ai-api-mcp .
docker run -it --rm --env-file .env ai-api-mcp

# Or use docker-compose
docker-compose up
```

### Available Tools

#### 1. Chat
Send messages to AI models and get responses.

```python
await mcp.chat(
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello!"}
    ],
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000
)
```

#### 2. List Models
Get all available models from configured providers.

```python
models = await mcp.list_models()
```

#### 3. Compare
Compare responses from multiple models.

```python
await mcp.compare(
    prompt="Explain quantum computing",
    models=["gpt-4", "claude-3-opus-20240229", "gemini-pro"],
    temperature=0.7
)
```

#### 4. Analyze
Analyze content with specific focus.

```python
await mcp.analyze(
    content="def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
    analysis_type="code",  # options: code, text, security, performance, general
    model="gpt-4"
)
```

#### 5. Generate
Generate content of specific types.

```python
await mcp.generate(
    prompt="Create a REST API for user management",
    generation_type="code",  # options: code, text, documentation, test
    model="gpt-4",
    language="python",
    framework="FastAPI"
)
```

## Supported Models (2025)

### OpenAI
- **gpt-4.1** - 1M+ context, multimodal with massive context
- **gpt-4.1-mini** - 1M context, fast multimodal
- **gpt-4.1-nano** - 1M context, ultra-fast
- **o3** - 200K context, advanced reasoning
- **o3-pro** - 200K context, deep thinking
- **o4-mini** - 200K context, fast reasoning
- gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo

### Anthropic
- **claude-opus-4** - Hybrid reasoning with deep thinking
- **claude-sonnet-4** - Hybrid reasoning
- **claude-3.7-sonnet** - Flexible reasoning
- **claude-3.5-sonnet** - Computer use capabilities
- **claude-3.5-haiku** - Fast and efficient
- claude-3-opus, claude-3-sonnet, claude-3-haiku

### Google
- **gemini-2.5-pro** - 1M context, multimodal with deep thinking
- **gemini-2.5-flash** - 1M context, fast advanced reasoning
- **gemini-2.5-flash-lite** - High throughput, ultra-fast
- **gemini-2.0-pro** - 1M context, agent capabilities
- **gemini-2.0-flash** - 1M context, real-time multimodal
- gemini-1.5-pro, gemini-1.5-flash

### xAI
- **grok-4** - 256K context (API), 130K (standard), book/codebase analysis
- **grok-3** - 128K context, vision capabilities
- **grok-2** - 131K context, vision, function calling
- **grok-2-mini** - 131K context, fast and efficient
- grok-1.5, grok-beta

## MCP Client Support

This server works with multiple MCP-supporting tools. See our [**MCP Installation Guide**](docs/MCP_INSTALLATION_GUIDE.md) for detailed setup instructions.

### Supported Clients

- **Claude Code (CLI)** - Anthropic's official CLI with MCP support
- **Claude Desktop** - Native desktop app with MCP integration
- **Cursor IDE** - AI-powered IDE with built-in MCP support
- **VS Code** - Via GitHub Copilot Chat extension
- **Windsurf Editor** - Next-gen editor with MCP capabilities
- **Continue Extension** - Open-source AI code assistant
- And more...

### Quick Configuration Example

```json
{
  "mcpServers": {
    "ai-api": {
      "command": "npx",
      "args": ["@ai-api/mcp-server"],
      "env": {
        "OPENAI_API_KEY": "your-key",
        "ANTHROPIC_API_KEY": "your-key",
        "GOOGLE_API_KEY": "your-key",
        "GROK_API_KEY": "your-key"
      }
    }
  }
}
```

## Development

### Project Structure
```
ai-api-mcp/
├── src/
│   ├── server.py           # FastMCP server implementation
│   ├── provider_manager.py # Manages all AI providers
│   ├── models.py          # Pydantic models
│   ├── utils.py           # Utility functions
│   └── providers/         # AI provider implementations
│       ├── base.py
│       ├── openai_provider.py
│       ├── gemini_provider.py
│       ├── anthropic_provider.py
│       └── grok_provider.py
├── .env.example
├── pyproject.toml
└── README.md
```

### Adding New Providers

1. Create a new provider class in `src/providers/`
2. Inherit from `AIProviderBase`
3. Implement required methods: `chat`, `list_models`, `validate_model`
4. Add provider to `ProviderManager` in `provider_manager.py`

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.