# Art Tactile Transform - Docker Launcher (Windows PowerShell)
# Starts the Docker container and opens the browser automatically

param(
    [switch]$Local
)

# Configuration
$ImageName = "fluidnotions/art-tactile-transform:latest"
$ContainerName = "art-tactile-transform"
$Port = 7860
$Url = "http://localhost:$Port"

# Colors
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Cyan"
$Red = "Red"

Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor $Blue
Write-Host "   Art Tactile Transform - Semantic Tactile Art Generator" -ForegroundColor $Blue
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor $Blue
Write-Host ""

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "✗ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor $Red
    exit 1
}

# Check if container already exists
$ContainerExists = docker ps -a --format "{{.Names}}" | Select-String -Pattern "^$ContainerName$"
$SkipStart = $false

if ($ContainerExists) {
    Write-Host "⚠ Container '$ContainerName' already exists." -ForegroundColor $Yellow

    # Check if it's running
    $ContainerRunning = docker ps --format "{{.Names}}" | Select-String -Pattern "^$ContainerName$"

    if ($ContainerRunning) {
        Write-Host "✓ Container is already running." -ForegroundColor $Green
        $SkipStart = $true
    } else {
        Write-Host "⟳ Starting existing container..." -ForegroundColor $Yellow
        docker start $ContainerName
        $SkipStart = $true
    }
}

# Pull latest image if not using local build
if (-not $Local) {
    Write-Host "⬇ Pulling latest image from Docker Hub..." -ForegroundColor $Blue
    try {
        docker pull $ImageName
    } catch {
        Write-Host "⚠ Could not pull latest image, using local version" -ForegroundColor $Yellow
    }
}

# Start container if not already running
if (-not $SkipStart) {
    Write-Host "🚀 Starting container..." -ForegroundColor $Blue
    docker run -d `
        --name $ContainerName `
        -p "${Port}:${Port}" `
        --restart unless-stopped `
        $ImageName
}

# Wait for service to be ready
Write-Host "⏳ Waiting for service to be ready..." -ForegroundColor $Yellow
$MaxWait = 60
$Waited = 0

while ($Waited -lt $MaxWait) {
    try {
        $Response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($Response.StatusCode -eq 200) {
            Write-Host "✓ Service is ready!" -ForegroundColor $Green
            break
        }
    } catch {
        # Still waiting
    }

    if ($Waited % 5 -eq 0) {
        Write-Host "  Still waiting... ($Waited`s/$MaxWait`s)" -ForegroundColor $Yellow
    }

    Start-Sleep -Seconds 1
    $Waited++
}

if ($Waited -ge $MaxWait) {
    Write-Host "✗ Service failed to start within $MaxWait seconds." -ForegroundColor $Red
    Write-Host "Check logs with: docker logs $ContainerName" -ForegroundColor $Red
    exit 1
}

# Open browser
Write-Host "🌐 Opening browser at $Url" -ForegroundColor $Green
Write-Host ""

Start-Process $Url

# Show helpful info
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor $Blue
Write-Host "✓ Art Tactile Transform is running!" -ForegroundColor $Green
Write-Host ""
Write-Host "  • URL: $Url" -ForegroundColor $Blue
Write-Host "  • Container: $ContainerName" -ForegroundColor $Blue
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  • View logs:    " -ForegroundColor $Blue -NoNewline
Write-Host "docker logs -f $ContainerName" -ForegroundColor $Yellow
Write-Host "  • Stop:         " -ForegroundColor $Blue -NoNewline
Write-Host "docker stop $ContainerName" -ForegroundColor $Yellow
Write-Host "  • Restart:      " -ForegroundColor $Blue -NoNewline
Write-Host "docker restart $ContainerName" -ForegroundColor $Yellow
Write-Host "  • Remove:       " -ForegroundColor $Blue -NoNewline
Write-Host "docker rm -f $ContainerName" -ForegroundColor $Yellow
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════" -ForegroundColor $Blue
