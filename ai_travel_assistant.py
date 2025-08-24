"""
AI 기반 여행 컨텐츠 생성 시스템

목적지, 여행일수, 계절, 여행 스타일 등을 분석하여
맞춤형 체크리스트, 준비물품, 현지정보, 위시리스트를 AI로 생성합니다.
"""

import json
import requests
from datetime import datetime, date
from typing import Dict, List, Optional

class AITravelAssistant:
    """AI 기반 여행 도우미"""
    
    def __init__(self):
        self.base_prompts = {
            'checklist': """
다음 여행 정보를 바탕으로 실용적인 체크리스트를 생성해주세요:
- 목적지: {destination}
- 여행 기간: {days}일
- 계절: {season}
- 여행 스타일: {travel_style}

카테고리별로 체크리스트를 만들어주세요:
1. 출발 전 (3-5개)
2. 1일차 (2-3개)  
3. 2일차 (여행이 3일 이상인 경우)
4. 3일차 (여행이 5일 이상인 경우)
5. 귀국 후 (1-2개)

각 항목은 다음 형식으로 반환해주세요:
{{"category": "출발 전", "title": "여권 유효기간 확인", "priority": "high", "description": "6개월 이상 남아있는지 확인"}}

실제 여행에서 놓치기 쉬운 중요한 사항들을 포함해주세요.
""",
            
            'items': """
다음 여행 정보를 바탕으로 필수 준비물품을 추천해주세요:
- 목적지: {destination}
- 여행 기간: {days}일
- 계절: {season}
- 여행 스타일: {travel_style}

카테고리별로 준비물을 분류해주세요:
1. 서류 (여권, 비자 등)
2. 의류 (현지 날씨와 문화 고려)
3. 용품 (현지에서 구하기 어려운 것들)
4. 약품 (현지 특성 고려)
5. 전자기기 (현지 전압, 인터넷 등 고려)

각 항목은 다음 형식으로 반환해주세요:
{{"category": "의류", "name": "방수 재킷", "quantity": 1, "notes": "우기철 필수품"}}

현지 특성을 반영한 실용적인 물품들을 추천해주세요.
""",
            
            'local_info': """
다음 목적지에 대한 실용적인 현지 정보를 제공해주세요:
- 목적지: {destination}
- 여행 기간: {days}일
- 계절: {season}

다음 카테고리별로 정보를 제공해주세요:
1. 환율 (현재 환율 정보)
2. 긴급연락처 (영사관, 응급실 등)
3. 교통수단 (추천 앱, 교통카드 등)
4. 맛집 (현지 특색 음식 2-3곳)
5. 기타 (팁 문화, 주의사항 등)

각 정보는 다음 형식으로 반환해주세요:
{{"category": "환율", "title": "현지 화폐", "content": "1달러 = 1300원 (변동)", "rating": null, "phone": null, "address": null}}

최신이고 정확한 정보를 제공해주세요.
""",
            
            'wishlist': """
다음 목적지의 여행자들이 꼭 가봐야 할 장소들을 추천해주세요:
- 목적지: {destination}
- 여행 기간: {days}일
- 계절: {season}
- 여행 스타일: {travel_style}

다음 카테고리별로 추천해주세요:
1. 관광지 (대표 명소)
2. 맛집 (현지 특색 음식점)
3. 체험 (현지만의 특별한 활동)
4. 쇼핑 (기념품, 특산품)
5. 기타 (숨은 명소)

여행 기간에 맞게 우선순위를 설정해주세요 ({days}일 여행).

각 장소는 다음 형식으로 반환해주세요:
{{"place_name": "에펠탑", "category": "관광지", "description": "파리의 상징적 랜드마크", "priority": "high", "address": "파리 7구"}}

현지인들도 추천하는 진정성 있는 장소들을 포함해주세요.
"""
        }
    
    def get_season(self, travel_date: date) -> str:
        """여행 날짜를 기준으로 계절 판단"""
        month = travel_date.month
        if month in [12, 1, 2]:
            return "겨울"
        elif month in [3, 4, 5]:
            return "봄"
        elif month in [6, 7, 8]:
            return "여름"
        else:
            return "가을"
    
    def determine_travel_style(self, destination: str, days: int) -> str:
        """목적지와 기간을 바탕으로 여행 스타일 추정"""
        if days <= 3:
            return "단기 여행"
        elif days <= 7:
            return "일반 여행"
        else:
            return "장기 여행"
    
    def generate_with_ai(self, prompt: str, category: str) -> str:
        """AI API를 사용한 컨텐츠 생성"""
        try:
            from ai_config import AIConfig
            from deepseek_client import DeepSeekClient
            import os
            
            # Claude API 사용 (우선순위)
            if AIConfig.AI_SERVICE == 'claude':
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if api_key:
                    from claude_client import ClaudeClient
                    client = ClaudeClient(api_key)
                    response = client.generate_completion(prompt, max_tokens=2000, temperature=0.7)
                    if response:
                        return response
                    else:
                        print(f"⚠️ Claude API 응답 없음, 시뮬레이션 모드로 전환")
                        return self.simulate_ai_response(prompt)
                else:
                    print(f"⚠️ ANTHROPIC_API_KEY 없음, 시뮬레이션 모드로 전환")
                    return self.simulate_ai_response(prompt)
            
            # DeepSeek API 사용
            elif AIConfig.AI_SERVICE == 'deepseek':
                api_key = os.getenv('DEEPSEEK_API_KEY')
                if api_key:
                    client = DeepSeekClient(api_key)
                    response = client.generate_completion(prompt, max_tokens=2000, temperature=0.7)
                    if response:
                        return response
                    else:
                        print(f"⚠️ DeepSeek API 응답 없음, 시뮬레이션 모드로 전환")
                        return self.simulate_ai_response(prompt)
                else:
                    print(f"⚠️ DEEPSEEK_API_KEY 없음, 시뮬레이션 모드로 전환")
                    return self.simulate_ai_response(prompt)
            
            # OpenAI API 사용 (기존)
            elif AIConfig.AI_SERVICE == 'openai':
                # OpenAI 구현 (추후 추가 가능)
                print(f"⚠️ OpenAI 미구현, 시뮬레이션 모드로 전환")
                return self.simulate_ai_response(prompt)
            
            # 시뮬레이션 모드
            else:
                return self.simulate_ai_response(prompt)
                
        except Exception as e:
            print(f"❌ AI 생성 오류 ({category}): {e}")
            return self.simulate_ai_response(prompt)
    
    def simulate_ai_response(self, prompt: str) -> str:
        """AI 응답 시뮬레이션 (데모용)"""
        # 실제로는 OpenAI, Claude, Gemini 등의 API를 사용
        # 여기서는 목적지에 따른 샘플 응답을 반환
        
        if "체크리스트" in prompt or "checklist" in prompt.lower():
            return '''[
    {"category": "출발 전", "title": "현지 날씨 확인", "priority": "high", "description": "여행 기간 동안의 날씨 예보 확인"},
    {"category": "출발 전", "title": "현지 화폐 환전", "priority": "medium", "description": "소액 현금 미리 준비"},
    {"category": "출발 전", "title": "여행자 보험 가입", "priority": "high", "description": "의료비 및 여행 취소 보장"},
    {"category": "1일차", "title": "현지 심카드 구매", "priority": "medium", "description": "공항이나 편의점에서 구매"},
    {"category": "1일차", "title": "교통카드 발급", "priority": "medium", "description": "대중교통 이용을 위한 카드"},
    {"category": "귀국 후", "title": "사진 백업", "priority": "low", "description": "여행 사진 정리 및 백업"}
]'''
        
        elif "준비물" in prompt or "items" in prompt.lower():
            return '''[
    {"category": "서류", "name": "여권 사본", "quantity": 2, "notes": "분실 대비용"},
    {"category": "의류", "name": "속건성 의류", "quantity": 3, "notes": "빠른 건조를 위해"},
    {"category": "용품", "name": "휴대용 충전기", "quantity": 1, "notes": "외출 시 필수"},
    {"category": "약품", "name": "지사제", "quantity": 1, "notes": "현지 음식 적응을 위해"},
    {"category": "전자기기", "name": "멀티 어댑터", "quantity": 1, "notes": "현지 콘센트 형태 확인"}
]'''
        
        elif "현지정보" in prompt or "local" in prompt.lower():
            return '''[
    {"category": "환율", "title": "현지 화폐 환율", "content": "실시간 환율 앱 확인 권장", "rating": null, "phone": null, "address": null},
    {"category": "긴급연락처", "title": "한국 영사관", "content": "24시간 긴급전화", "rating": null, "phone": "+1-000-000-0000", "address": "현지 영사관 주소"},
    {"category": "교통수단", "title": "현지 교통 앱", "content": "Uber, Grab 등 추천", "rating": 4.5, "phone": null, "address": null},
    {"category": "맛집", "title": "현지 특색 음식점", "content": "현지인 추천 맛집", "rating": 4.8, "phone": null, "address": "현지 주소"}
]'''
        
        elif "위시리스트" in prompt or "wishlist" in prompt.lower():
            return '''[
    {"place_name": "대표 관광명소", "category": "관광지", "description": "현지 대표 랜드마크", "priority": "high", "address": "관광지 주소"},
    {"place_name": "현지 전통시장", "category": "쇼핑", "description": "현지 문화 체험 가능", "priority": "medium", "address": "시장 주소"},
    {"place_name": "현지 특색 체험", "category": "체험", "description": "현지만의 독특한 활동", "priority": "high", "address": "체험 장소"},
    {"place_name": "현지 맛집", "category": "맛집", "description": "현지인들이 자주 가는 곳", "priority": "medium", "address": "맛집 주소"}
]'''
        
        return "[]"  # 기본값
    
    def generate_smart_content(self, destination: str, days: int, start_date: date) -> Dict:
        """AI 기반 스마트 컨텐츠 생성"""
        season = self.get_season(start_date)
        travel_style = self.determine_travel_style(destination, days)
        
        context = {
            'destination': destination,
            'days': days,
            'season': season,
            'travel_style': travel_style
        }
        
        # AI 서비스별 전용 처리
        try:
            from ai_config import AIConfig
            import os
            
            # Claude 전용 처리 (우선순위)
            if AIConfig.AI_SERVICE == 'claude' and os.getenv('ANTHROPIC_API_KEY'):
                print(f"🤖 Claude AI로 {destination} 컨텐츠 생성 중...")
                
                from claude_client import ClaudeClient
                api_key = os.getenv('ANTHROPIC_API_KEY')
                client = ClaudeClient(api_key)
                
                # Claude 전용 메서드 사용
                claude_result = client.generate_travel_content(
                    destination=destination,
                    days=days,
                    season=season,
                    travel_style=travel_style
                )
                
                if any(claude_result.values()):  # 결과가 있으면
                    print(f"✅ Claude AI 컨텐츠 생성 완료!")
                    return claude_result
                else:
                    print(f"⚠️ Claude 결과 없음, 기본 방식으로 전환")
            
            # DeepSeek 전용 처리
            elif AIConfig.AI_SERVICE == 'deepseek' and os.getenv('DEEPSEEK_API_KEY'):
                print(f"🤖 DeepSeek AI로 {destination} 컨텐츠 생성 중...")
                
                from deepseek_client import DeepSeekClient
                api_key = os.getenv('DEEPSEEK_API_KEY')
                client = DeepSeekClient(api_key)
                
                # DeepSeek 전용 메서드 사용
                deepseek_result = client.generate_travel_content(
                    destination=destination,
                    days=days,
                    season=season,
                    travel_style=travel_style
                )
                
                if any(deepseek_result.values()):  # 결과가 있으면
                    print(f"✅ DeepSeek AI 컨텐츠 생성 완료!")
                    return deepseek_result
                else:
                    print(f"⚠️ DeepSeek 결과 없음, 기본 방식으로 전환")
            
        except Exception as e:
            print(f"❌ AI 처리 오류: {e}, 기본 방식으로 전환")
        
        # 기본 방식 (프롬프트 기반)
        results = {}
        
        # 각 카테고리별로 AI 컨텐츠 생성
        for category, prompt_template in self.base_prompts.items():
            try:
                prompt = prompt_template.format(**context)
                ai_response = self.generate_with_ai(prompt, category)
                
                # JSON 파싱
                if ai_response.startswith('[') and ai_response.endswith(']'):
                    results[category] = json.loads(ai_response)
                else:
                    # JSON이 아닌 경우 기본값 사용
                    results[category] = []
                    
            except Exception as e:
                print(f"AI 생성 오류 ({category}): {e}")
                results[category] = []
        
        return results
    
    def enhance_existing_content(self, destination: str, existing_data: Dict) -> Dict:
        """기존 컨텐츠를 AI로 개선"""
        # 기존 데이터를 분석하여 부족한 부분을 AI로 보완
        enhanced = existing_data.copy()
        
        # 예: 체크리스트가 너무 적으면 AI로 추가 생성
        if len(enhanced.get('checklists', [])) < 5:
            ai_checklists = self.generate_smart_content(destination, 5, date.today())
            enhanced['checklists'].extend(ai_checklists.get('checklist', []))
        
        return enhanced

