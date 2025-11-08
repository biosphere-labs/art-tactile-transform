"""Art Tactile Transform - Convert 2D images to 3D tactile models."""

__version__ = "0.1.0"

from .main import generate_3d, query_depth_model, heightmap_to_stl

__all__ = ["generate_3d", "query_depth_model", "heightmap_to_stl"]