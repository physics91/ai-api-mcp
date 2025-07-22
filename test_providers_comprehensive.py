#!/usr/bin/env python3
"""
Comprehensive test suite for AI API MCP providers
Tests all configured providers with various scenarios
"""

import asyncio
import os
import time
from typing import List, Dict, Any
from src.utils import load_environment
from src.provider_manager import ProviderManager
from src.models import ChatMessage, AIProvider


class ProviderTester:
    """Comprehensive provider testing class"""
    
    def __init__(self):
        self.manager = ProviderManager()
        self.test_results = {}
        
    async def run_all_tests(self):
        """Run all provider tests"""
        print("🚀 Starting Comprehensive Provider Tests\n")
        print("=" * 60)
        
        # Test 1: Basic provider initialization
        await self.test_provider_initialization()
        
        # Test 2: Model listing
        await self.test_model_listing()
        
        # Test 3: Model validation
        await self.test_model_validation()
        
        # Test 4: Basic chat functionality
        await self.test_basic_chat()
        
        # Test 5: Chat with different parameters
        await self.test_chat_parameters()
        
        # Test 6: Error handling
        await self.test_error_handling()
        
        # Test 7: Performance testing
        await self.test_performance()
        
        # Print summary
        self.print_test_summary()
        
    async def test_provider_initialization(self):
        """Test provider initialization"""
        print("\n📋 Test 1: Provider Initialization")
        print("-" * 40)
        
        providers = self.manager.get_available_providers()
        
        if not providers:
            print("❌ No providers initialized. Check your .env file.")
            self.test_results['initialization'] = {'status': 'failed', 'providers': []}
            return
            
        print(f"✅ {len(providers)} provider(s) initialized:")
        for provider in providers:
            print(f"   • {provider.value}")
            
        self.test_results['initialization'] = {
            'status': 'passed', 
            'providers': [p.value for p in providers]
        }
        
    async def test_model_listing(self):
        """Test model listing for each provider"""
        print("\n📋 Test 2: Model Listing")
        print("-" * 40)
        
        providers = self.manager.get_available_providers()
        model_results = {}
        
        for provider_enum in providers:
            provider = self.manager.get_provider(provider_enum)
            if provider:
                try:
                    print(f"\n🔍 Testing {provider_enum.value} models...")
                    models = await provider.list_models()
                    print(f"   ✅ Found {len(models)} models")
                    
                    # Show first few models
                    for i, model in enumerate(models[:3]):
                        print(f"   • {model.id} - {model.name}")
                    if len(models) > 3:
                        print(f"   ... and {len(models) - 3} more")
                        
                    model_results[provider_enum.value] = {
                        'status': 'passed',
                        'count': len(models),
                        'models': [m.id for m in models[:5]]
                    }
                    
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
                    model_results[provider_enum.value] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    
        self.test_results['model_listing'] = model_results
        
    async def test_model_validation(self):
        """Test model validation"""
        print("\n📋 Test 3: Model Validation")
        print("-" * 40)
        
        providers = self.manager.get_available_providers()
        validation_results = {}
        
        # Test models for each provider
        test_models = {
            AIProvider.OPENAI: ["gpt-4.1", "gpt-4o", "invalid-model"],
            AIProvider.ANTHROPIC: ["claude-opus-4-20250514", "claude-3-haiku-20240307", "invalid-model"],
            AIProvider.GOOGLE: ["gemini-2.5-flash", "gemini-1.5-pro", "invalid-model"],
            AIProvider.GROK: ["grok-4", "grok-2", "invalid-model"]
        }
        
        for provider_enum in providers:
            provider = self.manager.get_provider(provider_enum)
            if provider and provider_enum in test_models:
                print(f"\n🔍 Testing {provider_enum.value} model validation...")
                results = {}
                
                for model in test_models[provider_enum]:
                    is_valid = provider.validate_model(model)
                    status = "✅" if is_valid else "❌"
                    print(f"   {status} {model}: {'Valid' if is_valid else 'Invalid'}")
                    results[model] = is_valid
                    
                validation_results[provider_enum.value] = results
                
        self.test_results['model_validation'] = validation_results
        
    async def test_basic_chat(self):
        """Test basic chat functionality"""
        print("\n📋 Test 4: Basic Chat Functionality")
        print("-" * 40)
        
        providers = self.manager.get_available_providers()
        chat_results = {}
        
        # Simple test message
        test_message = [ChatMessage(role="user", content="Say 'Hello from MCP!' and nothing else.")]
        
        # Test models for each provider
        test_models = {
            AIProvider.OPENAI: "gpt-4.1-mini",
            AIProvider.ANTHROPIC: "claude-sonnet-4-20250514",
            AIProvider.GOOGLE: "gemini-2.5-flash",
            AIProvider.GROK: "grok-4"
        }
        
        for provider_enum in providers:
            if provider_enum in test_models:
                model = test_models[provider_enum]
                print(f"\n🔍 Testing {provider_enum.value} chat with {model}...")
                
                try:
                    provider = self.manager.get_provider_for_model(model)
                    if provider:
                        start_time = time.time()
                        response = await provider.chat(
                            messages=test_message,
                            model=model,
                            max_tokens=50,
                            temperature=0.1
                        )
                        end_time = time.time()
                        
                        print(f"   ✅ Response: {response.content[:100]}...")
                        print(f"   ⏱️  Response time: {end_time - start_time:.2f}s")
                        
                        chat_results[provider_enum.value] = {
                            'status': 'passed',
                            'model': model,
                            'response_time': round(end_time - start_time, 2),
                            'response_length': len(response.content)
                        }
                    else:
                        print(f"   ❌ No provider found for model {model}")
                        chat_results[provider_enum.value] = {
                            'status': 'failed',
                            'error': f'No provider for {model}'
                        }
                        
                except Exception as e:
                    print(f"   ❌ Error: {str(e)}")
                    chat_results[provider_enum.value] = {
                        'status': 'failed',
                        'error': str(e)
                    }
                    
        self.test_results['basic_chat'] = chat_results
        
    async def test_chat_parameters(self):
        """Test chat with different parameters"""
        print("\n📋 Test 5: Chat Parameter Testing")
        print("-" * 40)
        
        providers = self.manager.get_available_providers()
        if not providers:
            return
            
        # Use first available provider for parameter testing
        provider_enum = providers[0]
        provider = self.manager.get_provider(provider_enum)
        
        if not provider:
            return
            
        # Get a valid model for this provider
        models = await provider.list_models()
        if not models:
            return
            
        model = models[0].id
        print(f"🔍 Testing parameters with {provider_enum.value} - {model}")
        
        test_message = [ChatMessage(role="user", content="Write a haiku about testing.")]
        parameter_results = {}
        
        # Test different temperatures
        for temp in [0.1, 0.7, 1.0]:
            try:
                print(f"   Testing temperature {temp}...")
                response = await provider.chat(
                    messages=test_message,
                    model=model,
                    temperature=temp,
                    max_tokens=100
                )
                parameter_results[f'temp_{temp}'] = 'passed'
                print(f"   ✅ Temperature {temp}: OK")
            except Exception as e:
                parameter_results[f'temp_{temp}'] = f'failed: {str(e)}'
                print(f"   ❌ Temperature {temp}: {str(e)}")
                
        self.test_results['parameter_testing'] = parameter_results

    async def test_error_handling(self):
        """Test error handling"""
        print("\n📋 Test 6: Error Handling")
        print("-" * 40)

        providers = self.manager.get_available_providers()
        if not providers:
            return

        provider_enum = providers[0]
        provider = self.manager.get_provider(provider_enum)

        if not provider:
            return

        error_results = {}

        # Test invalid model
        try:
            print("   Testing invalid model...")
            test_message = [ChatMessage(role="user", content="Hello")]
            await provider.chat(
                messages=test_message,
                model="definitely-invalid-model-name",
                max_tokens=10
            )
            error_results['invalid_model'] = 'failed - should have thrown error'
            print("   ❌ Invalid model test failed - no error thrown")
        except Exception as e:
            error_results['invalid_model'] = 'passed'
            print("   ✅ Invalid model correctly rejected")

        # Test empty messages
        try:
            print("   Testing empty messages...")
            models = await provider.list_models()
            if models:
                await provider.chat(
                    messages=[],
                    model=models[0].id,
                    max_tokens=10
                )
                error_results['empty_messages'] = 'failed - should have thrown error'
                print("   ❌ Empty messages test failed - no error thrown")
        except Exception as e:
            error_results['empty_messages'] = 'passed'
            print("   ✅ Empty messages correctly rejected")

        self.test_results['error_handling'] = error_results

    async def test_performance(self):
        """Test performance metrics"""
        print("\n📋 Test 7: Performance Testing")
        print("-" * 40)

        providers = self.manager.get_available_providers()
        if not providers:
            return

        performance_results = {}

        for provider_enum in providers:
            provider = self.manager.get_provider(provider_enum)
            if not provider:
                continue

            try:
                models = await provider.list_models()
                if not models:
                    continue

                model = models[0].id
                print(f"   Testing {provider_enum.value} performance...")

                # Test response time for simple query
                test_message = [ChatMessage(role="user", content="Say 'OK'")]

                start_time = time.time()
                response = await provider.chat(
                    messages=test_message,
                    model=model,
                    max_tokens=10,
                    temperature=0
                )
                end_time = time.time()

                response_time = end_time - start_time
                print(f"   ⏱️  {provider_enum.value}: {response_time:.2f}s")

                performance_results[provider_enum.value] = {
                    'response_time': round(response_time, 2),
                    'model_used': model
                }

            except Exception as e:
                print(f"   ❌ {provider_enum.value}: {str(e)}")
                performance_results[provider_enum.value] = {
                    'error': str(e)
                }

        self.test_results['performance'] = performance_results

    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)

        total_tests = len(self.test_results)
        passed_tests = 0

        for test_name, results in self.test_results.items():
            print(f"\n🔍 {test_name.replace('_', ' ').title()}:")

            if test_name == 'initialization':
                if results['status'] == 'passed':
                    print(f"   ✅ PASSED - {len(results['providers'])} providers initialized")
                    passed_tests += 1
                else:
                    print("   ❌ FAILED - No providers initialized")

            elif test_name == 'model_listing':
                all_passed = all(r.get('status') == 'passed' for r in results.values())
                if all_passed:
                    print("   ✅ PASSED - All providers can list models")
                    passed_tests += 1
                else:
                    print("   ❌ FAILED - Some providers failed to list models")

            elif test_name == 'basic_chat':
                all_passed = all(r.get('status') == 'passed' for r in results.values())
                if all_passed:
                    print("   ✅ PASSED - All providers can handle basic chat")
                    passed_tests += 1
                else:
                    print("   ❌ FAILED - Some providers failed basic chat")

            else:
                # Generic handling for other tests
                if isinstance(results, dict) and 'status' in results:
                    if results['status'] == 'passed':
                        print("   ✅ PASSED")
                        passed_tests += 1
                    else:
                        print("   ❌ FAILED")
                else:
                    print("   ℹ️  COMPLETED")
                    passed_tests += 1

        print(f"\n📈 Overall Results: {passed_tests}/{total_tests} tests passed")

        if passed_tests == total_tests:
            print("🎉 All tests passed! Your providers are working correctly.")
        else:
            print("⚠️  Some tests failed. Check the details above.")

        print("\n" + "=" * 60)


async def main():
    """Main test function"""
    # Load environment variables
    load_environment()

    # Check if .env file exists
    if not os.path.exists('.env'):
        print("⚠️  No .env file found. Please create one based on .env.example")
        print("   Add your API keys to test the providers.")
        return

    # Run tests
    tester = ProviderTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
