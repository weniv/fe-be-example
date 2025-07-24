# FastAPI 부트캠프 프로젝트 - Step 8: GitHub Actions CI/CD

이 단계에서는 GitHub Actions를 사용하여 CI/CD 파이프라인을 설정합니다.

## 학습 목표
- GitHub Actions 워크플로우 이해
- 자동화된 테스트 설정
- 배포 자동화
- CI/CD 개념 이해

## 프로젝트 구조
```
fastapi-bootcamp/
├── .github/
│   └── workflows/
│       ├── test.yml
│       ├── deploy.yml
│       └── simple-deploy.yml
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud.py
│   └── requirements.txt
├── frontend/
│   ├── todo.html
│   ├── simple-style.css
│   └── simple-script.js
├── .gitignore
├── simple.env.example
├── run_dev.sh / run_dev.bat
├── run_production.sh
└── README.md
```

## 새로 추가된 내용

### GitHub Actions 워크플로우
- **.github/workflows/test.yml**: 자동 테스트 실행
- **.github/workflows/simple-deploy.yml**: 간단한 배포 워크플로우
- **.github/workflows/deploy.yml**: 기존 고급 배포 워크플로우

## CI/CD 파이프라인

### 1. 테스트 자동화 (test.yml)
```yaml
# Push나 PR 시 자동 실행
- Python 3.11 환경 설정
- 의존성 설치
- FastAPI 앱 로드 테스트
- 데이터베이스 테이블 생성 테스트
```

### 2. 배포 자동화 (simple-deploy.yml)
```yaml
# main/master 브랜치 push 시 실행
- 배포 정보 출력
- 실제 배포 로직은 주석으로 예시 제공
```

## GitHub Actions 사용법

### 1. 워크플로우 확인
- GitHub 저장소 → Actions 탭에서 실행 상태 확인
- 각 단계별 로그 확인 가능

### 2. Secrets 설정 (실제 배포 시)
Settings → Secrets and variables → Actions에서 설정:
```
EC2_SSH_KEY: SSH 키 파일 내용
EC2_HOST: 서버 IP 주소
EC2_USER: 서버 로그인 사용자명
SECRET_KEY: 애플리케이션 시크릿 키
DATABASE_URL: 데이터베이스 연결 URL
```

### 3. 브랜치 전략
- **feature 브랜치**: 새 기능 개발
- **develop 브랜치**: 개발 통합
- **main/master 브랜치**: 프로덕션 배포

## CI/CD 흐름

1. **개발자가 코드 푸시**
2. **자동 테스트 실행** (test.yml)
   - 코드 품질 검증
   - 기본 기능 테스트
   - 오류 시 배포 중단
3. **테스트 통과 시 배포** (deploy.yml)
   - 서버에 자동 배포
   - 서비스 재시작
   - 배포 완료 알림

## 장점

### CI (Continuous Integration)
- 코드 변경 시 자동 테스트
- 빠른 오류 발견
- 코드 품질 향상

### CD (Continuous Deployment)
- 자동화된 배포
- 배포 시간 단축
- 인간 실수 방지

## 실제 사용 시나리오

### 1. 새 기능 추가
```bash
git checkout -b feature/new-todo-priority
# 코드 작성
git push origin feature/new-todo-priority
# Pull Request 생성 → 자동 테스트 실행
```

### 2. 프로덕션 배포
```bash
git checkout main
git merge feature/new-todo-priority
git push origin main
# 자동 테스트 → 배포 실행
```

## 확장 가능한 기능

1. **고급 테스트**
   - 단위 테스트 (pytest)
   - 통합 테스트
   - 코드 커버리지

2. **배포 전략**
   - Blue-Green 배포
   - 카나리 배포
   - 롤백 기능

3. **모니터링**
   - 슬랙 알림
   - 이메일 알림
   - 성능 모니터링

## 완성된 부트캠프 프로젝트! 🎉

