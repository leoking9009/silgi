"""
목적지별 여행 템플릿 시스템

목적지와 여행일수에 따라 자동으로 체크리스트, 준비물품, 현지정보, 위시리스트를 생성합니다.
"""

from datetime import date, timedelta

class DestinationTemplate:
    """목적지별 템플릿 기본 클래스"""
    
    def __init__(self, destination, days):
        self.destination = destination.lower()
        self.days = days
    
    def get_template_data(self):
        """템플릿 데이터를 반환합니다"""
        return {
            'checklists': self.get_checklists(),
            'items': self.get_items(),
            'local_infos': self.get_local_infos(),
            'wishlists': self.get_wishlists(),
            'expenses': self.get_sample_expenses()
        }
    
    def get_checklists(self):
        """기본 체크리스트 + 목적지 특화 체크리스트"""
        base_checklists = [
            {'category': '출발 전', 'title': '여권 유효기간 확인', 'priority': 'high'},
            {'category': '출발 전', 'title': '항공권 예약 확인', 'priority': 'high'},
            {'category': '출발 전', 'title': '숙소 예약 확인', 'priority': 'high'},
            {'category': '출발 전', 'title': '여행자 보험 가입', 'priority': 'medium'},
            {'category': '출발 전', 'title': '현지 화폐 환전', 'priority': 'medium'},
            {'category': '1일차', 'title': '숙소 체크인', 'priority': 'high'},
            {'category': '귀국 후', 'title': '사진 정리', 'priority': 'low'},
        ]
        
        # 여행일수에 따른 추가 체크리스트
        if self.days >= 3:
            base_checklists.extend([
                {'category': '1일차', 'title': '현지 교통카드/패스 구매', 'priority': 'medium'},
                {'category': '2일차', 'title': '주요 관광지 방문', 'priority': 'high'},
            ])
        
        if self.days >= 5:
            base_checklists.extend([
                {'category': '3일차', 'title': '현지 맛집 탐방', 'priority': 'medium'},
                {'category': '3일차', 'title': '쇼핑 및 기념품 구매', 'priority': 'low'},
            ])
        
        if self.days >= 7:
            base_checklists.append(
                {'category': '출발 전', 'title': '장기여행용 약품 준비', 'priority': 'medium'}
            )
        
        return base_checklists + self.get_destination_checklists()
    
    def get_destination_checklists(self):
        """목적지별 특화 체크리스트"""
        return []
    
    def get_items(self):
        """기본 준비물품 + 목적지 특화 물품"""
        base_items = [
            {'category': '서류', 'name': '여권', 'quantity': 1, 'notes': '유효기간 6개월 이상'},
            {'category': '서류', 'name': '항공권', 'quantity': 1, 'notes': '모바일 체크인 완료'},
            {'category': '전자기기', 'name': '휴대폰 충전기', 'quantity': 1, 'notes': ''},
            {'category': '약품', 'name': '개인상비약', 'quantity': 1, 'notes': '소화제, 두통약 등'},
        ]
        
        # 여행일수에 따른 의류 수량 조정
        clothing_qty = min(self.days, 7)  # 최대 7벌
        base_items.append({
            'category': '의류', 'name': '여행용 옷', 'quantity': clothing_qty, 
            'notes': f'{self.days}일 여행용'
        })
        
        return base_items + self.get_destination_items()
    
    def get_destination_items(self):
        """목적지별 특화 준비물품"""
        return []
    
    def get_local_infos(self):
        """목적지별 현지정보"""
        return []
    
    def get_wishlists(self):
        """목적지별 추천 위시리스트"""
        return []
    
    def get_sample_expenses(self):
        """목적지별 예상 지출"""
        return []

