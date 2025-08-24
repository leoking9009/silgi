"""
DeepSeek AI 설정 도우미

DeepSeek API 키를 설정하고 연결을 테스트하는 스크립트입니다.
"""

import os
import sys
from deepseek_client import DeepSeekClient

def setup_deepseek():
    """DeepSeek AI 설정 및 테스트"""
    
    print("🤖 DeepSeek AI 설정 도우미")
    print("=" * 50)
    
    # 현재 설정 확인
    current_api_key = os.getenv('DEEPSEEK_API_KEY')
    current_service = os.getenv('AI_SERVICE', 'simulation')
    
    print(f"현재 AI 서비스: {current_service}")
    print(f"DeepSeek API 키: {'설정됨' if current_api_key else '설정 안됨'}")
    print()
    
    # API 키 입력
    if not current_api_key:
        print("📝 DeepSeek API 키를 입력해주세요:")
        print("(DeepSeek 홈페이지: https://platform.deepseek.com/)")
        api_key = input("API 키: ").strip()
        
        if not api_key:
            print("❌ API 키가 입력되지 않았습니다.")
            return False
        
        # 환경변수 설정 (현재 세션에서만)
        os.environ['DEEPSEEK_API_KEY'] = api_key
        os.environ['AI_SERVICE'] = 'deepseek'
        
        print("✅ 환경변수가 설정되었습니다 (현재 세션에서만)")
        print()
        print("💡 영구 설정을 위해서는 다음 명령어를 PowerShell에서 실행하세요:")
        print(f'$env:DEEPSEEK_API_KEY="{api_key}"')
        print('$env:AI_SERVICE="deepseek"')
        print()
    else:
        api_key = current_api_key
        print("✅ DeepSeek API 키가 이미 설정되어 있습니다.")
    
    # 연결 테스트
    print("🔗 DeepSeek API 연결 테스트 중...")
    try:
        client = DeepSeekClient(api_key)
        
        if client.test_connection():
            print("🎉 DeepSeek AI 연결 성공!")
            
            # 간단한 여행 컨텐츠 생성 테스트
            print("\n🧪 여행 컨텐츠 생성 테스트 중...")
            result = client.generate_travel_content(
                destination="서울, 대한민국",
                days=3,
                season="봄",
                travel_style="단기 여행"
            )
            
            total_items = sum(len(items) for items in result.values())
            print(f"✅ 테스트 성공! 총 {total_items}개 항목 생성됨")
            print(f"   📋 체크리스트: {len(result.get('checklist', []))}개")
            print(f"   🎒 준비물품: {len(result.get('items', []))}개") 
            print(f"   ℹ️ 현지정보: {len(result.get('local_info', []))}개")
            print(f"   ❤️ 위시리스트: {len(result.get('wishlist', []))}개")
            
            return True
        else:
            print("❌ DeepSeek API 연결 실패")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def show_usage_guide():
    """사용법 가이드 표시"""
    print("\n📖 DeepSeek AI 사용법")
    print("=" * 50)
    print("1. DeepSeek 계정 생성: https://platform.deepseek.com/")
    print("2. API 키 발급")
    print("3. 이 스크립트 실행: python setup_deepseek.py")
    print("4. 여행 앱에서 'AI 맞춤형 추천' 체크박스 활성화")
    print("5. 실시간 AI 추천 받기!")
    print()
    print("💰 DeepSeek 요금:")
    print("   - 매우 저렴한 API 사용료")
    print("   - 1M 토큰당 약 $0.14 (GPT-3.5보다 7배 저렴)")
    print("   - 첫 사용자에게는 무료 크레딧 제공")

if __name__ == "__main__":
    try:
        success = setup_deepseek()
        
        if success:
            print("\n🚀 설정 완료! 이제 여행 앱에서 AI 기능을 사용할 수 있습니다.")
            print("   브라우저에서 http://localhost:5000 을 열고")
            print("   '새 여행 만들기' → 'AI 맞춤형 추천 사용' 체크 → 여행 생성!")
        else:
            print("\n❌ 설정 실패. API 키를 확인해주세요.")
            show_usage_guide()
    
    except KeyboardInterrupt:
        print("\n\n👋 설정이 중단되었습니다.")
    except Exception as e:
        print(f"\n❌ 예상치 못한 오류: {e}")
        show_usage_guide()
