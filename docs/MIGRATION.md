# Migration Guide: v1.0 to v2.0

## Overview

Version 2.0 introduces a complete restructuring of the codebase to support GUI development while maintaining full backwards compatibility with the v1.0 CLI interface. This guide explains what has changed and how to update your code if needed.

## For CLI Users

### No Changes Required!

If you're using the CLI interface, **nothing needs to change**:

```bash
# Still works exactly as before
art-tactile-transform

# Or use the new explicit CLI command
art-tactile-cli
```

Your `.env` files and environment variables work exactly the same.

### Configuration

The same `.env` file format is supported:

```bash
MODEL_NAME=Intel/dpt-large
IMAGE_PATH=input.jpg
OUTPUT_PATH=output.stl
RESOLUTION=128
# ... all other parameters work as before
```

## For Python API Users

### Import Changes

If you were importing from `main.py`, update your imports:

#### Old Way (v1.0)
```python
from art_tactile_transform.main import generate_3d, heightmap_to_stl, process_image
```

#### New Way (v2.0)
```python
# Option 1: Import from specific modules
from art_tactile_transform.cli import generate_3d
from art_tactile_transform.core.mesh_generation import heightmap_to_stl
from art_tactile_transform.core.image_processing import process_image

# Option 2: Import from package root (recommended)
from art_tactile_transform import (
    generate_3d,
    heightmap_to_stl,
    process_image,
)
```

### Using the New Parameter System

v2.0 introduces type-safe parameter classes:

#### Old Way (v1.0)
```python
import os
os.environ['MIN_HEIGHT_MM'] = '0.5'
os.environ['MAX_HEIGHT_MM'] = '2.0'
# ... set many environment variables
generate_3d()
```

#### New Way (v2.0)
```python
from art_tactile_transform.models.parameters import PhysicalParams, ProcessingParams

# Create parameter objects
physical = PhysicalParams(
    width_mm=150.0,
    relief_depth_mm=3.0,
    base_thickness_mm=2.0
)

processing = ProcessingParams(
    resolution=128,
    smoothing=2.0,
    edge_strength=60.0
)

# Use in your code
# (Note: New API functions coming in v2.1 to use these directly)
```

### Using Presets

v2.0 introduces a preset system:

```python
from art_tactile_transform.models.presets import get_builtin_preset, list_builtin_presets

# List available presets
presets = list_builtin_presets()
for preset in presets:
    print(f"{preset['name']}: {preset['description']}")

# Load a preset
params = get_builtin_preset('portrait_high_detail')
print(f"Resolution: {params.processing.resolution}")
print(f"Width: {params.physical.width_mm}mm")
```

### Custom Preset Management

```python
from art_tactile_transform.models.presets import PresetManager
from art_tactile_transform.models.parameters import AllParams

manager = PresetManager()

# Create custom parameters
my_params = AllParams(
    physical=PhysicalParams(width_mm=200.0),
    processing=ProcessingParams(resolution=256)
)

# Save as preset
manager.save_preset(
    name="my_custom_preset",
    params=my_params,
    description="My custom settings for large prints"
)

# Load later
loaded = manager.load_preset("my_custom_preset")
```

## Module Structure Changes

### Before (v1.0)

```
src/art_tactile_transform/
├── __init__.py
└── main.py    # Everything in one file
```

### After (v2.0)

```
src/art_tactile_transform/
├── __init__.py
├── cli.py              # CLI entry point
├── gui.py              # GUI entry point (new!)
├── core/               # Core processing
│   ├── image_processing.py
│   ├── mesh_generation.py
│   └── validation.py
├── processing/         # Processing pipelines
│   ├── depth_estimation.py
│   └── semantic_mapping.py
├── models/             # Parameter models (new!)
│   ├── parameters.py
│   └── presets.py
└── utils/              # Utilities (new!)
    ├── file_handling.py
    └── logging.py
```

## Function Location Changes

| v1.0 Location | v2.0 Location | Notes |
|--------------|---------------|-------|
| `main.generate_3d()` | `cli.generate_3d()` | Also available from root |
| `main.query_depth_model()` | `processing.depth_estimation.query_depth_model()` | Moved to processing module |
| `main.heightmap_to_stl()` | `core.mesh_generation.heightmap_to_stl()` | Moved to core |
| `main.calculate_normals()` | `core.mesh_generation.calculate_normals()` | Moved to core |
| `main.process_image()` | `core.image_processing.process_image()` | Moved to core |
| N/A | `core.image_processing.resize_to_resolution()` | New function |
| N/A | `core.image_processing.image_to_heightmap()` | New function |
| N/A | `core.validation.validate_mesh()` | New function |

## New Features in v2.0

### 1. Type-Safe Parameters

```python
from art_tactile_transform.models.parameters import PhysicalParams

# Parameters with validation
params = PhysicalParams(
    width_mm=150.0,
    relief_depth_mm=3.0
)

# Automatic validation
try:
    bad_params = PhysicalParams(width_mm=-10)  # Raises ValueError
except ValueError as e:
    print(f"Invalid parameter: {e}")
```

### 2. Preset System

