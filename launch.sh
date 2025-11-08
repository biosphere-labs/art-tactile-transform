#!/bin/bash
# Art Tactile Transform - Docker Launcher (Linux/macOS)
# Starts the Docker container and opens the browser automatically

set -e

# Configuration
IMAGE_NAME="fluidnotions/art-tactile-transform:latest"
CONTAINER_NAME="art-tactile-transform"
PORT=7860
URL="http://localhost:${PORT}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}   Art Tactile Transform - Semantic Tactile Art Generator${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

# Check if container already exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}⚠ Container '${CONTAINER_NAME}' already exists.${NC}"

    # Check if it's running
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo -e "${GREEN}✓ Container is already running.${NC}"
        SKIP_START=true
    else
        echo -e "${YELLOW}⟳ Starting existing container...${NC}"
        docker start ${CONTAINER_NAME}
        SKIP_START=true
    fi
else
    SKIP_START=false
fi

# Pull latest image if not running local build
if [ "$1" != "--local" ]; then
    echo -e "${BLUE}⬇ Pulling latest image from Docker Hub...${NC}"
    docker pull ${IMAGE_NAME} || echo -e "${YELLOW}⚠ Could not pull latest image, using local version${NC}"
fi

# Start container if not already running
if [ "$SKIP_START" = false ]; then
    echo -e "${BLUE}🚀 Starting container...${NC}"
    docker run -d \
        --name ${CONTAINER_NAME} \
        -p ${PORT}:${PORT} \
        --restart unless-stopped \
        ${IMAGE_NAME}
fi

# Wait for service to be ready
echo -e "${YELLOW}⏳ Waiting for service to be ready...${NC}"
MAX_WAIT=60
WAITED=0

while [ $WAITED -lt $MAX_WAIT ]; do
    if curl -s -o /dev/null -w "%{http_code}" ${URL} | grep -q "200"; then
        echo -e "${GREEN}✓ Service is ready!${NC}"
        break
    fi

    if [ $((WAITED % 5)) -eq 0 ]; then
        echo -e "${YELLOW}  Still waiting... (${WAITED}s/${MAX_WAIT}s)${NC}"
    fi

    sleep 1
    WAITED=$((WAITED + 1))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    echo -e "${RED}✗ Service failed to start within ${MAX_WAIT} seconds.${NC}"
    echo -e "${RED}Check logs with: docker logs ${CONTAINER_NAME}${NC}"
    exit 1
fi

# Open browser
echo -e "${GREEN}🌐 Opening browser at ${URL}${NC}"
echo ""

# Detect OS and open browser
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open ${URL}
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v xdg-open > /dev/null; then
        xdg-open ${URL}
    elif command -v gnome-open > /dev/null; then
        gnome-open ${URL}
    else
        echo -e "${YELLOW}⚠ Could not auto-open browser. Please open: ${URL}${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Unknown OS. Please open: ${URL}${NC}"
fi

# Show helpful info
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✓ Art Tactile Transform is running!${NC}"
echo ""
echo -e "  ${BLUE}•${NC} URL: ${URL}"
echo -e "  ${BLUE}•${NC} Container: ${CONTAINER_NAME}"
echo ""
echo -e "Useful commands:"
echo -e "  ${BLUE}•${NC} View logs:    ${YELLOW}docker logs -f ${CONTAINER_NAME}${NC}"
echo -e "  ${BLUE}•${NC} Stop:         ${YELLOW}docker stop ${CONTAINER_NAME}${NC}"
echo -e "  ${BLUE}•${NC} Restart:      ${YELLOW}docker restart ${CONTAINER_NAME}${NC}"
echo -e "  ${BLUE}•${NC} Remove:       ${YELLOW}docker rm -f ${CONTAINER_NAME}${NC}"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