class CebuTemplate(DestinationTemplate):
    """세부(필리핀) 여행 템플릿"""
    
    def get_destination_checklists(self):
        lists = [
            {'category': '출발 전', 'title': '수영복 준비', 'priority': 'high'},
            {'category': '출발 전', 'title': '선크림 구매 (SPF50+)', 'priority': 'high'},
            {'category': '1일차', 'title': '심카드 또는 로밍 설정', 'priority': 'medium'},
        ]
        
        if self.days >= 2:
            lists.append({'category': '2일차', 'title': '오슬롭 고래상어 투어 예약', 'priority': 'high'})
        
        return lists
    
    def get_destination_items(self):
        return [
            {'category': '의류', 'name': '수영복', 'quantity': 2, 'notes': '해변 활동용'},
            {'category': '의류', 'name': '썬글라스', 'quantity': 1, 'notes': '자외선 차단'},
            {'category': '용품', 'name': '선크림', 'quantity': 1, 'notes': 'SPF 50 이상'},
            {'category': '용품', 'name': '수건', 'quantity': 2, 'notes': '속건성 여행용'},
            {'category': '용품', 'name': '스노클링 장비', 'quantity': 1, 'notes': '선택사항'},
            {'category': '전자기기', 'name': '방수카메라', 'quantity': 1, 'notes': '수중 촬영용'},
        ]
    
    def get_local_infos(self):
        return [
            {'category': '환율', 'title': '필리핀 페소 환율', 'content': '1 PHP ≈ 22원 (변동)', 'rating': None},
            {'category': '긴급연락처', 'title': '한국 총영사관', 'content': '세부 한국 총영사관', 
             'phone': '+63-32-231-0909', 'address': 'Cebu City'},
            {'category': '교통수단', 'title': 'Grab 앱', 'content': '동남아 대표 택시 앱', 'rating': 4.5},
            {'category': '맛집', 'title': '렉촌 맛집', 'content': '필리핀 전통 돼지고기 요리', 'rating': 4.8},
            {'category': '기타', 'title': '날씨', 'content': '열대성 기후, 연중 26-32도, 우기 6-11월', 'rating': None},
        ]
    
    def get_wishlists(self):
        basic_list = [
            {'place_name': '오슬롭 고래상어 투어', 'category': '체험', 'description': '고래상어와 스노클링', 'priority': 'high'},
            {'place_name': '카와산 폭포', 'category': '관광지', 'description': '캐녀닝과 폭포수영', 'priority': 'high'},
            {'place_name': '템플 오브 리아', 'category': '관광지', 'description': '힌두 사원', 'priority': 'medium'},
        ]
        
        if self.days >= 4:
            basic_list.extend([
                {'place_name': '보홀 초콜릿 힐', 'category': '관광지', 'description': '보홀섬 당일치기', 'priority': 'medium'},
                {'place_name': 'SM 시티 세부', 'category': '쇼핑', 'description': '대형 쇼핑몰', 'priority': 'low'},
            ])
        
        return basic_list

class TokyoTemplate(DestinationTemplate):
    """도쿄(일본) 여행 템플릿"""
    
    def get_destination_checklists(self):
        lists = [
            {'category': '출발 전', 'title': '엔화 환전', 'priority': 'high'},
            {'category': '출발 전', 'title': '포켓와이파이 예약', 'priority': 'medium'},
            {'category': '1일차', 'title': 'IC카드(Suica/Pasmo) 구매', 'priority': 'high'},
        ]
        
        if self.days >= 3:
            lists.append({'category': '2일차', 'title': '디즈니랜드/디즈니시 티켓 예약', 'priority': 'medium'})
        
        return lists
    
    def get_destination_items(self):
        # 계절별 의류 (간단화: 봄/가을 기준)
        return [
            {'category': '의류', 'name': '가벼운 외투', 'quantity': 1, 'notes': '일교차 대비'},
            {'category': '의류', 'name': '편한 운동화', 'quantity': 1, 'notes': '많이 걸어야 함'},
            {'category': '전자기기', 'name': '포켓와이파이', 'quantity': 1, 'notes': '인터넷 연결용'},
            {'category': '용품', 'name': '에코백', 'quantity': 1, 'notes': '비닐봉지 유료'},
        ]
    
    def get_local_infos(self):
        return [
            {'category': '환율', 'title': '엔화 환율', 'content': '1 JPY ≈ 9원 (변동)', 'rating': None},
            {'category': '교통수단', 'title': 'JR 패스', 'content': '외국인 전용 무제한 교통패스', 'rating': 4.8},
            {'category': '맛집', 'title': '스시 잔마이', 'content': '유명 스시 체인점', 'rating': 4.5},
            {'category': '기타', 'title': '팁 문화', 'content': '일본은 팁 문화가 없음', 'rating': None},
        ]
    
    def get_wishlists(self):
        return [
            {'place_name': '센소지 절', 'category': '관광지', 'description': '아사쿠사 전통 사원', 'priority': 'high'},
            {'place_name': '도쿄 스카이트리', 'category': '관광지', 'description': '도쿄 랜드마크', 'priority': 'high'},
            {'place_name': '시부야 교차로', 'category': '관광지', 'description': '세계 최대 횡단보도', 'priority': 'medium'},
            {'place_name': '츠키지 시장', 'category': '맛집', 'description': '신선한 해산물', 'priority': 'high'},
        ]

