# FastAPI 부트캠프 프로젝트

## 프로젝트 개요
초보자를 위한 FastAPI 백엔드와 JavaScript 프론트엔드를 포함한 간단한 할일 관리 애플리케이션입니다. GitHub Actions를 통한 자동 배포까지 포함되어 있습니다.

## 프로젝트 구조
```
fastapi-bootcamp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── database.py
│   │   └── crud.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .github/
│   └── workflows/
│       └── deploy.yml
├── docker-compose.yml
└── README.md
```

## 개발 단계

### 1단계: 프로젝트 초기 설정
다음 디렉토리 구조를 생성해주세요:

```bash
mkdir -p fastapi-bootcamp/backend/app
mkdir -p fastapi-bootcamp/frontend
mkdir -p fastapi-bootcamp/.github/workflows
cd fastapi-bootcamp
```

### 2단계: 백엔드 (FastAPI) 개발

#### backend/requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
sqlite3
pydantic==2.5.0
python-multipart==0.0.6
```

#### backend/app/database.py
```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### backend/app/models.py
```python
from sqlalchemy import Column, Integer, String, Boolean
from .database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    completed = Column(Boolean, default=False)
```

#### backend/app/crud.py
```python
from sqlalchemy.orm import Session
from . import models
from pydantic import BaseModel
from typing import Optional

class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool

    class Config:
        from_attributes = True

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate):
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        if todo.title is not None:
            db_todo.title = todo.title
        if todo.description is not None:
            db_todo.description = todo.description
        if todo.completed is not None:
            db_todo.completed = todo.completed
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
```

#### backend/app/main.py
```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models
from .database import SessionLocal, engine, get_db
from .crud import TodoCreate, TodoUpdate, TodoResponse

# 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="할일 관리 API",
    description="간단한 할일 관리 애플리케이션 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드와의 통신을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영환경에서는 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "할일 관리 API에 오신 것을 환영합니다!"}

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
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 3단계: 프론트엔드 (JavaScript) 개발

#### frontend/index.html
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>할일 관리 앱</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
        <h1>할일 관리 앱</h1>
        
        <!-- 할일 추가 폼 -->
        <div class="todo-form">
            <h2>새 할일 추가</h2>
            <input type="text" id="todoTitle" placeholder="할일 제목" required>
            <input type="text" id="todoDescription" placeholder="할일 설명 (선택사항)">
            <button onclick="addTodo()">추가</button>
        </div>

        <!-- 할일 목록 -->
        <div class="todo-list">
            <h2>할일 목록</h2>
            <div id="todos"></div>
        </div>
    </div>

    <script src="script.js"></script>
</body>
</html>
```

#### frontend/style.css
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 30px;
}

h2 {
    color: #34495e;
    margin-bottom: 20px;
}

.todo-form {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 30px;
}

.todo-form input {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 16px;
}

.todo-form button {
    background-color: #3498db;
    color: white;
    padding: 12px 24px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
}

.todo-form button:hover {
    background-color: #2980b9;
}

.todo-list {
    background: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.todo-item {
    background: #f8f9fa;
    padding: 15px;
    margin: 10px 0;
    border-radius: 4px;
    border-left: 4px solid #3498db;
}

.todo-item.completed {
    background: #d4edda;
    border-left-color: #28a745;
}

.todo-item h3 {
    margin-bottom: 5px;
    color: #2c3e50;
}

.todo-item.completed h3 {
    text-decoration: line-through;
    color: #6c757d;
}

.todo-item p {
    margin-bottom: 10px;
    color: #666;
}

.todo-actions {
    display: flex;
    gap: 10px;
}

.todo-actions button {
    padding: 6px 12px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.complete-btn {
    background-color: #28a745;
    color: white;
}

.complete-btn:hover {
    background-color: #218838;
}

.delete-btn {
    background-color: #dc3545;
    color: white;
}

.delete-btn:hover {
    background-color: #c82333;
}

.error {
    color: #dc3545;
    background-color: #f8d7da;
    padding: 10px;
    border-radius: 4px;
    margin: 10px 0;
}

.loading {
    text-align: center;
    color: #6c757d;
    font-style: italic;
}
```

#### frontend/script.js
```javascript
// API 기본 URL (백엔드 서버 주소)
const API_BASE_URL = 'http://localhost:8000';

// 페이지 로드 시 할일 목록 불러오기
document.addEventListener('DOMContentLoaded', function() {
    loadTodos();
});

// 할일 목록 불러오기
async function loadTodos() {
    try {
        showLoading();
        const response = await fetch(`${API_BASE_URL}/todos/`);
        
        if (!response.ok) {
            throw new Error('할일 목록을 불러오는데 실패했습니다');
        }
        
        const todos = await response.json();
        displayTodos(todos);
    } catch (error) {
        showError(error.message);
    }
}

// 할일 목록 화면에 표시
function displayTodos(todos) {
    const todosContainer = document.getElementById('todos');
    
    if (todos.length === 0) {
        todosContainer.innerHTML = '<p class="loading">등록된 할일이 없습니다.</p>';
        return;
    }
    
    todosContainer.innerHTML = todos.map(todo => `
        <div class="todo-item ${todo.completed ? 'completed' : ''}">
            <h3>${todo.title}</h3>
            <p>${todo.description || '설명 없음'}</p>
            <div class="todo-actions">
                <button class="complete-btn" onclick="toggleTodo(${todo.id}, ${!todo.completed})">
                    ${todo.completed ? '미완료로 변경' : '완료'}
                </button>
                <button class="delete-btn" onclick="deleteTodo(${todo.id})">
                    삭제
                </button>
            </div>
        </div>
    `).join('');
}

// 새 할일 추가
async function addTodo() {
    const title = document.getElementById('todoTitle').value.trim();
    const description = document.getElementById('todoDescription').value.trim();
    
    if (!title) {
        showError('할일 제목을 입력해주세요');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/todos/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description
            })
        });
        
        if (!response.ok) {
            throw new Error('할일 추가에 실패했습니다');
        }
        
        // 폼 초기화
        document.getElementById('todoTitle').value = '';
        document.getElementById('todoDescription').value = '';
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 할일 완료 상태 토글
async function toggleTodo(todoId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                completed: completed
            })
        });
        
        if (!response.ok) {
            throw new Error('할일 상태 변경에 실패했습니다');
        }
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 할일 삭제
async function deleteTodo(todoId) {
    if (!confirm('이 할일을 삭제하시겠습니까?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/todos/${todoId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            throw new Error('할일 삭제에 실패했습니다');
        }
        
        // 할일 목록 새로고침
        loadTodos();
        
    } catch (error) {
        showError(error.message);
    }
}

