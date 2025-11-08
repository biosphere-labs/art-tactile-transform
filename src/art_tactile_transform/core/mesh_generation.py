"""3D mesh generation from heightmaps."""

from pathlib import Path
from typing import Tuple

import numpy as np


def calculate_normals(
    z00: float, z10: float, z01: float, z11: float, i: int, j: int, pixel_scale: float
) -> Tuple[float, float, float]:
    """Calculate proper surface normals for STL triangles.

    Args:
        z00: Height at position (i, j)
        z10: Height at position (i+1, j)
        z01: Height at position (i, j+1)
        z11: Height at position (i+1, j+1)
        i: Row index
        j: Column index
        pixel_scale: Physical scale per pixel in mm

    Returns:
        Tuple of (nx, ny, nz) representing the unit normal vector
    """
    # Create vectors for the triangle surface
    v1 = np.array([pixel_scale, 0.0, z10 - z00])
    v2 = np.array([0.0, pixel_scale, z01 - z00])

    # Cross product gives normal vector
    normal = np.cross(v1, v2)
    length = np.linalg.norm(normal)

    if length > 0:
        normal = normal / length
    else:
        normal = np.array([0.0, 0.0, 1.0])

    return tuple(normal)


def heightmap_to_stl(
    heightmap: np.ndarray,
    output_path: str,
    min_height_mm: float = 0.2,
    max_height_mm: float = 2.0,
    base_thickness_mm: float = 1.0,
    pixel_scale_mm: float = 0.2,
) -> None:
    """Save an enhanced ASCII STL derived from the heightmap with proper scaling.

    Args:
        heightmap: 2D numpy array with normalized heights (0.0-1.0)
        output_path: Path to save the STL file
        min_height_mm: Minimum height in millimeters
        max_height_mm: Maximum height in millimeters
        base_thickness_mm: Thickness of the base plate in millimeters
        pixel_scale_mm: Physical scale per pixel in millimeters

    Raises:
        ValueError: If heightmap is invalid
        IOError: If file cannot be written
    """
    if heightmap.size == 0:
        raise ValueError("Heightmap cannot be empty")

    if heightmap.ndim != 2:
        raise ValueError("Heightmap must be a 2D array")

    height, width = heightmap.shape

    # Normalize heightmap to physical dimensions
    normalized_heights = (
        heightmap * (max_height_mm - min_height_mm) + min_height_mm + base_thickness_mm
    )

    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("solid tactile_model\n")

        # Generate top surface triangles
        for i in range(height - 1):
            for j in range(width - 1):
                z00 = normalized_heights[i, j]
                z10 = normalized_heights[i + 1, j]
                z01 = normalized_heights[i, j + 1]
                z11 = normalized_heights[i + 1, j + 1]

                x0, x1 = i * pixel_scale_mm, (i + 1) * pixel_scale_mm
                y0, y1 = j * pixel_scale_mm, (j + 1) * pixel_scale_mm

                # First triangle
                normal = calculate_normals(z00, z10, z01, z11, i, j, pixel_scale_mm)
                f.write(
                    f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n"
                )
                f.write("    outer loop\n")
                f.write(f"      vertex {x0:.3f} {y0:.3f} {z00:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y0:.3f} {z10:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y1:.3f} {z11:.3f}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")

                # Second triangle
                f.write(
                    f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n"
                )
                f.write("    outer loop\n")
                f.write(f"      vertex {x0:.3f} {y0:.3f} {z00:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y1:.3f} {z11:.3f}\n")
                f.write(f"      vertex {x0:.3f} {y1:.3f} {z01:.3f}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")

        # Add base plate (bottom surface)
        max_x = (height - 1) * pixel_scale_mm
        max_y = (width - 1) * pixel_scale_mm
        base_z = base_thickness_mm

        # Base rectangle (two triangles)
        f.write("  facet normal 0.0 0.0 -1.0\n")
        f.write("    outer loop\n")
        f.write(f"      vertex 0.0 0.0 {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} {max_y:.3f} {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} 0.0 {base_z:.3f}\n")
        f.write("    endloop\n")
        f.write("  endfacet\n")

        f.write("  facet normal 0.0 0.0 -1.0\n")
        f.write("    outer loop\n")
        f.write(f"      vertex 0.0 0.0 {base_z:.3f}\n")
        f.write(f"      vertex 0.0 {max_y:.3f} {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} {max_y:.3f} {base_z:.3f}\n")
        f.write("    endloop\n")
        f.write("  endfacet\n")

        f.write("endsolid tactile_model\n")
