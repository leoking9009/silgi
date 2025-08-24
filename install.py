#!/usr/bin/env python3
"""
여행 필수사항 관리 웹앱 설치 스크립트

이 스크립트는 초기 설치 및 설정을 자동화합니다.
"""

import os
import sys
import subprocess
import sqlite3
from datetime import datetime, date

def print_banner():
    """설치 배너를 출력합니다."""
    print("🌊" * 50)
    print("   여행 필수사항 관리 웹앱 설치 스크립트")
    print("🌊" * 50)
    print()

def check_python_version():
    """Python 버전을 확인합니다."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 이상이 필요합니다.")
        print(f"현재 버전: {sys.version}")
        sys.exit(1)
    print(f"✅ Python 버전 확인: {sys.version}")

def install_dependencies():
    """의존성 패키지를 설치합니다."""
    print("\n📦 의존성 패키지 설치 중...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ 의존성 패키지 설치 완료")
    except subprocess.CalledProcessError as e:
        print(f"❌ 의존성 설치 실패: {e}")
        sys.exit(1)

def create_directories():
    """필요한 디렉토리를 생성합니다."""
    print("\n📁 디렉토리 생성 중...")
    directories = [
        'static/uploads',
        'static/images',
        'logs',
        'instance'
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ {directory} 디렉토리 생성")
        except Exception as e:
            print(f"❌ {directory} 디렉토리 생성 실패: {e}")

def create_database():
    """데이터베이스를 생성하고 초기화합니다."""
    print("\n💾 데이터베이스 초기화 중...")
    try:
        # Flask 앱 컨텍스트에서 데이터베이스 생성
        from app import app, db
        with app.app_context():
            db.create_all()
            print("✅ 데이터베이스 테이블 생성 완료")
            
            # 샘플 데이터 생성 여부 확인
            create_sample = input("\n샘플 여행 데이터를 생성하시겠습니까? (y/N): ").lower().strip()
            if create_sample == 'y':
                create_sample_data(db)
                
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {e}")

def create_sample_data(db):
    """샘플 데이터를 생성합니다."""
    print("📝 샘플 데이터 생성 중...")
    try:
        from app import Trip, Checklist, Item, LocalInfo, Expense, Wishlist
        
        # 샘플 여행 생성
        sample_trip = Trip(
            name="제주도 힐링 여행",
            destination="제주도",
            start_date=date(2024, 3, 15),
            end_date=date(2024, 3, 18)
        )
        db.session.add(sample_trip)
        db.session.commit()
        
        # 샘플 체크리스트
        checklists = [
            Checklist(trip_id=sample_trip.id, category="출발 전", title="여권 확인", priority="high"),
            Checklist(trip_id=sample_trip.id, category="출발 전", title="항공권 확인", priority="high"),
            Checklist(trip_id=sample_trip.id, category="1일차", title="숙소 체크인", priority="medium"),
            Checklist(trip_id=sample_trip.id, category="귀국 후", title="사진 정리", priority="low"),
        ]
        
        # 샘플 준비물품
        items = [
            Item(trip_id=sample_trip.id, category="서류", name="여권", quantity=1),
            Item(trip_id=sample_trip.id, category="의류", name="여행용 가방", quantity=1),
            Item(trip_id=sample_trip.id, category="전자기기", name="휴대폰 충전기", quantity=1),
        ]
        
        # 샘플 현지정보
        local_infos = [
            LocalInfo(trip_id=sample_trip.id, category="환율", title="원/달러 환율", content="1달러 = 1,300원"),
            LocalInfo(trip_id=sample_trip.id, category="맛집", title="흑돼지 맛집", content="제주 흑돼지 전문점", rating=4.5),
        ]
        
        # 샘플 위시리스트
        wishlists = [
            Wishlist(trip_id=sample_trip.id, place_name="성산일출봉", category="관광지", priority="high"),
            Wishlist(trip_id=sample_trip.id, place_name="한라산", category="관광지", priority="medium"),
        ]
        
        # 데이터베이스에 추가
        for items_list in [checklists, items, local_infos, wishlists]:
            for item in items_list:
                db.session.add(item)
        
        db.session.commit()
        print("✅ 샘플 데이터 생성 완료")
        
    except Exception as e:
        print(f"❌ 샘플 데이터 생성 실패: {e}")
        db.session.rollback()

def create_config_file():
    """환경 설정 파일을 생성합니다."""
    print("\n⚙️  환경 설정 파일 생성...")
    
    if not os.path.exists('.env'):
        env_content = """# 여행 관리 웹앱 환경 설정
FLASK_ENV=development
SECRET_KEY=your-secret-key-please-change-this
DEBUG=True
HOST=0.0.0.0
PORT=5000
"""
        try:
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            print("✅ .env 파일 생성 완료")
        except Exception as e:
            print(f"❌ .env 파일 생성 실패: {e}")
    else:
        print("✅ .env 파일이 이미 존재합니다")

def print_completion_message():
    """설치 완료 메시지를 출력합니다."""
    print("\n" + "🎉" * 50)
    print("   설치가 완료되었습니다!")
    print("🎉" * 50)
    print()
    print("📋 다음 단계:")
    print("  1. python run.py 또는 python app.py 실행")
    print("  2. 브라우저에서 http://localhost:5000 접속")
    print("  3. 새 여행 계획을 만들어보세요!")
    print()
    print("🔧 추가 설정:")
    print("  - .env 파일에서 SECRET_KEY 변경")
    print("  - static/images/ 폴더에 PWA 아이콘 추가")
    print("  - 프로덕션 배포 시 config.py 수정")
    print()
    print("🌊 즐거운 여행 계획 되세요!")

def main():
    """메인 설치 함수"""
    print_banner()
    
    try:
        check_python_version()
        install_dependencies()
        create_directories()
        create_config_file()
        create_database()
        print_completion_message()
        
    except KeyboardInterrupt:
        print("\n\n❌ 설치가 중단되었습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 설치 중 오류가 발생했습니다: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
