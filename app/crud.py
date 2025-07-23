"""
CRUD (Create, Read, Update, Delete) 작업 모듈

이 파일의 역할:
1. 데이터베이스와 상호작용하는 함수들을 정의합니다
2. API 요청/응답 데이터의 구조를 정의합니다 (Pydantic 스키마)
3. 실제 데이터베이스 작업(생성, 조회, 수정, 삭제)을 수행합니다

초보자를 위한 설명:
- CRUD는 데이터베이스의 기본 4가지 작업을 의미합니다
  * Create: 새 데이터 생성
  * Read: 데이터 조회
  * Update: 데이터 수정  
  * Delete: 데이터 삭제
- Pydantic은 데이터 검증과 직렬화를 도와주는 라이브러리입니다
- 이 파일은 FastAPI와 데이터베이스 사이의 다리 역할을 합니다
"""
from sqlalchemy.orm import Session  # 데이터베이스 세션을 위한 import
from . import models  # 같은 패키지의 models.py에서 Todo 모델 가져오기
from pydantic import BaseModel, EmailStr  # 데이터 검증을 위한 BaseModel, 이메일 검증
from typing import Optional  # 선택적 필드 타입 힌트
from datetime import datetime  # 날짜/시간 처리
from .auth import get_password_hash  # 비밀번호 해싱 함수 가져오기

# ====== Pydantic 스키마 정의 ======
# 스키마는 API로 주고받는 데이터의 형태를 정의합니다
# 클라이언트가 보내는 데이터가 올바른 형식인지 자동으로 검증해줍니다

# ====== 사용자 관련 스키마 ======

class UserCreate(BaseModel):
    """
    사용자 회원가입 요청 스키마
    클라이언트가 새 계정을 만들 때 보내는 데이터 구조
    """
    username: str  # 필수 필드: 사용자명 (로그인 ID)
    email: EmailStr  # 필수 필드: 이메일 주소 (자동 유효성 검증)
    password: str  # 필수 필드: 비밀번호 (평문으로 받아서 서버에서 해싱)

class UserLogin(BaseModel):
    """
    사용자 로그인 요청 스키마
    클라이언트가 로그인할 때 보내는 데이터 구조
    """
    username: str  # 필수 필드: 사용자명
    password: str  # 필수 필드: 비밀번호

class UserResponse(BaseModel):
    """
    사용자 응답 스키마
    API가 클라이언트에게 반환하는 사용자 데이터 구조
    보안상 비밀번호는 포함하지 않음
    """
    id: int  # 사용자 고유 ID
    username: str  # 사용자명
    email: str  # 이메일 주소
    is_active: bool  # 계정 활성 상태
    created_at: datetime  # 계정 생성 일시

    class Config:
        # SQLAlchemy 모델을 Pydantic 모델로 변환할 때 필요
        from_attributes = True

class Token(BaseModel):
    """
    JWT 토큰 응답 스키마
    로그인 성공 시 반환되는 토큰 정보
    """
    access_token: str  # JWT 액세스 토큰
    token_type: str  # 토큰 타입 (보통 "bearer")

# ====== 할일 관련 스키마 ======

class TodoCreate(BaseModel):
    """
    할일 생성 요청 스키마
    클라이언트가 새 할일을 만들 때 보내는 데이터 구조
    """
    title: str  # 필수 필드: 할일 제목
    description: Optional[str] = None  # 선택적 필드: 할일 설명
    priority: Optional[int] = 2  # 선택적 필드: 우선순위 (1: 높음, 2: 보통, 3: 낮음)

class TodoUpdate(BaseModel):
    """
    할일 수정 요청 스키마
    모든 필드가 선택적이어서 부분 업데이트 가능
    """
    title: Optional[str] = None  # 선택적: 새로운 제목
    description: Optional[str] = None  # 선택적: 새로운 설명
    completed: Optional[bool] = None  # 선택적: 완료 상태
    priority: Optional[int] = None  # 선택적: 우선순위

class TodoResponse(BaseModel):
    """
    할일 응답 스키마
    API가 클라이언트에게 반환하는 할일 데이터 구조
    """
    id: int  # 할일 고유 ID
    title: str  # 할일 제목
    description: Optional[str]  # 할일 설명 (없을 수 있음)
    completed: bool  # 완료 상태
    priority: int  # 우선순위
    created_at: datetime  # 생성 일시
    owner_id: int  # 할일 작성자 ID

    class Config:
        # SQLAlchemy 모델을 Pydantic 모델로 변환할 때 필요
        # ORM 모드 활성화로 ORM 객체를 직접 사용 가능
        from_attributes = True

# ====== 사용자 관련 CRUD 함수들 ======

