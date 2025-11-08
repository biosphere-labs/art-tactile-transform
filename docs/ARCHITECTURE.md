# Architecture Documentation

## Overview

Art Tactile Transform has been restructured to support professional GUI application development while maintaining backwards compatibility with the CLI interface. The new architecture separates concerns into modular components that can be used independently or composed together.

## Directory Structure

```
src/art_tactile_transform/
├── __init__.py              # Public API exports
├── cli.py                   # CLI entry point (backwards compatible)
├── gui.py                   # GUI entry point (placeholder for v2.0)
├── main.py                  # Legacy file (deprecated, use cli.py)
│
├── core/                    # Core processing modules
│   ├── __init__.py
│   ├── image_processing.py  # Image preprocessing and manipulation
│   ├── mesh_generation.py   # STL file generation from heightmaps
│   └── validation.py        # Mesh validation and quality checks
│
├── processing/              # Image processing pipelines
│   ├── __init__.py
│   ├── depth_estimation.py  # Legacy depth-based method
│   └── semantic_mapping.py  # Future semantic-based methods
│
├── models/                  # Data models and parameters
│   ├── __init__.py
│   ├── parameters.py        # Parameter dataclasses
│   └── presets.py          # Preset management system
│
└── utils/                   # Utility modules
    ├── __init__.py
    ├── file_handling.py    # File operations and validation
    └── logging.py          # Logging configuration
```

## Module Responsibilities

### Core Modules (`core/`)

#### `image_processing.py`
- **Purpose**: Image preprocessing and manipulation
- **Key Functions**:
  - `process_image()`: Apply blur, clamping, inversion
  - `resize_to_resolution()`: Intelligent image resizing
  - `image_to_heightmap()`: Convert grayscale image to normalized heightmap
- **Dependencies**: PIL, NumPy

#### `mesh_generation.py`
- **Purpose**: Generate 3D meshes from heightmaps
- **Key Functions**:
  - `heightmap_to_stl()`: Create STL file from heightmap
  - `calculate_normals()`: Compute surface normals for triangles
- **Output**: ASCII STL format with proper normals and base plate
- **Dependencies**: NumPy

#### `validation.py`
- **Purpose**: Validate mesh quality and detect issues
- **Key Functions**:
  - `validate_mesh()`: Check for common STL problems
- **Checks**: Triangle count, vertex count, file format
- **Dependencies**: None (pure Python)

### Processing Modules (`processing/`)

#### `depth_estimation.py`
- **Purpose**: Legacy depth estimation using transformer models
- **Key Functions**:
  - `query_depth_model()`: Use Hugging Face transformers for depth
- **Note**: This is the v1.0 approach, will be supplemented by semantic methods
- **Dependencies**: transformers, torch, PIL

#### `semantic_mapping.py`
- **Purpose**: Future semantic-based height mapping (placeholder)
- **Planned Features**:
  - Face detection for portraits
  - Object segmentation for landscapes
  - OCR for text
  - Edge detection for diagrams
- **Dependencies**: TBD (MediaPipe, SAM, pytesseract)

### Model Modules (`models/`)

#### `parameters.py`
- **Purpose**: Type-safe parameter management
- **Classes**:
  - `PhysicalParams`: Physical dimensions (width, height, thickness, etc.)
  - `ProcessingParams`: Image processing settings
  - `SemanticParams`: Semantic processing settings (for v2.0)
  - `AllParams`: Container for all parameter types
- **Benefits**: Type checking, validation, serialization
- **Dependencies**: dataclasses

#### `presets.py`
- **Purpose**: Manage parameter presets
- **Built-in Presets**:
  - Portrait - High Detail
  - Portrait - Simple
  - Landscape - Dramatic
  - Text - Maximum Legibility
  - Diagram - Technical
  - Art - Impressionist
- **Features**:
  - Load/save custom presets
  - JSON-based storage
  - Preset discovery
- **Dependencies**: json, pathlib

### Utility Modules (`utils/`)

#### `file_handling.py`
- **Purpose**: File operations and validation
- **Key Functions**:
  - `validate_image_file()`: Check file exists and format supported
  - `ensure_output_dir()`: Create output directories
  - `get_output_filename()`: Generate output filenames
  - `list_image_files()`: Find all images in a directory
  - `load_image()`: Safe image loading
- **Dependencies**: PIL, pathlib

#### `logging.py`
- **Purpose**: Centralized logging configuration
- **Key Functions**:
  - `setup_logging()`: Configure loggers
  - `get_logger()`: Get module-specific logger
- **Classes**:
  - `ProgressLogger`: Track progress for long operations
- **Dependencies**: logging

## Entry Points

