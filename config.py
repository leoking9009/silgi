"""
애플리케이션 설정 파일

다양한 환경(개발, 테스트, 프로덕션)에 대한 설정을 관리합니다.
"""

import os
from datetime import timedelta

class Config:
    """기본 설정 클래스"""
    
    # 기본 Flask 설정
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 데이터베이스 설정
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///travel_manager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # 업로드 설정
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'static/uploads'
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # 세션 설정
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_COOKIE_SECURE = False  # HTTPS에서는 True로 설정
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # PWA 설정
    APP_NAME = os.environ.get('APP_NAME') or '여행 필수사항 관리'
    APP_SHORT_NAME = os.environ.get('APP_SHORT_NAME') or '여행관리'
    APP_DESCRIPTION = os.environ.get('APP_DESCRIPTION') or '세부 여행 필수사항을 관리하는 웹앱'
    THEME_COLOR = os.environ.get('THEME_COLOR') or '#0077be'
    BACKGROUND_COLOR = os.environ.get('BACKGROUND_COLOR') or '#e8f4f8'
    
    # 보안 설정
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    @staticmethod
    def init_app(app):
        """애플리케이션 초기화"""
        pass

class DevelopmentConfig(Config):
    """개발 환경 설정"""
    DEBUG = True
    DEVELOPMENT = True
    
    # 개발 환경에서는 더 관대한 설정
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False  # 개발 시 편의성을 위해

class TestingConfig(Config):
    """테스트 환경 설정"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
    # 테스트용 임시 업로드 폴더
    UPLOAD_FOLDER = '/tmp/test_uploads'

class ProductionConfig(Config):
    """프로덕션 환경 설정"""
    DEBUG = False
    
    # 프로덕션 보안 설정
    SESSION_COOKIE_SECURE = True
    WTF_CSRF_ENABLED = True
    
    # 로깅 설정
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # 로그 파일 설정
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug:
            file_handler = RotatingFileHandler(
                'logs/travel_manager.log',
                maxBytes=10240,
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('여행 관리 웹앱이 시작되었습니다')

# 환경별 설정 매핑
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """현재 환경에 맞는 설정을 반환합니다."""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
