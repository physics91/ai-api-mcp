import asyncio
import os
import time
from src.utils import load_environment
from src.provider_manager import ProviderManager

async def test_providers():
    """Test basic functionality of the MCP server"""

    # Load environment
    load_environment()

    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Please create one based on .env.example")
        return

    # Initialize provider manager
    manager = ProviderManager()

    print("\n🚀 Testing AI API MCP Server")
    print("=" * 50)

    # Test 1: List available providers
    print("\n📋 1. Available Providers:")
    providers = manager.get_available_providers()
    if providers:
        for provider in providers:
            print(f"   ✅ {provider.value}")
        print(f"\n   Total: {len(providers)} provider(s) configured")
    else:
        print("   ❌ No providers configured. Please add API keys to .env file")
        return

    # Test 2: List all models
    print("\n📋 2. Available Models:")
    try:
        start_time = time.time()
        models = await manager.list_all_models()
        end_time = time.time()

        if models:
            # Group models by provider
            provider_models = {}
            for model in models:
                if model.provider not in provider_models:
                    provider_models[model.provider] = []
                provider_models[model.provider].append(model)

            for provider, provider_model_list in provider_models.items():
                print(f"\n   🔹 {provider.value} ({len(provider_model_list)} models):")
                for model in provider_model_list[:3]:  # Show first 3 models
                    print(f"     • {model.id}")
                if len(provider_model_list) > 3:
                    print(f"     ... and {len(provider_model_list) - 3} more")

            print(f"\n   ⏱️  Model listing took {end_time - start_time:.2f}s")
            print(f"   📊 Total: {len(models)} models available")
        else:
            print("   ❌ No models available")
    except Exception as e:
        print(f"   ❌ Error listing models: {e}")

    # Test 3: Test chat with available providers
    print("\n📋 3. Testing Chat Functionality:")

    # Test models for each provider
    test_models = {
        "openai": ["gpt-3.5-turbo", "gpt-4"],
        "anthropic": ["claude-3-haiku-20240307", "claude-3-sonnet-20240229"],
        "google": ["gemini-pro", "gemini-1.5-pro"],
        "grok": ["grok-2-mini", "grok-2"]
    }

    chat_tested = False

    for provider in providers:
        provider_name = provider.value
        if provider_name in test_models:
            print(f"\n   🔍 Testing {provider_name}:")

            for model in test_models[provider_name]:
                try:
                    from src.models import ChatMessage
                    provider_instance = manager.get_provider_for_model(model)
                    if provider_instance:
                        print(f"     Testing {model}...")
                        messages = [ChatMessage(role="user", content="Say 'Hello from MCP!' and nothing else.")]

                        start_time = time.time()
                        response = await provider_instance.chat(
                            messages=messages,
                            model=model,
                            max_tokens=50,
                            temperature=0.1
                        )
                        end_time = time.time()

                        print(f"     ✅ {model}: {response.content[:50]}...")
                        print(f"     ⏱️  Response time: {end_time - start_time:.2f}s")
                        chat_tested = True
                        break  # Test only first working model per provider
                    else:
                        print(f"     ❌ {model}: No provider found")
                except Exception as e:
                    print(f"     ❌ {model}: {str(e)}")

    if not chat_tested:
        print("   ⚠️  No chat functionality could be tested")

    print("\n" + "=" * 50)
    print("✅ Basic test complete!")
    print("\nFor comprehensive testing, run: python test_providers_comprehensive.py")

if __name__ == "__main__":
    asyncio.run(test_providers())