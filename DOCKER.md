# Docker Deployment Guide

## Quick Start

### Pull from Docker Hub

```bash
docker pull fluidnotions/art-tactile-transform:latest
```

### Run the Container

```bash
docker run -d \
  --name art-tactile-transform \
  -p 7860:7860 \
  fluidnotions/art-tactile-transform:latest
```

Then open your browser to: `http://localhost:7860`

---

## Using Docker Compose

### Start the Service

```bash
docker-compose up -d
```

### View Logs

```bash
docker-compose logs -f
```

### Stop the Service

```bash
docker-compose down
```

---

## Configuration

### Environment Variables

- `GRADIO_SERVER_NAME`: Server hostname (default: `0.0.0.0`)
- `GRADIO_SERVER_PORT`: Server port (default: `7860`)

### Volumes

Mount a local directory for persistent outputs:

```bash
docker run -d \
  --name art-tactile-transform \
  -p 7860:7860 \
  -v $(pwd)/outputs:/app/outputs \
  fluidnotions/art-tactile-transform:latest
```

---

## Building from Source

### Build the Image

```bash
docker build -t fluidnotions/art-tactile-transform:latest .
```

### Build with Version Tag

```bash
docker build -t fluidnotions/art-tactile-transform:v0.1.0 .
```

---

## Pushing to Docker Hub

### Login to Docker Hub

```bash
docker login
```

### Tag the Image

```bash
docker tag fluidnotions/art-tactile-transform:latest fluidnotions/art-tactile-transform:v0.1.0
```

### Push to Registry

```bash
docker push fluidnotions/art-tactile-transform:latest
docker push fluidnotions/art-tactile-transform:v0.1.0
```

---

## Advanced Usage

### Run with GPU Support (NVIDIA)

For faster processing with CUDA:

```bash
docker run -d \
  --name art-tactile-transform \
  --gpus all \
  -p 7860:7860 \
  fluidnotions/art-tactile-transform:latest
```

**Note**: Requires NVIDIA Container Toolkit installed.

### Custom Port

Run on a different port:

```bash
docker run -d \
  --name art-tactile-transform \
  -p 8080:7860 \
  fluidnotions/art-tactile-transform:latest
```

Access at: `http://localhost:8080`

### Interactive Shell

Debug or inspect the container:

```bash
docker run -it \
  --entrypoint /bin/bash \
  fluidnotions/art-tactile-transform:latest
```

---

## Troubleshooting

### Container Won't Start

Check logs:

```bash
docker logs art-tactile-transform
```

### Port Already in Use

Change the host port:

```bash
docker run -d \
  --name art-tactile-transform \
  -p 7861:7860 \
  fluidnotions/art-tactile-transform:latest
```

### Model Download Issues

The container downloads the AI model on first run. This may take a few minutes. Check logs:

```bash
docker logs -f art-tactile-transform
```

### Memory Issues

Increase Docker memory limit (Docker Desktop → Settings → Resources):

- Recommended: 4GB minimum
- Optimal: 8GB or more

---

## Health Check

The container includes a health check endpoint. View status:

```bash
docker inspect --format='{{.State.Health.Status}}' art-tactile-transform
```

---

## Image Information

- **Image Name**: `fluidnotions/art-tactile-transform`
- **Tags**: `latest`, `v0.1.0`
- **Base Image**: `python:3.13-slim`
- **Exposed Port**: `7860`
- **Working Directory**: `/app`

---

## What This Application Does

Art Tactile Transform converts flat images into 3D printable tactile representations designed for blind and visually impaired users.

### Key Innovation

Unlike traditional depth estimation, it uses **semantic height mapping**:

- **Faces = RAISED** (important to feel)
- **Backgrounds = LOWERED** (not important)
- **Features = HIGHEST** (eyes, nose, mouth emphasized)

### Use Cases

- Creating tactile art for blind users
- Educational materials for visually impaired students
- Museum accessibility exhibits
- Converting portraits, landscapes, text, and diagrams into 3D models

---

## Support

- **Repository**: https://github.com/fluidnotions/art-tactile-transform
- **Docker Hub**: https://hub.docker.com/r/fluidnotions/art-tactile-transform
- **Issues**: https://github.com/fluidnotions/art-tactile-transform/issues

---

## License

See the LICENSE file in the repository.
