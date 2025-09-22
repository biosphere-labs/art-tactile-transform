"""Tests for image processing functionality."""

import numpy as np
import pytest
from PIL import Image

from art_tactile_transform.main import process_image


@pytest.mark.unit
class TestImageProcessing:
    """Test suite for image processing functions."""

    def test_grayscale_conversion(self, sample_image):
        """Test conversion of RGB images to grayscale."""
        processed = process_image(sample_image)
        assert processed.mode == 'L'
        assert processed.size == sample_image.size

    def test_already_grayscale(self, sample_grayscale_image):
        """Test processing of already grayscale images."""
        processed = process_image(sample_grayscale_image)
        assert processed.mode == 'L'
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
        original_array = np.array(sample_grayscale_image)

        # Test different blur radii
        for radius in [0, 1, 3, 5]:
            processed = process_image(sample_grayscale_image, gaussian_blur_radius=radius)
            processed_array = np.array(processed)

            if radius == 0:
                # No blur should preserve the image exactly
                np.testing.assert_array_equal(original_array, processed_array)
            else:
                # Blur should change the image
                assert not np.array_equal(original_array, processed_array)

    def test_clamping_effects(self, sample_grayscale_image):
        """Test value clamping with different ranges."""
        # Test various clamping ranges
        clamp_tests = [
            (0, 255),    # No clamping
            (50, 200),   # Moderate clamping
            (100, 150),  # Heavy clamping
            (0, 128),    # Lower half only
            (128, 255)   # Upper half only
        ]

        for clamp_min, clamp_max in clamp_tests:
            processed = process_image(
                sample_grayscale_image,
                clamp_min=clamp_min,
                clamp_max=clamp_max
            )

            # Check that processing completes without error
            assert processed.mode == 'L'
            assert processed.size == sample_grayscale_image.size

            # Check value ranges are reasonable
            processed_array = np.array(processed)
            assert processed_array.min() >= 0
            assert processed_array.max() <= 255

    def test_height_inversion(self, sample_grayscale_image):
        """Test height inversion functionality."""
        processed_normal = process_image(sample_grayscale_image, invert_heights=False)
        processed_inverted = process_image(sample_grayscale_image, invert_heights=True)

        normal_array = np.array(processed_normal)
        inverted_array = np.array(processed_inverted)

        # Arrays should be different (inverted)
        assert not np.array_equal(normal_array, inverted_array)

        # Check that inversion actually inverts values
        # For a simple test, check that high values become low and vice versa
        normal_mean = np.mean(normal_array)
        inverted_mean = np.mean(inverted_array)

        # The means should be roughly complementary (around 255)
        total_mean = normal_mean + inverted_mean
        assert 200 < total_mean < 310  # Allow some tolerance due to processing

    def test_combined_processing(self, sample_grayscale_image):
        """Test combined processing with multiple parameters."""
        processed = process_image(
            sample_grayscale_image,
            gaussian_blur_radius=2,
            clamp_min=30,
            clamp_max=220,
            border_pixels=3,
            invert_heights=True
        )

        # Check basic properties
        assert processed.mode == 'L'

        # Check size includes border
        original_width, original_height = sample_grayscale_image.size
        expected_width = original_width + 6  # 3 pixels on each side
        expected_height = original_height + 6

        assert processed.size == (expected_width, expected_height)

        # Check that all processing steps were applied
        processed_array = np.array(processed)
        original_array = np.array(sample_grayscale_image)

        # Should be different due to all the processing
        assert not np.array_equal(
            processed_array[3:-3, 3:-3],  # Remove border for comparison
            original_array
        )

    def test_edge_cases(self):
        """Test edge cases for image processing."""
        # Test with very small image
        tiny_image = Image.new('L', (2, 2), color=128)
        processed = process_image(tiny_image)
        assert processed.size == (2, 2)

        # Test with single pixel image
        single_pixel = Image.new('L', (1, 1), color=100)
        processed = process_image(single_pixel)
        assert processed.size == (1, 1)

        # Test with very large border relative to image size
        small_image = Image.new('L', (4, 4), color=128)
        processed = process_image(small_image, border_pixels=10)
        assert processed.size == (24, 24)  # 4 + 20

    def test_processing_preserves_quality(self, sample_grayscale_image):
        """Test that processing maintains reasonable image quality."""
        processed = process_image(
            sample_grayscale_image,
            gaussian_blur_radius=1,
            clamp_min=10,
            clamp_max=245
        )

        original_array = np.array(sample_grayscale_image)
        processed_array = np.array(processed)

        # Check that we maintain reasonable dynamic range
        original_range = np.max(original_array) - np.min(original_array)
        processed_range = np.max(processed_array) - np.min(processed_array)

        # Processing should maintain significant dynamic range
        # (allowing for some reduction due to clamping and blur)
        assert processed_range > original_range * 0.5

    @pytest.mark.parametrize("border_size", [0, 1, 5, 10, 20])
    def test_border_sizes_parametrized(self, sample_grayscale_image, border_size):
        """Parametrized test for different border sizes."""
        processed = process_image(sample_grayscale_image, border_pixels=border_size)

        original_width, original_height = sample_grayscale_image.size
        expected_width = original_width + 2 * border_size
        expected_height = original_height + 2 * border_size

        assert processed.size == (expected_width, expected_height)

    @pytest.mark.parametrize("blur_radius", [0, 1, 2, 3, 5, 8])
    def test_blur_radius_parametrized(self, sample_grayscale_image, blur_radius):
        """Parametrized test for different blur radius values."""
        processed = process_image(sample_grayscale_image, gaussian_blur_radius=blur_radius)

        # Should always maintain same size and mode
        assert processed.size == sample_grayscale_image.size
        assert processed.mode == 'L'

        # Check that result is reasonable
        processed_array = np.array(processed)
        assert processed_array.min() >= 0
        assert processed_array.max() <= 255