```python
from art_tactile_transform.models.presets import get_builtin_preset

# Use built-in presets
portrait_params = get_builtin_preset('portrait_high_detail')
landscape_params = get_builtin_preset('landscape_dramatic')
text_params = get_builtin_preset('text_maximum_legibility')
```

### 3. Improved File Handling

```python
from art_tactile_transform.utils.file_handling import (
    validate_image_file,
    load_image,
    get_output_filename
)

# Validate before processing
try:
    path = validate_image_file('input.jpg')
    image = load_image(path)
except FileNotFoundError:
    print("File not found")
except ValueError:
    print("Unsupported format")
```

### 4. Better Logging

```python
from art_tactile_transform.utils.logging import setup_logging, get_logger

# Configure logging
setup_logging(level='DEBUG', log_file='app.log')

# Use logger
logger = get_logger('my_module')
logger.info("Processing started")
```

### 5. Mesh Validation

```python
from art_tactile_transform.core.validation import validate_mesh

# Validate generated STL
results = validate_mesh('output.stl')
if results['valid']:
    print(f"Valid mesh with {results['triangle_count']} triangles")
else:
    print(f"Errors: {results['errors']}")
    print(f"Warnings: {results['warnings']}")
```

## Breaking Changes

### None for CLI Users

There are **no breaking changes** if you use the CLI interface.

### Minimal for Python API Users

1. **Import paths changed**: Update imports from `main.py` to new module locations
2. **Module reorganization**: Functions moved to more logical locations

### Compatibility Layer

The package root (`__init__.py`) re-exports all commonly used functions, so this works:

```python
# This works and will continue to work
from art_tactile_transform import generate_3d, heightmap_to_stl, process_image

# No need to know internal module structure
```

## Deprecation Timeline

- **v2.0**: `main.py` deprecated but still functional
- **v2.5**: `main.py` will show deprecation warnings
- **v3.0**: `main.py` will be removed

## Migration Checklist

### For CLI Users
- [ ] No changes needed!
- [ ] Optionally, try `art-tactile-cli` command

### For Python API Users
- [ ] Update imports from `main` to specific modules or package root
- [ ] Test your code with new imports
- [ ] Consider using new parameter classes for better type safety
- [ ] Explore preset system for common configurations

### For Developers
- [ ] Update test imports
- [ ] Use new modular structure for new features
- [ ] Follow architecture guidelines in `docs/ARCHITECTURE.md`
- [ ] Add tests to appropriate module directories

## Getting Help

- **Architecture Questions**: See `docs/ARCHITECTURE.md`
- **Feature Roadmap**: See `docs/prd/tactile-art-gui-v2.md`
- **Issues**: Open a GitHub issue
- **Examples**: Check `examples/` directory (coming soon)

## Example Migration

### Before (v1.0)

```python
import os
from art_tactile_transform.main import generate_3d

os.environ['MODEL_NAME'] = 'Intel/dpt-large'
os.environ['IMAGE_PATH'] = 'input.jpg'
os.environ['OUTPUT_PATH'] = 'output.stl'
os.environ['RESOLUTION'] = '128'

generate_3d()
```

### After (v2.0) - Option 1: No Changes

```python
# Exact same code works!
import os
from art_tactile_transform import generate_3d  # Import from root now

os.environ['MODEL_NAME'] = 'Intel/dpt-large'
os.environ['IMAGE_PATH'] = 'input.jpg'
os.environ['OUTPUT_PATH'] = 'output.stl'
os.environ['RESOLUTION'] = '128'

generate_3d()
```

### After (v2.0) - Option 2: Use New Features

```python
from art_tactile_transform.models.presets import get_builtin_preset
from art_tactile_transform.utils.file_handling import load_image
from art_tactile_transform.core.image_processing import (
    process_image,
    resize_to_resolution,
    image_to_heightmap
)
from art_tactile_transform.core.mesh_generation import heightmap_to_stl

# Load preset
params = get_builtin_preset('portrait_high_detail')

# Load and process image
image = load_image('input.jpg')
processed = process_image(
    image,
    gaussian_blur_radius=params.processing.gaussian_blur_radius,
    invert_heights=params.processing.invert_heights
)
resized = resize_to_resolution(processed, params.processing.resolution)
heightmap = image_to_heightmap(resized)

# Generate STL
heightmap_to_stl(
    heightmap,
    'output.stl',
    min_height_mm=params.physical.get_min_height_mm(),
    max_height_mm=params.physical.get_max_height_mm(),
    base_thickness_mm=params.physical.base_thickness_mm,
    pixel_scale_mm=params.physical.pixel_scale_mm
)
```

## Benefits of Migration

1. **Type Safety**: Parameter validation catches errors early
2. **Modularity**: Use only the components you need
3. **Testability**: Each module can be tested independently
4. **Maintainability**: Clear separation of concerns
5. **Extensibility**: Easy to add new processing modes
6. **GUI Ready**: Architecture supports upcoming GUI features

## Future-Proofing

The new architecture is designed to support:

- **Phase 1**: Gradio GUI with real-time preview
- **Phase 2**: Multiple processing modes (portrait, landscape, text, diagram)
- **Phase 3**: Advanced features (batch processing, plugins)
- **Phase 4**: Desktop application with offline support

By migrating to the new structure now, you'll be ready for these future enhancements!
