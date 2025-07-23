"""
FastAPI 메인 애플리케이션 모듈

이 파일의 역할:
1. FastAPI 애플리케이션을 생성하고 설정합니다
2. 인증 및 할일 관리 API 엔드포인트를 정의합니다
3. JWT 토큰 기반 사용자 인증 시스템을 제공합니다
4. CORS 미들웨어로 크로스 오리진 요청을 허용합니다
5. 데이터베이스 연결을 관리하고 자동으로 테이블을 생성합니다

주요 기능:
- 🔐 사용자 회원가입/로그인 (JWT 토큰 발급)
- 📝 개인별 할일 CRUD 작업 (생성, 조회, 수정, 삭제)
- 🔒 토큰 기반 인증으로 사용자별 데이터 격리
- 🌏 CORS 설정으로 프론트엔드와 안전한 통신

초보자를 위한 설명:
- FastAPI: Python으로 만든 현대적이고 빠른 웹 API 프레임워크
- 엔드포인트: 클라이언트가 요청을 보낼 수 있는 URL 주소 (예: /login, /todos/)
- CORS: 다른 도메인에서 이 API를 사용할 수 있도록 허용하는 설정
- JWT: JSON Web Token, 사용자 인증 정보를 안전하게 전달하는 토큰
- 미들웨어: 모든 요청에 공통으로 적용되는 기능들
"""

# ====== 필요한 라이브러리들을 가져옵니다 ======
from fastapi import FastAPI, Depends, HTTPException, status  # FastAPI 핵심 기능들
from fastapi.middleware.cors import CORSMiddleware          # CORS 처리를 위한 미들웨어
from sqlalchemy.orm import Session                          # 데이터베이스 세션 타입
from typing import List                                     # 리스트 타입 힌트
from datetime import timedelta                              # 토큰 만료 시간 설정용

# ====== 우리가 만든 모듈들을 가져옵니다 ======
from . import crud, models                                  # CRUD 함수들과 데이터베이스 모델
from .database import SessionLocal, engine, get_db         # 데이터베이스 연결 관련
from .crud import (
    TodoCreate, TodoUpdate, TodoResponse,                   # 할일 관련 스키마
    UserCreate, UserLogin, UserResponse, Token             # 사용자 관련 스키마
)
from .auth import (
    authenticate_user, create_access_token,                 # 인증 관련 함수
    get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES    # 사용자 확인 함수
)

# ====== 데이터베이스 초기화 ======
# 애플리케이션이 시작될 때 데이터베이스 테이블들을 자동으로 생성합니다
# 이미 테이블이 있다면 건드리지 않고, 없다면 새로 만듭니다
print("📊 데이터베이스 테이블을 확인하고 생성 중...")
models.Base.metadata.create_all(bind=engine)
print("✅ 데이터베이스 초기화 완료!")

# ====== FastAPI 애플리케이션 생성 ======
app = FastAPI(
    title="📝 할일 관리 API",  # 자동 생성되는 API 문서에 표시될 제목
    description="한국 시간 기준으로 작동하는 간단한 할일 관리 애플리케이션 API입니다.",  
    version="1.0.0",  # API 버전 (클라이언트가 호환성을 확인할 때 사용)
    docs_url="/docs",  # Swagger UI 문서 경로 (기본값)
    redoc_url="/redoc"  # ReDoc 문서 경로 (기본값)
)

# CORS (Cross-Origin Resource Sharing) 설정
# 프론트엔드가 다른 포트에서 실행되어도 API에 접근할 수 있도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인에서 접근 허용 (개발용)
    # 실제 운영환경에서는 특정 도메인만 허용해야 함
    # 예: allow_origins=["http://localhost:3000", "https://mydomain.com"]
    allow_credentials=True,  # 쿠키 포함 요청 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT, DELETE 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

# ====== API 엔드포인트 정의 ======

@app.get("/")
def read_root():
    """
    루트 엔드포인트
    API가 정상적으로 작동하는지 확인하는 용도
    """
    return {"message": "할일 관리 API에 오신 것을 환영합니다!"}

# ====== 인증 관련 엔드포인트 ======

