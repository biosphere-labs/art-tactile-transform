@echo off
REM Art Tactile Transform - Windows Installer
REM This script installs the application and creates a desktop shortcut

echo ============================================
echo Art Tactile Transform - Installation
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.10 or later from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

REM Display Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

REM Upgrade pip
echo Upgrading pip...
venv\Scripts\python.exe -m pip install --upgrade pip
echo.

REM Install core dependencies
echo Installing core dependencies (~100MB)...
echo This may take 2-5 minutes depending on your internet speed.
echo.
venv\Scripts\pip.exe install -r requirements-core.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install core dependencies
    pause
    exit /b 1
)
echo Core dependencies installed successfully!
echo.

REM Install the package itself
echo Installing Art Tactile Transform...
cd ..
venv\Scripts\pip.exe install -e .
if %errorlevel% neq 0 (
    echo ERROR: Failed to install application
    pause
    exit /b 1
)
cd windows
echo.

REM Create desktop shortcut
echo Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Art Tactile Transform.lnk

REM Create a VBScript to generate the shortcut
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = "%SHORTCUT%" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%SCRIPT_DIR%launcher.bat" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%SCRIPT_DIR%" >> CreateShortcut.vbs
echo oLink.Description = "Art Tactile Transform - AI-powered 3D tactile art generator" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs

cscript //nologo CreateShortcut.vbs
del CreateShortcut.vbs

if exist "%SHORTCUT%" (
    echo Desktop shortcut created successfully!
) else (
    echo Warning: Could not create desktop shortcut
)
echo.

echo ============================================
echo Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Double-click "Art Tactile Transform" on your desktop
echo 2. First run will download AI models (~500MB, 2-5 min)
echo 3. Subsequent runs will be instant!
echo.
echo Or run manually: launcher.bat
echo.
pause
