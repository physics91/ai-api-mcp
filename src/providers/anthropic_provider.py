from typing import List, AsyncGenerator, Optional
from anthropic import AsyncAnthropic

from .base import AIProviderBase
from ..models import ChatMessage, ChatResponse, ModelInfo, AIProvider


class AnthropicProvider(AIProviderBase):
    """Anthropic Claude provider implementation"""
    
    MODELS = {
        "claude-opus-4-20250514": {
            "name": "Claude Opus 4",
            "context_window": 200000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "analysis", "hybrid_reasoning", "deep_think"]
        },
        "claude-sonnet-4-20250514": {
            "name": "Claude Sonnet 4",
            "context_window": 200000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "hybrid_reasoning"]
        },
        "claude-3-7-sonnet-20250224": {
            "name": "Claude 3.7 Sonnet",
            "context_window": 200000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "flexible_reasoning"]
        },
        "claude-3-5-sonnet-20241022": {
            "name": "Claude 3.5 Sonnet",
            "context_window": 200000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "computer_use"]
        },
        "claude-3-5-haiku-20241022": {
            "name": "Claude 3.5 Haiku",
            "context_window": 200000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "fast", "efficient"]
        },
        "claude-3-opus-20240229": {
            "name": "Claude 3 Opus",
            "context_window": 200000,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "vision", "analysis"]
        },
        "claude-3-sonnet-20240229": {
            "name": "Claude 3 Sonnet",
            "context_window": 200000,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "vision"]
        },
        "claude-3-haiku-20240307": {
            "name": "Claude 3 Haiku",
            "context_window": 200000,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "fast"]
        }
    }
    
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncAnthropic(api_key=api_key)
        
    @property
    def provider_name(self) -> AIProvider:
        return AIProvider.ANTHROPIC
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatResponse | AsyncGenerator[str, None]:
        """Send chat messages to Claude"""
        
        # Extract system message if present
        system_message = None
        anthropic_messages = []
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Set default max_tokens if not provided
        if max_tokens is None:
            max_tokens = 4096
        
        try:
            if stream:
                return self._stream_chat(
                    anthropic_messages, model, system_message,
                    temperature, max_tokens
                )
            else:
                # Prepare parameters
                params = {
                    "model": model,
                    "messages": anthropic_messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                }

                # Only add system parameter if we have a system message
                if system_message:
                    params["system"] = system_message

                response = await self.client.messages.create(**params)
                
                return ChatResponse(
                    content=response.content[0].text,
                    model=model,
                    provider=self.provider_name,
                    usage={
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    } if hasattr(response, 'usage') else None
                )
        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")
    
    async def _stream_chat(
        self,
        messages: List[dict],
        model: str,
        system: Optional[str],
        temperature: float,
        max_tokens: int
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            # Prepare parameters
            params = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }

            # Only add system parameter if we have a system message
            if system:
                params["system"] = system

            stream = await self.client.messages.create(**params)
            
            async for event in stream:
                if event.type == "content_block_delta":
                    if hasattr(event.delta, 'text'):
                        yield event.delta.text
                        
        except Exception as e:
            raise Exception(f"Anthropic streaming error: {str(e)}")
    
    async def list_models(self) -> List[ModelInfo]:
        """List available Claude models"""
        models = []
        
        for model_id, info in self.MODELS.items():
            models.append(ModelInfo(
                id=model_id,
                name=info["name"],
                provider=self.provider_name,
                description=f"Anthropic {info['name']} model",
                context_window=info["context_window"],
                max_output_tokens=info["max_output_tokens"],
                supported_features=info["features"]
            ))
            
        return models
    
    def validate_model(self, model: str) -> bool:
        """Check if model is valid for Anthropic"""
        return model in self.MODELS