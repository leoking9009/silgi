"""
AI API 설정 파일

실제 AI 서비스를 사용하기 위한 설정들
"""

import os
from typing import Optional

class AIConfig:
    """AI 서비스 설정"""
    
    # OpenAI 설정
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = 'gpt-3.5-turbo'
    
    # Google Gemini 설정
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    
    # Claude 설정
    ANTHROPIC_API_KEY: Optional[str] = os.getenv('ANTHROPIC_API_KEY')
    
    # DeepSeek 설정 (추가)
    DEEPSEEK_API_KEY: Optional[str] = os.getenv('DEEPSEEK_API_KEY')
    DEEPSEEK_BASE_URL: str = os.getenv('DEEPSEEK_BASE_URL', 'https://api.deepseek.com')
    
    # 사용할 AI 서비스 선택 (claude, deepseek, openai, gemini, simulation)
    AI_SERVICE: str = os.getenv('AI_SERVICE', 'claude')
    
    # 최대 토큰 수
    MAX_TOKENS: int = 2000
    
    # 응답 온도 (창의성)
    TEMPERATURE: float = 0.7
    
    @classmethod
    def is_ai_available(cls) -> bool:
        """실제 AI 서비스 사용 가능 여부"""
        if cls.AI_SERVICE == 'simulation':
            return True
        elif cls.AI_SERVICE == 'openai':
            return cls.OPENAI_API_KEY is not None
        elif cls.AI_SERVICE == 'gemini':
            return cls.GEMINI_API_KEY is not None
        elif cls.AI_SERVICE == 'claude':
            return cls.ANTHROPIC_API_KEY is not None
        elif cls.AI_SERVICE == 'deepseek':
            return cls.DEEPSEEK_API_KEY is not None
        return False
    
    @classmethod
    def get_service_status(cls) -> str:
        """현재 AI 서비스 상태"""
        if cls.AI_SERVICE == 'simulation':
            return "🤖 시뮬레이션 모드 (데모용)"
        elif cls.is_ai_available():
            return f"✅ {cls.AI_SERVICE.upper()} 연결됨"
        else:
            return f"❌ {cls.AI_SERVICE.upper()} API 키 필요"

# 환경변수 설정 예시 (실제 사용시)
"""
# Claude 설정 (권장)
# Windows PowerShell
$env:ANTHROPIC_API_KEY="your-claude-api-key-here"
$env:AI_SERVICE="claude"

# Linux/Mac
export ANTHROPIC_API_KEY="your-claude-api-key-here"
export AI_SERVICE="claude"

# 기타 AI 서비스
$env:DEEPSEEK_API_KEY="your-deepseek-api-key-here"
$env:AI_SERVICE="deepseek"
$env:OPENAI_API_KEY="your-openai-api-key-here"
$env:AI_SERVICE="openai"

# .env 파일 (python-dotenv 사용시)
ANTHROPIC_API_KEY=your-claude-api-key-here
AI_SERVICE=claude
DEEPSEEK_API_KEY=your-deepseek-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
"""
