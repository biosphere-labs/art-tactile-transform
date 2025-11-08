# Art Tactile Transform

Transform flat images into 3D printable tactile representations using AI depth estimation. Generate properly scaled STL files for accessibility, education, and artistic expression.

## Version 2.0 - Restructured Architecture

This version introduces a modular architecture designed to support GUI development while maintaining full backwards compatibility with the CLI interface.

## Features

### Current (v2.0)
- **AI-Powered Depth Estimation**: Uses Hugging Face transformers (e.g., Intel/dpt-large)
- **Advanced Image Processing**: Blur, clamping, borders, height inversion
- **Physical Scaling**: Real-world dimensions in millimeters
- **Enhanced STL Generation**: Proper normals, base plates, validation
- **Modular Architecture**: Separate core, processing, and utility modules
- **Parameter System**: Type-safe parameter classes with validation
- **Preset System**: Built-in presets for common use cases
- **Dual Entry Points**: CLI and GUI interfaces

### Coming Soon (v2.1+)
- **Interactive GUI**: Real-time parameter adjustment with 3D preview
- **Multiple Processing Modes**: Portrait, landscape, text, diagram modes
- **Semantic Height Mapping**: Subject-aware height assignment
- **Batch Processing**: Process multiple images efficiently

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

### Command Line Interface

```bash
# Using the CLI command
uv run art-tactile-cli

# Or the backwards-compatible command
uv run art-tactile-transform
```

### GUI Interface (Coming Soon)

```bash
# Launch the GUI (Phase 1 implementation in progress)
uv run art-tactile-gui
```

### Python API - Basic Usage

```python
# Backwards compatible - works exactly as before
from art_tactile_transform import generate_3d

output_file = generate_3d()
print(f"Generated: {output_file}")
```

### Python API - New Modular Approach

```python
from art_tactile_transform import (
    load_image,
    process_image,
    resize_to_resolution,
    image_to_heightmap,
    heightmap_to_stl,
)

# Load and process image
image = load_image('input.jpg')
processed = process_image(image, gaussian_blur_radius=2)
resized = resize_to_resolution(processed, 128)
heightmap = image_to_heightmap(resized)

# Generate STL
heightmap_to_stl(
    heightmap,
    'output.stl',
    min_height_mm=0.5,
    max_height_mm=3.0,
    base_thickness_mm=2.0,
    pixel_scale_mm=0.2
)
```

### Using Presets

```python
from art_tactile_transform.models.presets import (
    get_builtin_preset,
    list_builtin_presets
)

# List available presets
presets = list_builtin_presets()
for preset in presets:
    print(f"{preset['name']}: {preset['description']}")

# Load a preset
params = get_builtin_preset('portrait_high_detail')
print(f"Resolution: {params.processing.resolution}")
print(f"Width: {params.physical.width_mm}mm")
```

### Available Built-in Presets

- **Portrait - High Detail**: Fine facial features with strong detail emphasis
- **Portrait - Simple**: Basic face shape with gentle features
- **Landscape - Dramatic**: Strong foreground/background contrast
- **Text - Maximum Legibility**: Very sharp, high relief for text
- **Diagram - Technical**: Sharp edges and flat regions
- **Art - Impressionist**: Soft, flowing features for artistic works

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

## STL Output Features

- **Proper Surface Normals**: Correct lighting and 3D printing orientation
- **Physical Scaling**: Real-world dimensions in millimeters
- **Base Plate**: Stable foundation for 3D printing
- **Tactile Height Mapping**: Configurable relief depth for accessibility

## Project Structure

```
src/art_tactile_transform/
├── cli.py                    # CLI entry point
├── gui.py                    # GUI entry point (placeholder)
├── core/                     # Core processing modules
│   ├── image_processing.py   # Image preprocessing
│   ├── mesh_generation.py    # STL generation
│   └── validation.py         # Mesh validation
├── processing/               # Processing pipelines
│   ├── depth_estimation.py   # Depth-based processing
│   └── semantic_mapping.py   # Semantic-based (future)
├── models/                   # Parameter management
│   ├── parameters.py         # Parameter classes
│   └── presets.py           # Preset system
└── utils/                    # Utilities
    ├── file_handling.py      # File operations
    └── logging.py            # Logging configuration
```

## Documentation

- **[Architecture Guide](docs/ARCHITECTURE.md)**: Detailed architecture documentation
- **[Migration Guide](docs/MIGRATION.md)**: Migrating from v1.0 to v2.0
- **[PRD](docs/prd/tactile-art-gui-v2.md)**: Product roadmap and future features
- **[Example Config](config/example.env)**: Configuration file example

## Backwards Compatibility

Version 2.0 maintains **full backwards compatibility**:
- All v1.0 CLI commands work unchanged
- Same `.env` configuration format
- Original Python API imports still supported
- No breaking changes for existing users

See [MIGRATION.md](docs/MIGRATION.md) for details.

## Troubleshooting

- **Missing dependencies**: Run `uv sync --dev`
- **Import errors**: Make sure you're using Python 3.13+
- **API errors**: Check `HF_API_TOKEN` and network connection
- **File not found**: Verify `IMAGE_PATH` exists
- **STL issues**: Check output directory permissions

## Contributing

See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for development guidelines.

## License

[Add license information]

## Acknowledgments

- Depth estimation models from [Hugging Face Transformers](https://huggingface.co/models)
- Built with modern Python packaging using [UV](https://docs.astral.sh/uv/)

