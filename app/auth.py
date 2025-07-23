"""
인증(Authentication) 관련 모듈

이 파일의 역할:
1. JWT 토큰을 생성하고 검증합니다
2. 비밀번호를 안전하게 해시화합니다
3. 로그인한 사용자를 확인하는 의존성 함수를 제공합니다

초보자를 위한 설명:
- JWT: JSON Web Token, 사용자 인증 정보를 안전하게 전달하는 토큰
- 해시: 비밀번호를 암호화하여 저장하는 방법
- 의존성 주입: FastAPI에서 자동으로 인증을 확인하는 방법
"""

import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import models
from .database import get_db

# ====== 보안 설정 ======

# 비밀번호 해싱을 위한 설정
# bcrypt: 안전한 해시 알고리즘
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer 토큰 스키마 (Authorization: Bearer <token> 형식)
security = HTTPBearer()

# JWT 토큰 설정
# 환경변수에서 비밀키를 가져오거나 기본값 사용
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"  # JWT 서명 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 토큰 만료 시간 (30분)

# ====== 비밀번호 관련 함수들 ======

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력받은 비밀번호가 해시된 비밀번호와 일치하는지 확인
    
    Args:
        plain_password: 사용자가 입력한 평문 비밀번호
        hashed_password: 데이터베이스에 저장된 해시된 비밀번호
    
    Returns:
        bool: 비밀번호가 일치하면 True, 아니면 False
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    비밀번호를 안전하게 해시화
    
    Args:
        password: 해시화할 평문 비밀번호
    
    Returns:
        str: 해시화된 비밀번호
    """
    return pwd_context.hash(password)

# ====== JWT 토큰 관련 함수들 ======

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    JWT 액세스 토큰을 생성합니다
    
    Args:
        data: 토큰에 포함할 데이터 (보통 사용자 ID)
        expires_delta: 토큰 만료 시간 (기본값: 30분)
    
    Returns:
        str: 생성된 JWT 토큰
    """
    # 토큰에 포함할 데이터를 복사
    to_encode = data.copy()
    
    # 만료 시간 설정
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # 만료 시간을 토큰 데이터에 추가
    to_encode.update({"exp": expire})
    
    # JWT 토큰 생성 및 반환
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """
    JWT 토큰을 검증하고 사용자명을 추출합니다
    
    Args:
        token: 검증할 JWT 토큰
    
    Returns:
        Optional[str]: 토큰이 유효하면 사용자명, 아니면 None
    """
    try:
        # 토큰 디코딩 및 검증
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # "sub"는 주체(subject)를 의미
        
        if username is None:
            return None
        return username
    except JWTError:
        # 토큰이 유효하지 않거나 만료된 경우
        return None

# ====== 사용자 인증 관련 함수들 ======

def authenticate_user(db: Session, username: str, password: str):
    """
    사용자명과 비밀번호로 사용자를 인증합니다
    
    Args:
        db: 데이터베이스 세션
        username: 사용자명
        password: 비밀번호
    
    Returns:
        User or False: 인증 성공시 사용자 객체, 실패시 False
    """
    # 사용자명으로 사용자 찾기
    user = db.query(models.User).filter(models.User.username == username).first()
    
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    if not user.is_active:
        return False
    
    return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    현재 로그인한 사용자를 반환하는 의존성 함수
    
    FastAPI의 Depends와 함께 사용하여 API 엔드포인트에서
    자동으로 로그인한 사용자를 확인할 수 있습니다.
    
    사용 예시:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"message": f"Hello {current_user.username}!"}
    
    Args:
        credentials: HTTP Bearer 토큰 (자동으로 추출됨)
        db: 데이터베이스 세션 (자동으로 주입됨)
    
    Returns:
        User: 현재 로그인한 사용자 객체
    
    Raises:
        HTTPException: 토큰이 유효하지 않거나 사용자를 찾을 수 없는 경우
    """
    # 401 Unauthorized 에러 템플릿
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보가 유효하지 않습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 토큰에서 사용자명 추출
    username = verify_token(credentials.credentials)
    if username is None:
        raise credentials_exception
    
    # 데이터베이스에서 사용자 찾기
    user = db.query(models.User).filter(models.User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """
    현재 로그인한 활성 사용자를 반환하는 의존성 함수
    
    get_current_user와 유사하지만 추가로 계정이 활성화되어 있는지 확인합니다.
    
    Args:
        current_user: 현재 로그인한 사용자 (자동으로 주입됨)
    
    Returns:
        User: 현재 로그인한 활성 사용자 객체
    
    Raises:
        HTTPException: 계정이 비활성화된 경우
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="비활성화된 계정입니다"
        )
    return current_user