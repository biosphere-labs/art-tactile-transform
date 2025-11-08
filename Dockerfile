# Art Tactile Transform - Docker Image
# Converts images into 3D printable tactile representations for blind users
# Uses semantic height mapping where faces are RAISED, backgrounds are LOWERED

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    g++ \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install UV package manager
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:$PATH"

# Copy project files
COPY pyproject.toml ./
COPY src/ ./src/
COPY README.md ./

# Install dependencies
# Note: Using opencv-python instead of opencv-python-headless for full compatibility
RUN uv pip install --system -e .

# Download model cache (optional - speeds up first run)
# Uncomment to pre-download the depth estimation model
# RUN python -c "from transformers import pipeline; pipeline('depth-estimation', model='LiheYoung/depth-anything-small-hf')"

# Expose Gradio port
EXPOSE 7860

# Set environment variables
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:7860/ || exit 1

# Run the GUI
CMD ["art-tactile-gui"]
