# AI API MCP Server - API Documentation

## Overview

The AI API MCP Server provides a unified interface for interacting with multiple AI providers through the Model Context Protocol (MCP). This document details all available tools and their parameters.

## Available Tools

### 1. `chat` - Chat with AI Models

Send messages to AI models and receive responses.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `messages` | Array[Object] | Yes | - | Array of message objects with 'role' and 'content' |
| `model` | string | Yes | - | Model ID (e.g., 'gpt-4', 'claude-3-opus-20240229') |
| `provider` | string | No | Auto-detect | Provider name ('openai', 'anthropic', 'google', 'grok') |
| `temperature` | float | No | 0.7 | Sampling temperature (0.0-2.0) |
| `max_tokens` | integer | No | Model default | Maximum tokens to generate |
| `stream` | boolean | No | false | Whether to stream the response |

#### Message Format

```json
{
  "role": "system" | "user" | "assistant",
  "content": "string"
}
```

#### Response Format

```json
{
  "content": "string",
  "model": "string",
  "provider": "string",
  "usage": {
    "prompt_tokens": "integer",
    "completion_tokens": "integer",
    "total_tokens": "integer"
  }
}
```

#### Example

```javascript
await mcp.chat({
  messages: [
    { role: "system", content: "You are a helpful assistant" },
    { role: "user", content: "Explain quantum computing in simple terms" }
  ],
  model: "gpt-4",
  temperature: 0.7,
  max_tokens: 500
})
```

### 2. `list_models` - List Available Models

Get all available AI models from all configured providers.

#### Parameters

None

#### Response Format

```json
[
  {
    "id": "string",
    "name": "string",
    "provider": "string",
    "description": "string",
    "context_window": "integer",
    "max_output_tokens": "integer",
    "supported_features": ["string"]
  }
]
```

#### Example

```javascript
const models = await mcp.list_models()
```

### 3. `compare` - Compare Model Responses

Send the same prompt to multiple models and compare their responses.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | The prompt to send to all models |
| `models` | Array[string] | Yes | - | List of model IDs to compare |
| `temperature` | float | No | 0.7 | Sampling temperature |
| `max_tokens` | integer | No | Model default | Maximum tokens to generate |

#### Response Format

```json
{
  "prompt": "string",
  "responses": [
    {
      "content": "string",
      "model": "string",
      "provider": "string",
      "usage": {}
    }
  ]
}
```

#### Example

```javascript
await mcp.compare({
  prompt: "What is the meaning of life?",
  models: ["gpt-4", "claude-3-opus-20240229", "gemini-pro"],
  temperature: 0.7
})
```

### 4. `analyze` - Analyze Content

Analyze content with AI models for specific insights.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `content` | string | Yes | - | Content to analyze |
| `analysis_type` | string | Yes | - | Type: 'code', 'text', 'security', 'performance', 'general' |
| `model` | string | Yes | - | Model ID to use |
| `provider` | string | No | Auto-detect | Provider name |

#### Response Format

```json
{
  "analysis": "string",
  "type": "string",
  "model": "string",
  "provider": "string"
}
```

#### Analysis Types

- **code**: Code quality, potential issues, and improvements
- **text**: Tone, clarity, structure, and key points
- **security**: Security vulnerabilities and recommendations
- **performance**: Performance issues and optimization opportunities
- **general**: Comprehensive analysis

#### Example

```javascript
await mcp.analyze({
  content: "def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
  analysis_type: "code",
  model: "gpt-4"
})
```

### 5. `generate` - Generate Content

Generate content using AI models with specific parameters.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Generation prompt |
| `generation_type` | string | Yes | - | Type: 'code', 'text', 'documentation', 'test' |
| `model` | string | Yes | - | Model ID to use |
| `provider` | string | No | Auto-detect | Provider name |
| `language` | string | No | - | Programming language (for code generation) |
| `framework` | string | No | - | Framework/library (for code generation) |

#### Response Format

```json
{
  "generated": "string",
  "type": "string",
  "model": "string",
  "provider": "string",
  "language": "string",
  "framework": "string"
}
```

#### Generation Types

- **code**: Generate code snippets or full programs
- **text**: Generate natural language text
- **documentation**: Generate comprehensive documentation
- **test**: Generate test cases and unit tests

#### Example

```javascript
await mcp.generate({
  prompt: "REST API for user authentication",
  generation_type: "code",
  model: "gpt-4",
  language: "python",
  framework: "FastAPI"
})
```

