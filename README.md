# Art Tactile Transform

Transform flat images into 3D printable tactile representations designed for blind and visually impaired users.

**Key Innovation**: Uses semantic height mapping where faces and important features are RAISED and backgrounds are LOWERED - optimized for touch perception, not photographic depth.

## Quick Start

### Option 1: Docker (Easiest)

```bash
./launch.sh          # Linux/macOS
.\launch.ps1         # Windows PowerShell
launch.bat           # Windows CMD
```

Automatically starts the container and opens your browser to the GUI.

See [LAUNCHER.md](LAUNCHER.md) for details.

### Option 2: Run Locally

```bash
# Install dependencies
uv sync

# Launch GUI
uv run art-tactile-gui
```

Opens at `http://localhost:7860`

---

## Features

### Web Interface
- **Drag & Drop Upload**: Upload portrait images directly in browser
- **Real-time 3D Preview**: See your tactile model before printing with orbit controls
- **Adjustable Parameters**: Fine-tune all settings with instant visual feedback
- **Instant Export**: Download STL files ready for 3D printing

### Semantic Height Mapping
- **Faces = HIGH**: Primary subjects elevated for tactile recognition
- **Features = HIGHEST**: Eyes, nose, mouth emphasized for detail
- **Background = LOW**: Irrelevant areas suppressed for clarity
- **Edges = ENHANCED**: Sharp boundaries for feature definition

### Output Quality
- **Proper Surface Normals**: Correct orientation for 3D printing
- **Physical Scaling**: Real-world dimensions in millimeters
- **Base Plate**: Stable foundation included
- **Smooth Gradients**: Pleasant touch experience

---

## Requirements

- **Python 3.13+**
- **UV** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

Or use Docker (no Python required):
- **Docker** ([get Docker](https://docs.docker.com/get-docker/))

---

## Installation

### Local Installation

```bash
# Clone repository
git clone <repository-url>
cd art-tactile-transform

# Install dependencies
uv sync

# Launch GUI
uv run art-tactile-gui
```

### Docker Installation

```bash
# Pull image
docker pull fluidnotions/art-tactile-transform:latest

# Run (auto-launches browser)
./launch.sh
```

---

## Usage

### Web Interface

1. **Launch**: Run `uv run art-tactile-gui` or use launcher script
2. **Upload**: Drag and drop a portrait image
3. **Adjust**: Use sliders to fine-tune the tactile representation
4. **Preview**: Rotate the 3D model to inspect quality
5. **Export**: Click "Download STL" for 3D printing

### Parameters

**Physical Dimensions:**
- **Width (mm)**: 50-300, default 150
- **Relief Depth (mm)**: 0.5-10, default 3
- **Base Thickness (mm)**: 0.5-5, default 2

**Processing:**
- **Smoothing**: 0-10, default 2 (Gaussian blur for smooth surfaces)
- **Resolution**: 64-256 vertices, default 128 (higher = more detail)

**Semantic Tuning:**
- **Subject Emphasis**: 0-200%, default 120 (how much to raise faces)
- **Background Suppression**: 0-100%, default 40 (how much to flatten background)
- **Feature Sharpness**: 0-100%, default 70 (emphasis on eyes, nose, mouth)
- **Edge Strength**: 0-100%, default 60 (edge detection intensity)

---

## Configuration (Optional)

Default parameters can be customized via `.env` file:

```bash
cp .env.example .env
```

Edit `.env` to change defaults:

```env
# Physical defaults (mm)
MIN_HEIGHT_MM=0.2
MAX_HEIGHT_MM=2.0
BASE_THICKNESS_MM=1.0
PIXEL_SCALE_MM=0.2

# Processing defaults
RESOLUTION=64
GAUSSIAN_BLUR_RADIUS=0
CLAMP_MIN=0
CLAMP_MAX=255
BORDER_PIXELS=0
INVERT_HEIGHTS=false

# Model (for depth estimation mode only)
MODEL_NAME=LiheYoung/depth-anything-small-hf
HF_API_TOKEN=
```

**Note**: IMAGE_PATH and OUTPUT_PATH are not needed - the GUI handles file upload/download dynamically.

---

## Why Semantic Height Mapping?

**Traditional depth estimation** uses photographic perspective:
- Distant objects = "far away" = low relief
- Near objects = "close" = high relief
- **Problem**: For Mona Lisa, this raises the background landscape instead of her face!

**Our semantic approach**:
- **Importance-based**: Height represents what matters for touch
- **Subject-focused**: Faces and key features always raised
- **Background-aware**: Unimportant areas suppressed
- **Result**: Blind users can actually recognize the subject

---

## Development

### Run Tests
```bash
uv run pytest
```

### Code Quality
```bash
uv run black .
uv run ruff check .
uv run mypy .
```

### Project Structure
```
src/art_tactile_transform/
├── gui.py                    # Web interface
├── cli.py                    # Command-line interface
├── core/                     # Core processing
├── models/                   # Parameter classes
├── processing/               # Processing pipelines
└── utils/                    # Utilities
```

---

## Docker Deployment

See complete Docker documentation:
- [DOCKER.md](DOCKER.md) - Complete guide
- [LAUNCHER.md](LAUNCHER.md) - Auto-launch scripts
- [README.Docker.md](README.Docker.md) - Quick reference

---

## Python API

```python
from art_tactile_transform.gui import create_semantic_heightmap, process_portrait_to_stl
import cv2

# Load image
image = cv2.imread("portrait.jpg")

# Process with semantic heightmap
stl_path, preview = process_portrait_to_stl(
    image,
    width_mm=150,
    relief_depth_mm=3,
    subject_emphasis=120,
    background_suppression=40
)
```

---

## Troubleshooting

**GUI won't start:**
```bash
uv sync  # Reinstall dependencies
```

**Docker port conflict:**
```bash
# Use different port
docker run -d -p 8080:7860 fluidnotions/art-tactile-transform:latest
# Access at http://localhost:8080
```

**STL file issues:**
- Ensure output directory has write permissions
- Check that model has no errors in 3D viewer
- Try increasing resolution for more detail

**Model download slow:**
- First run downloads AI model (~500MB)
- Subsequent runs use cached model

---

## Contributing

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design and [MIGRATION.md](docs/MIGRATION.md) for API details.

---

## License

See LICENSE file.

---

**Built for accessibility** - Making visual art accessible through touch.