def get_user(db: Session, user_id: int):
    """
    특정 ID의 사용자를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        user_id: 조회할 사용자의 ID
    
    Returns:
        User or None: 사용자 객체 또는 None (없는 경우)
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    """
    사용자명으로 사용자를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        username: 조회할 사용자명
    
    Returns:
        User or None: 사용자 객체 또는 None (없는 경우)
    """
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    """
    이메일로 사용자를 조회합니다.
    
    Args:
        db: 데이터베이스 세션
        email: 조회할 이메일 주소
    
    Returns:
        User or None: 사용자 객체 또는 None (없는 경우)
    """
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """
    새로운 사용자를 생성합니다.
    
    Args:
        db: 데이터베이스 세션
        user: 생성할 사용자 데이터
    
    Returns:
        User: 생성된 사용자 객체
    """
    # 비밀번호를 해시화하여 안전하게 저장
    hashed_password = get_password_hash(user.password)
    
    # SQLAlchemy 모델 생성
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)  # 세션에 추가
    db.commit()  # 데이터베이스에 커밋
    db.refresh(db_user)  # 생성된 ID 등 최신 정보로 갱신
    return db_user

# ====== 할일 관련 CRUD 함수들 ======

def get_todos(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    """
    특정 사용자의 할일 목록을 조회합니다.
    우선순위 순으로 정렬됩니다. (1: 높음, 2: 보통, 3: 낮음)
    
    Args:
        db: 데이터베이스 세션
        owner_id: 할일 소유자의 사용자 ID
        skip: 건너뛸 레코드 수 (페이지네이션용)
        limit: 반환할 최대 레코드 수
    
    Returns:
        List[Todo]: 해당 사용자의 할일 목록 (우선순위순)
    """
    return db.query(models.Todo).filter(models.Todo.owner_id == owner_id).order_by(models.Todo.priority, models.Todo.created_at.desc()).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int, owner_id: int):
    """
    특정 ID의 할일을 조회합니다 (소유자 확인 포함).
    
    Args:
        db: 데이터베이스 세션
        todo_id: 조회할 할일의 ID
        owner_id: 할일 소유자의 사용자 ID
    
    Returns:
        Todo or None: 할일 객체 또는 None (없거나 권한 없는 경우)
    """
    return db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == owner_id).first()

def create_todo(db: Session, todo: TodoCreate, owner_id: int):
    """
    새로운 할일을 생성합니다.
    
    Args:
        db: 데이터베이스 세션
        todo: 생성할 할일 데이터
        owner_id: 할일을 소유할 사용자의 ID
    
    Returns:
        Todo: 생성된 할일 객체
    """
    # Pydantic 모델을 SQLAlchemy 모델로 변환 (소유자 ID 포함)
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        priority=todo.priority,
        owner_id=owner_id  # 로그인한 사용자를 소유자로 설정
    )
    db.add(db_todo)  # 세션에 추가
    db.commit()  # 데이터베이스에 커밋
    db.refresh(db_todo)  # 생성된 ID 등 최신 정보로 갱신
    return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoUpdate, owner_id: int):
    """
    기존 할일을 수정합니다 (소유자 확인 포함).
    
    Args:
        db: 데이터베이스 세션
        todo_id: 수정할 할일의 ID
        todo: 수정할 데이터 (부분 업데이트 가능)
        owner_id: 할일 소유자의 사용자 ID
    
    Returns:
        Todo or None: 수정된 할일 객체 또는 None (없거나 권한 없는 경우)
    """
    # 해당 할일이 존재하고 소유자가 일치하는지 확인
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == owner_id).first()
    
    if db_todo:
        # 제공된 필드만 업데이트 (None이 아닌 경우만)
        if todo.title is not None:
            db_todo.title = todo.title
        if todo.description is not None:
            db_todo.description = todo.description
        if todo.completed is not None:
            db_todo.completed = todo.completed
        if todo.priority is not None:
            db_todo.priority = todo.priority
        
        db.commit()  # 변경사항 커밋
        db.refresh(db_todo)  # 최신 정보로 갱신
    
    return db_todo

def delete_todo(db: Session, todo_id: int, owner_id: int):
    """
    할일을 삭제합니다 (소유자 확인 포함).
    
    Args:
        db: 데이터베이스 세션
        todo_id: 삭제할 할일의 ID
        owner_id: 할일 소유자의 사용자 ID
    
    Returns:
        Todo or None: 삭제된 할일 객체 또는 None (없거나 권한 없는 경우)
    """
    # 삭제할 할일 찾기 (소유자 확인 포함)
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == owner_id).first()
    
    if db_todo:
        db.delete(db_todo)  # 세션에서 삭제
        db.commit()  # 데이터베이스에서 실제로 삭제
    
    return db_todo