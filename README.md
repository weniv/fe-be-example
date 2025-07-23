# FastAPI 부트캠프 프로젝트 - 할일 관리 애플리케이션

## 📋 프로젝트 개요

이 프로젝트는 FastAPI와 JavaScript를 활용한 풀스택 웹 애플리케이션 개발을 학습하기 위한 부트캠프 프로젝트입니다. 간단한 할일(Todo) 관리 애플리케이션을 통해 백엔드 API 개발, 프론트엔드 개발,
그리고 AWS EC2 배포까지 전체 개발 과정을 경험할 수 있습니다.

### 주요 기능

- ✅ 할일 추가, 조회, 수정, 삭제 (CRUD)
- ✅ 할일 완료 상태 토글
- ✅ **우선순위 설정** (높음/보통/낮음) - 색상으로 구분
- ✅ **실시간 검색** 기능 (제목, 설명 검색)
- ✅ **한국 시간(KST) 기준** 생성일자 표시
- ✅ 반응형 웹 인터페이스
- ✅ RESTful API 설계
- ✅ 자동 API 문서화
- ✅ **환경변수 기반 설정** (.env 파일 지원)
- ✅ **AWS Lightsail 데이터베이스** 연동 지원

### 기술 스택

- **백엔드**: FastAPI, SQLAlchemy, SQLite/PostgreSQL, Pydantic, Python-dotenv
- **프론트엔드**: HTML5, CSS3, Vanilla JavaScript
- **데이터베이스**: SQLite (개발용), PostgreSQL (AWS Lightsail 배포용)
- **배포**: AWS EC2, Nginx
- **CI/CD**: GitHub Actions

## 🚀 시작하기

### 사전 요구사항

- Python 3.11 이상
- Node.js (선택사항, 프론트엔드 서버용)

### 프로젝트 구조

```
fe-be-example/
├── app/                    # 백엔드 애플리케이션
│   ├── __init__.py        # 패키지 초기화
│   ├── main.py            # FastAPI 메인 애플리케이션
│   ├── models.py          # 데이터베이스 모델
│   ├── database.py        # 데이터베이스 설정
│   └── crud.py            # CRUD 작업 및 스키마
├── frontend/              # 프론트엔드 애플리케이션
│   ├── index.html         # 메인 HTML 페이지
│   ├── style.css          # 스타일시트
│   └── script.js          # JavaScript 로직
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions 워크플로우
├── requirements.txt       # Python 패키지 의존성
└── README.md              # 프로젝트 문서
```

## ⚙️ 환경 설정

### 환경변수 파일 생성

프로젝트 루트에 `.env` 파일을 생성하세요:

```bash
# .env.example 파일을 복사하여 .env 파일 생성
cp .env.example .env
```

`.env` 파일 내용:
```bash
# 로컬 개발용 (기본값)
DATABASE_URL=sqlite:///./todos.db

# AWS Lightsail 데이터베이스 사용 시 (아래 값들을 실제 값으로 변경)
# DATABASE_URL=postgresql://username:password@your-db-host:5432/todos_db
# DB_USER=your_username  
# DB_PASSWORD=your_password
# DB_HOST=your_lightsail_db_host
# DB_PORT=5432
# DB_NAME=todos_db
```

> ⚠️ **중요**: `.env` 파일은 절대 Git에 올리지 마세요! 이미 `.gitignore`에 포함되어 있습니다.

## 💻 로컬 개발 환경 실행

### 백엔드 실행

```bash
# 프로젝트 루트 디렉토리에서

# 가상환경 생성 및 활성화 (권장)
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# FastAPI 서버 실행
uvicorn app.main:app --reload
```

백엔드 서버가 실행되면:

- API: http://localhost:8000
- API 문서 (Swagger UI): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

### 프론트엔드 실행

```bash
# frontend 디렉토리로 이동
cd frontend

# Python의 간단한 HTTP 서버 사용
python -m http.server 3000

# 또는 Node.js의 http-server 사용 (npm install -g http-server 필요)
http-server -p 3000
```

프론트엔드가 실행되면:

- 웹 애플리케이션: http://localhost:3000

## 📡 API 엔드포인트

### 기본 정보

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`

### 엔드포인트 목록

| 메서드    | 엔드포인트         | 설명        | 요청 본문                                                                |
|--------|---------------|-----------|----------------------------------------------------------------------|
| GET    | `/`           | API 정보 확인 | -                                                                    |
| GET    | `/todos/`     | 모든 할일 조회  | -                                                                    |
| POST   | `/todos/`     | 새 할일 생성   | `{"title": "string", "description": "string"}`                       |
| GET    | `/todos/{id}` | 특정 할일 조회  | -                                                                    |
| PUT    | `/todos/{id}` | 할일 수정     | `{"title": "string", "description": "string", "completed": boolean}` |
| DELETE | `/todos/{id}` | 할일 삭제     | -                                                                    |

### API 사용 예시

#### 새 할일 생성

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "FastAPI 공부하기", "description": "부트캠프 과제 완성"}'
```

