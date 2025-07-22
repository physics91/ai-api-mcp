from typing import List, AsyncGenerator, Optional, Dict
import openai
from openai import AsyncOpenAI

from .base import AIProviderBase
from ..models import ChatMessage, ChatResponse, ModelInfo, AIProvider


class OpenAIProvider(AIProviderBase):
    """OpenAI GPT provider implementation"""
    
    MODELS = {
        # Flagship GPT Models
        "gpt-4.1": {
            "name": "GPT-4.1",
            "context_window": 1000000,
            "max_output_tokens": 32768,
            "features": ["chat", "code", "vision", "audio", "json_mode", "massive_context"]
        },
        "gpt-4o": {
            "name": "GPT-4o",
            "context_window": 128000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "audio", "json_mode"]
        },
        "gpt-4o-audio-preview": {
            "name": "GPT-4o Audio",
            "context_window": 128000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "audio", "json_mode"]
        },
        "chatgpt-4o-latest": {
            "name": "ChatGPT-4o",
            "context_window": 128000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "audio", "json_mode"]
        },
        
        # Cost-Optimized Models
        "gpt-4.1-mini": {
            "name": "GPT-4.1 Mini",
            "context_window": 1000000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "audio", "json_mode", "massive_context", "fast"]
        },
        "gpt-4.1-nano": {
            "name": "GPT-4.1 Nano",
            "context_window": 1000000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "massive_context", "ultra_fast"]
        },
        "gpt-4o-mini": {
            "name": "GPT-4o Mini",
            "context_window": 128000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "json_mode", "fast"]
        },
        "gpt-4o-mini-audio-preview": {
            "name": "GPT-4o Mini Audio",
            "context_window": 128000,
            "max_output_tokens": 16384,
            "features": ["chat", "code", "vision", "audio", "json_mode", "fast"]
        },
        
        # Reasoning Models (o-series)
        "o4-mini": {
            "name": "o4-mini",
            "context_window": 200000,
            "max_output_tokens": 65536,
            "features": ["chat", "code", "reasoning", "advanced_reasoning", "fast"]
        },
        "o3": {
            "name": "o3",
            "context_window": 200000,
            "max_output_tokens": 100000,
            "features": ["chat", "code", "reasoning", "advanced_reasoning"]
        },
        "o3-pro": {
            "name": "o3-pro",
            "context_window": 200000,
            "max_output_tokens": 100000,
            "features": ["chat", "code", "reasoning", "advanced_reasoning", "deep_thinking"]
        },
        "o3-mini": {
            "name": "o3-mini",
            "context_window": 200000,
            "max_output_tokens": 65536,
            "features": ["chat", "code", "reasoning", "advanced_reasoning", "fast"]
        },
        "o1": {
            "name": "o1",
            "context_window": 200000,
            "max_output_tokens": 100000,
            "features": ["chat", "code", "reasoning", "advanced_reasoning"]
        },
        "o1-mini": {
            "name": "o1-mini",
            "context_window": 128000,
            "max_output_tokens": 65536,
            "features": ["chat", "code", "reasoning", "advanced_reasoning"]
        },
        "o1-pro": {
            "name": "o1-pro",
            "context_window": 200000,
            "max_output_tokens": 100000,
            "features": ["chat", "code", "reasoning", "advanced_reasoning", "deep_thinking"]
        },
        
        # Older GPT Models
        "gpt-4-turbo": {
            "name": "GPT-4 Turbo",
            "context_window": 128000,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "vision", "json_mode"]
        },
        "gpt-4": {
            "name": "GPT-4",
            "context_window": 8192,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "vision"]
        },
        "gpt-3.5-turbo": {
            "name": "GPT-3.5 Turbo",
            "context_window": 16385,
            "max_output_tokens": 4096,
            "features": ["chat", "code", "fast"]
        }
    }
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        
    @property
    def provider_name(self) -> AIProvider:
        return AIProvider.OPENAI
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatResponse | AsyncGenerator[str, None]:
        """Send chat messages to OpenAI"""
        
        # Convert our message format to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        try:
            # Reasoning models (o-series) use different parameters
            is_reasoning_model = model.startswith(('o1', 'o3', 'o4'))

            if stream:
                return self._stream_chat(
                    openai_messages, model, temperature, max_tokens, is_reasoning_model
                )
            else:
                # Build parameters based on model type
                params = {
                    "model": model,
                    "messages": openai_messages,
                }

                if is_reasoning_model:
                    # Reasoning models use max_completion_tokens and don't support temperature
                    if max_tokens:
                        params["max_completion_tokens"] = max_tokens
                else:
                    # Regular models use max_tokens and temperature
                    params["temperature"] = temperature
                    if max_tokens:
                        params["max_tokens"] = max_tokens

                response = await self.client.chat.completions.create(**params)

                return ChatResponse(
                    content=response.choices[0].message.content,
                    model=model,
                    provider=self.provider_name,
                    usage={
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    } if response.usage else None
                )
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def _stream_chat(
        self,
        messages: List[Dict],
        model: str,
        temperature: float,
        max_tokens: Optional[int],
        is_reasoning_model: bool = False
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            # Build parameters based on model type
            params = {
                "model": model,
                "messages": messages,
                "stream": True
            }

            if is_reasoning_model:
                # Reasoning models use max_completion_tokens and don't support temperature
                if max_tokens:
                    params["max_completion_tokens"] = max_tokens
            else:
                # Regular models use max_tokens and temperature
                params["temperature"] = temperature
                if max_tokens:
                    params["max_tokens"] = max_tokens

            stream = await self.client.chat.completions.create(**params)
            
            async for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise Exception(f"OpenAI streaming error: {str(e)}")
    
    async def list_models(self) -> List[ModelInfo]:
        """List available OpenAI models"""
        models = []
        
        for model_id, info in self.MODELS.items():
            models.append(ModelInfo(
                id=model_id,
                name=info["name"],
                provider=self.provider_name,
                description=f"OpenAI {info['name']} model",
                context_window=info["context_window"],
                max_output_tokens=info["max_output_tokens"],
                supported_features=info["features"]
            ))
            
        return models
    
    def validate_model(self, model: str) -> bool:
        """Check if model is valid for OpenAI"""
        return model in self.MODELS