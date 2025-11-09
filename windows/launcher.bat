@echo off
REM Art Tactile Transform - Launcher
REM Handles first-run setup and launches the GUI

REM Change to script directory
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo ERROR: Virtual environment not found!
    echo Please run install.bat first.
    echo.
    pause
    exit /b 1
)

echo ============================================
echo Art Tactile Transform - AI Depth Estimation
echo ============================================
echo.

REM Check if PyTorch is installed (first-run check)
echo Checking dependencies...
venv\Scripts\python.exe -c "import torch" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo FIRST-TIME SETUP
    echo ============================================
    echo.
    echo Downloading AI models and PyTorch (~2GB)
    echo This will take 5-10 minutes depending on your internet speed.
    echo.
    echo What's being downloaded:
    echo   - PyTorch CPU (~1.5GB) - Deep learning framework
    echo   - Transformers (~200MB) - AI model library
    echo   - Depth model (~500MB) - Downloaded automatically on first use
    echo.
    pause
    echo.
    echo Downloading PyTorch...
    venv\Scripts\pip.exe install -r requirements-pytorch.txt
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Failed to install PyTorch dependencies
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
    echo.
    echo PyTorch installed successfully!
    echo.
)

REM Launch the GUI
echo Launching GUI...
echo.
echo The browser will open automatically at http://localhost:7860
echo.
echo Press Ctrl+C in this window to stop the server.
echo.

REM Run the GUI application
venv\Scripts\python.exe -m art_tactile_transform.gui

REM If the GUI exits, pause so user can see any error messages
if %errorlevel% neq 0 (
    echo.
    echo GUI exited with error code %errorlevel%
    pause
)
