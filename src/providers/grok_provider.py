from typing import List, AsyncGenerator, Optional
import httpx
import json

from .base import AIProviderBase
from ..models import ChatMessage, ChatResponse, ModelInfo, AIProvider


class GrokProvider(AIProviderBase):
    """xAI Grok provider implementation"""
    
    MODELS = {
        # Grok 4 Series (Latest Reasoning Models)
        "grok-4-0709": {
            "name": "Grok 4",
            "context_window": 256000,
            "max_output_tokens": 32768,
            "features": ["chat", "code", "reasoning", "advanced_reasoning", "function_calling", "structured_outputs"]
        },
        
        # Grok 3 Series
        "grok-3": {
            "name": "Grok 3",
            "context_window": 131072,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "reasoning", "vision", "function_calling", "structured_outputs"]
        },
        "grok-3-mini": {
            "name": "Grok 3 Mini",
            "context_window": 131072,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "reasoning", "fast", "efficient"]
        },
        "grok-3-fast": {
            "name": "Grok 3 Fast",
            "context_window": 131072,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "reasoning", "fast", "regional"]
        },
        "grok-3-mini-fast": {
            "name": "Grok 3 Mini Fast",
            "context_window": 131072,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "reasoning", "fast", "efficient", "ultra_fast"]
        },
        
        # Grok 2 Series (Vision Models)
        "grok-2-vision-1212": {
            "name": "Grok 2 Vision",
            "context_window": 32768,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "reasoning", "vision", "function_calling", "structured_outputs"]
        }
    }
    
    def __init__(self, api_key: str, base_url: Optional[str] = None, **kwargs):
        super().__init__(api_key, **kwargs)
        self.base_url = base_url or "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
    @property
    def provider_name(self) -> AIProvider:
        return AIProvider.GROK
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatResponse | AsyncGenerator[str, None]:
        """Send chat messages to Grok"""
        
        # Convert messages to API format
        api_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Check if it's a reasoning model (Grok 4)
        is_reasoning_model = model.startswith('grok-4')
        
        payload = {
            "model": model,
            "messages": api_messages
        }
        
        # Reasoning models don't support temperature
        if not is_reasoning_model:
            payload["temperature"] = temperature
            
        if max_tokens:
            payload["max_tokens"] = max_tokens
            
        if stream:
            payload["stream"] = True
            
        try:
            async with httpx.AsyncClient() as client:
                if stream:
                    return self._stream_chat(client, payload, model)
                else:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers=self.headers,
                        json=payload,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    
                    return ChatResponse(
                        content=data["choices"][0]["message"]["content"],
                        model=model,
                        provider=self.provider_name,
                        usage={
                            "prompt_tokens": data["usage"]["prompt_tokens"],
                            "completion_tokens": data["usage"]["completion_tokens"],
                            "total_tokens": data["usage"]["total_tokens"]
                        } if "usage" in data else None
                    )
        except httpx.HTTPStatusError as e:
            raise Exception(f"Grok API HTTP error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Grok API error: {str(e)}")
    
    async def _stream_chat(
        self,
        client: httpx.AsyncClient,
        payload: dict,
        model: str
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60.0
            ) as response:
                response.raise_for_status()
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str == "[DONE]":
                            break
                            
                        try:
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                content = data["choices"][0].get("delta", {}).get("content")
                                if content:
                                    yield content
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            raise Exception(f"Grok streaming error: {str(e)}")
    
    async def list_models(self) -> List[ModelInfo]:
        """List available Grok models"""
        models = []
        
        for model_id, info in self.MODELS.items():
            models.append(ModelInfo(
                id=model_id,
                name=info["name"],
                provider=self.provider_name,
                description=f"xAI {info['name']} model",
                context_window=info["context_window"],
                max_output_tokens=info["max_output_tokens"],
                supported_features=info["features"]
            ))
            
        return models
    
    def validate_model(self, model: str) -> bool:
        """Check if model is valid for Grok"""
        return model in self.MODELS