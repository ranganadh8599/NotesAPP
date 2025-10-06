@echo off
echo ========================================
echo Starting Notes API Server
echo ========================================
echo.
echo Server will be available at:
echo - API: http://localhost:8000
echo - Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn main:app --reload --host 127.0.0.1 --port 8000