# AI 여행 도우미 통합 함수
def generate_ai_travel_content(destination: str, days: int, start_date: date) -> Dict:
    """AI 기반 여행 컨텐츠 생성 메인 함수"""
    assistant = AITravelAssistant()
    
    # 목적지별 지능형 분석
    enhanced_destination = analyze_destination(destination)
    
    # AI 컨텐츠 생성
    ai_content = assistant.generate_smart_content(enhanced_destination, days, start_date)
    
    return {
        'checklists': ai_content.get('checklist', []),
        'items': ai_content.get('items', []),
        'local_infos': ai_content.get('local_info', []),
        'wishlists': ai_content.get('wishlist', []),
        'ai_generated': True,
        'generation_info': {
            'destination': enhanced_destination,
            'analyzed_season': assistant.get_season(start_date),
            'travel_style': assistant.determine_travel_style(destination, days),
            'generated_at': datetime.now().isoformat()
        }
    }

def analyze_destination(destination: str) -> str:
    """목적지 분석 및 표준화"""
    # 목적지명 정규화 및 추가 정보 분석
    destination_lower = destination.lower().strip()
    
    # 지역별 그룹핑
    asia_destinations = {
        '도쿄': 'Tokyo, Japan',
        '오사카': 'Osaka, Japan', 
        '서울': 'Seoul, South Korea',
        '부산': 'Busan, South Korea',
        '방콕': 'Bangkok, Thailand',
        '세부': 'Cebu, Philippines',
        '싱가포르': 'Singapore',
        '홍콩': 'Hong Kong',
        '타이베이': 'Taipei, Taiwan'
    }
    
    europe_destinations = {
        '파리': 'Paris, France',
        '런던': 'London, UK',
        '로마': 'Rome, Italy',
        '바르셀로나': 'Barcelona, Spain',
        '암스테르담': 'Amsterdam, Netherlands'
    }
    
    # 한국어 → 영어 표준화
    for kr_name, en_name in {**asia_destinations, **europe_destinations}.items():
        if kr_name in destination_lower:
            return en_name
    
    return destination  # 원본 반환

# 실시간 정보 가져오기 (선택사항)
def get_realtime_info(destination: str) -> Dict:
    """실시간 정보 조회 (날씨, 환율 등)"""
    try:
        # 실제로는 OpenWeatherMap, CurrencyAPI 등 사용
        return {
            'weather': f"{destination}의 현재 날씨 정보",
            'currency': f"{destination}의 현재 환율 정보",
            'events': f"{destination}의 현재 이벤트 정보"
        }
    except:
        return {}

if __name__ == "__main__":
    # 테스트
    result = generate_ai_travel_content("도쿄", 5, date(2024, 10, 15))
    print("AI 생성 결과:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
