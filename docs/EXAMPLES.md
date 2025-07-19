# AI API MCP Server - Usage Examples

This guide provides practical examples of using the AI API MCP Server in various scenarios.

## Table of Contents

1. [Basic Chat Examples](#basic-chat-examples)
2. [Model Comparison](#model-comparison)
3. [Content Analysis](#content-analysis)
4. [Content Generation](#content-generation)
5. [Streaming Responses](#streaming-responses)
6. [Advanced Use Cases](#advanced-use-cases)

## Basic Chat Examples

### Simple Conversation

```javascript
// Simple question
const response = await mcp.chat({
  messages: [
    { role: "user", content: "What is the capital of France?" }
  ],
  model: "gpt-3.5-turbo"
});

console.log(response.content);
// Output: "The capital of France is Paris."
```

### Conversation with Context

```javascript
// Multi-turn conversation
const response = await mcp.chat({
  messages: [
    { role: "system", content: "You are a helpful geography teacher." },
    { role: "user", content: "What is the capital of France?" },
    { role: "assistant", content: "The capital of France is Paris." },
    { role: "user", content: "Tell me more about it." }
  ],
  model: "claude-3-sonnet-20240229",
  temperature: 0.7,
  max_tokens: 200
});
```

### Using Specific Providers

```javascript
// Force using a specific provider
const response = await mcp.chat({
  messages: [
    { role: "user", content: "Explain photosynthesis" }
  ],
  model: "gemini-pro",
  provider: "google",
  temperature: 0.5
});
```

## Model Comparison

### Compare Multiple Models

```javascript
// Compare responses from different models
const comparison = await mcp.compare({
  prompt: "Write a haiku about artificial intelligence",
  models: ["gpt-4", "claude-3-haiku-20240307", "gemini-pro"],
  temperature: 0.8
});

// Display results
comparison.responses.forEach(response => {
  console.log(`\n${response.model}:\n${response.content}`);
});
```

### Benchmark Code Generation

```javascript
// Compare code generation capabilities
const codeComparison = await mcp.compare({
  prompt: "Write a Python function to calculate fibonacci numbers with memoization",
  models: ["gpt-4", "claude-3-opus-20240229", "grok-beta"],
  temperature: 0.2
});

// Analyze which model provides the best implementation
codeComparison.responses.forEach(response => {
  console.log(`\n=== ${response.model} ===`);
  console.log(response.content);
  console.log(`Tokens used: ${response.usage?.total_tokens || 'N/A'}`);
});
```

## Content Analysis

### Code Analysis

```javascript
// Analyze Python code
const pythonCode = `
def process_data(items):
    result = []
    for i in range(len(items)):
        if items[i] > 0:
            result.append(items[i] * 2)
    return result
`;

const analysis = await mcp.analyze({
  content: pythonCode,
  analysis_type: "code",
  model: "gpt-4"
});

console.log(analysis.analysis);
// Output: Detailed analysis of code quality, suggestions for improvement
```

### Security Analysis

```javascript
// Check for security vulnerabilities
const webCode = `
app.get('/user/:id', (req, res) => {
  const query = "SELECT * FROM users WHERE id = " + req.params.id;
  db.query(query, (err, result) => {
    res.json(result);
  });
});
`;

const securityCheck = await mcp.analyze({
  content: webCode,
  analysis_type: "security",
  model: "claude-3-opus-20240229"
});

console.log(securityCheck.analysis);
// Output: SQL injection vulnerability detected, recommendations for fixes
```

### Text Analysis

```javascript
// Analyze writing style and clarity
const essay = `
The impact of technology on society has been profound. 
It has revolutionized how we communicate, work, and live. 
However, it also presents challenges that we must address.
`;

const textAnalysis = await mcp.analyze({
  content: essay,
  analysis_type: "text",
  model: "gemini-pro"
});
```

## Content Generation

### Generate Code with Framework

```javascript
// Generate FastAPI endpoint
const apiCode = await mcp.generate({
  prompt: "User registration endpoint with email validation",
  generation_type: "code",
  model: "gpt-4",
  language: "python",
  framework: "FastAPI"
});

console.log(apiCode.generated);
```

### Generate Documentation

```javascript
// Generate comprehensive documentation
const docGeneration = await mcp.generate({
  prompt: `
class UserService:
    def create_user(self, email: str, password: str) -> User:
        """Creates a new user account"""
        pass
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticates user credentials"""
        pass
  `,
  generation_type: "documentation",
  model: "claude-3-opus-20240229"
});
```

### Generate Test Cases

```javascript
// Generate unit tests
const testGeneration = await mcp.generate({
  prompt: "Calculator class with add, subtract, multiply, divide methods",
  generation_type: "test",
  model: "gpt-4",
  language: "javascript",
  framework: "jest"
});
```

## Streaming Responses

### Basic Streaming

```javascript
// Stream response for better UX
const streamResponse = await mcp.chat({
  messages: [
    { role: "user", content: "Write a short story about a robot" }
  ],
  model: "gpt-4",
  stream: true
});

// Handle streaming chunks
for await (const chunk of streamResponse) {
  process.stdout.write(chunk);
}
```

### Streaming with Progress

```javascript
// Stream with progress tracking
let totalContent = "";
const streamResponse = await mcp.chat({
  messages: [
    { role: "user", content: "Explain quantum computing in detail" }
  ],
  model: "claude-3-opus-20240229",
  stream: true,
  max_tokens: 1000
});

for await (const chunk of streamResponse) {
  totalContent += chunk;
  console.clear();
  console.log(`Generated ${totalContent.length} characters...`);
  console.log(totalContent);
}
```

## Advanced Use Cases

### Multi-Model Pipeline

```javascript
// Use different models for different tasks
async function processDocument(document) {
  // Step 1: Summarize with a fast model
  const summary = await mcp.chat({
    messages: [
      { role: "user", content: `Summarize this document: ${document}` }
    ],
    model: "gpt-3.5-turbo",
    temperature: 0.3
  });

  // Step 2: Extract key points with a powerful model
  const keyPoints = await mcp.analyze({
    content: summary.content,
    analysis_type: "text",
    model: "claude-3-opus-20240229"
  });

  // Step 3: Generate action items
  const actions = await mcp.generate({
    prompt: keyPoints.analysis,
    generation_type: "text",
    model: "gpt-4"
  });

  return {
    summary: summary.content,
    keyPoints: keyPoints.analysis,
    actions: actions.generated
  };
}
```

### Intelligent Model Selection

```javascript
// Choose model based on task complexity
async function smartChat(prompt, complexity = "medium") {
  const modelMap = {
    simple: "gpt-3.5-turbo",
    medium: "gpt-4",
    complex: "claude-3-opus-20240229",
    visual: "gemini-pro-vision"
  };

  const response = await mcp.chat({
    messages: [{ role: "user", content: prompt }],
    model: modelMap[complexity] || modelMap.medium,
    temperature: complexity === "simple" ? 0.3 : 0.7
  });

  return response;
}

// Usage
const simpleAnswer = await smartChat("What is 2+2?", "simple");
const complexAnswer = await smartChat("Explain the theory of relativity", "complex");
```

### Error Handling and Fallbacks

```javascript
// Robust implementation with fallbacks
async function reliableChat(messages, preferredModel = "gpt-4") {
  const fallbackModels = [
    "gpt-4",
    "claude-3-sonnet-20240229",
    "gemini-pro",
    "gpt-3.5-turbo"
  ];

  // Try preferred model first
  if (!fallbackModels.includes(preferredModel)) {
    fallbackModels.unshift(preferredModel);
  }

  for (const model of fallbackModels) {
    try {
      const response = await mcp.chat({
        messages,
        model,
        max_tokens: 500
      });
      
      console.log(`Success with model: ${model}`);
      return response;
    } catch (error) {
      console.log(`Failed with ${model}: ${error.message}`);
      continue;
    }
  }

  throw new Error("All models failed");
}
```

### Batch Processing

```javascript
// Process multiple requests efficiently
async function batchAnalyze(documents) {
  const analyses = await Promise.all(
    documents.map(doc => 
      mcp.analyze({
        content: doc.content,
        analysis_type: doc.type || "general",
        model: "gpt-4"
      }).catch(error => ({
        error: error.message,
        document: doc.id
      }))
    )
  );

  return analyses;
}

// Usage
const documents = [
  { id: 1, content: "Python code here...", type: "code" },
  { id: 2, content: "Security report here...", type: "security" },
  { id: 3, content: "Business proposal here...", type: "text" }
];

const results = await batchAnalyze(documents);
```

## Best Practices

1. **Choose the Right Model**: 
   - Use faster/cheaper models for simple tasks
   - Reserve powerful models for complex reasoning

2. **Optimize Token Usage**:
   - Set appropriate `max_tokens` limits
   - Use concise prompts when possible

3. **Handle Errors Gracefully**:
   - Implement retry logic for transient failures
   - Have fallback models ready

4. **Use Streaming for Long Responses**:
   - Improves user experience
   - Allows early termination if needed

5. **Cache Responses When Appropriate**:
   - For repeated queries
   - For expensive model calls

6. **Monitor Usage**:
   - Track token consumption
   - Set up alerts for unusual usage

## Common Patterns

### Conversation Memory

```javascript
class ConversationManager {
  constructor() {
    this.history = [];
  }

  async sendMessage(content, model = "gpt-4") {
    this.history.push({ role: "user", content });
    
    const response = await mcp.chat({
      messages: this.history,
      model,
      max_tokens: 500
    });

    this.history.push({ 
      role: "assistant", 
      content: response.content 
    });

    return response;
  }

  clearHistory() {
    this.history = [];
  }
}

// Usage
const conversation = new ConversationManager();
await conversation.sendMessage("Hello!");
await conversation.sendMessage("What did I just say?");
```

### Response Validation

```javascript
async function getStructuredData(prompt, model = "gpt-4") {
  const response = await mcp.chat({
    messages: [
      { 
        role: "system", 
        content: "Always respond with valid JSON" 
      },
      { role: "user", content: prompt }
    ],
    model,
    temperature: 0.1
  });

  try {
    return JSON.parse(response.content);
  } catch (e) {
    throw new Error("Invalid JSON response");
  }
}
```