# FastAPI 부트캠프 프로젝트 - Step 8: GitHub Actions CI/CD

이 단계에서는 GitHub Actions를 사용하여 CI/CD(지속적 통합/지속적 배포) 파이프라인을 구축합니다.

## 학습 목표
- **CI/CD 개념** 이해 및 실제 적용
- **GitHub Actions 워크플로우** 작성 및 관리
- **자동화된 테스트** 설정 및 실행
- **자동 배포** 시스템 구축
- **DevOps 베스트 프랙티스** 학습

## 프로젝트 구조
```
fastapi-bootcamp/
├── .github/
│   └── workflows/
│       ├── ci.yml           # CI 워크플로우 (테스트 자동화)
│       └── deploy.yml       # CD 워크플로우 (배포 자동화)
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
├── .env.example
├── .gitignore
└── README.md
```

## CI/CD 파이프라인 구성

### 🧪 CI (Continuous Integration) - ci.yml
**목적**: 코드 변경 시 자동으로 품질을 검증하여 안정성 보장

```yaml
# 트리거 조건
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]
```

**실행 단계**:
1. **📥 소스 코드 체크아웃**: GitHub 저장소에서 최신 코드 가져오기
2. **🐍 Python 3.11 설정**: 일관된 Python 환경 구성
3. **📦 의존성 설치**: requirements.txt 기반 패키지 설치
4. **🚀 FastAPI 앱 로드 테스트**: 애플리케이션이 정상적으로 시작되는지 확인
5. **🗄️ 데이터베이스 모델 테스트**: SQLAlchemy 모델과 테이블 생성 검증
6. **📊 CRUD 스키마 테스트**: Pydantic 모델 유효성 검사
7. **🔍 코드 품질 체크**: Python 구문 오류 검사

### 🚀 CD (Continuous Deployment) - deploy.yml
**목적**: main 브랜치에 코드가 푸시되면 자동으로 EC2 서버에 배포

```yaml
# 트리거 조건
on:
  push:
    branches: [ main, master ]
```

**실행 단계**:
1. **📋 배포 정보 확인**: 배포 메타데이터 출력
2. **🔑 EC2 배포 설정**: SSH 키 설정 및 배포 스크립트 실행
3. **🎉 배포 완료 알림**: 성공/실패 상태에 따른 알림

## GitHub Actions 사용법

### 1. 워크플로우 모니터링
1. GitHub 저장소 → **Actions** 탭 클릭
2. 실행 중인 워크플로우 상태 확인
3. 각 단계별 로그 및 실행 결과 확인
4. 실패한 경우 상세 에러 메시지 분석

### 2. GitHub Secrets 설정 (실제 배포용)
**Settings** → **Secrets and variables** → **Actions**에서 다음 환경변수 설정:

```bash
# 🔑 EC2 서버 접속 정보
EC2_SSH_KEY=-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----

EC2_HOST=your-ec2-public-ip
EC2_USER=ubuntu

# 🔐 애플리케이션 보안 설정
SECRET_KEY=your-super-secure-secret-key

# 💾 데이터베이스 설정 (선택사항)
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### 3. 브랜치 전략 권장사항
```
main/master    ← 프로덕션 배포 (자동 배포 실행)
    ↑
develop        ← 개발 통합 브랜치
    ↑
