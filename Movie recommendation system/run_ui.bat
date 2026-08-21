@echo off
title CineMatch AI - Movie Recommendation System
color 0A

echo ============================================================
echo    🎬 CineMatch AI - Movie Recommendation System
echo ============================================================
echo.

:: Navigate to the project directory
cd /d "%~dp0"

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.12+ from https://python.org
    pause
    exit /b 1
)

echo [1/4] Checking virtual environment...

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo       Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo       Virtual environment created successfully.
) else (
    echo       Virtual environment found.
)

echo.
echo [2/4] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo       Activated.

echo.
echo [3/4] Installing/updating dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [WARNING] Some packages may have failed to install.
    echo          Attempting to continue...
)
echo       Dependencies ready.

echo.
echo [4/4] Launching CineMatch AI...
echo.
echo ============================================================
echo    The app will open in your default browser.
echo    If not, navigate to: http://localhost:8501
echo    Press Ctrl+C to stop the server.
echo ============================================================
echo.

python run.py

pause