이제 전체 개발 과정을 경험했습니다:
1. ✅ 프로젝트 초기 설정
2. ✅ FastAPI 백엔드 개발
3. ✅ 데이터베이스 모델링
4. ✅ REST API 구현
5. ✅ 프론트엔드 개발
6. ✅ API 연동
7. ✅ 배포 준비
8. ✅ CI/CD 자동화

## 🚀 빠른 시작

### 📋 사전 요구사항

- **Python 3.11** 이상
- **Git** - 버전 관리
- **텍스트 에디터** (VS Code 권장)

### 📂 프로젝트 구조

```
fe-be-example/
├── 📁 app/                     # 🐍 백엔드 애플리케이션
│   ├── __init__.py             # 패키지 초기화 파일
│   ├── main.py                 # 🚀 FastAPI 메인 애플리케이션
│   ├── models.py               # 🗄️ 데이터베이스 모델 (User, Todo)
│   ├── database.py             # 🔌 데이터베이스 연결 설정
│   ├── crud.py                 # 📊 CRUD 작업 및 Pydantic 스키마
│   └── auth.py                 # 🔐 JWT 인증 시스템
├── 📁 frontend/                # 🌐 프론트엔드 애플리케이션
│   ├── home.html               # 🏠 홈페이지 (랜딩 페이지)
│   ├── login.html              # 🔑 로그인 페이지
│   ├── signup.html             # ✍️ 회원가입 페이지
│   ├── index.html              # 📋 할일 관리 메인 페이지
│   ├── style.css               # 🎨 통합 스타일시트
│   ├── auth.js                 # 🔐 인증 관련 JavaScript
│   └── script.js               # 📝 할일 관리 JavaScript
├── 📁 .github/workflows/       # ⚙️ GitHub Actions
│   └── deploy.yml              # 🚀 자동 배포 워크플로우
├── requirements.txt            # 📦 Python 의존성
├── .env.example               # 🔧 환경변수 템플릿
├── .gitignore                 # 🚫 Git 제외 파일
└── README.md                  # 📖 프로젝트 문서
```

## ⚙️ 환경 설정

### 1. 프로젝트 클론

```bash
git clone <repository-url>
cd fe-be-example
```

### 2. 환경변수 설정

`.env.example` 파일을 복사하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

`.env` 파일 내용 예시:

```bash
# 🔐 JWT 보안 설정
SECRET_KEY=your-super-secret-jwt-key-change-in-production

# 💾 데이터베이스 설정 (로컬 개발용)
DATABASE_URL=sqlite:///./todos.db

# 🌐 AWS Lightsail 데이터베이스 사용 시 (실제 값으로 변경)
# DATABASE_URL=postgresql://username:password@host:5432/todos_db
# DB_USER=your_username
# DB_PASSWORD=your_password
# DB_HOST=your-lightsail-db-host
# DB_PORT=5432
# DB_NAME=todos_db
```

> ⚠️ **보안 주의**: `.env` 파일은 절대 Git에 올리지 마세요!

### 3. 백엔드 실행

```bash
# 가상환경 생성 및 활성화
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux  
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt

# FastAPI 서버 실행 (개발 모드)
uvicorn app.main:app --reload
```

서버가 실행되면:

- 🌐 **API 서버**: http://localhost:8000
- 📚 **API 문서 (Swagger)**: http://localhost:8000/docs
- 📖 **API 문서 (ReDoc)**: http://localhost:8000/redoc

### 4. 프론트엔드 실행

```bash
# frontend 디렉토리로 이동
cd frontend

# Python HTTP 서버 실행
python -m http.server 3000
```

프론트엔드 접속:

- 🏠 **홈페이지**: http://localhost:3000/home.html
- 🔑 **로그인**: http://localhost:3000/login.html
- ✍️ **회원가입**: http://localhost:3000/signup.html
- 📋 **할일 관리**: http://localhost:3000/index.html

## 🎮 사용법

### 1. 첫 사용자 등록

