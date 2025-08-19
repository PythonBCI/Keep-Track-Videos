@echo off
REM Desktop Cat - Video Quest Game Launcher for Windows
REM Double-click this file to run the game!

echo Starting Desktop Cat - Video Quest Game...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python 3.6+ and try again.
    echo.
    echo You can download Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Run the application
python desktop_cat.py

REM Keep window open if there's an error
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Please check the message above.
    pause
)