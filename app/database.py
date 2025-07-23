"""
데이터베이스 설정 모듈
SQLAlchemy를 사용하여 데이터베이스와 연결을 관리합니다.
환경변수를 통해 SQLite(개발용) 또는 PostgreSQL(배포용) 연결을 지원합니다.

초보자를 위한 설명:
- 이 파일은 데이터베이스와 연결하는 설정을 담당합니다
- 개발할 때는 SQLite(파일 기반 DB), 배포할 때는 PostgreSQL(서버 DB)을 사용합니다
- 환경변수(.env 파일)를 통해 데이터베이스 정보를 안전하게 관리합니다
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .env 파일에서 환경변수를 로드합니다
# .env 파일에는 데이터베이스 접속 정보와 같은 민감한 정보가 들어있습니다
# 이 파일은 보안상 git에 올리지 않고 로컬에만 저장합니다
load_dotenv()

# 환경변수에서 데이터베이스 URL을 가져옵니다
# os.getenv(): 환경변수 값을 가져오는 함수
# 두 번째 인자는 환경변수가 없을 때 사용할 기본값입니다
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todos.db")

# 데이터베이스 연결 설정을 결정합니다
# SQLite와 PostgreSQL은 서로 다른 설정이 필요하기 때문입니다
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    # SQLite 사용 시: 멀티스레드 접근을 허용하는 설정
    # SQLite는 기본적으로 한 번에 하나의 스레드만 접근 가능하지만
    # FastAPI는 여러 스레드를 동시에 사용하므로 이 제한을 해제해야 합니다
    connect_args = {"check_same_thread": False}
else:
    # PostgreSQL 등 서버 기반 데이터베이스 사용 시
    # 이미 멀티스레드를 지원하므로 특별한 설정이 필요하지 않습니다
    connect_args = {}

# 데이터베이스 엔진 생성
# 엔진은 데이터베이스와의 실제 연결을 관리하는 객체입니다
# 모든 데이터베이스 작업은 이 엔진을 통해 수행됩니다
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # 데이터베이스 연결 URL
    connect_args=connect_args  # 데이터베이스별 연결 설정
)

# 세션 팩토리 생성
# 세션은 데이터베이스와의 대화를 나타내는 객체입니다
# 하나의 세션에서 여러 데이터베이스 작업을 수행할 수 있습니다
SessionLocal = sessionmaker(
    autocommit=False,  # 자동 커밋 비활성화 - 개발자가 직접 commit() 호출해야 함
    autoflush=False,   # 자동 플러시 비활성화 - 성능 향상을 위해
    bind=engine        # 위에서 생성한 엔진과 연결
)

# 모든 데이터베이스 모델의 기본 클래스
# 이 클래스를 상속받아 실제 테이블 구조(모델)를 정의합니다
# 예: class Todo(Base): ...
Base = declarative_base()

def get_db():
    """
    데이터베이스 세션을 생성하고 반환하는 의존성 함수
    
    FastAPI의 의존성 주입(Dependency Injection) 시스템에서 사용됩니다.
    각 API 요청마다 새로운 데이터베이스 세션을 생성하고,
    요청이 끝나면 자동으로 세션을 정리합니다.
    
    사용 예시:
        @app.get("/todos/")
        def get_todos(db: Session = Depends(get_db)):
            # 이 함수 안에서 db를 사용하여 데이터베이스 작업 수행
    
    Yields:
        Session: SQLAlchemy 데이터베이스 세션 객체
        
    동작 과정:
        1. 새로운 데이터베이스 세션 생성
        2. API 함수에 세션 전달 (yield)
        3. API 함수 실행 완료 후 세션 정리 (finally 블록)
    """
    # 새로운 데이터베이스 세션 생성
    db = SessionLocal()
    try:
        # yield 키워드로 세션을 API 함수에 전달
        # 이 지점에서 API 함수가 실행되고, 완료되면 아래 finally로 이동
        yield db
    finally:
        # API 함수 실행이 완료되면 (성공/실패 관계없이) 세션을 닫아 메모리 정리
        # 이는 데이터베이스 연결을 안전하게 해제하기 위한 중요한 단계입니다
        db.close()