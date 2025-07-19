import asyncio
from typing import List, Dict, Any
from fastmcp import FastMCP

from .utils import load_environment
from .provider_manager import ProviderManager
from .models import (
    ChatMessage, ChatRequest, ChatResponse,
    CompareRequest, CompareResponse,
    AnalyzeRequest, GenerateRequest,
    AIProvider
)

# Initialize environment
load_environment()

# Create MCP server
mcp = FastMCP("AI API MCP Server")

# Initialize provider manager
provider_manager = ProviderManager()


@mcp.tool()
async def chat(
    messages: List[Dict[str, str]], 
    model: str,
    provider: str = None,
    temperature: float = 0.7,
    max_tokens: int = None,
    stream: bool = False
) -> Dict[str, Any]:
    """
    Chat with AI models from various providers
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model ID (e.g., 'gpt-4', 'claude-3-opus', 'gemini-pro')
        provider: Optional provider name ('openai', 'anthropic', 'google', 'grok')
        temperature: Sampling temperature (0.0-2.0)
        max_tokens: Maximum tokens to generate
        stream: Whether to stream the response
        
    Returns:
        Response with content, model info, and usage stats
    """
    try:
        # Convert messages
        chat_messages = [ChatMessage(**msg) for msg in messages]
        
        # Get provider
        provider_enum = AIProvider(provider) if provider else None
        ai_provider = provider_manager.get_provider_for_model(model, provider_enum)
        
        if not ai_provider:
            return {"error": f"No provider found for model: {model}"}
        
        # Make chat request
        response = await ai_provider.chat(
            messages=chat_messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=stream
        )
        
        if stream:
            # For streaming, collect all chunks
            content = ""
            async for chunk in response:
                content += chunk
            
            return {
                "content": content,
                "model": model,
                "provider": ai_provider.provider_name.value
            }
        else:
            return response.model_dump()
            
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def list_models() -> List[Dict[str, Any]]:
    """
    List all available AI models from all configured providers
    
    Returns:
        List of model information including ID, name, provider, and capabilities
    """
    try:
        models = await provider_manager.list_all_models()
        return [model.model_dump() for model in models]
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
async def compare(
    prompt: str,
    models: List[str],
    temperature: float = 0.7,
    max_tokens: int = None
) -> Dict[str, Any]:
    """
    Compare responses from multiple AI models
    
    Args:
        prompt: The prompt to send to all models
        models: List of model IDs to compare
        temperature: Sampling temperature
        max_tokens: Maximum tokens to generate
        
    Returns:
        Comparison results with responses from each model
    """
    try:
        responses = []
        
        # Create messages
        messages = [ChatMessage(role="user", content=prompt)]
        
        # Run all requests concurrently
        tasks = []
        for model in models:
            provider = provider_manager.get_provider_for_model(model)
            if provider:
                task = provider.chat(
                    messages=messages,
                    model=model,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False
                )
                tasks.append((model, task))
        
        # Wait for all responses
        for model, task in tasks:
            try:
                response = await task
                responses.append(response.model_dump())
            except Exception as e:
                responses.append({
                    "model": model,
                    "error": str(e)
                })
        
        return {
            "prompt": prompt,
            "responses": responses
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def analyze(
    content: str,
    analysis_type: str,
    model: str,
    provider: str = None
) -> Dict[str, Any]:
    """
    Analyze content using AI models
    
    Args:
        content: Content to analyze
        analysis_type: Type of analysis ('code', 'text', 'security', 'performance', 'general')
        model: Model ID to use
        provider: Optional provider name
        
    Returns:
        Analysis results
    """
    try:
        # Create analysis prompt based on type
        prompts = {
            "code": f"Analyze this code and provide insights on quality, potential issues, and improvements:\n\n{content}",
            "text": f"Analyze this text for tone, clarity, structure, and key points:\n\n{content}",
            "security": f"Analyze this code for security vulnerabilities and provide recommendations:\n\n{content}",
            "performance": f"Analyze this code for performance issues and optimization opportunities:\n\n{content}",
            "general": f"Provide a comprehensive analysis of the following:\n\n{content}"
        }
        
        prompt = prompts.get(analysis_type, prompts["general"])
        messages = [ChatMessage(role="user", content=prompt)]
        
        # Get provider
        provider_enum = AIProvider(provider) if provider else None
        ai_provider = provider_manager.get_provider_for_model(model, provider_enum)
        
        if not ai_provider:
            return {"error": f"No provider found for model: {model}"}
        
        response = await ai_provider.chat(
            messages=messages,
            model=model,
            temperature=0.3,  # Lower temperature for analysis
            stream=False
        )
        
        return {
            "analysis": response.content,
            "type": analysis_type,
            "model": model,
            "provider": ai_provider.provider_name.value
        }
        
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def generate(
    prompt: str,
    generation_type: str,
    model: str,
    provider: str = None,
    language: str = None,
    framework: str = None
) -> Dict[str, Any]:
    """
    Generate content using AI models
    
    Args:
        prompt: Generation prompt
        generation_type: Type of generation ('code', 'text', 'documentation', 'test')
        model: Model ID to use
        provider: Optional provider name
        language: Programming language (for code generation)
        framework: Framework/library (for code generation)
        
    Returns:
        Generated content
    """
    try:
        # Enhance prompt based on generation type
        enhanced_prompt = prompt
        
        if generation_type == "code":
            if language:
                enhanced_prompt = f"Generate {language} code:\n{prompt}"
            if framework:
                enhanced_prompt += f"\nUse {framework} framework/library."
                
        elif generation_type == "documentation":
            enhanced_prompt = f"Generate comprehensive documentation for:\n{prompt}"
            
        elif generation_type == "test":
            enhanced_prompt = f"Generate test cases for:\n{prompt}"
            if language:
                enhanced_prompt += f"\nUse {language} testing framework."
        
        messages = [ChatMessage(role="user", content=enhanced_prompt)]
        
        # Get provider
        provider_enum = AIProvider(provider) if provider else None
        ai_provider = provider_manager.get_provider_for_model(model, provider_enum)
        
        if not ai_provider:
            return {"error": f"No provider found for model: {model}"}
        
        response = await ai_provider.chat(
            messages=messages,
            model=model,
            temperature=0.7,
            stream=False
        )
        
        return {
            "generated": response.content,
            "type": generation_type,
            "model": model,
            "provider": ai_provider.provider_name.value,
            "language": language,
            "framework": framework
        }
        
    except Exception as e:
        return {"error": str(e)}


def main():
    """Run the MCP server"""
    mcp.run()


if __name__ == "__main__":
    main()