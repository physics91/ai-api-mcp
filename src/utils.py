import os
from typing import Dict, Optional
from dotenv import load_dotenv

from .models import AIProvider


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()


def get_api_key(provider: AIProvider) -> Optional[str]:
    """Get API key for the specified provider"""
    key_mapping = {
        AIProvider.OPENAI: "OPENAI_API_KEY",
        AIProvider.ANTHROPIC: "ANTHROPIC_API_KEY",
        AIProvider.GOOGLE: "GOOGLE_API_KEY",
        AIProvider.GROK: "GROK_API_KEY"
    }
    
    env_var = key_mapping.get(provider)
    if env_var:
        return os.getenv(env_var)
    return None


def get_provider_config() -> Dict[AIProvider, Dict[str, str]]:
    """Get configuration for all providers"""
    config = {}
    
    for provider in AIProvider:
        api_key = get_api_key(provider)
        if api_key:
            config[provider] = {"api_key": api_key}
            
            # Add custom base URLs if specified
            if provider == AIProvider.OPENAI:
                base_url = os.getenv("OPENAI_BASE_URL")
                if base_url:
                    config[provider]["base_url"] = base_url
            elif provider == AIProvider.GROK:
                base_url = os.getenv("GROK_BASE_URL")
                if base_url:
                    config[provider]["base_url"] = base_url
                    
    return config


def extract_provider_from_model(model: str) -> Optional[AIProvider]:
    """Try to determine provider from model name"""
    model_lower = model.lower()
    
    if "gpt" in model_lower or "davinci" in model_lower or "curie" in model_lower:
        return AIProvider.OPENAI
    elif "claude" in model_lower:
        return AIProvider.ANTHROPIC
    elif "gemini" in model_lower:
        return AIProvider.GOOGLE
    elif "grok" in model_lower:
        return AIProvider.GROK
        
    return None


def get_retry_config() -> Dict[str, int | float]:
    """Get retry configuration from environment"""
    return {
        "max_retries": int(os.getenv("MAX_RETRIES", "3")),
        "retry_delay": float(os.getenv("RETRY_DELAY", "1.0"))
    }