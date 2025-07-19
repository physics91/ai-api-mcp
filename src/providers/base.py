from abc import ABC, abstractmethod
from typing import List, AsyncGenerator, Optional
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import (
    ChatMessage, ChatResponse, ModelInfo, AIProvider
)


class AIProviderBase(ABC):
    """Base class for all AI providers"""
    
    def __init__(self, api_key: str, max_retries: int = 3, retry_delay: float = 1.0):
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
    @property
    @abstractmethod
    def provider_name(self) -> AIProvider:
        """Return the provider name"""
        pass
    
    @abstractmethod
    async def chat(
        self,
        messages: List[ChatMessage],
        model: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> ChatResponse | AsyncGenerator[str, None]:
        """Send chat messages to the AI model"""
        pass
    
    @abstractmethod
    async def list_models(self) -> List[ModelInfo]:
        """List available models for this provider"""
        pass
    
    @abstractmethod
    def validate_model(self, model: str) -> bool:
        """Check if the model is valid for this provider"""
        pass
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request_with_retry(self, request_func, *args, **kwargs):
        """Generic retry wrapper for API requests"""
        try:
            return await request_func(*args, **kwargs)
        except Exception as e:
            print(f"Request failed for {self.provider_name}: {str(e)}")
            raise