// 로딩 표시
function showLoading() {
    document.getElementById('todos').innerHTML = '<p class="loading">로딩 중...</p>';
}

// 오류 메시지 표시
function showError(message) {
    const todosContainer = document.getElementById('todos');
    todosContainer.innerHTML = `<div class="error">${message}</div>`;
}

// Enter 키로 할일 추가
document.getElementById('todoTitle').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});

document.getElementById('todoDescription').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTodo();
    }
});
```

### 4단계: Docker 설정

#### backend/Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### docker-compose.yml
```yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - PYTHONPATH=/app

  frontend:
    image: nginx:alpine
    ports:
      - "3000:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
    depends_on:
      - backend
```

### 5단계: GitHub Actions 배포 설정

#### .github/workflows/deploy.yml
```yml
name: Deploy FastAPI App

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Test with pytest
      run: |
        cd backend
        # 여기에 테스트 코드 실행 명령어 추가
        python -c "from app.main import app; print('FastAPI app loaded successfully')"

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build and deploy
      run: |
        echo "배포 스크립트를 여기에 추가하세요"
        # 예: Docker 이미지 빌드 및 배포
        # docker build -t fastapi-app ./backend
        # docker push your-registry/fastapi-app
```

### 6단계: README.md
```markdown
# FastAPI 부트캠프 프로젝트

초보자를 위한 FastAPI 백엔드와 JavaScript 프론트엔드를 포함한 할일 관리 애플리케이션입니다.

## 기능
- 할일 추가, 조회, 수정, 삭제 (CRUD)
- 할일 완료 상태 토글
- 반응형 웹 인터페이스

## 실행 방법

### 1. 로컬 개발 환경

#### 백엔드 실행
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### 프론트엔드 실행
```bash
cd frontend
# 간단한 HTTP 서버 실행 (Python 3)
python -m http.server 3000
```

### 2. Docker 사용
```bash
docker-compose up --build
```

## API 엔드포인트
- `GET /`: API 정보
- `GET /todos/`: 모든 할일 조회
- `POST /todos/`: 새 할일 생성
- `GET /todos/{id}`: 특정 할일 조회
- `PUT /todos/{id}`: 할일 수정
- `DELETE /todos/{id}`: 할일 삭제

## 학습 목표
1. FastAPI를 사용한 REST API 개발
2. SQLAlchemy를 사용한 데이터베이스 연동
3. JavaScript를 사용한 API 호출
4. Docker를 사용한 컨테이너화
5. GitHub Actions를 사용한 CI/CD

## 다음 단계
- 인증/권한 시스템 추가
- 데이터베이스를 PostgreSQL로 변경
- 프론트엔드 프레임워크 (React, Vue.js) 사용
- 실제 클라우드 서비스에 배포
```

## 개발 지시사항

1. **백엔드 개발 시작**: 먼저 `backend/` 디렉토리를 생성하고 FastAPI 애플리케이션을 개발하세요.

2. **데이터베이스 설정**: SQLite를 사용하여 간단한 로컬 데이터베이스를 설정하세요.

3. **API 테스트**: FastAPI의 자동 문서화 기능(`/docs`)을 사용하여 API를 테스트하세요.

4. **프론트엔드 개발**: 백엔드 API가 완성되면 JavaScript로 프론트엔드를 개발하세요.

5. **CORS 설정**: 프론트엔드와 백엔드가 다른 포트에서 실행되므로 CORS 설정이 필요합니다.

6. **Docker 컨테이너화**: 개발이 완료되면 Docker를 사용하여 애플리케이션을 컨테이너화하세요.

7. **GitHub Actions 설정**: 코드가 GitHub에 푸시될 때 자동으로 테스트와 배포가 실행되도록 설정하세요.

## 강의 진행 순서
1. FastAPI 기본 개념 설명
2. 데이터베이스 모델링과 SQLAlchemy
3. CRUD API 개발
4. 프론트엔드 JavaScript 개발
5. API 연동 및 테스트
6. Docker 컨테이너화
7. GitHub Actions CI/CD 설정
8. 배포 및 운영

이 프로젝트를 통해 학생들은 실제 웹 애플리케이션 개발의 전체 과정을 경험할 수 있습니다.