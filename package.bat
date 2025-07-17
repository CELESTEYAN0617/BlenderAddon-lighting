@echo off
echo =====================================================
echo Procedural Lighting System - Addon Packaging Tool
echo =====================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.6+ and try again
    pause
    exit /b 1
)

echo Running packaging script...
echo.
python package_addon.py

echo.
echo Packaging complete!
pause 