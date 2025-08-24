#!/usr/bin/env python3
"""
여행 필수사항 관리 웹앱 실행 스크립트

이 스크립트는 Flask 애플리케이션을 실행하기 위한 진입점입니다.
개발 환경과 프로덕션 환경에서 모두 사용할 수 있습니다.
"""

import os
import sys
from app import app, db

def create_database():
    """데이터베이스 테이블을 생성합니다."""
    with app.app_context():
        db.create_all()
        print("✅ 데이터베이스 테이블이 생성되었습니다.")

def run_app():
    """Flask 애플리케이션을 실행합니다."""
    # 환경 변수에서 설정 읽기
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🌊 여행 관리 웹앱을 시작합니다...")
    print(f"📍 주소: http://{host}:{port}")
    print(f"🔧 디버그 모드: {'ON' if debug else 'OFF'}")
    print(f"💾 데이터베이스: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 데이터베이스 초기화
    create_database()
    
    # 업로드 폴더 생성
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    print(f"📁 업로드 폴더: {app.config['UPLOAD_FOLDER']}")
    
    print("\n🚀 애플리케이션을 시작합니다...\n")
    
    # Flask 앱 실행
    app.run(
        host=host,
        port=port,
        debug=debug,
        threaded=True
    )

if __name__ == '__main__':
    try:
        run_app()
    except KeyboardInterrupt:
        print("\n\n👋 여행 관리 웹앱을 종료합니다. 안전한 여행 되세요!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류가 발생했습니다: {e}")
        sys.exit(1)
