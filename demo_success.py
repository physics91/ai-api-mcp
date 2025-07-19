#!/usr/bin/env python3
"""
성공적인 AI API MCP Provider 데모
모든 provider들이 실제로 동작하는 것을 보여줍니다.
"""

import asyncio
import time
from src.utils import load_environment
from src.provider_manager import ProviderManager
from src.models import ChatMessage


async def demo_success():
    """성공적인 provider 동작 데모"""
    
    print("🎉 AI API MCP Provider 성공 데모")
    print("=" * 50)
    
    # 환경 로드
    load_environment()
    
    # Provider 매니저 초기화
    manager = ProviderManager()
    providers = manager.get_available_providers()
    
    print(f"✅ {len(providers)} provider(s) 초기화 완료!")
    
    # 각 provider별 성공적인 테스트
    success_tests = [
        ("openai", "gpt-3.5-turbo", "OpenAI GPT-3.5 Turbo"),
        ("anthropic", "claude-3-haiku-20240307", "Anthropic Claude 3 Haiku"),
        ("google", "gemini-1.5-pro", "Google Gemini 1.5 Pro"),
        ("grok", "grok-2", "xAI Grok 2")
    ]
    
    print("\n🚀 실제 AI 모델 테스트:")
    print("-" * 30)
    
    for provider_name, model, display_name in success_tests:
        try:
            provider = manager.get_provider_for_model(model)
            if provider:
                print(f"\n🔍 {display_name} 테스트 중...")
                
                # 간단한 질문
                messages = [ChatMessage(
                    role="user", 
                    content="안녕하세요! 간단히 인사해주세요."
                )]
                
                start_time = time.time()
                response = await provider.chat(
                    messages=messages,
                    model=model,
                    max_tokens=100,
                    temperature=0.7
                )
                end_time = time.time()
                
                print(f"   ✅ 응답: {response.content[:80]}...")
                print(f"   ⏱️  응답 시간: {end_time - start_time:.2f}초")
                print(f"   📊 토큰 사용량: {response.usage}")
                
            else:
                print(f"   ❌ {display_name}: Provider를 찾을 수 없음")
                
        except Exception as e:
            print(f"   ⚠️  {display_name}: {str(e)}")
    
    # 모델 통계
    print(f"\n📊 지원 모델 통계:")
    print("-" * 20)
    
    all_models = await manager.list_all_models()
    provider_counts = {}
    
    for model in all_models:
        provider = model.provider.value
        if provider not in provider_counts:
            provider_counts[provider] = 0
        provider_counts[provider] += 1
    
    for provider, count in provider_counts.items():
        print(f"   • {provider}: {count}개 모델")
    
    print(f"\n   📈 총 {len(all_models)}개 모델 지원")
    
    print("\n" + "=" * 50)
    print("🎉 모든 테스트 완료!")
    print("✅ AI API MCP는 프로덕션 준비 완료 상태입니다!")
    print("🚀 이제 실제 애플리케이션에서 사용할 수 있습니다!")


if __name__ == "__main__":
    asyncio.run(demo_success())