## Model Support Matrix (2025)

| Provider | Models | Context Window | Features |
|----------|--------|----------------|----------|
| **OpenAI** | gpt-4.1 | 1M+ | chat, code, vision, audio, json_mode, massive_context |
| | gpt-4.1-mini | 1M | chat, code, vision, audio, json_mode, massive_context, fast |
| | gpt-4.1-nano | 1M | chat, code, massive_context, ultra_fast |
| | o3 | 200K | chat, code, advanced_reasoning, agent, tools |
| | o3-pro | 200K | chat, code, advanced_reasoning, agent, tools, deep_think |
| | o4-mini | 200K | chat, code, reasoning, agent, tools, fast |
| | gpt-4o | 128K | chat, code, vision, audio, json_mode |
| | gpt-4o-mini | 128K | chat, code, vision, json_mode, fast |
| | gpt-4-turbo | 128K | chat, code, vision, json_mode |
| | gpt-3.5-turbo | 16K | chat, code, fast, legacy |
| **Anthropic** | claude-opus-4-20250514 | 200K | chat, code, vision, analysis, hybrid_reasoning, deep_think |
| | claude-sonnet-4-20250514 | 200K | chat, code, vision, hybrid_reasoning |
| | claude-3-7-sonnet-20250224 | 200K | chat, code, vision, flexible_reasoning |
| | claude-3-5-sonnet-20241022 | 200K | chat, code, vision, computer_use |
| | claude-3-5-haiku-20241022 | 200K | chat, code, fast, efficient |
| | claude-3-opus-20240229 | 200K | chat, code, vision, analysis |
| | claude-3-sonnet-20240229 | 200K | chat, code, vision |
| | claude-3-haiku-20240307 | 200K | chat, code, fast |
| **Google** | gemini-2.5-pro | 1M | chat, code, vision, audio, video, advanced_reasoning, deep_think |
| | gemini-2.5-flash | 1M | chat, code, vision, advanced_reasoning, fast |
| | gemini-2.5-flash-lite-preview-06-17 | 128K | chat, code, ultra_fast, high_throughput |
| | gemini-2.0-pro | 1M | chat, code, vision, reasoning, agent |
| | gemini-2.0-flash-001 | 1M | chat, code, vision, audio, video, realtime, fast |
| | gemini-1.5-pro | 128K | chat, code, vision, long_context |
| | gemini-1.5-flash | 128K | chat, code, vision, long_context, fast |
| **xAI** | grok-4 | 256K | chat, code, reasoning, extended_context, book_analysis, codebase_analysis |
| | grok-4-standard | 130K | chat, code, reasoning, extended_context |
| | grok-3 | 128K | chat, code, reasoning, vision |
| | grok-2 | 131K | chat, code, reasoning, vision, function_calling |
| | grok-2-mini | 131K | chat, code, reasoning, fast, efficient |
| | grok-1.5 | 128K | chat, code, reasoning |
| | grok-beta | 131K | chat, code, reasoning, experimental |

## Error Handling

All tools return errors in a consistent format:

```json
{
  "error": "string describing the error"
}
```

Common error types:
- **Invalid API Key**: The provided API key is incorrect or missing
- **Model Not Found**: The specified model is not available
- **Rate Limit**: API rate limit exceeded
- **Network Error**: Connection issues with the AI provider
- **Invalid Parameters**: Request parameters are invalid or missing

## Rate Limits and Retries

The server implements automatic retry logic with exponential backoff:
- Default max retries: 3
- Default retry delay: 1.0 seconds (exponentially increasing)
- Configurable via environment variables

## Best Practices

1. **Model Selection**: Choose models based on your specific needs:
   - For fast responses: Use models with 'fast' feature
   - For long documents: Use models with high context windows
   - For vision tasks: Use models with 'vision' feature

2. **Temperature Settings**:
   - 0.0-0.3: Deterministic, focused responses
   - 0.4-0.7: Balanced creativity and consistency
   - 0.8-2.0: Creative, varied responses

3. **Token Management**:
   - Set `max_tokens` to control response length
   - Monitor usage in responses for cost tracking

4. **Error Handling**:
   - Always handle potential errors in your application
   - Implement your own retry logic for critical operations

5. **Streaming**:
   - Use streaming for long responses to improve UX
   - Handle stream interruptions gracefully