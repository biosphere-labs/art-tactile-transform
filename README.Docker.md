# Art Tactile Transform - Docker Quick Start

Transform images into 3D printable tactile art for blind users - now available as a Docker container!

## 🚀 Fastest Start (Auto-Opens Browser!)

### Linux/macOS
```bash
./launch.sh
```

### Windows (PowerShell)
```powershell
.\launch.ps1
```

### Windows (Command Prompt)
```cmd
launch.bat
```

**What it does**: Starts container + opens browser automatically!

See [LAUNCHER.md](LAUNCHER.md) for details.

---

## One-Line Manual Deployment

```bash
docker run -d -p 7860:7860 fluidnotions/art-tactile-transform:latest
```

Then open browser to: **http://localhost:7860**

---

## What You Get

A fully-functional web interface that converts images into tactile 3D models:

- **Upload images** (portraits, landscapes, text, diagrams)
- **Adjust parameters** in real-time
- **Preview in 3D** with orbit controls
- **Export STL files** ready for 3D printing

### The Innovation

Unlike traditional depth estimation (which would raise backgrounds), this uses **semantic height mapping**:

- **Faces = HIGH** (what blind users need to feel)
- **Backgrounds = LOW** (not important)
- **Features = HIGHEST** (eyes, nose, mouth emphasized)

Result: Tactile art that blind users can actually recognize!

---

## Quick Examples

### Run on Different Port

```bash
docker run -d -p 8080:7860 fluidnotions/art-tactile-transform:latest
```

Access at: http://localhost:8080

### Save Outputs to Local Directory

```bash
docker run -d \
  -p 7860:7860 \
  -v $(pwd)/my-outputs:/app/outputs \
  fluidnotions/art-tactile-transform:latest
```

### Use with Docker Compose

```bash
# Download docker-compose.yml from repo
curl -O https://raw.githubusercontent.com/fluidnotions/art-tactile-transform/main/docker-compose.yml

# Start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## System Requirements

- **Docker**: Version 20.10+ recommended
- **Memory**: 4GB minimum, 8GB optimal
- **Disk**: ~2GB for image + models
- **Ports**: 7860 (or custom port)

---

## Complete Documentation

See [DOCKER.md](DOCKER.md) for:
- Advanced configuration
- GPU support (NVIDIA)
- Troubleshooting
- Building from source
- Push to private registry

---

## Support

- **Repository**: https://github.com/fluidnotions/art-tactile-transform
- **Docker Hub**: https://hub.docker.com/r/fluidnotions/art-tactile-transform
- **Issues**: https://github.com/fluidnotions/art-tactile-transform/issues

---

**Powered by**: Python 3.13, Gradio, OpenCV, PyTorch, Transformers