class JejuTemplate(DestinationTemplate):
    """제주도 여행 템플릿"""
    
    def get_destination_checklists(self):
        lists = [
            {'category': '출발 전', 'title': '렌터카 예약', 'priority': 'high'},
            {'category': '1일차', 'title': '렌터카 인수', 'priority': 'high'},
        ]
        
        if self.days >= 2:
            lists.append({'category': '2일차', 'title': '한라산 등반 준비', 'priority': 'medium'})
        
        return lists
    
    def get_destination_items(self):
        return [
            {'category': '서류', 'name': '운전면허증', 'quantity': 1, 'notes': '렌터카 이용시'},
            {'category': '의류', 'name': '등산화', 'quantity': 1, 'notes': '한라산 등반용'},
            {'category': '의류', 'name': '바람막이', 'quantity': 1, 'notes': '제주 바람 대비'},
            {'category': '용품', 'name': '등산 배낭', 'quantity': 1, 'notes': '당일치기용'},
        ]
    
    def get_local_infos(self):
        return [
            {'category': '교통수단', 'title': '렌터카 업체', 'content': '제주공항 내 다수 업체', 'rating': 4.0},
            {'category': '맛집', 'title': '흑돼지 맛집', 'content': '제주 특산품', 'rating': 4.7},
            {'category': '기타', 'title': '날씨', 'content': '바람이 강함, 우산보다 바람막이 추천', 'rating': None},
        ]
    
    def get_wishlists(self):
        return [
            {'place_name': '성산일출봉', 'category': '관광지', 'description': 'UNESCO 세계자연유산', 'priority': 'high'},
            {'place_name': '한라산', 'category': '관광지', 'description': '대한민국 최고봉', 'priority': 'high'},
            {'place_name': '섭지코지', 'category': '관광지', 'description': '아름다운 해안절벽', 'priority': 'medium'},
            {'place_name': '제주 올레길', 'category': '체험', 'description': '트레킹 코스', 'priority': 'medium'},
        ]

# 템플릿 팩토리
def get_destination_template(destination, days):
    """목적지에 따른 적절한 템플릿을 반환합니다"""
    destination_lower = destination.lower()
    
    if any(keyword in destination_lower for keyword in ['세부', 'cebu']):
        return CebuTemplate(destination, days)
    elif any(keyword in destination_lower for keyword in ['도쿄', 'tokyo', '일본', 'japan']):
        return TokyoTemplate(destination, days)
    elif any(keyword in destination_lower for keyword in ['제주', 'jeju']):
        return JejuTemplate(destination, days)
    else:
        # 기본 템플릿
        return DestinationTemplate(destination, days)

def apply_template_to_trip(trip_id, destination, days):
    """여행에 템플릿을 적용합니다"""
    from app import app, db, Checklist, Item, LocalInfo, Wishlist
    
    template = get_destination_template(destination, days)
    template_data = template.get_template_data()
    
    with app.app_context():
        # 체크리스트 추가
        for checklist_data in template_data['checklists']:
            checklist = Checklist(
                trip_id=trip_id,
                category=checklist_data['category'],
                title=checklist_data['title'],
                priority=checklist_data['priority']
            )
            db.session.add(checklist)
        
        # 준비물품 추가
        for item_data in template_data['items']:
            item = Item(
                trip_id=trip_id,
                category=item_data['category'],
                name=item_data['name'],
                quantity=item_data['quantity'],
                notes=item_data['notes']
            )
            db.session.add(item)
        
        # 현지정보 추가
        for info_data in template_data['local_infos']:
            local_info = LocalInfo(
                trip_id=trip_id,
                category=info_data['category'],
                title=info_data['title'],
                content=info_data['content'],
                rating=info_data.get('rating'),
                phone=info_data.get('phone'),
                address=info_data.get('address')
            )
            db.session.add(local_info)
        
        # 위시리스트 추가
        for wishlist_data in template_data['wishlists']:
            from app import Wishlist
            wishlist = Wishlist(
                trip_id=trip_id,
                place_name=wishlist_data['place_name'],
                category=wishlist_data['category'],
                description=wishlist_data['description'],
                priority=wishlist_data['priority']
            )
            db.session.add(wishlist)
        
        db.session.commit()
        
        return {
            'checklists': len(template_data['checklists']),
            'items': len(template_data['items']),
            'local_infos': len(template_data['local_infos']),
            'wishlists': len(template_data['wishlists'])
        }
