from typing import Dict, List, Optional
from .models import AIProvider, ModelInfo
from .providers.base import AIProviderBase
from .providers.openai_provider import OpenAIProvider
from .providers.gemini_provider import GeminiProvider
from .providers.anthropic_provider import AnthropicProvider
from .providers.grok_provider import GrokProvider
from .utils import get_provider_config, extract_provider_from_model, get_retry_config


class ProviderManager:
    """Manages all AI providers"""
    
    def __init__(self):
        self.providers: Dict[AIProvider, AIProviderBase] = {}
        self._initialize_providers()
        
    def _initialize_providers(self):
        """Initialize all configured providers"""
        provider_config = get_provider_config()
        retry_config = get_retry_config()
        
        for provider, config in provider_config.items():
            try:
                if provider == AIProvider.OPENAI:
                    self.providers[provider] = OpenAIProvider(
                        api_key=config["api_key"],
                        base_url=config.get("base_url"),
                        **retry_config
                    )
                elif provider == AIProvider.GOOGLE:
                    self.providers[provider] = GeminiProvider(
                        api_key=config["api_key"],
                        **retry_config
                    )
                elif provider == AIProvider.ANTHROPIC:
                    self.providers[provider] = AnthropicProvider(
                        api_key=config["api_key"],
                        **retry_config
                    )
                elif provider == AIProvider.GROK:
                    self.providers[provider] = GrokProvider(
                        api_key=config["api_key"],
                        base_url=config.get("base_url"),
                        **retry_config
                    )
                    
                print(f"Initialized {provider.value} provider")
            except Exception as e:
                print(f"Failed to initialize {provider.value} provider: {str(e)}")
    
    def get_provider(self, provider: AIProvider) -> Optional[AIProviderBase]:
        """Get a specific provider"""
        return self.providers.get(provider)
    
    def get_provider_for_model(self, model: str, preferred_provider: Optional[AIProvider] = None) -> Optional[AIProviderBase]:
        """Get provider for a specific model"""
        # If provider is specified, use it
        if preferred_provider:
            provider = self.get_provider(preferred_provider)
            if provider and provider.validate_model(model):
                return provider
            else:
                raise ValueError(f"Model {model} is not supported by {preferred_provider.value}")
        
        # Try to extract provider from model name
        detected_provider = extract_provider_from_model(model)
        if detected_provider:
            provider = self.get_provider(detected_provider)
            if provider and provider.validate_model(model):
                return provider
        
        # Search all providers for the model
        for provider in self.providers.values():
            if provider.validate_model(model):
                return provider
                
        return None
    
    async def list_all_models(self) -> List[ModelInfo]:
        """List all available models from all providers"""
        all_models = []
        
        for provider in self.providers.values():
            try:
                models = await provider.list_models()
                all_models.extend(models)
            except Exception as e:
                print(f"Failed to list models for {provider.provider_name}: {str(e)}")
                
        return all_models
    
    def get_available_providers(self) -> List[AIProvider]:
        """Get list of available providers"""
        return list(self.providers.keys())