#!/bin/bash

# Production 실행 스크립트
echo "Starting FastAPI Todo App in production mode..."

# 환경변수 파일 확인
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and configure it."
    exit 1
fi

# 가상환경 활성화
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# 의존성 설치
echo "Installing dependencies..."
cd backend
pip install -r requirements.txt

# 서버 실행
echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000