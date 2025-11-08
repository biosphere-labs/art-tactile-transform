# Quick Launch Scripts - Auto-Open Browser

These launcher scripts automatically start the Docker container AND open your browser to the GUI.

## Usage

### Linux/macOS

```bash
./launch.sh
```

**What it does:**
1. ✓ Checks if Docker is running
2. ✓ Pulls latest image from Docker Hub
3. ✓ Starts container (or reuses existing)
4. ✓ Waits for service to be ready
5. ✓ **Opens your browser automatically** to http://localhost:7860

**Use local image** (skip Docker Hub pull):
```bash
./launch.sh --local
```

---

### Windows (PowerShell)

```powershell
.\launch.ps1
```

**Use local image:**
```powershell
.\launch.ps1 -Local
```

---

### Windows (Command Prompt)

```cmd
launch.bat
```

**Use local image:**
```cmd
launch.bat --local
```

---

## Features

All launcher scripts provide:

- ✅ **Automatic browser opening** - No manual URL entry needed
- ✅ **Container reuse** - Detects existing containers and reuses them
- ✅ **Health checking** - Waits for service to be fully ready
- ✅ **Color-coded output** - Easy to see status at a glance
- ✅ **Helpful tips** - Shows useful Docker commands after launch
- ✅ **Error handling** - Clear messages if something goes wrong

---

## What You'll See

```
════════════════════════════════════════════════════════════════
   Art Tactile Transform - Semantic Tactile Art Generator
════════════════════════════════════════════════════════════════

⬇ Pulling latest image from Docker Hub...
🚀 Starting container...
⏳ Waiting for service to be ready...
✓ Service is ready!
🌐 Opening browser at http://localhost:7860

════════════════════════════════════════════════════════════════
✓ Art Tactile Transform is running!

  • URL: http://localhost:7860
  • Container: art-tactile-transform

Useful commands:
  • View logs:    docker logs -f art-tactile-transform
  • Stop:         docker stop art-tactile-transform
  • Restart:      docker restart art-tactile-transform
  • Remove:       docker rm -f art-tactile-transform

════════════════════════════════════════════════════════════════
```

Your browser will open automatically to the GUI!

---

## Troubleshooting

### Docker not running
```
✗ Docker is not running. Please start Docker and try again.
```
**Solution**: Start Docker Desktop

### Port already in use
Edit the launcher script and change `PORT=7860` to another port like `PORT=7861`

### Browser doesn't open
The launcher will show the URL. Copy and paste it into your browser:
```
http://localhost:7860
```

---

## Manual Docker Commands

If you prefer manual control:

```bash
# Pull image
docker pull fluidnotions/art-tactile-transform:latest

# Run container
docker run -d --name art-tactile-transform -p 7860:7860 fluidnotions/art-tactile-transform:latest

# Open browser manually
# Then navigate to: http://localhost:7860
```

---

## Advanced: Custom Port

To run on a different port, edit the launcher script:

**Linux/macOS** (`launch.sh`):
```bash
PORT=8080  # Change this line
```

**Windows** (`launch.ps1` or `launch.bat`):
```powershell
$Port = 8080  # PowerShell
set PORT=8080 REM Batch
```

Then access at: `http://localhost:8080`

---

## Benefits Over Manual Launch

| Manual Docker | Launcher Script |
|---------------|----------------|
| 5-6 commands | 1 command |
| Copy/paste URL | Browser opens automatically |
| Wait and check manually | Auto-waits with progress |
| No visual feedback | Color-coded status |
| Remember commands | Helpful command list shown |

**Time saved**: ~30 seconds per launch 🚀
