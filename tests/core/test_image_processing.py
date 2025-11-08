"""Tests for image processing functionality."""

import numpy as np
import pytest
from PIL import Image

from art_tactile_transform.core.image_processing import (
    image_to_heightmap,
    process_image,
    resize_to_resolution,
)


@pytest.mark.unit
class TestImageProcessing:
    """Test suite for image processing functions."""

    def test_grayscale_conversion(self, sample_image):
        """Test conversion of RGB images to grayscale."""
        processed = process_image(sample_image)
        assert processed.mode == "L"
        assert processed.size == sample_image.size

    def test_already_grayscale(self, sample_grayscale_image):
        """Test processing of already grayscale images."""
        processed = process_image(sample_grayscale_image)
        assert processed.mode == "L"
        assert processed.size == sample_grayscale_image.size

    def test_border_addition_various_sizes(self, sample_grayscale_image):
        """Test border addition with various sizes."""
        original_size = sample_grayscale_image.size

        for border_size in [0, 1, 5, 10]:
            processed = process_image(sample_grayscale_image, border_pixels=border_size)
            expected_width = original_size[0] + 2 * border_size
            expected_height = original_size[1] + 2 * border_size

            assert processed.size == (expected_width, expected_height)

    def test_gaussian_blur_effects(self, sample_grayscale_image):
        """Test Gaussian blur with different radius values."""
        # Test different blur radii
        for radius in [0, 1, 3]:
            processed = process_image(
                sample_grayscale_image, gaussian_blur_radius=radius
            )
            assert processed.mode == "L"
            assert processed.size == sample_grayscale_image.size

    def test_height_inversion(self, sample_grayscale_image):
        """Test height inversion functionality."""
        processed_normal = process_image(sample_grayscale_image, invert_heights=False)
        processed_inverted = process_image(sample_grayscale_image, invert_heights=True)

        normal_array = np.array(processed_normal)
        inverted_array = np.array(processed_inverted)

        # Arrays should be different (inverted)
        assert not np.array_equal(normal_array, inverted_array)

    def test_parameter_validation(self, sample_grayscale_image):
        """Test parameter validation."""
        # Invalid clamp values
        with pytest.raises(ValueError):
            process_image(sample_grayscale_image, clamp_min=-1)

        with pytest.raises(ValueError):
            process_image(sample_grayscale_image, clamp_max=300)

        with pytest.raises(ValueError):
            process_image(sample_grayscale_image, clamp_min=200, clamp_max=100)

        with pytest.raises(ValueError):
            process_image(sample_grayscale_image, gaussian_blur_radius=-1)


@pytest.mark.unit
def test_resize_to_resolution(sample_image):
    """Test image resizing functionality."""
    # Test square resize
    resized = resize_to_resolution(sample_image, 128, maintain_aspect=False)
    assert resized.size == (128, 128)

    # Test aspect ratio maintenance
    resized_aspect = resize_to_resolution(sample_image, 128, maintain_aspect=True)
    assert resized_aspect.size[0] == 128


@pytest.mark.unit
def test_image_to_heightmap(sample_grayscale_image):
    """Test conversion of image to heightmap."""
    heightmap = image_to_heightmap(sample_grayscale_image)

    assert isinstance(heightmap, np.ndarray)
    assert heightmap.ndim == 2
    assert heightmap.min() >= 0.0
    assert heightmap.max() <= 1.0

    # Test with non-grayscale image
    rgb_image = Image.new("RGB", (10, 10))
    with pytest.raises(ValueError, match="grayscale"):
        image_to_heightmap(rgb_image)
