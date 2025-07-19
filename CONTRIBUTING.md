# Contributing to AI API MCP Server

Thank you for your interest in contributing to AI API MCP Server! This guide will help you get started.

## 🤝 How to Contribute

### Reporting Issues

1. Check [existing issues](https://github.com/yourusername/ai-api-mcp/issues) first
2. Use issue templates when available
3. Include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Open a [feature request](https://github.com/yourusername/ai-api-mcp/issues/new?template=feature_request.md)
2. Explain the use case
3. Provide examples if possible

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

## 🛠️ Development Setup

### Prerequisites

- Python 3.10+
- Node.js 16+ (for npm/npx features)
- Git

### Local Development

```bash
# Clone your fork
git clone https://github.com/yourusername/ai-api-mcp.git
cd ai-api-mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_providers.py

# Run linting
ruff check src/
black --check src/
mypy src/
```

## 📝 Code Style

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://github.com/psf/black) for formatting
- Use [Ruff](https://github.com/astral-sh/ruff) for linting
- Type hints are required for all functions

### Example

```python
from typing import List, Optional

async def process_messages(
    messages: List[str], 
    max_length: Optional[int] = None
) -> str:
    """Process a list of messages.
    
    Args:
        messages: List of message strings
        max_length: Optional maximum length
        
    Returns:
        Processed message string
    """
    # Implementation here
    pass
```

## 🧪 Testing Guidelines

### Writing Tests

```python
# tests/test_example.py
import pytest
from src.models import ChatMessage

class TestChatMessage:
    def test_create_message(self):
        msg = ChatMessage(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
    
    @pytest.mark.asyncio
    async def test_async_operation(self):
        # Test async functions
        result = await some_async_function()
        assert result is not None
```

### Test Structure

```
tests/
├── test_providers/
│   ├── test_openai.py
│   ├── test_gemini.py
│   └── test_anthropic.py
├── test_server.py
├── test_models.py
└── conftest.py
```

## 🏗️ Adding a New Provider

### Step 1: Create Provider Class

```python
# src/providers/new_provider.py
from .base import AIProviderBase
from ..models import AIProvider, ChatResponse

class NewProvider(AIProviderBase):
    """Implementation for New AI Provider"""
    
    @property
    def provider_name(self) -> AIProvider:
        return AIProvider.NEW
    
    async def chat(self, messages, model, **kwargs):
        # Implementation
        pass
    
    async def list_models(self):
        # Return available models
        pass
    
    def validate_model(self, model: str) -> bool:
        # Check if model is valid
        pass
```

### Step 2: Update Models

```python
# src/models.py
class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    GROK = "grok"
    NEW = "new"  # Add new provider
```

### Step 3: Update Provider Manager

```python
# src/provider_manager.py
from .providers.new_provider import NewProvider

# In _initialize_providers method:
elif provider == AIProvider.NEW:
    self.providers[provider] = NewProvider(
        api_key=config["api_key"],
        **retry_config
    )
```

### Step 4: Add Tests

```python
# tests/test_providers/test_new.py
import pytest
from src.providers.new_provider import NewProvider

class TestNewProvider:
    @pytest.fixture
    def provider(self):
        return NewProvider(api_key="test_key")
    
    def test_provider_name(self, provider):
        assert provider.provider_name == "new"
```

## 📚 Documentation

### Update Documentation

When adding features, update:
- API documentation in `docs/API.md`
- Examples in `docs/EXAMPLES.md`
- README if needed

### Documentation Style

- Use clear, concise language
- Include code examples
- Add type information
- Keep formatting consistent

## 🔄 Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🎯 Areas for Contribution

### Good First Issues

- Add more examples to documentation
- Improve error messages
- Add unit tests for edge cases
- Fix typos and improve docs

### Feature Ideas

- Support for more AI providers
- Caching mechanisms
- Rate limiting improvements
- Response filtering/moderation
- Plugin system

### Performance

- Optimize token counting
- Improve streaming performance
- Add connection pooling
- Implement request batching

## 💬 Getting Help

- Join discussions in [GitHub Discussions](https://github.com/yourusername/ai-api-mcp/discussions)
- Ask questions in issues
- Check existing documentation

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Every contribution helps make AI API MCP Server better for everyone. We appreciate your time and effort!