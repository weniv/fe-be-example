@echo off
echo Starting FastAPI Todo App in development mode...

echo Starting backend server...
start cmd /k "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo Starting frontend server...
start cmd /k "cd frontend && python -m http.server 3000"

echo.
echo ========================================
echo Servers are running:
echo Backend API: http://localhost:8000
echo Backend Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000/todo.html
echo ========================================
echo.
echo Close the opened command windows to stop the servers
pause