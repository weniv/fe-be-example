from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

# 환경변수 로드 (.env 파일에서)
load_dotenv()

from . import crud, models
from .database import SessionLocal, engine, get_db
from .crud import TodoCreate, TodoUpdate, TodoResponse

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# 환경변수에서 설정값 가져오기
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")

# FastAPI 앱 생성
app = FastAPI(
    title="할일 관리 API",
    description="간단한 할일 관리 애플리케이션 API - 배포 준비 완료",
    version="1.0.0"
)

# CORS 미들웨어 설정 (환경에 따라 다르게 설정)
if ENVIRONMENT == "production":
    # 프로덕션에서는 특정 도메인만 허용
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
else:
    # 개발 환경에서는 모든 도메인 허용
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/")
def read_root():
    return {"message": "할일 관리 API에 오신 것을 환영합니다!"}

@app.get("/health")
def health_check():
    """서버 상태 확인용 엔드포인트 (배포 모니터링용)"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "message": "서버가 정상적으로 실행 중입니다"
    }

@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

@app.delete("/todos/{todo_id}", response_model=TodoResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="할일을 찾을 수 없습니다")
    return db_todo

if __name__ == "__main__":
    import uvicorn
    # 환경변수에서 포트 설정 가져오기 (기본값: 8000)
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)