"""Tests for CLI interface."""

import os
from pathlib import Path

import pytest
from PIL import Image

from art_tactile_transform.cli import generate_3d


@pytest.mark.requires_env
def test_generate_3d_missing_env(monkeypatch):
    """Test generate_3d with missing environment variables."""
    # Mock load_dotenv to prevent loading from .env file
    monkeypatch.setattr("art_tactile_transform.cli.load_dotenv", lambda **kwargs: None)

    # Clear all environment variables
    for var in ["MODEL_NAME", "IMAGE_PATH", "OUTPUT_PATH"]:
        monkeypatch.delenv(var, raising=False)

    with pytest.raises(
        ValueError, match="MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set"
    ):
        generate_3d()


@pytest.mark.requires_env
def test_generate_3d_missing_file(tmp_path, mock_env_vars, monkeypatch):
    """Test generate_3d with missing input file."""
    # Override with non-existent file
    monkeypatch.setenv("IMAGE_PATH", str(tmp_path / "nonexistent.png"))
    monkeypatch.setenv("OUTPUT_PATH", str(tmp_path / "output.stl"))

    with pytest.raises(FileNotFoundError, match="Input image not found"):
        generate_3d()


@pytest.mark.integration
def test_generate_3d_full_pipeline(
    tmp_path, sample_image, mock_env_vars, monkeypatch
):
    """Test the complete generation pipeline."""
    # Create test input image
    input_path = tmp_path / "input.png"
    sample_image.save(input_path)

    # Set up environment
    output_path = tmp_path / "test_output.stl"
    monkeypatch.setenv("IMAGE_PATH", str(input_path))
    monkeypatch.setenv("OUTPUT_PATH", str(output_path))

    # Mock the depth model
    def mock_query_depth(image, model_name):
        # Return a simple grayscale version
        return image.convert("L")

    monkeypatch.setattr(
        "art_tactile_transform.cli.query_depth_model", mock_query_depth
    )

    result = generate_3d()

    assert result == str(output_path)
    assert output_path.exists()

    content = output_path.read_text()
    assert "solid tactile_model" in content
    assert "endsolid tactile_model" in content


@pytest.mark.integration
@pytest.mark.slow
def test_generate_3d_with_all_parameters(tmp_path, sample_image, monkeypatch):
    """Test generation with all possible parameters set."""
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.stl"
    sample_image.save(input_path)

    # Set all environment variables
    env_vars = {
        "MODEL_NAME": "test-model",
        "IMAGE_PATH": str(input_path),
        "OUTPUT_PATH": str(output_path),
        "RESOLUTION": "16",
        "MIN_HEIGHT_MM": "0.3",
        "MAX_HEIGHT_MM": "2.5",
        "BASE_THICKNESS_MM": "0.8",
        "PIXEL_SCALE_MM": "0.15",
        "GAUSSIAN_BLUR_RADIUS": "2",
        "CLAMP_MIN": "10",
        "CLAMP_MAX": "240",
        "BORDER_PIXELS": "3",
        "INVERT_HEIGHTS": "true",
        "HF_API_TOKEN": "test-token",
    }

    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    # Mock the depth model
    def mock_query_depth(image, model_name):
        return image.convert("L")

    monkeypatch.setattr(
        "art_tactile_transform.cli.query_depth_model", mock_query_depth
    )

    result = generate_3d()

    assert result == str(output_path)
    assert output_path.exists()

    # Verify the file has reasonable size (not empty, not too large)
    file_size = output_path.stat().st_size
    assert 1000 < file_size < 100000  # Between 1KB and 100KB for a small test image
