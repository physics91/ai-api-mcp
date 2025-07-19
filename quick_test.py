#!/usr/bin/env python3
"""
Quick test script to check if providers are working
"""

import asyncio
import os
from src.utils import load_environment
from src.provider_manager import ProviderManager
from src.models import ChatMessage


async def quick_test():
    """Quick test of provider functionality"""
    
    print("🔍 Quick Provider Test")
    print("=" * 30)
    
    # Load environment
    load_environment()
    
    # Check .env file
    if not os.path.exists('.env'):
        print("❌ No .env file found!")
        print("   Create .env file with your API keys")
        return
    
    # Initialize manager
    try:
        manager = ProviderManager()
        providers = manager.get_available_providers()
        
        if not providers:
            print("❌ No providers configured")
            return
            
        print(f"✅ {len(providers)} provider(s) ready:")
        for p in providers:
            print(f"   • {p.value}")
            
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return
    
    # Quick chat test
    print("\n🗨️  Testing chat...")
    
    # Try each provider
    for provider_enum in providers:
        try:
            provider = manager.get_provider(provider_enum)
            if not provider:
                continue
                
            # Get first available model
            models = await provider.list_models()
            if not models:
                print(f"   ❌ {provider_enum.value}: No models")
                continue
                
            model = models[0].id
            
            # Simple test
            messages = [ChatMessage(role="user", content="Say 'OK'")]
            response = await provider.chat(
                messages=messages,
                model=model,
                max_tokens=10
            )
            
            print(f"   ✅ {provider_enum.value}: {response.content.strip()}")
            
        except Exception as e:
            print(f"   ❌ {provider_enum.value}: {str(e)}")
    
    print("\n✅ Quick test complete!")


if __name__ == "__main__":
    asyncio.run(quick_test())