1. **홈페이지 접속**: http://localhost:3000/home.html
2. **"회원가입하기"** 버튼 클릭
3. **사용자 정보 입력**:
    - 사용자명 (3자 이상)
    - 이메일 주소
    - 비밀번호 (6자 이상)
    - 비밀번호 확인
4. **회원가입 완료** 후 자동으로 로그인 페이지로 이동

### 2. 로그인

1. **로그인 페이지**에서 사용자명과 비밀번호 입력
2. **JWT 토큰 발급** 및 자동 저장
3. **할일 관리 페이지**로 자동 이동

### 3. 할일 관리

#### 할일 추가

- 제목 입력 (필수)
- 설명 입력 (선택)
- 우선순위 선택 (높음/보통/낮음)
- "추가" 버튼 클릭 또는 Enter 키

#### 할일 관리

- **완료 토글**: "완료" 버튼으로 상태 변경
- **검색**: 실시간 제목/설명 검색
- **삭제**: "삭제" 버튼 (확인 대화상자)
- **우선순위별 정렬**: 자동으로 높은 우선순위부터 표시

### 4. 로그아웃

- 상단 **"로그아웃"** 버튼 클릭
- JWT 토큰 자동 삭제
- 로그인 페이지로 리다이렉트

## 🔌 API 엔드포인트

### 🔐 인증 관련

| 메서드    | 엔드포인트     | 설명              | 인증 필요 |
|--------|-----------|-----------------|-------|
| `POST` | `/signup` | 회원가입            | ❌     |
| `POST` | `/login`  | 로그인 (JWT 토큰 발급) | ❌     |
| `GET`  | `/me`     | 현재 사용자 정보 조회    | ✅     |

### 📝 할일 관리

| 메서드      | 엔드포인트         | 설명         | 인증 필요 |
|----------|---------------|------------|-------|
| `GET`    | `/todos/`     | 내 할일 목록 조회 | ✅     |
| `POST`   | `/todos/`     | 새 할일 생성    | ✅     |
| `GET`    | `/todos/{id}` | 특정 할일 조회   | ✅     |
| `PUT`    | `/todos/{id}` | 할일 수정      | ✅     |
| `DELETE` | `/todos/{id}` | 할일 삭제      | ✅     |

### 📋 API 사용 예시

#### 회원가입

```bash
curl -X POST "http://localhost:8000/signup" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com", 
       "password": "securepassword"
     }'
```

#### 로그인

```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "password": "securepassword"
     }'
```

#### 할일 생성 (인증 필요)

```bash
curl -X POST "http://localhost:8000/todos/" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -d '{
       "title": "FastAPI 공부하기",
       "description": "부트캠프 과제 완성",
       "priority": 1
     }'
```

## 🚀 AWS EC2 배포

### 🔧 EC2 설정

1. **EC2 인스턴스 생성**
    - **AMI**: Ubuntu 22.04 LTS
    - **인스턴스 타입**: t2.micro (프리 티어)
    - **키 페어**: 새로 생성 및 다운로드 (.pem)

2. **보안 그룹 설정**
   ```
   - SSH (22): 내 IP만 허용
   - HTTP (80): 모든 소스 (0.0.0.0/0)
   - HTTPS (443): 모든 소스 (0.0.0.0/0)
   - Custom TCP (8000): 모든 소스 (개발/테스트용)
   ```

3. **EC2 접속**
   ```bash
   chmod 400 your-key.pem
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

### 🛠️ 서버 환경 구성

```bash
# 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 필수 패키지 설치
sudo apt install python3-pip python3-venv nginx git -y

# 프로젝트 클론
git clone https://github.com/your-username/your-repo.git ~/fastapi-app
cd ~/fastapi-app

# Python 환경 설정
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ⚙️ GitHub Actions 배포 설정

**GitHub Secrets** 설정 (Settings > Secrets and variables > Actions):

```
🔑 EC2 접속
- EC2_SSH_KEY: .pem 키 파일 전체 내용
- EC2_HOST: EC2 퍼블릭 IP 주소
- EC2_USER: ubuntu

🗄️ 데이터베이스 (선택사항)
- DATABASE_URL: PostgreSQL 연결 URL
- DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

🔐 보안
- SECRET_KEY: JWT 서명용 비밀 키
```