### CLI (`cli.py`)
- **Command**: `art-tactile-cli` (or `art-tactile-transform` for backwards compatibility)
- **Purpose**: Command-line interface using environment variables
- **Configuration**: `.env` file or environment variables
- **Backwards Compatible**: Yes, maintains original `generate_3d()` function
- **Use Case**: Batch processing, scripting, automation

### GUI (`gui.py`)
- **Command**: `art-tactile-gui`
- **Purpose**: Interactive graphical interface (Phase 1 implementation)
- **Status**: Placeholder (coming in v2.0)
- **Planned Features**:
  - Real-time parameter adjustment
  - 3D preview with orbit controls
  - Multiple processing modes
  - Preset management
- **Framework**: Gradio (Phase 1), Electron + Three.js (Phase 2)

## Data Flow

### CLI Processing Pipeline

```
1. Load .env configuration
   ↓
2. Validate input file
   ↓
3. Load image (utils.file_handling)
   ↓
4. Run depth estimation (processing.depth_estimation)
   ↓
5. Process image (core.image_processing)
   ↓
6. Resize to target resolution
   ↓
7. Convert to heightmap
   ↓
8. Generate STL mesh (core.mesh_generation)
   ↓
9. Save to file
   ↓
10. Validate output (optional)
```

### Future GUI Pipeline (v2.0)

```
1. User uploads image
   ↓
2. Select processing mode (portrait/landscape/text/diagram)
   ↓
3. Apply mode-specific processing (processing.semantic_mapping)
   ↓
4. Real-time parameter adjustment
   ├─> Update 3D preview
   └─> Regenerate heightmap
   ↓
5. Export STL when satisfied
```

## Backwards Compatibility

### V1.0 Compatibility
- Original `generate_3d()` function available in `cli.py`
- Same environment variable names
- Same `.env` file format
- Original command `art-tactile-transform` still works

### Migration Path
- Old import: `from art_tactile_transform.main import generate_3d`
- New import: `from art_tactile_transform.cli import generate_3d`
- Or use: `from art_tactile_transform import generate_3d` (works with both)

### Breaking Changes
None for CLI users. The `main.py` file is deprecated but still exists for compatibility.

## Extension Points

### Adding New Processing Modes
1. Add mode logic to `processing/semantic_mapping.py`
2. Create preset in `models/presets.py`
3. Add parameters to `SemanticParams` if needed
4. Update GUI to expose mode selection

### Adding New Export Formats
1. Create new module in `core/` (e.g., `obj_generation.py`)
2. Implement format-specific writer
3. Add to CLI/GUI export options

### Custom Preprocessing
1. Extend `core/image_processing.py` with new functions
2. Add parameters to `ProcessingParams`
3. Wire into processing pipeline

## Testing Architecture

### Test Organization
```
tests/
├── core/              # Tests for core modules
│   ├── test_image_processing.py
│   └── test_mesh_generation.py
├── processing/        # Tests for processing modules
├── models/            # Tests for parameter/preset models
├── utils/             # Tests for utilities
└── test_cli.py        # Integration tests for CLI
```

### Test Categories
- **Unit tests**: Individual function testing
- **Integration tests**: Full pipeline testing
- **API tests**: External API mocking
- **Slow tests**: Performance/long-running tests

## Dependencies

### Core Dependencies
- `numpy`: Numerical operations, heightmaps
- `pillow`: Image loading and manipulation
- `transformers`: Depth estimation models
- `torch`: Deep learning backend
- `python-dotenv`: Environment configuration
- `scipy`: Image processing operations

### Optional Dependencies
- `gradio`: GUI framework (Phase 1)
- Development tools: pytest, black, ruff, mypy

## Performance Considerations

### Current Performance
- Small images (512×512): ~5-10 seconds
- Medium images (1024×1024): ~15-30 seconds
- Large images (2048×2048): ~45-90 seconds

### Optimization Opportunities
1. **Caching**: Cache depth model in memory
2. **Progressive rendering**: Low-res preview, high-res final
3. **Parallel processing**: Batch processing multiple images
4. **GPU acceleration**: Use CUDA for depth estimation

## Future Enhancements

See `docs/prd/tactile-art-gui-v2.md` for complete roadmap.

### Phase 1 (MVP)
- Gradio-based GUI
- Portrait mode with face detection
- Basic parameter controls
- 3D preview

### Phase 2 (Multi-Mode)
- Landscape, text, diagram modes
- Semantic segmentation
- Advanced parameters
- Mode auto-detection

### Phase 3 (Polish)
- Enhanced 3D viewer
- Preset system
- Batch processing
- Quality validation

### Phase 4 (Production)
- Electron desktop app
- Offline functionality
- Installer packages
- Plugin system