#### 모든 할일 조회

```bash
curl "http://localhost:8000/todos/"
```

#### 할일 완료 상태 변경

```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

## 🎯 사용 시나리오

### 1. 첫 실행

1. 백엔드와 프론트엔드 서버를 실행합니다.
2. 웹 브라우저에서 http://localhost:3000 에 접속합니다.
3. 빈 할일 목록이 표시됩니다.

### 2. 할일 추가

1. "새 할일 추가" 섹션에서 제목을 입력합니다.
2. 선택적으로 설명을 추가합니다.
3. "추가" 버튼을 클릭하거나 Enter 키를 누릅니다.
4. 새 할일이 목록에 즉시 나타납니다.

### 3. 할일 관리

1. **완료 표시**: 각 할일의 "완료" 버튼을 클릭하여 완료 상태로 변경합니다.
2. **미완료로 변경**: 완료된 할일의 "미완료로 변경" 버튼을 클릭합니다.
3. **삭제**: "삭제" 버튼을 클릭하고 확인 대화상자에서 확인합니다.

### 4. API 문서 확인

1. http://localhost:8000/docs 에 접속합니다.
2. Swagger UI에서 각 API 엔드포인트를 테스트할 수 있습니다.
3. "Try it out" 버튼으로 직접 API를 호출해볼 수 있습니다.

## 🛠️ 개발 가이드

### 백엔드 수정

1. `app/` 디렉토리의 파일을 수정합니다.
2. 새로운 모델이나 엔드포인트 추가 시:
    - `models.py`: 데이터베이스 모델 정의
    - `crud.py`: 비즈니스 로직 및 스키마 정의
    - `main.py`: API 엔드포인트 추가

### 프론트엔드 수정

1. `frontend/` 디렉토리의 파일을 수정합니다.
2. 스타일 변경: `style.css`
3. 기능 추가: `script.js`
4. 레이아웃 변경: `index.html`

### 데이터베이스 초기화

```bash
# SQLite 데이터베이스 파일 삭제
rm todos.db

# 서버 재시작하면 자동으로 새 DB 생성
```

## 📚 학습 목표

이 프로젝트를 통해 다음을 학습할 수 있습니다:

1. **FastAPI 기초**
    - API 라우팅 및 엔드포인트 생성
    - Pydantic을 활용한 데이터 검증
    - 자동 API 문서화

2. **데이터베이스 연동**
    - SQLAlchemy ORM 사용법
    - CRUD 패턴 구현
    - 데이터베이스 세션 관리

3. **프론트엔드 개발**
    - Fetch API를 사용한 비동기 통신
    - DOM 조작 및 이벤트 처리
    - 반응형 UI 구현

4. **AWS EC2 배포**
    - EC2 인스턴스 설정
    - Nginx 웹 서버 구성
    - GitHub Actions를 통한 자동 배포

5. **CI/CD**
    - GitHub Actions 워크플로우 작성
    - 자동화된 테스트 및 배포

## 🔄 다음 단계

프로젝트를 확장하고 싶다면:

1. **인증 시스템 추가**
    - JWT 토큰 기반 인증
    - 사용자별 할일 관리

2. **데이터베이스 업그레이드**
    - PostgreSQL로 마이그레이션
    - Alembic으로 데이터베이스 마이그레이션 관리

3. **프론트엔드 프레임워크**
    - React, Vue.js, 또는 Svelte로 재구현
    - 상태 관리 라이브러리 도입

4. **테스트 추가**
    - pytest로 백엔드 유닛 테스트
    - Jest로 프론트엔드 테스트

5. **실제 배포**
    - AWS, GCP, 또는 Heroku에 배포
    - 도메인 연결 및 HTTPS 설정

## 🚀 AWS EC2 배포 가이드

### EC2 인스턴스 설정

1. **EC2 인스턴스 생성**
    - Ubuntu 22.04 LTS AMI 선택
    - t2.micro 인스턴스 타입 (프리 티어)
    - 키 페어(.pem) 생성 및 다운로드

2. **보안 그룹 설정**
   ```
   - SSH (22번 포트): 내 IP에서만
   - HTTP (80번 포트): 모든 소스
   - HTTPS (443번 포트): 모든 소스
   - 커스텀 TCP (8000번 포트): 모든 소스 (개발용)
   ```

3. **EC2 접속**
   ```bash
   # 키 파일 권한 설정
   chmod 400 your-key.pem
   
   # SSH 접속
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```

### 서버 설정

1. **필수 패키지 설치**
   ```bash
   # 시스템 업데이트
   sudo apt update && sudo apt upgrade -y
   
   # Python 및 필수 패키지 설치
   sudo apt install python3-pip python3-venv nginx git -y
   ```

2. **프로젝트 셋업**
   ```bash
   # 프로젝트 클론
   git clone https://github.com/your-username/your-repo.git ~/fastapi-app
   cd ~/fastapi-app
   
   # 가상환경 생성 및 의존성 설치
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Nginx 설정**
   ```bash
   # 기본 Nginx 사이트 비활성화
   sudo rm /etc/nginx/sites-enabled/default
   
   # Nginx 설정 파일 생성
   sudo nano /etc/nginx/sites-available/fastapi-app
   ```

   다음 내용 추가:
   ```nginx
   server {
       listen 80;
       server_name _;  # 모든 도메인 허용
       
       # 프론트엔드 정적 파일 서빙
       location / {
           root /home/ubuntu/fastapi-app/frontend;
           index index.html;
           try_files $uri $uri/ /index.html;
       }
       
       # 백엔드 API 리버스 프록시
       location /todos {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $http_host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
       
       # API 문서 프록시
       location /docs {
           proxy_pass http://127.0.0.1:8000/docs;
           proxy_set_header Host $http_host;
       }
       
       location /openapi.json {
           proxy_pass http://127.0.0.1:8000/openapi.json;
           proxy_set_header Host $http_host;
       }
   }
   ```

   ```bash
   # 사이트 활성화
   sudo ln -s /etc/nginx/sites-available/fastapi-app /etc/nginx/sites-enabled/
   
   # Nginx 설정 테스트
   sudo nginx -t
   
   # Nginx 재시작
   sudo systemctl restart nginx
   ```

