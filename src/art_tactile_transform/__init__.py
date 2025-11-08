"""Art Tactile Transform - Convert 2D images to 3D tactile models."""

__version__ = "0.1.0"

# Core processing
from .core.image_processing import (
    image_to_heightmap,
    process_image,
    resize_to_resolution,
)
from .core.mesh_generation import calculate_normals, heightmap_to_stl
from .core.validation import validate_mesh

# Processing pipelines
from .processing.depth_estimation import query_depth_model
from .processing.semantic_mapping import semantic_height_mapping

# Parameter models
from .models.parameters import (
    AllParams,
    PhysicalParams,
    ProcessingParams,
    SemanticParams,
)
from .models.presets import (
    PresetManager,
    get_builtin_preset,
    list_builtin_presets,
)

# Utilities
from .utils.file_handling import (
    ensure_output_dir,
    get_output_filename,
    load_image,
    validate_image_file,
)
from .utils.logging import get_logger, setup_logging

# CLI function for backwards compatibility
from .cli import generate_3d

__all__ = [
    # Core
    "process_image",
    "resize_to_resolution",
    "image_to_heightmap",
    "heightmap_to_stl",
    "calculate_normals",
    "validate_mesh",
    # Processing
    "query_depth_model",
    "semantic_height_mapping",
    # Parameters
    "PhysicalParams",
    "ProcessingParams",
    "SemanticParams",
    "AllParams",
    # Presets
    "PresetManager",
    "get_builtin_preset",
    "list_builtin_presets",
    # Utilities
    "validate_image_file",
    "ensure_output_dir",
    "get_output_filename",
    "load_image",
    "setup_logging",
    "get_logger",
    # CLI
    "generate_3d",
]