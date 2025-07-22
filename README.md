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
npx @physics91org/ai-api-mcp
```

#### Using Bun
```bash
bunx @physics91org/ai-api-mcp
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
npx @physics91org/ai-api-mcp

# With bunx  
bunx @physics91org/ai-api-mcp
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
#### Flagship GPT Models
- **gpt-4.1** - 1M context, multimodal with massive context
- **gpt-4o** - 128K context, fast, intelligent, flexible
- **gpt-4o-audio-preview** - 128K context, audio inputs/outputs
- **chatgpt-4o-latest** - 128K context, ChatGPT version

#### Cost-Optimized Models
- **gpt-4.1-mini** - 1M context, fast multimodal
- **gpt-4.1-nano** - 1M context, ultra-fast
- **gpt-4o-mini** - 128K context, fast and affordable
- **gpt-4o-mini-audio-preview** - 128K context, audio support

#### Reasoning Models (o-series)
- **o4-mini** - 200K context, faster reasoning
- **o3** - 200K context, most powerful reasoning
- **o3-pro** - 200K context, deep thinking
- **o3-mini** - 200K context, small reasoning alternative
- **o1** - 200K context, previous reasoning model
- **o1-mini** - 128K context, small reasoning alternative
- **o1-pro** - 200K context, enhanced reasoning

#### Older Models
- **gpt-4-turbo**, **gpt-4**, **gpt-3.5-turbo**

### Anthropic
#### Claude 4 Models (Latest Generation)
- **claude-opus-4-20250514** - Most powerful and capable model (32K output)
- **claude-sonnet-4-20250514** - High-performance with exceptional reasoning (64K output)

#### Claude 3.x Models
- **claude-3-7-sonnet-20250219** - High intelligence with extended thinking (64K output)
- **claude-3-5-sonnet-20241022** - Previous intelligent model v2 (8K output)
- **claude-3-5-sonnet-20240620** - Previous intelligent model (8K output)
- **claude-3-5-haiku-20241022** - Fastest model with intelligence (8K output)
- **claude-3-haiku-20240307** - Fast and compact for quick responses (4K output)

### Google
#### Gemini 2.5 Series (Latest with Thinking)
- **gemini-2.5-pro** - 1M context, advanced reasoning with deep thinking
- **gemini-2.5-flash** - 1M context, fast advanced reasoning with thinking
- **gemini-2.5-flash-lite-preview-06-17** - 1M context, ultra-fast and cost-effective

#### Gemini 2.0 Series
- **gemini-2.0-flash** - 1M context, real-time multimodal capabilities
- **gemini-2.0-flash-lite** - 1M context, cost-effective and fast

#### Gemini 1.5 Series (Deprecated)
- **gemini-1.5-flash** - 1M context, fast multimodal (deprecated)
- **gemini-1.5-flash-8b** - 1M context, high volume processing (deprecated)
- **gemini-1.5-pro** - 2M context, complex reasoning (deprecated)

### xAI
#### Grok 4 Series (Latest Reasoning Models)
- **grok-4-0709** - 256K context, advanced reasoning with function calling

#### Grok 3 Series
- **grok-3** - 131K context, vision and function calling capabilities
- **grok-3-mini** - 131K context, fast and efficient reasoning
- **grok-3-fast** - 131K context, high-speed processing with regional availability
- **grok-3-mini-fast** - 131K context, ultra-fast efficient processing

#### Grok 2 Series (Vision Models)
- **grok-2-vision-1212** - 32K context, vision capabilities with function calling

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
      "args": ["@physics91org/ai-api-mcp"],
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