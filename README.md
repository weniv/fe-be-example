# FastAPI 부트캠프 프로젝트 - Step 7: 배포 준비

이 단계에서는 애플리케이션을 실제 서버에 배포할 수 있도록 환경 설정과 보안을 강화합니다.

## 학습 목표
- **환경변수 관리**: 개발/프로덕션 설정 분리
- **보안 강화**: 민감한 정보 보호 및 CORS 설정
- **배포 체크리스트**: 실제 배포 전 확인사항
- **모니터링 준비**: 헬스체크 엔드포인트 구현

## 프로젝트 구조
```
fastapi-bootcamp/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # 환경변수 지원 추가
│   │   ├── database.py
│   │   ├── models.py
│   │   └── crud.py
│   └── requirements.txt     # python-dotenv 포함
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── .env.example             # 환경변수 템플릿 (새로 추가)
├── .gitignore              # Git 제외 파일 목록 (새로 추가)
└── README.md
```

## 새로 추가된 배포 준비 기능

### 1. 환경변수 지원 (.env.example)
```bash
# 서버 환경 설정
ENVIRONMENT=development

# JWT 보안 키 (프로덕션에서는 반드시 변경!)
SECRET_KEY=your-super-secret-jwt-key-change-in-production-please

# 데이터베이스 설정
DATABASE_URL=sqlite:///./todos.db

# CORS 설정 (프로덕션에서는 특정 도메인만 허용)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# 서버 포트 설정
PORT=8000

# 프론트엔드 URL (배포 시 실제 도메인으로 변경)
FRONTEND_URL=http://localhost:3000
```

### 2. 백엔드 보안 강화 (main.py)
- **환경별 CORS 설정**: 개발/프로덕션 환경에 따른 다른 CORS 정책
- **환경변수 로드**: `python-dotenv`를 사용한 설정 관리
- **헬스체크 엔드포인트**: 배포 모니터링을 위한 `/health` 엔드포인트
- **포트 설정**: 환경변수에서 포트 번호 가져오기

### 3. .gitignore 파일
- **보안 파일 제외**: `.env`, 데이터베이스 파일, 로그 파일
- **개발 환경 파일**: IDE 설정, 캐시 파일, 임시 파일
- **Python 관련 파일**: `__pycache__`, `.pyc` 파일 등

## 배포 준비 체크리스트

### 🔧 환경 설정
- [ ] `.env.example`을 복사하여 `.env` 파일 생성
- [ ] 프로덕션용 `SECRET_KEY` 생성 및 설정
- [ ] 실제 도메인으로 `ALLOWED_ORIGINS` 설정
- [ ] 데이터베이스 URL 설정 (프로덕션용)

### 🔐 보안 확인
- [ ] `.env` 파일이 `.gitignore`에 포함되어 있는지 확인
- [ ] 하드코딩된 민감한 정보가 없는지 코드 점검
- [ ] CORS 설정이 프로덕션 환경에 맞게 제한되어 있는지 확인
- [ ] SECRET_KEY가 충분히 복잡하고 안전한지 확인

### 📦 의존성 관리
- [ ] `requirements.txt`에 모든 필요한 패키지가 포함되어 있는지 확인
- [ ] 패키지 버전이 고정되어 있는지 확인 (보안 및 안정성)

## 실행 방법

### 1. 환경변수 설정
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 열어서 실제 값으로 수정
# 특히 SECRET_KEY와 ALLOWED_ORIGINS는 반드시 변경!
```

### 2. 개발 환경 실행
```bash
# 백엔드 실행
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 프론트엔드 실행 (별도 터미널)
cd frontend
python -m http.server 3000
```

### 3. 프로덕션 환경 설정 예시
```bash
# .env 파일에 프로덕션 설정
ENVIRONMENT=production
SECRET_KEY=very-secure-random-string-for-production
DATABASE_URL=postgresql://user:password@host:5432/todos_db
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
PORT=8000
```

## 배포 옵션 및 고려사항

### 1. 클라우드 플랫폼
#### AWS EC2
- **장점**: 완전한 제어권, 확장성
- **설정**: Ubuntu 22.04 LTS, Nginx 리버스 프록시
- **보안**: Security Group, SSL/TLS 인증서

#### Heroku
- **장점**: 간단한 배포, 자동 확장
- **설정**: `Procfile` 필요, PostgreSQL 애드온
- **환경변수**: Heroku Dashboard에서 설정

#### Railway/Render
- **장점**: 모던 플랫폼, Git 연동
- **설정**: `railway.json` 또는 설정 파일
- **무료 티어**: 개발/테스트 용도로 적합

### 2. 데이터베이스 마이그레이션
```bash
# 개발: SQLite (현재)
DATABASE_URL=sqlite:///./todos.db

# 프로덕션: PostgreSQL (권장)
DATABASE_URL=postgresql://username:password@host:5432/database_name
```

### 3. 웹서버 설정 (Nginx 예시)
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/frontend;
        try_files $uri $uri/ =404;
    }

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 모니터링 및 로그

### 헬스체크 엔드포인트
```bash
# 서버 상태 확인
curl http://localhost:8000/health

# 응답 예시
{
  "status": "healthy",
  "environment": "development",
  "message": "서버가 정상적으로 실행 중입니다"
}
```

### 로그 모니터링
- **개발**: 콘솔 출력으로 충분
- **프로덕션**: 로그 파일 관리, 로그 로테이션 설정
- **모니터링 도구**: Prometheus, Grafana, ELK Stack

## 보안 베스트 프랙티스

### 1. SECRET_KEY 생성
```python
# Python으로 안전한 키 생성
import secrets
secret_key = secrets.token_urlsafe(32)
print(secret_key)
```

### 2. HTTPS 설정
```bash
# Let's Encrypt 인증서 (무료)
sudo certbot --nginx -d yourdomain.com
```

### 3. 방화벽 설정
```bash
# UFW 방화벽 (Ubuntu)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

## 문제 해결

### 환경변수가 로드되지 않는 경우
1. `.env` 파일이 프로젝트 루트에 있는지 확인
2. `python-dotenv`가 설치되어 있는지 확인
3. 환경변수 이름과 값에 공백이 없는지 확인

### CORS 오류가 발생하는 경우
1. `ALLOWED_ORIGINS` 설정이 올바른지 확인
2. 프론트엔드 도메인이 정확히 포함되어 있는지 확인
3. 프로토콜(`http://` vs `https://`)이 일치하는지 확인

### 데이터베이스 연결 오류
1. `DATABASE_URL` 형식이 올바른지 확인
2. 데이터베이스 서버가 실행 중인지 확인
3. 네트워크 연결 및 방화벽 설정 확인

## 다음 단계 미리보기
Step 8에서는 GitHub Actions를 사용한 CI/CD 파이프라인을 구축하여 자동 배포를 설정합니다.

## 🎯 이 단계에서 배운 내용

- ✅ **환경변수 관리**: 개발과 프로덕션 설정 분리
- ✅ **보안 강화**: 민감한 정보 보호와 적절한 CORS 설정
- ✅ **배포 준비**: 실제 배포를 위한 체크리스트와 설정
- ✅ **모니터링**: 헬스체크 엔드포인트로 서버 상태 확인
- ✅ **베스트 프랙티스**: 보안과 운영을 고려한 코드 작성

이제 애플리케이션이 실제 서버에 배포할 준비가 완료되었습니다! 🚀