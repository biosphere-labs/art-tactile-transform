"""Tests for the main art_tactile_transform functionality."""

from io import BytesIO
from pathlib import Path
from unittest.mock import Mock

import numpy as np
import pytest
from PIL import Image

from art_tactile_transform.main import (
    calculate_normals,
    generate_3d,
    heightmap_to_stl,
    process_image,
    query_hf_api,
)


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
def test_process_image_basic(sample_image):
    """Test basic image processing functionality."""
    # Test basic processing
    processed = process_image(sample_image)
    assert processed.mode == 'L'
    assert processed.size == sample_image.size


@pytest.mark.unit
def test_process_image_with_border(sample_image):
    """Test image processing with border addition."""
    processed_border = process_image(sample_image, border_pixels=5)
    original_width, original_height = sample_image.size
    new_width, new_height = processed_border.size

    assert new_width == original_width + 10  # 5 pixels on each side
    assert new_height == original_height + 10


@pytest.mark.unit
def test_process_image_inversion(sample_image):
    """Test image processing with height inversion."""
    processed_normal = process_image(sample_image, invert_heights=False)
    processed_inverted = process_image(sample_image, invert_heights=True)

    assert processed_normal.mode == 'L'
    assert processed_inverted.mode == 'L'
    assert processed_normal.size == processed_inverted.size

    # Check that inversion actually changes the image
    normal_array = np.array(processed_normal)
    inverted_array = np.array(processed_inverted)
    assert not np.array_equal(normal_array, inverted_array)


@pytest.mark.unit
def test_process_image_gaussian_blur(sample_grayscale_image):
    """Test image processing with Gaussian blur."""
    # Test without blur
    processed_sharp = process_image(sample_grayscale_image, gaussian_blur_radius=0)

    # Test with blur
    processed_blurred = process_image(sample_grayscale_image, gaussian_blur_radius=3)

    assert processed_sharp.size == processed_blurred.size

    # Blurred image should be different from original
    sharp_array = np.array(processed_sharp)
    blurred_array = np.array(processed_blurred)
    assert not np.array_equal(sharp_array, blurred_array)


@pytest.mark.unit
def test_process_image_clamping(sample_grayscale_image):
    """Test image processing with value clamping."""
    processed = process_image(
        sample_grayscale_image,
        clamp_min=50,
        clamp_max=200
    )

    # Check that all values are within the clamped range after normalization
    processed_array = np.array(processed)
    # Values should be normalized to 0-255 after clamping
    assert processed_array.min() >= 0
    assert processed_array.max() <= 255


@pytest.mark.unit
def test_heightmap_to_stl_basic(sample_heightmap, tmp_path):
    """Test basic STL generation functionality."""
    output_file = tmp_path / 'test.stl'

    heightmap_to_stl(
        sample_heightmap,
        str(output_file),
        min_height_mm=0.5,
        max_height_mm=2.0,
        base_thickness_mm=1.0,
        pixel_scale_mm=0.2
    )

    assert output_file.exists()

    content = output_file.read_text()
    lines = content.strip().splitlines()

    # Check STL format
    assert lines[0] == 'solid tactile_model'
    assert lines[-1] == 'endsolid tactile_model'
    assert 'facet normal' in content
    assert 'vertex' in content


@pytest.mark.unit
def test_heightmap_to_stl_parameters(tmp_path):
    """Test STL generation with different parameters."""
    heightmap = np.array([[0.0, 1.0], [0.5, 0.25]])
    output = tmp_path / 'enhanced.stl'

    heightmap_to_stl(
        heightmap,
        str(output),
        min_height_mm=0.1,
        max_height_mm=3.0,
        base_thickness_mm=2.0,
        pixel_scale_mm=0.5
    )

    content = output.read_text()

    # Check for proper STL structure
    assert 'solid tactile_model' in content
    assert 'endsolid tactile_model' in content
    assert 'vertex' in content
    assert 'facet normal' in content

    # Check that base thickness appears in coordinates
    assert '2.000' in content  # base thickness should appear


@pytest.mark.unit
def test_heightmap_to_stl_triangle_count(sample_heightmap, tmp_path):
    """Test that STL generates expected number of triangles."""
    output_file = tmp_path / 'triangles.stl'

    heightmap_to_stl(sample_heightmap, str(output_file))

    content = output_file.read_text()
    triangle_count = content.count('facet normal')

    height, width = sample_heightmap.shape
    # Each quad becomes 2 triangles, plus base triangles
    expected_surface_triangles = (height - 1) * (width - 1) * 2
    base_triangles = 2  # Simple base with 2 triangles

    assert triangle_count >= expected_surface_triangles
    assert triangle_count <= expected_surface_triangles + base_triangles + 10  # Allow some flexibility


