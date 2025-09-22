"""Tests for STL generation functionality."""

import re
from pathlib import Path

import numpy as np
import pytest

from art_tactile_transform.main import calculate_normals, heightmap_to_stl


@pytest.mark.unit
class TestSTLGeneration:
    """Test suite for STL generation functions."""

    def test_calculate_normals_basic(self):
        """Test basic normal vector calculation."""
        normal = calculate_normals(0.0, 1.0, 0.5, 0.75, 0, 0, 0.2)

        assert len(normal) == 3
        assert all(isinstance(n, float) for n in normal)

        # Check that normal is unit length
        normal_array = np.array(normal)
        length = np.linalg.norm(normal_array)
        assert abs(length - 1.0) < 1e-6

    def test_calculate_normals_flat_surface(self):
        """Test normal calculation for flat surfaces."""
        # All heights the same should give upward normal
        normal = calculate_normals(1.0, 1.0, 1.0, 1.0, 0, 0, 0.2)

        assert len(normal) == 3

        # For a flat surface, normal should point upward (positive Z)
        assert normal[2] > 0  # Z component should be positive

    def test_calculate_normals_edge_cases(self):
        """Test normal calculation edge cases."""
        # Test with zero pixel scale
        normal = calculate_normals(0.0, 1.0, 0.5, 0.75, 0, 0, 0.0)
        assert len(normal) == 3

        # Test with extreme height differences
        normal = calculate_normals(0.0, 100.0, 50.0, 75.0, 0, 0, 0.1)
        assert len(normal) == 3

        # Normal should still be unit length
        normal_array = np.array(normal)
        length = np.linalg.norm(normal_array)
        assert abs(length - 1.0) < 1e-6

    def test_heightmap_to_stl_file_creation(self, sample_heightmap, tmp_path):
        """Test that STL file is created successfully."""
        output_file = tmp_path / 'test.stl'

        heightmap_to_stl(sample_heightmap, str(output_file))

        assert output_file.exists()
        assert output_file.stat().st_size > 0

    def test_heightmap_to_stl_format_validation(self, sample_heightmap, tmp_path):
        """Test that generated STL has correct format."""
        output_file = tmp_path / 'format_test.stl'

        heightmap_to_stl(sample_heightmap, str(output_file))

        content = output_file.read_text()
        lines = content.strip().splitlines()

        # Check header and footer
        assert lines[0] == 'solid tactile_model'
        assert lines[-1] == 'endsolid tactile_model'

        # Check for required STL elements
        assert 'facet normal' in content
        assert 'outer loop' in content
        assert 'vertex' in content
        assert 'endloop' in content
        assert 'endfacet' in content

    def test_heightmap_to_stl_triangle_structure(self, sample_heightmap, tmp_path):
        """Test that triangles are properly structured."""
        output_file = tmp_path / 'triangle_test.stl'

        heightmap_to_stl(sample_heightmap, str(output_file))

        content = output_file.read_text()

        # Count facets and vertices
        facet_count = content.count('facet normal')
        vertex_count = content.count('vertex')

        # Each facet should have exactly 3 vertices
        assert vertex_count == facet_count * 3

        # Check loop structure
        outer_loop_count = content.count('outer loop')
        endloop_count = content.count('endloop')
        endfacet_count = content.count('endfacet')

        assert outer_loop_count == facet_count
        assert endloop_count == facet_count
        assert endfacet_count == facet_count

    def test_heightmap_to_stl_coordinate_scaling(self, tmp_path):
        """Test coordinate scaling in STL output."""
        # Create simple 2x2 heightmap
        heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
        output_file = tmp_path / 'scaling_test.stl'

        pixel_scale_mm = 0.5
        base_thickness_mm = 1.0
        min_height_mm = 0.1
        max_height_mm = 2.0

        heightmap_to_stl(
            heightmap,
            str(output_file),
            min_height_mm=min_height_mm,
            max_height_mm=max_height_mm,
            base_thickness_mm=base_thickness_mm,
            pixel_scale_mm=pixel_scale_mm
        )

        content = output_file.read_text()

        # Check that coordinates appear with expected scaling
        # Base thickness should appear in Z coordinates
        assert f'{base_thickness_mm:.3f}' in content

        # Check that X and Y coordinates use pixel scaling
        expected_x = 1 * pixel_scale_mm  # 1 pixel * scale
        assert f'{expected_x:.3f}' in content or f'{expected_x:.6f}' in content

    def test_heightmap_to_stl_height_mapping(self, tmp_path):
        """Test height value mapping to physical dimensions."""
        # Create heightmap with known values
        heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
        output_file = tmp_path / 'height_test.stl'

        min_height_mm = 0.5
        max_height_mm = 3.0
        base_thickness_mm = 1.0

        heightmap_to_stl(
            heightmap,
            str(output_file),
            min_height_mm=min_height_mm,
            max_height_mm=max_height_mm,
            base_thickness_mm=base_thickness_mm
        )

        content = output_file.read_text()

        # Calculate expected Z values
        height_range = max_height_mm - min_height_mm

        # For heightmap value 0.0: min_height + base_thickness
        expected_z_min = min_height_mm + base_thickness_mm

        # For heightmap value 1.0: max_height + base_thickness
        expected_z_max = max_height_mm + base_thickness_mm

        # Check that these values appear in the STL
        # Allow for floating point formatting variations
        min_found = any([
            f'{expected_z_min:.3f}' in content,
            f'{expected_z_min:.6f}' in content,
            f'{expected_z_min:.1f}' in content
        ])

        max_found = any([
            f'{expected_z_max:.3f}' in content,
            f'{expected_z_max:.6f}' in content,
            f'{expected_z_max:.1f}' in content
        ])

        assert min_found, f"Expected Z value {expected_z_min} not found in STL"
        assert max_found, f"Expected Z value {expected_z_max} not found in STL"

    def test_heightmap_to_stl_base_plate(self, sample_heightmap, tmp_path):
        """Test that base plate is included in STL."""
        output_file = tmp_path / 'base_test.stl'
        base_thickness = 1.5

        heightmap_to_stl(
            sample_heightmap,
            str(output_file),
            base_thickness_mm=base_thickness
        )

        content = output_file.read_text()

        # Base plate should have triangles at the base thickness Z level
        base_z_str = f'{base_thickness:.3f}'
        assert base_z_str in content

        # Should have downward-pointing normals for base
        assert 'facet normal 0.0 0.0 -1.0' in content or 'facet normal 0.000000 0.000000 -1.000000' in content

    def test_heightmap_to_stl_normal_vectors(self, sample_heightmap, tmp_path):
        """Test that normal vectors are properly formatted."""
        output_file = tmp_path / 'normals_test.stl'

        heightmap_to_stl(sample_heightmap, str(output_file))

        content = output_file.read_text()

        # Find all normal vectors
        normal_pattern = r'facet normal ([-+]?\d*\.?\d+) ([-+]?\d*\.?\d+) ([-+]?\d*\.?\d+)'
        normals = re.findall(normal_pattern, content)

        assert len(normals) > 0, "No normal vectors found"

        for normal_str in normals:
            # Convert to floats and check unit length
            nx, ny, nz = map(float, normal_str)
            length = (nx**2 + ny**2 + nz**2)**0.5

            # Normal should be unit length (allow small floating point errors)
            assert abs(length - 1.0) < 1e-3, f"Normal {normal_str} is not unit length: {length}"

    def test_heightmap_to_stl_triangle_count(self, tmp_path):
        """Test expected number of triangles for known heightmap size."""
        # Create 3x3 heightmap
        heightmap = np.ones((3, 3))
        output_file = tmp_path / 'count_test.stl'

        heightmap_to_stl(heightmap, str(output_file))

        content = output_file.read_text()
        triangle_count = content.count('facet normal')

        # For 3x3 heightmap: (3-1) * (3-1) * 2 = 8 surface triangles
        # Plus base triangles (at least 2)
        expected_surface_triangles = 2 * 2 * 2  # 8
        expected_min_total = expected_surface_triangles + 2  # At least 10

        assert triangle_count >= expected_min_total

    @pytest.mark.parametrize("size", [(2, 2), (3, 3), (4, 4), (5, 5)])
    def test_heightmap_to_stl_different_sizes(self, tmp_path, size):
        """Test STL generation with different heightmap sizes."""
        heightmap = np.random.rand(*size)
        output_file = tmp_path / f'size_test_{size[0]}x{size[1]}.stl'

        heightmap_to_stl(heightmap, str(output_file))

        assert output_file.exists()

        content = output_file.read_text()

        # Should have valid STL structure
        assert content.startswith('solid tactile_model')
        assert content.strip().endswith('endsolid tactile_model')
        assert 'facet normal' in content

    def test_heightmap_to_stl_extreme_values(self, tmp_path):
        """Test STL generation with extreme parameter values."""
        heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
        output_file = tmp_path / 'extreme_test.stl'

        # Test with extreme but valid values
        heightmap_to_stl(
            heightmap,
            str(output_file),
            min_height_mm=0.01,
            max_height_mm=100.0,
            base_thickness_mm=0.1,
            pixel_scale_mm=10.0
        )

        assert output_file.exists()

        content = output_file.read_text()
        assert 'solid tactile_model' in content
        assert 'vertex' in content

    def test_heightmap_to_stl_output_path_creation(self, sample_heightmap, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        # Create nested directory path
        nested_dir = tmp_path / 'nested' / 'directory'
        output_file = nested_dir / 'test.stl'

        # Directory doesn't exist yet
        assert not nested_dir.exists()

        heightmap_to_stl(sample_heightmap, str(output_file))

        # Directory should be created and file should exist
        assert output_file.exists()
        assert nested_dir.exists()