feature/*      ← 기능 개발 브랜치 (테스트만 실행)
```

## CI/CD 워크플로우 실행 흐름

### 📈 일반적인 개발 흐름
```mermaid
graph LR
    A[코드 작성] --> B[Git Push]
    B --> C[CI 테스트 실행]
    C --> D{테스트 통과?}
    D -->|Yes| E[배포 실행]
    D -->|No| F[테스트 실패 알림]
    E --> G[서비스 업데이트]
    F --> A
```

### 🔄 실제 사용 시나리오

#### 시나리오 1: 새 기능 개발
```bash
# 1. 기능 브랜치 생성
git checkout -b feature/todo-priority

# 2. 코드 작성 및 커밋
git add .
git commit -m "Add priority field to todos"

# 3. 브랜치 푸시 → CI 테스트 자동 실행
git push origin feature/todo-priority

# 4. Pull Request 생성 → CI 테스트 재실행
# GitHub에서 PR 생성

# 5. 테스트 통과 후 메인 브랜치 병합
git checkout main
git merge feature/todo-priority

# 6. 메인 브랜치 푸시 → CI 테스트 + 자동 배포 실행
git push origin main
```

#### 시나리오 2: 긴급 버그 수정
```bash
# 1. 핫픽스 브랜치 생성
git checkout -b hotfix/database-connection

# 2. 버그 수정 및 즉시 배포
git add .
git commit -m "Fix database connection timeout"
git push origin main  # 직접 메인에 푸시 → 즉시 배포
```

## 자동화된 테스트 내용

### ✅ FastAPI 앱 로드 테스트
```python
# 애플리케이션이 정상적으로 로드되는지 확인
from app.main import app
print(f'✅ 앱 제목: {app.title}')
print(f'📝 앱 설명: {app.description}')
```

### ✅ 데이터베이스 모델 테스트
```python
# 데이터베이스 테이블 생성 테스트
from app.database import engine, Base
from app.models import Todo

Base.metadata.create_all(bind=engine)
print('✅ 데이터베이스 테이블 생성 성공!')
```

### ✅ Pydantic 스키마 검증
```python
# 데이터 유효성 검사 테스트
from app.crud import TodoCreate

valid_todo = TodoCreate(title='테스트', description='설명')
# 제목 필수 필드 검증 등
```

## 실제 배포 설정 가이드

### 1. EC2 인스턴스 준비
```bash
# Ubuntu 22.04 LTS 인스턴스 생성
# 보안 그룹 설정:
# - SSH (22): 내 IP만 허용
# - HTTP (80): 모든 소스 허용
# - HTTPS (443): 모든 소스 허용
# - Custom TCP (8000): 모든 소스 허용 (개발용)
```

### 2. 서버 환경 구성
```bash
# EC2 서버에 접속 후 실행
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv nginx git -y

# 프로젝트 클론
git clone https://github.com/your-username/your-repo.git ~/fastapi-app
cd ~/fastapi-app

# Python 가상환경 설정
python3 -m venv venv
source venv/bin/activate
cd backend && pip install -r requirements.txt
```

### 3. 배포 워크플로우 활성화
```yaml
# deploy.yml 파일에서 실제 배포 활성화
- name: 🚀 EC2에 실제 배포
  if: true  # false에서 true로 변경
```

## CI/CD의 장점

### 🔍 품질 보장
- **자동 테스트**: 모든 코드 변경 시 품질 검증
- **빠른 피드백**: 문제 발생 시 즉시 알림
- **회귀 방지**: 기존 기능 손상 없이 새 기능 추가

### 🚀 배포 효율성
- **자동 배포**: 수동 배포 작업 제거
- **일관성**: 항상 동일한 배포 프로세스
- **롤백 지원**: 문제 발생 시 이전 버전 복구 가능

### 👥 팀 협업
- **코드 리뷰**: Pull Request를 통한 코드 품질 관리
- **투명성**: 모든 배포 과정이 로그로 기록
- **책임 추적**: 누가 언제 무엇을 배포했는지 추적 가능

## 고급 확장 기능

### 🧪 고급 테스트
```yaml
# pytest를 사용한 단위 테스트
- name: Run pytest
  run: |
    cd backend
    pip install pytest pytest-cov
    pytest tests/ --cov=app --cov-report=xml

# 코드 커버리지 체크
- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
```

### 🔔 알림 시스템
```yaml
# 슬랙 알림 추가
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### 🎯 다양한 배포 전략
- **Blue-Green 배포**: 무중단 배포
- **카나리 배포**: 일부 사용자에게만 먼저 배포
- **롤링 배포**: 서버를 하나씩 순차적으로 업데이트

## 문제 해결

### ❌ CI 테스트 실패
1. **의존성 문제**: requirements.txt 확인
2. **환경 차이**: 로컬과 CI 환경 버전 일치 여부
3. **코드 문법 오류**: Python 구문 검사

### ❌ 배포 실패
1. **SSH 키 문제**: GitHub Secrets의 EC2_SSH_KEY 확인
2. **서버 접근 불가**: EC2 보안 그룹 및 네트워크 설정 확인
3. **권한 문제**: EC2 사용자 권한 및 파일 소유권 확인

### 🔍 디버깅 방법
```bash
# 로컬에서 GitHub Actions 환경 시뮬레이션
docker run --rm -v $(pwd):/workspace -w /workspace ubuntu:22.04 bash
apt update && apt install python3 python3-pip -y
cd backend && pip install -r requirements.txt
python -c "from app.main import app; print('App loaded successfully!')"
```

## 🎯 이 단계에서 배운 내용

- ✅ **CI/CD 개념**: 지속적 통합과 지속적 배포의 이해
- ✅ **GitHub Actions**: 워크플로우 작성 및 자동화 설정
- ✅ **자동 테스트**: 코드 품질 보장을 위한 테스트 자동화
- ✅ **자동 배포**: 코드 변경 시 서버 자동 업데이트
- ✅ **DevOps 실천**: 개발과 운영의 효율적인 통합

## 🎉 부트캠프 완주 축하!

**전체 8단계 완료**:
1. ✅ **프로젝트 설정**: 기본 구조 생성
2. ✅ **백엔드 기초**: FastAPI 앱 기본 틀
3. ✅ **데이터베이스**: SQLAlchemy 모델링
4. ✅ **CRUD API**: RESTful API 완성
5. ✅ **프론트엔드**: HTML/CSS/JS 구현
6. ✅ **API 연동**: 실제 데이터 통신
7. ✅ **배포 준비**: 환경 설정 및 보안
8. ✅ **CI/CD**: 자동화된 개발 워크플로우

이제 여러분은 **풀스택 개발자**이자 **DevOps 엔지니어**의 기초 지식을 모두 갖추었습니다! 🚀

**다음 도전 과제**:
- 더 복잡한 애플리케이션 개발
- 마이크로서비스 아키텍처 학습
- 쿠버네티스와 도커 활용
- 실제 프로덕션 환경 운영

**Happy Coding & Deploying! 💻✨🚀**