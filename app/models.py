"""
데이터베이스 모델 정의 모듈
SQLAlchemy ORM을 사용하여 Todo 테이블의 구조를 정의합니다.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
from .database import Base

# 한국 표준시(KST) 타임존 설정
# UTC+9 시간으로 한국 시간을 나타냄
KST = timezone(timedelta(hours=9))

def get_kst_now():
    """
    현재 한국 시간을 반환하는 함수
    
    Returns:
        datetime: 한국 표준시(KST) 기준 현재 시간
    """
    return datetime.now(KST)

class User(Base):
    """
    사용자(User) 모델 클래스
    데이터베이스의 users 테이블과 매핑됩니다.
    
    초보자를 위한 설명:
    - 이 클래스는 사용자 정보를 저장하는 테이블을 정의합니다
    - 사용자는 여러 개의 할일을 가질 수 있습니다 (1:N 관계)
    - 비밀번호는 해시(암호화)되어 저장됩니다
    """
    # 테이블 이름 지정
    __tablename__ = "users"

    # id 컬럼: 기본 키, 자동 증가
    # 각 사용자를 구분하는 고유한 번호입니다
    id = Column(Integer, primary_key=True, index=True)
    
    # username 컬럼: 사용자명 (로그인할 때 사용)
    # unique=True: 같은 사용자명은 하나만 존재할 수 있음
    # index=True: 로그인 시 빠른 검색을 위한 인덱스 생성
    username = Column(String, unique=True, index=True, nullable=False)
    
    # email 컬럼: 이메일 주소
    # unique=True: 같은 이메일은 하나만 가입 가능
    email = Column(String, unique=True, index=True, nullable=False)
    
    # hashed_password 컬럼: 암호화된 비밀번호
    # 보안상 실제 비밀번호가 아닌 해시값을 저장합니다
    hashed_password = Column(String, nullable=False)
    
    # is_active 컬럼: 계정 활성 상태
    # False면 비활성화된 계정 (로그인 불가)
    is_active = Column(Boolean, default=True)
    
    # created_at 컬럼: 계정 생성일시 (한국 표준시 기준)
    created_at = Column(DateTime, default=get_kst_now)
    
    # todos 관계: 이 사용자가 작성한 모든 할일들
    # relationship(): SQLAlchemy에서 테이블 간의 관계를 정의
    # back_populates: Todo 모델의 owner와 연결
    # cascade: 사용자 삭제 시 관련 할일들도 함께 삭제
    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")

class Todo(Base):
    """
    할일(Todo) 모델 클래스
    데이터베이스의 todos 테이블과 매핑됩니다.
    
    초보자를 위한 설명:
    - 이 클래스는 할일 정보를 저장하는 테이블을 정의합니다
    - 각 할일은 한 명의 사용자에게 속합니다 (N:1 관계)
    - 사용자가 삭제되면 관련된 할일들도 함께 삭제됩니다
    """
    # 테이블 이름 지정
    __tablename__ = "todos"

    # id 컬럼: 기본 키, 자동 증가
    # primary_key=True: 이 컬럼을 기본 키로 설정
    # index=True: 검색 성능 향상을 위한 인덱스 생성
    id = Column(Integer, primary_key=True, index=True)
    
    # title 컬럼: 할일 제목 (문자열)
    # index=True: 제목으로 검색할 때 성능 향상
    title = Column(String, index=True, nullable=False)
    
    # description 컬럼: 할일 설명 (문자열)
    # 선택적 필드로, NULL 값 허용
    description = Column(String, index=True)
    
    # completed 컬럼: 완료 여부 (불린)
    # default=False: 기본값은 미완료 상태
    completed = Column(Boolean, default=False)
    
    # priority 컬럼: 우선순위 (1: 높음, 2: 보통, 3: 낮음)
    # default=2: 기본값은 보통 우선순위
    priority = Column(Integer, default=2)
    
    # created_at 컬럼: 생성 일시 (한국 표준시 기준)
    # default=get_kst_now: 한국 시간을 기본값으로 설정
    created_at = Column(DateTime, default=get_kst_now)
    
    # owner_id 컬럼: 이 할일을 작성한 사용자의 ID (외래키)
    # ForeignKey(): 다른 테이블의 기본 키를 참조하는 외래키
    # nullable=False: 반드시 사용자가 지정되어야 함
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # owner 관계: 이 할일을 작성한 사용자 객체
    # back_populates: User 모델의 todos와 연결
    owner = relationship("User", back_populates="todos")