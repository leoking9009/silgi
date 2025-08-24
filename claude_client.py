"""
Claude AI API 클라이언트

Anthropic의 Claude AI 모델을 활용하여 
맞춤형 여행 컨텐츠를 생성하는 클라이언트입니다.
"""

import json
import requests
from typing import Dict, List, Optional
from datetime import datetime

class ClaudeClient:
    """Claude AI API 클라이언트"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.anthropic.com"):
        """
        Claude 클라이언트 초기화
        
        Args:
            api_key: Anthropic API 키
            base_url: API 베이스 URL
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.headers = {
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        self.model = "claude-3-haiku-20240307"  # Claude의 빠른 모델
    
    def generate_completion(self, prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> str:
        """
        Claude API를 사용하여 텍스트 생성
        
        Args:
            prompt: 입력 프롬프트
            max_tokens: 최대 토큰 수
            temperature: 생성 창의성 (0.0-1.0)
            
        Returns:
            생성된 텍스트
        """
        try:
            payload = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = requests.post(
                f"{self.base_url}/v1/messages",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Claude API 응답 구조에 맞춰 텍스트 추출
                content = result.get('content', [])
                if content and len(content) > 0:
                    return content[0].get('text', '').strip()
                return ""
            else:
                print(f"Claude API 오류: {response.status_code} - {response.text}")
                return ""
                
        except requests.exceptions.RequestException as e:
            print(f"Claude API 요청 오류: {e}")
            return ""
        except Exception as e:
            print(f"Claude 처리 오류: {e}")
            return ""
    
    def generate_travel_content(self, destination: str, days: int, season: str, travel_style: str) -> Dict:
        """
        여행 컨텐츠 생성
        
        Args:
            destination: 목적지
            days: 여행 일수
            season: 계절
            travel_style: 여행 스타일
            
        Returns:
            생성된 여행 컨텐츠
        """
        
        # Claude는 더 자연스러운 대화형 프롬프트를 선호함
        base_context = f"""
안녕하세요! 여행 전문가로서 다음 여행에 대한 맞춤형 추천을 부탁드립니다:

📍 목적지: {destination}
📅 여행 기간: {days}일
🌤️ 계절: {season}
🎯 여행 스타일: {travel_style}

각 카테고리별로 JSON 형태로 응답해주세요.
"""
        
        # 체크리스트 생성 프롬프트
        checklist_prompt = f"""{base_context}

**체크리스트 요청:**
여행 준비를 위한 단계별 체크리스트를 만들어주세요.

다음 카테고리로 분류해주세요:
- 출발 전 (3-4개): 여행 전 필수 준비사항
- 1일차 (2-3개): 도착 후 첫날 할 일
- 2일차 (여행이 3일 이상인 경우, 1-2개)
- 3일차 (여행이 5일 이상인 경우, 1-2개)  
- 귀국 후 (1-2개): 여행 후 정리사항

다음 JSON 형식으로만 응답해주세요:
[
    {{"category": "출발 전", "title": "여권 유효기간 확인", "priority": "high", "description": "6개월 이상 남아있는지 확인"}},
    {{"category": "1일차", "title": "현지 심카드 구매", "priority": "medium", "description": "공항이나 편의점에서 구매"}}
]

목적지의 특성과 계절을 고려한 실용적인 체크리스트를 만들어주세요.
다른 설명 없이 JSON 배열만 응답해주세요.
"""

        # 준비물품 생성 프롬프트
        items_prompt = f"""{base_context}

**준비물품 요청:**
여행에 필요한 준비물품을 카테고리별로 추천해주세요.

다음 카테고리로 분류해주세요:
- 서류 (여권, 비자, 보험 등)
- 의류 (현지 날씨와 문화 고려)
- 용품 (현지에서 구하기 어려운 것들)
- 약품 (현지 특성 고려)
- 전자기기 (현지 전압, 인터넷 등 고려)

다음 JSON 형식으로만 응답해주세요:
[
    {{"category": "의류", "name": "방수 재킷", "quantity": 1, "notes": "우기철 필수품"}},
    {{"category": "전자기기", "name": "멀티 어댑터", "quantity": 1, "notes": "현지 콘센트 형태 확인"}}
]

현지 특성을 반영한 실용적인 물품들을 추천해주세요.
다른 설명 없이 JSON 배열만 응답해주세요.
"""

        # 현지정보 생성 프롬프트
        local_info_prompt = f"""{base_context}

**현지정보 요청:**
여행지에서 유용한 현지 정보를 제공해주세요.

다음 카테고리로 분류해주세요:
- 환율 (현재 환율 정보 및 팁)
- 긴급연락처 (영사관, 응급실, 경찰 등)
- 교통수단 (추천 앱, 교통카드, 택시 팁 등)
- 맛집 (현지 특색 음식 2-3곳)
- 기타 (팁 문화, 주의사항, 에티켓 등)

다음 JSON 형식으로만 응답해주세요:
[
    {{"category": "환율", "title": "현지 화폐 정보", "content": "1달러 = 1300원 (변동)", "rating": null, "phone": null, "address": null}},
    {{"category": "맛집", "title": "현지 특색 음식점", "content": "현지인 추천 맛집", "rating": 4.8, "phone": "+82-2-1234-5678", "address": "서울시 중구 명동"}}
]

최신이고 정확한 정보를 제공해주세요.
다른 설명 없이 JSON 배열만 응답해주세요.
"""

        # 위시리스트 생성 프롬프트
        wishlist_prompt = f"""{base_context}

**위시리스트 요청:**
여행자들이 꼭 가봐야 할 장소들을 추천해주세요.

다음 카테고리로 분류해주세요:
- 관광지 (대표 명소, 박물관 등)
- 맛집 (현지 특색 음식점)
- 체험 (현지만의 특별한 활동)
- 쇼핑 (기념품, 특산품 구매처)
- 기타 (숨은 명소, 포토스팟 등)

여행 기간 {days}일에 맞게 우선순위를 설정해주세요.

다음 JSON 형식으로만 응답해주세요:
[
    {{"place_name": "에펠탑", "category": "관광지", "description": "파리의 상징적 랜드마크", "priority": "high", "address": "파리 7구"}},
    {{"place_name": "현지 전통시장", "category": "쇼핑", "description": "현지 문화 체험 가능", "priority": "medium", "address": "시장 주소"}}
]

현지인들도 추천하는 진정성 있는 장소들을 포함해주세요.
다른 설명 없이 JSON 배열만 응답해주세요.
"""

        # 각 카테고리별 컨텐츠 생성
        result = {}
        
        print(f"🤖 Claude AI로 {destination} 여행 컨텐츠 생성 중...")
        
        try:
            # 체크리스트 생성
            print("📋 체크리스트 생성 중...")
            checklist_response = self.generate_completion(checklist_prompt)
            result['checklist'] = self._parse_json_response(checklist_response, 'checklist')
            
            # 준비물품 생성
            print("🎒 준비물품 생성 중...")
            items_response = self.generate_completion(items_prompt)
            result['items'] = self._parse_json_response(items_response, 'items')
            
            # 현지정보 생성
            print("ℹ️ 현지정보 생성 중...")
            local_info_response = self.generate_completion(local_info_prompt)
            result['local_info'] = self._parse_json_response(local_info_response, 'local_info')
            
            # 위시리스트 생성
            print("❤️ 위시리스트 생성 중...")
            wishlist_response = self.generate_completion(wishlist_prompt)
            result['wishlist'] = self._parse_json_response(wishlist_response, 'wishlist')
            
            print(f"✅ Claude AI 컨텐츠 생성 완료!")
            
        except Exception as e:
            print(f"❌ Claude 컨텐츠 생성 오류: {e}")
            # 기본값 반환
            result = {
                'checklist': [],
                'items': [],
                'local_info': [],
                'wishlist': []
            }
        
        return result
    
    def _parse_json_response(self, response: str, category: str) -> List[Dict]:
        """
        AI 응답을 JSON으로 파싱
        
        Args:
            response: AI 응답 텍스트
            category: 카테고리명 (로깅용)
            
        Returns:
            파싱된 JSON 리스트
        """
        try:
            # JSON 부분만 추출 (```json 등 제거)
            response = response.strip()
            
            # 마크다운 코드 블록 제거
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0]
            elif '```' in response:
                parts = response.split('```')
                if len(parts) >= 2:
                    response = parts[1]
                else:
                    response = response.replace('```', '')
            
            # JSON 시작과 끝 찾기
            start_idx = response.find('[')
            end_idx = response.rfind(']')
            
            if start_idx != -1 and end_idx != -1:
                response = response[start_idx:end_idx+1]
            
            # JSON 파싱
            parsed = json.loads(response.strip())
            
            if isinstance(parsed, list):
                print(f"✅ {category} 파싱 성공: {len(parsed)}개 항목")
                return parsed
            else:
                print(f"⚠️ {category} 응답이 배열이 아닙니다.")
                return []
                
        except json.JSONDecodeError as e:
            print(f"❌ {category} JSON 파싱 오류: {e}")
            print(f"응답 내용: {response[:200]}...")
            return []
        except Exception as e:
            print(f"❌ {category} 처리 오류: {e}")
            return []
    
    def test_connection(self) -> bool:
        """
        Claude API 연결 테스트
        
        Returns:
            연결 성공 여부
        """
        try:
            test_prompt = "안녕하세요! 간단한 연결 테스트입니다. '연결 성공'이라고 답해주세요."
            response = self.generate_completion(test_prompt, max_tokens=50)
            
            if response and len(response) > 0:
                print(f"✅ Claude API 연결 성공: {response}")
                return True
            else:
                print("❌ Claude API 연결 실패: 응답 없음")
                return False
                
        except Exception as e:
            print(f"❌ Claude API 연결 테스트 오류: {e}")
            return False

# 테스트 함수
def test_claude_client():
    """Claude 클라이언트 테스트"""
    import os
    
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("❌ ANTHROPIC_API_KEY 환경변수가 설정되지 않았습니다.")
        print("다음과 같이 설정해주세요:")
        print("$env:ANTHROPIC_API_KEY=\"your-claude-api-key\"")
        return False
    
    client = ClaudeClient(api_key)
    
    # 연결 테스트
    if not client.test_connection():
        return False
    
    # 여행 컨텐츠 생성 테스트
    result = client.generate_travel_content(
        destination="도쿄, 일본",
        days=5,
        season="가을",
        travel_style="일반 여행"
    )
    
    print("\n🎉 Claude 여행 컨텐츠 생성 결과:")
    print(f"📋 체크리스트: {len(result.get('checklist', []))}개")
    print(f"🎒 준비물품: {len(result.get('items', []))}개")
    print(f"ℹ️ 현지정보: {len(result.get('local_info', []))}개")
    print(f"❤️ 위시리스트: {len(result.get('wishlist', []))}개")
    
    return True

if __name__ == "__main__":
    test_claude_client()
