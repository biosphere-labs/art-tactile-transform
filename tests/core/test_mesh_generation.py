"""Tests for mesh generation module."""

import numpy as np
import pytest

from art_tactile_transform.core.mesh_generation import calculate_normals, heightmap_to_stl


@pytest.mark.unit
def test_calculate_normals():
    """Test normal vector calculation for STL triangles."""
    normal = calculate_normals(0.0, 1.0, 0.5, 0.75, 0, 0, 0.2)

    assert len(normal) == 3
    assert all(isinstance(n, float) for n in normal)

    # Test that normal is unit length (or close to it)
    normal_array = np.array(normal)
    length = np.linalg.norm(normal_array)
    assert abs(length - 1.0) < 1e-6, f"Normal should be unit length, got {length}"


@pytest.mark.unit
def test_calculate_normals_edge_cases():
    """Test normal calculation edge cases."""
    # Test with identical heights (should give default normal)
    normal = calculate_normals(1.0, 1.0, 1.0, 1.0, 0, 0, 0.2)
    assert len(normal) == 3

    # Test with zero pixel scale
    normal = calculate_normals(0.0, 1.0, 0.5, 0.75, 0, 0, 0.0)
    assert len(normal) == 3


@pytest.mark.unit
def test_heightmap_to_stl_basic(sample_heightmap, tmp_path):
    """Test basic STL generation functionality."""
    output_file = tmp_path / "test.stl"

    heightmap_to_stl(
        sample_heightmap,
        str(output_file),
        min_height_mm=0.5,
        max_height_mm=2.0,
        base_thickness_mm=1.0,
        pixel_scale_mm=0.2,
    )

    assert output_file.exists()

    content = output_file.read_text()
    lines = content.strip().splitlines()

    # Check STL format
    assert lines[0] == "solid tactile_model"
    assert lines[-1] == "endsolid tactile_model"
    assert "facet normal" in content
    assert "vertex" in content


@pytest.mark.unit
def test_heightmap_to_stl_parameters(tmp_path):
    """Test STL generation with different parameters."""
    heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
    output = tmp_path / "enhanced.stl"

    heightmap_to_stl(
        heightmap,
        str(output),
        min_height_mm=0.1,
        max_height_mm=3.0,
        base_thickness_mm=2.0,
        pixel_scale_mm=0.5,
    )

    content = output.read_text()

    # Check for proper STL structure
    assert "solid tactile_model" in content
    assert "endsolid tactile_model" in content
    assert "vertex" in content
    assert "facet normal" in content

    # Check that base thickness appears in coordinates
    assert "2.000" in content  # base thickness should appear


@pytest.mark.unit
def test_heightmap_to_stl_triangle_count(sample_heightmap, tmp_path):
    """Test that STL generates expected number of triangles."""
    output_file = tmp_path / "triangles.stl"

    heightmap_to_stl(sample_heightmap, str(output_file))

    content = output_file.read_text()
    triangle_count = content.count("facet normal")

    height, width = sample_heightmap.shape
    # Each quad becomes 2 triangles, plus base triangles
    expected_surface_triangles = (height - 1) * (width - 1) * 2
    base_triangles = 2  # Simple base with 2 triangles

    assert triangle_count >= expected_surface_triangles
    assert (
        triangle_count <= expected_surface_triangles + base_triangles + 10
    )  # Allow some flexibility


@pytest.mark.unit
def test_heightmap_to_stl_invalid_input(tmp_path):
    """Test STL generation with invalid inputs."""
    output_file = tmp_path / "invalid.stl"

    # Test with empty heightmap
    with pytest.raises(ValueError, match="cannot be empty"):
        heightmap_to_stl(np.array([]), str(output_file))

    # Test with 1D heightmap
    with pytest.raises(ValueError, match="must be a 2D array"):
        heightmap_to_stl(np.array([1, 2, 3]), str(output_file))