4. **FastAPI 서비스 설정**
   ```bash
   # systemd 서비스 파일 생성
   sudo nano /etc/systemd/system/fastapi.service
   ```

   다음 내용 추가:
   ```ini
   [Unit]
   Description=FastAPI app
   After=network.target
   
   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/fastapi-app
   Environment="PATH=/home/ubuntu/fastapi-app/venv/bin"
   ExecStart=/home/ubuntu/fastapi-app/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   Restart=always
   
   [Install]
   WantedBy=multi-user.target
   ```

   ```bash
   # 서비스 시작
   sudo systemctl daemon-reload
   sudo systemctl start fastapi
   sudo systemctl enable fastapi
   ```

### GitHub Actions 배포 설정

1. **GitHub Secrets 설정**
   저장소 Settings > Secrets and variables > Actions에서 다음 secrets를 추가:
   
   **EC2 접속 관련:**
   - `EC2_SSH_KEY`: EC2 인스턴스의 .pem 키 파일 전체 내용
   - `EC2_HOST`: EC2 퍼블릭 IP 주소 또는 도메인
   - `EC2_USER`: ubuntu (기본값)
   
   **데이터베이스 관련 (AWS Lightsail DB 사용 시):**
   - `DATABASE_URL`: PostgreSQL 연결 URL (예: `postgresql://user:password@host:5432/dbname`)
   - `DB_USER`: 데이터베이스 사용자명
   - `DB_PASSWORD`: 데이터베이스 비밀번호
   - `DB_HOST`: Lightsail 데이터베이스 호스트
   - `DB_PORT`: 데이터베이스 포트 (보통 5432)
   - `DB_NAME`: 데이터베이스 이름

2. **배포 테스트**
   ```bash
   # master 브랜치에 push하면 자동 배포
   git add .
   git commit -m "Deploy to EC2"
   git push origin master
   ```

### 프론트엔드 API URL 수정

프론트엔드가 EC2에서 올바르게 작동하려면 `frontend/script.js`에서 API URL을 수정해야 합니다:

```javascript
// 개발 환경 (로컬)
// const API_BASE_URL = 'http://localhost:8000';

// 프로덕션 환경 (EC2 배포 시)
const API_BASE_URL = '';  // Nginx가 /todos로 프록시하므로 별도 경로 불필요
```

## 🤝 기여하기

이 프로젝트는 교육 목적으로 만들어졌습니다. 개선 사항이나 버그를 발견하면 이슈를 생성하거나 PR을 보내주세요.

## 📄 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용할 수 있습니다.

---

**Happy Coding! 🚀**