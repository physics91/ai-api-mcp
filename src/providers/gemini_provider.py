from typing import List, AsyncGenerator, Optional
import google.generativeai as genai
import asyncio

from .base import AIProviderBase
from ..models import ChatMessage, ChatResponse, ModelInfo, AIProvider


class GeminiProvider(AIProviderBase):
    """Google Gemini provider implementation"""
    
    MODELS = {
        "gemini-2.5-pro": {
            "name": "Gemini 2.5 Pro",
            "context_window": 1000000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "audio", "video", "advanced_reasoning", "deep_think"]
        },
        "gemini-2.5-flash": {
            "name": "Gemini 2.5 Flash",
            "context_window": 1000000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "advanced_reasoning", "fast"]
        },
        "gemini-2.5-flash-lite-preview-06-17": {
            "name": "Gemini 2.5 Flash Lite",
            "context_window": 128000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "ultra_fast", "high_throughput"]
        },
        "gemini-2.0-pro": {
            "name": "Gemini 2.0 Pro",
            "context_window": 1000000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "reasoning", "agent"]
        },
        "gemini-2.0-flash-001": {
            "name": "Gemini 2.0 Flash",
            "context_window": 1000000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "audio", "video", "realtime", "fast"]
        },
        "gemini-1.5-pro": {
            "name": "Gemini 1.5 Pro",
            "context_window": 128000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "long_context"]
        },
        "gemini-1.5-flash": {
            "name": "Gemini 1.5 Flash",
            "context_window": 128000,
            "max_output_tokens": 8192,
            "features": ["chat", "code", "vision", "long_context", "fast"]
        }
    }
    
    def __init__(self, api_key: str, **kwargs):
        super().__init__(api_key, **kwargs)
        genai.configure(api_key=api_key)
        
    @property
    def provider_name(self) -> AIProvider:
        return AIProvider.GOOGLE
    
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatResponse | AsyncGenerator[str, None]:
        """Send chat messages to Gemini"""
        
        # Initialize the model
        generation_config = genai.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        gemini_model = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config
        )
        
        # Convert messages to Gemini format
        gemini_messages = self._convert_messages(messages)
        
        try:
            if stream:
                return self._stream_chat(gemini_model, gemini_messages, model)
            else:
                # Run synchronous method in thread pool
                response = await asyncio.to_thread(
                    gemini_model.generate_content,
                    gemini_messages
                )

                # Check if response was blocked or empty
                if not response.candidates or not response.candidates[0].content.parts:
                    # Try to get the reason for blocking
                    if response.candidates and response.candidates[0].finish_reason:
                        finish_reason = response.candidates[0].finish_reason
                        if finish_reason == 2:  # SAFETY
                            raise Exception("Response was blocked by safety filters")
                        elif finish_reason == 3:  # RECITATION
                            raise Exception("Response was blocked due to recitation")
                        else:
                            raise Exception(f"Response generation failed (finish_reason: {finish_reason})")
                    else:
                        raise Exception("No response generated")

                # Extract text content
                content = ""
                if response.candidates and response.candidates[0].content.parts:
                    for part in response.candidates[0].content.parts:
                        if hasattr(part, 'text'):
                            content += part.text

                if not content:
                    content = "No content generated"

                return ChatResponse(
                    content=content,
                    model=model,
                    provider=self.provider_name,
                    usage={
                        "prompt_tokens": response.usage_metadata.prompt_token_count,
                        "completion_tokens": response.usage_metadata.candidates_token_count,
                        "total_tokens": response.usage_metadata.total_token_count
                    } if hasattr(response, 'usage_metadata') else None
                )
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def _convert_messages(self, messages: List[ChatMessage]) -> List[dict]:
        """Convert our message format to Gemini format"""
        gemini_messages = []
        
        for msg in messages:
            if msg.role == "system":
                # Gemini doesn't have system role, prepend to first user message
                if gemini_messages and gemini_messages[0]["role"] == "user":
                    gemini_messages[0]["parts"][0] = f"{msg.content}\n\n{gemini_messages[0]['parts'][0]}"
                else:
                    gemini_messages.insert(0, {
                        "role": "user",
                        "parts": [msg.content]
                    })
            elif msg.role == "user":
                gemini_messages.append({
                    "role": "user",
                    "parts": [msg.content]
                })
            elif msg.role == "assistant":
                gemini_messages.append({
                    "role": "model",
                    "parts": [msg.content]
                })
                
        return gemini_messages
    
    async def _stream_chat(
        self,
        model: genai.GenerativeModel,
        messages: List[dict],
        model_name: str
    ) -> AsyncGenerator[str, None]:
        """Stream chat responses"""
        try:
            # Run synchronous streaming in thread pool
            response = await asyncio.to_thread(
                model.generate_content,
                messages,
                stream=True
            )
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            raise Exception(f"Gemini streaming error: {str(e)}")
    
    async def list_models(self) -> List[ModelInfo]:
        """List available Gemini models"""
        models = []
        
        for model_id, info in self.MODELS.items():
            models.append(ModelInfo(
                id=model_id,
                name=info["name"],
                provider=self.provider_name,
                description=f"Google {info['name']} model",
                context_window=info["context_window"],
                max_output_tokens=info["max_output_tokens"],
                supported_features=info["features"]
            ))
            
        return models
    
    def validate_model(self, model: str) -> bool:
        """Check if model is valid for Gemini"""
        return model in self.MODELS