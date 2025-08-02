@echo off
REM MP4 to MP3 Converter - Windows Batch File
REM This script runs the MP4 to MP3 converter application

echo Starting MP4 to MP3 Converter...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

REM Check if the main script exists
if not exist "mp4_to_mp3_converter.py" (
    echo Error: mp4_to_mp3_converter.py not found
    echo Please ensure you're running this from the correct directory
    pause
    exit /b 1
)

REM Run the application
python mp4_to_mp3_converter.py

REM Keep window open if there was an error
if errorlevel 1 (
    echo.
    echo Application exited with an error
    pause
)
