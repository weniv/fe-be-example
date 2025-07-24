# FastAPI 부트캠프 프로젝트 - Step 6: API 연동

이 단계에서는 프론트엔드와 백엔드 API를 연동하여 실제 데이터 통신을 구현합니다.

## 학습 목표
- **Fetch API** 사용법과 HTTP 메서드 이해
- **async/await** 비동기 처리 패턴 학습
- **CORS** 개념과 설정 방법 이해
- **에러 처리**와 사용자 피드백 구현

## 프로젝트 구조
```
fastapi-bootcamp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## 주요 변경사항

### frontend/script.js 대폭 개선
- **더미 데이터 제거**: Step 5에서 사용했던 하드코딩된 데이터 삭제
- **실제 API 통신 구현**:
  - `loadTodos()`: GET /todos/ - 서버에서 할일 목록 불러오기
  - `addTodo()`: POST /todos/ - 서버에 새 할일 추가
  - `toggleTodo()`: PUT /todos/{id} - 서버에서 할일 상태 변경
  - `deleteTodo()`: DELETE /todos/{id} - 서버에서 할일 삭제

- **비동기 처리 구현**:
  - `async/await` 패턴 사용
  - `fetch()` API로 HTTP 요청 처리
  - JSON 데이터 송수신

- **사용자 경험 개선**:
  - 로딩 상태 표시 (`showLoading()`)
  - 에러 메시지 표시 (`showError()`)
  - 입력 폼 자동 초기화

## 실행 방법

### 1. 백엔드 서버 실행 (필수)
```bash
cd backend
# FastAPI 서버 실행 (포트 8000)
uvicorn app.main:app --reload
```

### 2. 프론트엔드 서버 실행
**별도의 터미널에서:**
```bash
cd frontend
# Python HTTP 서버 실행 (포트 3000)
python -m http.server 3000
```

### 3. 애플리케이션 사용
1. 브라우저에서 http://localhost:3000/index.html 접속
2. 할일을 추가, 완료/미완료 토글, 삭제해보세요
3. **데이터는 SQLite 데이터베이스에 영구 저장됩니다!**

## API 통신 흐름

### 1. 페이지 로드 시
```javascript
// 페이지 로드 → 자동으로 할일 목록 불러오기
loadTodos() → GET http://localhost:8000/todos/
```

### 2. 할일 추가 시
```javascript
// 폼 제출 → 서버에 새 할일 생성
addTodo() → POST http://localhost:8000/todos/
// 성공 후 목록 새로고침
→ loadTodos()
```

### 3. 완료 상태 변경 시
```javascript
// 완료 버튼 클릭 → 서버에서 상태 업데이트
toggleTodo(id, completed) → PUT http://localhost:8000/todos/{id}
// 성공 후 목록 새로고침
→ loadTodos()
```

### 4. 할일 삭제 시
```javascript
// 삭제 버튼 클릭 → 확인 후 서버에서 삭제
deleteTodo(id) → DELETE http://localhost:8000/todos/{id}
// 성공 후 목록 새로고침
→ loadTodos()
```

## 주요 구현 기능

### ✅ 실제 API 연동
- FastAPI 백엔드와 완전한 데이터 통신
- HTTP 메서드별 적절한 요청 처리
- JSON 데이터 형식 송수신

### ✅ 비동기 처리
- `async/await` 패턴으로 코드 가독성 향상
- `fetch()` API 사용한 모던 JavaScript
- Promise 기반 에러 처리

### ✅ 사용자 경험
- 로딩 상태 표시로 응답성 향상
- 명확한 에러 메시지 제공
- Enter 키 지원으로 편의성 증대

### ✅ 데이터 영속성
- SQLite 데이터베이스에 실제 저장
- 페이지 새로고침 후에도 데이터 유지
- 서버 재시작 후에도 데이터 보존

## 문제 해결 가이드

### CORS 에러가 발생하는 경우
```bash
Access to fetch at 'http://localhost:8000/todos/' from origin 'http://localhost:3000' has been blocked by CORS policy
```
**해결방법**: 백엔드의 CORS 설정이 main.py에 이미 구현되어 있습니다:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용 설정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### API 연결이 안 되는 경우
1. **백엔드 서버 확인**: http://localhost:8000에서 서버 실행 중인지 확인
2. **포트 충돌 확인**: 8000번 port가 다른 프로그램에서 사용 중인지 확인
3. **브라우저 개발자 도구**: Network 탭에서 실제 요청/응답 확인

### 데이터가 저장되지 않는 경우
- 백엔드 로그 확인: 서버 터미널에서 에러 메시지 확인
- SQLite 파일 확인: `backend/todos.db` 파일이 생성되었는지 확인

## 다음 단계 미리보기
Step 7에서는 배포 준비를 위한 환경 설정과 최적화를 진행합니다:
- 환경변수 관리
- 프로덕션 설정 분리
- 보안 강화

## 코드 이해하기

### fetch() API 사용 예시
```javascript
// GET 요청 - 데이터 조회
const response = await fetch(`${API_BASE_URL}/todos/`);
const todos = await response.json();

// POST 요청 - 데이터 생성
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
```

### 에러 처리 패턴
```javascript
try {
    const response = await fetch(url);
    if (!response.ok) {
        throw new Error('요청이 실패했습니다');
    }
    const data = await response.json();
    // 성공 처리
} catch (error) {
    showError(error.message);
}
```

## 🎉 축하합니다!

이제 완전한 풀스택 웹 애플리케이션을 구현했습니다:
- ✅ **백엔드**: FastAPI + SQLAlchemy + SQLite
- ✅ **프론트엔드**: HTML + CSS + JavaScript
- ✅ **API 통신**: RESTful API + JSON
- ✅ **데이터 영속성**: 데이터베이스 저장

실제 웹 개발에서 사용되는 핵심 기술들을 모두 경험해보셨습니다!