@pytest.mark.api
def test_query_hf_api_with_timeout(monkeypatch, mock_hf_api_response):
    """Test API query with timeout handling."""
    from conftest import MockResponse

    def fake_post(url, headers=None, data=None, timeout=None):
        assert timeout == 30
        assert 'test-model' in url
        return MockResponse(mock_hf_api_response)

    monkeypatch.setattr('art_tactile_transform.main.requests.post', fake_post)
    result = query_hf_api(b'image_data', 'test-model', 'token123')
    assert result == mock_hf_api_response


@pytest.mark.api
def test_query_hf_api_error_handling(monkeypatch):
    """Test API error handling."""
    def failing_post(*args, **kwargs):
        raise Exception("Network error")

    monkeypatch.setattr('art_tactile_transform.main.requests.post', failing_post)

    with pytest.raises(RuntimeError, match="Failed to query Hugging Face API"):
        query_hf_api(b'image_data', 'test-model')


@pytest.mark.api
def test_query_hf_api_with_headers(monkeypatch, mock_hf_api_response):
    """Test API query with authentication headers."""
    from conftest import MockResponse

    captured_headers = {}

    def fake_post(url, headers=None, data=None, timeout=None):
        captured_headers.update(headers or {})
        return MockResponse(mock_hf_api_response)

    monkeypatch.setattr('art_tactile_transform.main.requests.post', fake_post)
    result = query_hf_api(b'image_data', 'test-model', 'test-token')

    assert 'Authorization' in captured_headers
    assert captured_headers['Authorization'] == 'Bearer test-token'
    assert result == mock_hf_api_response


@pytest.mark.requires_env
def test_generate_3d_missing_env(monkeypatch):
    """Test generate_3d with missing environment variables."""
    # Clear all environment variables
    for var in ['MODEL_NAME', 'IMAGE_PATH', 'OUTPUT_PATH']:
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(ValueError, match="MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set"):
        generate_3d()


@pytest.mark.requires_env
def test_generate_3d_missing_file(tmp_path, mock_env_vars, monkeypatch):
    """Test generate_3d with missing input file."""
    # Override with non-existent file
    monkeypatch.setenv('IMAGE_PATH', str(tmp_path / 'nonexistent.png'))
    monkeypatch.setenv('OUTPUT_PATH', str(tmp_path / 'output.stl'))

    with pytest.raises(FileNotFoundError, match="Input image not found"):
        generate_3d()


@pytest.mark.integration
def test_generate_3d_full_pipeline(tmp_path, sample_image, mock_successful_api_call, mock_env_vars, monkeypatch):
    """Test the complete generation pipeline."""
    # Create test input image
    input_path = tmp_path / 'input.png'
    sample_image.save(input_path)

    # Set up environment
    output_path = tmp_path / 'test_output.stl'
    monkeypatch.setenv('IMAGE_PATH', str(input_path))
    monkeypatch.setenv('OUTPUT_PATH', str(output_path))

    result = generate_3d()

    assert result == str(output_path)
    assert output_path.exists()

    content = output_path.read_text()
    assert 'solid tactile_model' in content
    assert 'endsolid tactile_model' in content


@pytest.mark.integration
@pytest.mark.slow
def test_generate_3d_with_all_parameters(tmp_path, sample_image, mock_successful_api_call, monkeypatch):
    """Test generation with all possible parameters set."""
    input_path = tmp_path / 'input.png'
    output_path = tmp_path / 'output.stl'
    sample_image.save(input_path)

    # Set all environment variables
    env_vars = {
        'MODEL_NAME': 'test-model',
        'IMAGE_PATH': str(input_path),
        'OUTPUT_PATH': str(output_path),
        'RESOLUTION': '16',
        'MIN_HEIGHT_MM': '0.3',
        'MAX_HEIGHT_MM': '2.5',
        'BASE_THICKNESS_MM': '0.8',
        'PIXEL_SCALE_MM': '0.15',
        'GAUSSIAN_BLUR_RADIUS': '2',
        'CLAMP_MIN': '10',
        'CLAMP_MAX': '240',
        'BORDER_PIXELS': '3',
        'INVERT_HEIGHTS': 'true',
        'HF_API_TOKEN': 'test-token'
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    result = generate_3d()

    assert result == str(output_path)
    assert output_path.exists()

    # Verify the file has reasonable size (not empty, not too large)
    file_size = output_path.stat().st_size
    assert 1000 < file_size < 100000  # Between 1KB and 100KB for a small test image