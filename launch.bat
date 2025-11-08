@echo off
REM Art Tactile Transform - Docker Launcher (Windows Batch)
REM Starts the Docker container and opens the browser automatically

setlocal enabledelayedexpansion

REM Configuration
set IMAGE_NAME=fluidnotions/art-tactile-transform:latest
set CONTAINER_NAME=art-tactile-transform
set PORT=7860
set URL=http://localhost:%PORT%

echo ================================================================
echo    Art Tactile Transform - Semantic Tactile Art Generator
echo ================================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not running. Please start Docker Desktop and try again.
    exit /b 1
)

REM Check if container already exists
docker ps -a --format "{{.Names}}" | findstr /R /C:"^%CONTAINER_NAME%$" >nul
if %errorlevel% equ 0 (
    echo [WARNING] Container '%CONTAINER_NAME%' already exists.

    REM Check if it's running
    docker ps --format "{{.Names}}" | findstr /R /C:"^%CONTAINER_NAME%$" >nul
    if %errorlevel% equ 0 (
        echo [OK] Container is already running.
        set SKIP_START=1
    ) else (
        echo [INFO] Starting existing container...
        docker start %CONTAINER_NAME%
        set SKIP_START=1
    )
) else (
    set SKIP_START=0
)

REM Pull latest image if not using local build
if "%1" neq "--local" (
    echo [INFO] Pulling latest image from Docker Hub...
    docker pull %IMAGE_NAME% 2>nul || echo [WARNING] Could not pull latest image, using local version
)

REM Start container if not already running
if !SKIP_START! equ 0 (
    echo [INFO] Starting container...
    docker run -d --name %CONTAINER_NAME% -p %PORT%:%PORT% --restart unless-stopped %IMAGE_NAME%
)

REM Wait for service to be ready
echo [INFO] Waiting for service to be ready...
set MAX_WAIT=60
set WAITED=0

:wait_loop
if !WAITED! geq %MAX_WAIT% goto wait_timeout

curl -s -o nul -w "%%{http_code}" %URL% 2>nul | findstr "200" >nul
if %errorlevel% equ 0 (
    echo [OK] Service is ready!
    goto service_ready
)

set /a MOD=!WAITED! %% 5
if !MOD! equ 0 (
    echo   Still waiting... (!WAITED!s/%MAX_WAIT%s^)
)

timeout /t 1 /nobreak >nul
set /a WAITED+=1
goto wait_loop

:wait_timeout
echo [ERROR] Service failed to start within %MAX_WAIT% seconds.
echo Check logs with: docker logs %CONTAINER_NAME%
exit /b 1

:service_ready
REM Open browser
echo [INFO] Opening browser at %URL%
echo.
start %URL%

REM Show helpful info
echo ================================================================
echo [OK] Art Tactile Transform is running!
echo.
echo   * URL: %URL%
echo   * Container: %CONTAINER_NAME%
echo.
echo Useful commands:
echo   * View logs:    docker logs -f %CONTAINER_NAME%
echo   * Stop:         docker stop %CONTAINER_NAME%
echo   * Restart:      docker restart %CONTAINER_NAME%
echo   * Remove:       docker rm -f %CONTAINER_NAME%
echo.
echo ================================================================

endlocal