**자동 배포 실행**:

```bash
git add .
git commit -m "Deploy to EC2"
git push origin master  # master 브랜치에 push하면 자동 배포
```

## 🎓 학습 목표

### 백엔드 개발

- ✅ **FastAPI 고급 기능** - 의존성 주입, 미들웨어, 예외 처리
- ✅ **JWT 인증 시스템** - 토큰 생성, 검증, 갱신
- ✅ **SQLAlchemy ORM** - 관계형 모델링, 세션 관리
- ✅ **보안 베스트 프랙티스** - 비밀번호 해싱, CORS, 환경변수
- ✅ **API 설계** - RESTful 원칙, 스키마 검증

### 프론트엔드 개발

- ✅ **모던 JavaScript** - ES6+, Fetch API, Promise/async-await
- ✅ **SPA 라우팅** - 클라이언트 사이드 네비게이션
- ✅ **상태 관리** - 로컬 스토리지, 토큰 관리
- ✅ **반응형 디자인** - CSS Grid, Flexbox, 미디어 쿼리
- ✅ **사용자 경험** - 로딩 상태, 에러 처리, 폼 검증

### DevOps & 배포

- ✅ **클라우드 배포** - AWS EC2, Nginx 설정
- ✅ **CI/CD 파이프라인** - GitHub Actions, 자동화
- ✅ **환경 관리** - 개발/스테이징/프로덕션 분리
- ✅ **보안 설정** - SSH 키, 환경변수, 방화벽

## 🔄 확장 아이디어

### 단기 개선사항

- 📱 **모바일 앱** - React Native/Flutter
- 🌙 **다크 모드** - 테마 전환 기능
- 📊 **할일 통계** - 완료율, 생산성 차트
- 🔔 **알림 시스템** - 브라우저 푸시 알림

### 장기 확장

- 👥 **팀 협업** - 할일 공유, 팀 관리
- 🔄 **실시간 동기화** - WebSocket, 멀티 디바이스
- 🤖 **AI 기능** - 스마트 우선순위, 일정 추천
- 📈 **고급 분석** - 생산성 인사이트, 리포팅

## 🤝 기여하기

1. **Fork** 이 저장소
2. **Feature 브랜치** 생성 (`git checkout -b feature/AmazingFeature`)
3. **변경사항 커밋** (`git commit -m 'Add some AmazingFeature'`)
4. **브랜치에 Push** (`git push origin feature/AmazingFeature`)
5. **Pull Request** 생성

## 📄 라이선스

이 프로젝트는 교육 목적으로 자유롭게 사용할 수 있습니다.

## 🆘 문제 해결

### 일반적인 문제들

**Q: JWT 토큰이 만료되었다는 에러가 나요**
A: 토큰은 30분 후 만료됩니다. 로그아웃 후 다시 로그인하세요.

**Q: CORS 에러가 발생해요**
A: 백엔드가 실행 중인지 확인하고, API_BASE_URL이 올바른지 확인하세요.

**Q: 데이터베이스 연결 오류**
A: .env 파일의 DATABASE_URL이 올바른지 확인하세요.

**Q: GitHub Actions 배포가 실패해요**
A: GitHub Secrets가 모두 올바르게 설정되었는지 확인하세요.

---

## 🎉 완성을 축하합니다!

이 프로젝트를 완성하신 것을 축하드립니다! 이제 여러분은:

- 🏗️ **풀스택 개발자**로서 백엔드와 프론트엔드를 모두 다룰 수 있습니다
- 🔐 **보안 인식**을 갖춘 개발자가 되었습니다
- ☁️ **클라우드 배포** 경험을 쌓았습니다
- 🤖 **자동화된 워크플로우**를 구축할 수 있습니다

**다음 스텝**: 포트폴리오에 추가하고, 더 큰 프로젝트에 도전해보세요! 🚀

---

**Happy Coding! 💻✨**