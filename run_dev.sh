#!/bin/bash

# Development 실행 스크립트
echo "Starting FastAPI Todo App in development mode..."

# 백엔드 서버 실행
echo "Starting backend server..."
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 프론트엔드 서버 실행
echo "Starting frontend server..."
cd ../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "Servers are running:"
echo "Backend API: http://localhost:8000"
echo "Backend Docs: http://localhost:8000/docs"
echo "Frontend: http://localhost:3000/todo.html"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop all servers"

# Ctrl+C 처리
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# 프로세스가 종료되기를 기다림
wait