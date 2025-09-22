# Art Tactile Transform

This project transforms flat images into 3D printable tactile representations using AI depth estimation models from Hugging Face. It generates properly scaled STL files with enhanced tactile features for accessibility and 3D printing.

## Features

- **AI-Powered Depth Estimation**: Uses Hugging Face models (e.g., Intel/dpt-large) for accurate depth mapping
- **Advanced Image Processing**: Gaussian blur, clamping, border addition, and height inversion
- **Physical Scaling**: Configurable dimensions in millimeters for real-world 3D printing
- **Enhanced STL Generation**: Proper surface normals, base plates, and physical scaling
- **Poetry Project**: Modern Python packaging with dependency management

## Requirements

- **Python 3.13** or later
- **Poetry** for dependency management

## Installation

### Step 1 – Install Python and Poetry

1. Visit <https://www.python.org/downloads/> and install **Python 3.13+**
2. Install Poetry: `pip install poetry` or follow [Poetry installation guide](https://python-poetry.org/docs/#installation)

### Step 2 – Get the project files

```bash
git clone <repository-url>
cd art-tactile-transform
```

### Step 3 – Install dependencies

```bash
poetry install
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

### Command Line
```bash
poetry run art-tactile-transform
```

### Python Script
```bash
poetry run python -m art_tactile_transform.main
```

### As Library
```python
from art_tactile_transform import generate_3d
output_file = generate_3d()
```

## Development

### Run Tests
```bash
poetry run pytest
```

### Code Quality
```bash
poetry run black .
poetry run ruff check .
poetry run mypy .
```

### Install for Development
```bash
poetry install --with dev
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

## STL Output Features

- **Proper Surface Normals**: Correct lighting and 3D printing orientation
- **Physical Scaling**: Real-world dimensions in millimeters
- **Base Plate**: Stable foundation for 3D printing
- **Tactile Height Mapping**: Configurable relief depth for accessibility

## Troubleshooting

- **Missing dependencies**: Run `poetry install`
- **API errors**: Check `HF_API_TOKEN` and network connection
- **File not found**: Verify `IMAGE_PATH` exists
- **STL issues**: Check output directory permissions

