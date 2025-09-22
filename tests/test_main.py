import os
import sys
from io import BytesIO
from pathlib import Path

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


class DummyResponse:
    def __init__(self, content: bytes):
        self.content = content

    def raise_for_status(self) -> None:
        return None


def test_calculate_normals():
    """Test normal vector calculation for STL triangles."""
    normal = calculate_normals(0.0, 1.0, 0.5, 0.75, 0, 0, 0.2)
    assert len(normal) == 3
    assert all(isinstance(n, float) for n in normal)


def test_process_image():
    """Test image processing pipeline."""
    # Create test image
    img = Image.new('RGB', (4, 4), color='white')

    # Test basic processing
    processed = process_image(img)
    assert processed.mode == 'L'
    assert processed.size == (4, 4)

    # Test with border
    processed_border = process_image(img, border_pixels=1)
    assert processed_border.size == (6, 6)

    # Test inversion
    processed_inverted = process_image(img, invert_heights=True)
    assert processed_inverted.mode == 'L'


def test_heightmap_to_stl(tmp_path):
    """Test STL generation with enhanced parameters."""
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

    text = output.read_text().strip().splitlines()
    assert text[0] == 'solid tactile_model'
    assert text[-1] == 'endsolid tactile_model'

    # Check for proper base thickness and scaling
    content = output.read_text()
    assert 'vertex' in content
    assert 'facet normal' in content
    assert '2.000' in content  # base thickness should appear


def test_query_hf_api_with_timeout(monkeypatch):
    """Test API query with timeout handling."""
    def fake_post(url, headers=None, data=None, timeout=None):
        assert timeout == 30
        return DummyResponse(b'depth_data')

    monkeypatch.setattr('art_tactile_transform.main.requests.post', fake_post)
    result = query_hf_api(b'image_data', 'test-model', 'token123')
    assert result == b'depth_data'


def test_query_hf_api_error_handling(monkeypatch):
    """Test API error handling."""
    def failing_post(*args, **kwargs):
        raise Exception("Network error")

    monkeypatch.setattr('art_tactile_transform.main.requests.post', failing_post)

    with pytest.raises(RuntimeError, match="Failed to query Hugging Face API"):
        query_hf_api(b'image_data', 'test-model')


def test_generate_3d_missing_env(tmp_path, monkeypatch):
    """Test generate_3d with missing environment variables."""
    # Clear all environment variables
    for var in ['MODEL_NAME', 'IMAGE_PATH', 'OUTPUT_PATH']:
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(ValueError, match="MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set"):
        generate_3d()


def test_generate_3d_missing_file(tmp_path, monkeypatch):
    """Test generate_3d with missing input file."""
    monkeypatch.setenv('MODEL_NAME', 'test-model')
    monkeypatch.setenv('IMAGE_PATH', str(tmp_path / 'nonexistent.png'))
    monkeypatch.setenv('OUTPUT_PATH', str(tmp_path / 'output.stl'))

    with pytest.raises(FileNotFoundError, match="Input image not found"):
        generate_3d()


def test_generate_3d_full_pipeline(tmp_path, monkeypatch):
    """Test the complete generation pipeline."""
    # Create test input image
    input_img = Image.new('RGB', (4, 4), color='gray')
    input_path = tmp_path / 'input.png'
    input_img.save(input_path)

    # Create fake depth response
    depth_img = Image.new('L', (4, 4), color=128)
    buf = BytesIO()
    depth_img.save(buf, format='PNG')
    depth_bytes = buf.getvalue()

    def fake_post(url, headers=None, data=None, timeout=None):
        return DummyResponse(depth_bytes)

    monkeypatch.setattr('art_tactile_transform.main.requests.post', fake_post)

    # Set environment variables
    output_path = tmp_path / 'test_output.stl'
    monkeypatch.setenv('MODEL_NAME', 'test-model')
    monkeypatch.setenv('IMAGE_PATH', str(input_path))
    monkeypatch.setenv('OUTPUT_PATH', str(output_path))
    monkeypatch.setenv('RESOLUTION', '4')
    monkeypatch.setenv('MIN_HEIGHT_MM', '0.5')
    monkeypatch.setenv('MAX_HEIGHT_MM', '3.0')
    monkeypatch.setenv('PIXEL_SCALE_MM', '0.3')

    result = generate_3d()

    assert result == str(output_path)
    assert output_path.exists()

    content = output_path.read_text()
    assert 'solid tactile_model' in content
    assert 'endsolid tactile_model' in content