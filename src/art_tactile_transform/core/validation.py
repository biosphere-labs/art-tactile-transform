"""Mesh validation and quality checks."""

from pathlib import Path
from typing import Dict, List, Optional


def validate_mesh(stl_path: str) -> Dict[str, any]:
    """Validate an STL file for common issues.

    Args:
        stl_path: Path to the STL file

    Returns:
        Dictionary containing validation results:
        - valid: bool
        - errors: List of error messages
        - warnings: List of warning messages
        - triangle_count: Number of triangles
        - file_size: File size in bytes

    Raises:
        FileNotFoundError: If STL file doesn't exist
    """
    path = Path(stl_path)
    if not path.exists():
        raise FileNotFoundError(f"STL file not found: {stl_path}")

    errors: List[str] = []
    warnings: List[str] = []
    triangle_count = 0

    try:
        with open(stl_path, "r", encoding="utf-8") as f:
            content = f.read()

            # Check for valid STL format
            if not content.startswith("solid"):
                errors.append("Invalid STL format: must start with 'solid'")

            if not content.rstrip().endswith("endsolid tactile_model"):
                warnings.append("STL file may be incomplete")

            # Count triangles
            triangle_count = content.count("facet normal")

            if triangle_count == 0:
                errors.append("No triangles found in STL file")

            # Check for basic completeness
            vertex_count = content.count("vertex")
            expected_vertices = triangle_count * 3

            if vertex_count != expected_vertices:
                warnings.append(
                    f"Vertex count mismatch: found {vertex_count}, expected {expected_vertices}"
                )

    except Exception as e:
        errors.append(f"Error reading STL file: {e}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "triangle_count": triangle_count,
        "file_size": path.stat().st_size if path.exists() else 0,
    }
