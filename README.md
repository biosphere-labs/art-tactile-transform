# Art Tactile Transform

This project transforms flat images into 3D printable tactile representations designed for blind and visually impaired users. Unlike traditional depth estimation, it uses semantic height mapping where faces and important features are RAISED and backgrounds are LOWERED - optimized for touch perception.

## Features

### Phase 1 MVP - Gradio GUI (NEW!)
- **Interactive Web Interface**: Easy-to-use Gradio-based GUI with real-time 3D preview
- **Portrait Mode Processing**: Face detection with semantic emphasis (faces HIGH, background LOW)
- **Adjustable Parameters**: Fine-tune subject emphasis, background suppression, feature sharpness, and edge strength
- **3D Preview**: Interactive orbit controls to inspect model before export
- **Instant STL Export**: Download ready-to-print files directly from browser

### Core Features
- **Semantic Height Mapping**: Height represents importance, not photographic depth
- **Face Detection**: OpenCV Haar Cascades for robust face and feature detection
- **Edge Enhancement**: Emphasize facial features and boundaries for tactile clarity
- **Physical Scaling**: Configurable dimensions in millimeters for real-world 3D printing
- **Enhanced STL Generation**: Proper surface normals, base plates, and physical scaling
- **UV Package Management**: Modern Python packaging with UV dependency resolution

## Requirements

- **Python 3.13** or later
- **UV** for dependency management

## Installation

### Step 1 – Install Python and UV

1. Visit <https://www.python.org/downloads/> and install **Python 3.13+**
2. Install UV: `pip install uv` or follow [UV installation guide](https://docs.astral.sh/uv/getting-started/installation/)

### Step 2 – Get the project files

```bash
git clone <repository-url>
cd art-tactile-transform
```

### Step 3 – Install dependencies

```bash
uv sync --dev
```

### Step 4 – Configure the program

```bash
cp .env.example .env
```

Edit the `.env` file and configure:

#### Required Settings
- `MODEL_NAME` – Hugging Face depth model (e.g., `Intel/dpt-large`)
- `IMAGE_PATH` – Input image file path (PNG/JPG)
- `OUTPUT_PATH` – Output STL file path
- `RESOLUTION` – Target resolution for processing (default: 64)

#### Optional Advanced Settings
- `MIN_HEIGHT_MM` – Minimum tactile height in mm (default: 0.2)
- `MAX_HEIGHT_MM` – Maximum tactile height in mm (default: 2.0)
- `BASE_THICKNESS_MM` – Base plate thickness in mm (default: 1.0)
- `PIXEL_SCALE_MM` – Millimeters per pixel scaling (default: 0.2)
- `INVERT_HEIGHTS` – Invert depth mapping (default: false)
- `GAUSSIAN_BLUR_RADIUS` – Blur radius in pixels (default: 0)
- `CLAMP_MIN/MAX` – Grayscale value clamping (default: 0/255)
- `BORDER_PIXELS` – Add border around image (default: 0)
- `HF_API_TOKEN` – Hugging Face API token (optional)

## Usage

### GUI Mode (Recommended for Phase 1 MVP)

Launch the interactive Gradio interface:

```bash
uv run art-tactile-gui
```

This will start a web server at `http://localhost:7860` with:
- **Image upload**: Drag and drop portrait images
- **Real-time parameter adjustment**: Sliders for all processing parameters
- **3D preview**: Interactive orbit controls to inspect the model
- **STL export**: Download button for 3D printing

#### GUI Parameters:

**Physical Parameters:**
- Width (mm): 50-300, default 150
- Relief Depth (mm): 0.5-10, default 3
- Base Thickness (mm): 0.5-5, default 2

**Processing Parameters:**
- Smoothing: 0-10, default 2
- Resolution: 64-256 vertices, default 128

**Semantic Parameters (Portrait Mode):**
- Subject Emphasis (%): 0-200, default 120 (how much to raise faces)
- Background Suppression (%): 0-100, default 40 (how much to flatten background)
- Feature Sharpness (%): 0-100, default 70 (emphasis on eyes, nose, mouth)
- Edge Strength (%): 0-100, default 60 (edge detection intensity)

### Command Line (Original)

For depth estimation mode (legacy):
```bash
uv run art-tactile-transform
```

### As Library
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

### Install for Development
```bash
uv sync --dev
```

## Example Configuration

```env
MODEL_NAME=Intel/dpt-large
IMAGE_PATH=input/artwork.jpg
OUTPUT_PATH=output/tactile_model.stl
RESOLUTION=128
MIN_HEIGHT_MM=0.5
MAX_HEIGHT_MM=3.0
BASE_THICKNESS_MM=2.0
PIXEL_SCALE_MM=0.15
GAUSSIAN_BLUR_RADIUS=2
```

## Key Innovation: Semantic vs. Photographic Depth

**Traditional approach (depth estimation)**: Uses photographic perspective where distant objects appear "far away". For the Mona Lisa, this emphasizes the background landscape over her face.

**Our approach (semantic height mapping)**: Height represents IMPORTANCE for touch:
- **Faces = RAISED**: Primary subjects are elevated for tactile recognition
- **Features = HIGHEST**: Eyes, nose, mouth emphasized even more
- **Background = LOWERED**: Irrelevant areas suppressed for clarity
- **Edges = ENHANCED**: Boundaries sharpened for feature definition

This makes tactile representations actually useful for blind users, who need to feel the subject matter, not photographic depth.

## STL Output Features

- **Proper Surface Normals**: Correct lighting and 3D printing orientation
- **Physical Scaling**: Real-world dimensions in millimeters
- **Base Plate**: Stable foundation for 3D printing
- **Tactile Height Mapping**: Configurable relief depth for accessibility
- **Smooth Gradients**: Gaussian filtering for pleasant touch experience

## Troubleshooting

- **Missing dependencies**: Run `uv sync --dev`
- **API errors**: Check `HF_API_TOKEN` and network connection
- **File not found**: Verify `IMAGE_PATH` exists
- **STL issues**: Check output directory permissions