@app.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    회원가입 엔드포인트
    새로운 사용자 계정을 생성합니다.
    
    Args:
        user: 회원가입 정보 (사용자명, 이메일, 비밀번호)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        UserResponse: 생성된 사용자 정보 (비밀번호 제외)
    
    Raises:
        HTTPException: 이미 존재하는 사용자명이나 이메일인 경우 400 에러
    """
    # 중복 사용자명 확인
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 사용자명입니다"
        )
    
    # 중복 이메일 확인
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 새 사용자 생성
    return crud.create_user(db=db, user=user)

@app.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    로그인 엔드포인트
    사용자 인증 후 JWT 토큰을 발급합니다.
    
    Args:
        user_credentials: 로그인 정보 (사용자명, 비밀번호)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        Token: JWT 액세스 토큰과 토큰 타입
    
    Raises:
        HTTPException: 인증 실패 시 401 에러
    """
    # 사용자 인증 확인
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자명 또는 비밀번호가 잘못되었습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # JWT 토큰 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    """
    현재 로그인한 사용자 정보 조회 엔드포인트
    JWT 토큰을 통해 인증된 사용자의 정보를 반환합니다.
    
    Args:
        current_user: 현재 로그인한 사용자 (자동 주입)
    
    Returns:
        UserResponse: 현재 사용자 정보
    """
    return current_user

# ====== 할일 관련 엔드포인트 ======

@app.post("/todos/", response_model=TodoResponse)
def create_todo(
    todo: TodoCreate, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    새로운 할일을 생성합니다.
    로그인한 사용자만 접근 가능하며, 해당 사용자의 할일로 등록됩니다.
    
    Args:
        todo: 생성할 할일 데이터 (제목, 설명, 우선순위)
        current_user: 현재 로그인한 사용자 (자동 주입)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        TodoResponse: 생성된 할일 정보
    """
    return crud.create_todo(db=db, todo=todo, owner_id=current_user.id)

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    현재 로그인한 사용자의 할일 목록을 조회합니다.
    
    Args:
        skip: 건너뛸 항목 수 (기본값: 0)
        limit: 반환할 최대 항목 수 (기본값: 100)
        current_user: 현재 로그인한 사용자 (자동 주입)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        List[TodoResponse]: 현재 사용자의 할일 목록
    """
    todos = crud.get_todos(db, owner_id=current_user.id, skip=skip, limit=limit)
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(
    todo_id: int, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    특정 ID의 할일을 조회합니다.
    자신의 할일만 조회할 수 있습니다.
    
    Args:
        todo_id: 조회할 할일의 ID
        current_user: 현재 로그인한 사용자 (자동 주입)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        TodoResponse: 할일 정보
    
    Raises:
        HTTPException: 할일을 찾을 수 없거나 접근 권한이 없는 경우 404 에러
    """
    db_todo = crud.get_todo(db, todo_id=todo_id, owner_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(
    todo_id: int, 
    todo: TodoUpdate, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    할일을 수정합니다.
    자신의 할일만 수정할 수 있습니다.
    
    Args:
        todo_id: 수정할 할일의 ID
        todo: 수정할 데이터 (제목, 설명, 완료 상태, 우선순위)
        current_user: 현재 로그인한 사용자 (자동 주입)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        TodoResponse: 수정된 할일 정보
    
    Raises:
        HTTPException: 할일을 찾을 수 없거나 접근 권한이 없는 경우 404 에러
    """
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo, owner_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(
    todo_id: int, 
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    할일을 삭제합니다.
    자신의 할일만 삭제할 수 있습니다.
    
    Args:
        todo_id: 삭제할 할일의 ID
        current_user: 현재 로그인한 사용자 (자동 주입)
        db: 데이터베이스 세션 (자동 주입)
    
    Returns:
        TodoResponse: 삭제된 할일 정보
    
    Raises:
        HTTPException: 할일을 찾을 수 없거나 접근 권한이 없는 경우 404 에러
    """
    db_todo = crud.delete_todo(db, todo_id=todo_id, owner_id=current_user.id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

# 이 파일을 직접 실행할 때만 서버 시작
if __name__ == "__main__":
    import uvicorn
    # 개발 서버 실행
    # host="0.0.0.0": 모든 네트워크 인터페이스에서 접근 가능
    # port=8000: 8000번 포트에서 실행
    uvicorn.run(app, host="0.0.0.0", port=8000)