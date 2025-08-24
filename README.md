# 🌊 여행 필수사항 관리 웹앱

세부 여행 필수사항을 관리하는 모던한 Flask 웹 애플리케이션입니다. 
바다색 테마의 직관적인 UI로 여행 준비부터 여행 후 정리까지 모든 과정을 체계적으로 관리할 수 있습니다.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-orange.svg)

## ✨ 주요 기능

### 🎯 핵심 관리 기능
- **스마트 체크리스트**: 여행 일정별 필수사항 관리 (출발 전, 1일차~3일차, 귀국 후)
- **준비물품 관리**: 카테고리별 패킹리스트 (서류, 의류, 용품, 약품, 전자기기)
- **현지 정보 저장**: 환율, 긴급연락처, 교통수단, 맛집 정보
- **예산 관리**: 지출 기록 및 카테고리별 분석
- **위시리스트**: 가고 싶은 곳 관리 및 방문 완료 체크
- **여행 기록**: 사진과 메모로 추억 저장

### 🎨 UI/UX 특징
- **바다색 테마**: 여행에 어울리는 바다색 계열 컬러 스킴
- **반응형 디자인**: 모바일 친화적 Bootstrap 5 기반
- **진행률 표시**: 실시간 체크리스트 및 패킹 진행률
- **직관적 탭 구성**: 카테고리별 깔끔한 정보 분류
- **인터랙티브 체크박스**: 부드러운 애니메이션과 피드백

### 📱 PWA (Progressive Web App)
- **오프라인 지원**: 인터넷 없이도 로컬에서 사용 가능
- **앱 설치**: 모바일/데스크톱에 앱처럼 설치 가능
- **백그라운드 동기화**: 온라인 복구 시 자동 데이터 동기화
- **푸시 알림**: 여행 일정 알림 (선택사항)

## 🛠️ 기술 스택

### Backend
- **Flask 2.3+**: 경량 웹 프레임워크
- **SQLAlchemy**: ORM 및 데이터베이스 관리
- **SQLite**: 로컬 데이터베이스
- **Werkzeug**: WSGI 유틸리티 라이브러리

### Frontend
- **Bootstrap 5.3**: 반응형 UI 프레임워크
- **Bootstrap Icons**: 아이콘 시스템
- **Vanilla JavaScript**: 순수 자바스크립트 (라이브러리 의존성 최소화)
- **CSS3**: 커스텀 스타일링 및 애니메이션

### PWA 기술
- **Service Worker**: 오프라인 캐싱 및 백그라운드 동기화
- **Web App Manifest**: 앱 설치 및 네이티브 앱 경험
- **LocalStorage**: 클라이언트 사이드 데이터 저장

## 🚀 설치 및 실행

### 요구사항
- Python 3.8 이상
- pip (패키지 관리자)

### 1. 저장소 클론
```bash
git clone <repository-url>
cd travel-manager
```

### 2. 가상환경 생성 (권장)
```bash
# Windows
python -m venv venv
venv\\Scripts\\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 애플리케이션 실행
```bash
python app.py
```

### 5. 브라우저에서 접속
```
http://localhost:5000
```

## 📱 PWA 설치

### 데스크톱 (Chrome/Edge)
1. 웹사이트 접속
2. 주소창 우측의 "설치" 버튼 클릭
3. "설치" 확인

### 모바일 (iOS Safari)
1. Safari에서 웹사이트 접속
2. 공유 버튼 탭
3. "홈 화면에 추가" 선택

### 모바일 (Android Chrome)
1. Chrome에서 웹사이트 접속
2. 메뉴 → "홈 화면에 추가"
3. 설치 확인

## 📊 데이터베이스 구조

### 주요 테이블
- **Trip**: 여행 기본 정보
- **Checklist**: 일정별 체크리스트
- **Item**: 준비물품 목록
- **LocalInfo**: 현지 정보
- **Expense**: 지출 기록
- **Wishlist**: 위시리스트
- **Memory**: 여행 기록

### 관계도
```
Trip (1) ←→ (N) Checklist
Trip (1) ←→ (N) Item
Trip (1) ←→ (N) LocalInfo
Trip (1) ←→ (N) Expense
Trip (1) ←→ (N) Wishlist
Trip (1) ←→ (N) Memory
```

## 🎯 사용법

### 1. 여행 계획 생성
1. "새 여행 만들기" 클릭
2. 여행 이름, 목적지, 날짜 입력
3. 자동으로 기본 체크리스트 생성

### 2. 체크리스트 관리
1. 여행 상세 페이지의 "체크리스트" 탭
2. 일정별로 분류된 항목들 확인
3. 완료된 항목 체크

### 3. 준비물품 관리
1. "준비물품" 탭에서 카테고리별 확인
2. 패킹 완료 시 체크박스 선택
3. 실시간 패킹 진행률 확인

### 4. 현지정보 저장
1. "현지정보" 탭에서 유용한 정보 저장
2. 환율, 연락처, 맛집 등 추가

### 5. 예산 관리
1. "예산관리" 탭에서 지출 기록
2. 카테고리별 분류 및 총액 확인

## 🔧 개발자 가이드

### 프로젝트 구조
```
travel-manager/
├── app.py                 # 메인 Flask 애플리케이션
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 문서
├── static/               # 정적 파일
│   ├── css/
│   │   └── custom.css    # 커스텀 스타일
│   ├── js/
│   │   ├── app.js        # 메인 JavaScript
│   │   └── sw.js         # Service Worker
│   └── uploads/          # 업로드된 파일
├── templates/            # Jinja2 템플릿
│   ├── base.html         # 기본 템플릿
│   ├── index.html        # 홈페이지
│   ├── create_trip.html  # 여행 생성
│   └── trip_detail.html  # 여행 상세
└── travel_manager.db     # SQLite 데이터베이스 (자동 생성)
```

### API 엔드포인트
- `GET /`: 홈페이지
- `GET /trip/<id>`: 여행 상세
- `GET/POST /create_trip`: 여행 생성
- `POST /api/toggle_checklist/<id>`: 체크리스트 토글
- `POST /api/toggle_item/<id>`: 아이템 토글
- `POST /api/toggle_wishlist/<id>`: 위시리스트 토글
- `POST /api/add_item`: 새 항목 추가
- `GET /manifest.json`: PWA 매니페스트

### 환경 설정
개발 환경에서는 `app.py`의 설정을 수정하세요:
```python
app.config['SECRET_KEY'] = 'your-secret-key'  # 프로덕션에서 변경 필요
app.config['DEBUG'] = False  # 프로덕션에서 False로 설정
```

## 🚀 배포

### 1. Heroku 배포
```bash
# Procfile 생성
echo "web: python app.py" > Procfile

# Heroku CLI로 배포
heroku create your-app-name
git push heroku main
```

### 2. Docker 배포
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### 3. 일반 서버 배포
- nginx + gunicorn 조합 권장
- HTTPS 설정 필수 (PWA 요구사항)
- 정적 파일 서빙 최적화

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- [Bootstrap](https://getbootstrap.com/) - UI 프레임워크
- [Bootstrap Icons](https://icons.getbootstrap.com/) - 아이콘 시스템
- [Flask](https://flask.palletsprojects.com/) - 웹 프레임워크
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM

## 📞 지원

문제가 있거나 기능 요청이 있다면 GitHub Issues를 통해 연락해 주세요.

---

**Happy Traveling! 🌊✈️**
