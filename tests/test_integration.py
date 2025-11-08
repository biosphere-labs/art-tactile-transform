"""Integration tests for the complete art_tactile_transform pipeline."""

import os
from pathlib import Path

import pytest
from PIL import Image

from art_tactile_transform.main import generate_3d


@pytest.mark.integration
class TestIntegration:
    """Integration tests for the complete pipeline."""

    def test_end_to_end_pipeline(self, tmp_path, sample_image, mock_successful_api_call):
        """Test the complete end-to-end pipeline."""
        # Setup test files
        input_path = tmp_path / 'test_input.png'
        output_path = tmp_path / 'test_output.stl'
        sample_image.save(input_path)

        # Set environment variables
        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path),
            'RESOLUTION': '32',
            'MIN_HEIGHT_MM': '0.5',
            'MAX_HEIGHT_MM': '2.0',
            'BASE_THICKNESS_MM': '1.0',
            'PIXEL_SCALE_MM': '0.2'
        }

        # Set environment variables
        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            # Run the pipeline
            result = generate_3d()

            # Verify results
            assert result == str(output_path)
            assert output_path.exists()

            # Check STL content
            content = output_path.read_text()
            assert 'solid tactile_model' in content
            assert 'endsolid tactile_model' in content
            assert 'facet normal' in content
            assert 'vertex' in content

            # Check file size is reasonable
            file_size = output_path.stat().st_size
            assert file_size > 500  # Should have substantial content

        finally:
            # Clean up environment variables
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_pipeline_with_image_processing(self, tmp_path, sample_image, mock_successful_api_call):
        """Test pipeline with all image processing options enabled."""
        input_path = tmp_path / 'processed_input.png'
        output_path = tmp_path / 'processed_output.stl'
        sample_image.save(input_path)

        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path),
            'RESOLUTION': '24',
            'MIN_HEIGHT_MM': '0.3',
            'MAX_HEIGHT_MM': '2.5',
            'BASE_THICKNESS_MM': '0.8',
            'PIXEL_SCALE_MM': '0.15',
            'GAUSSIAN_BLUR_RADIUS': '2',
            'CLAMP_MIN': '20',
            'CLAMP_MAX': '230',
            'BORDER_PIXELS': '3',
            'INVERT_HEIGHTS': 'false'
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = generate_3d()

            assert result == str(output_path)
            assert output_path.exists()

            # Content validation
            content = output_path.read_text()
            assert 'solid tactile_model' in content

            # Check that processing parameters affected the output
            # The file should have triangles and proper structure
            triangle_count = content.count('facet normal')
            assert triangle_count > 0

        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_pipeline_with_height_inversion(self, tmp_path, sample_image, mock_successful_api_call):
        """Test pipeline with height inversion enabled."""
        input_path = tmp_path / 'inverted_input.png'
        output_path = tmp_path / 'inverted_output.stl'
        sample_image.save(input_path)

        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path),
            'INVERT_HEIGHTS': 'true'
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = generate_3d()
            assert result == str(output_path)
            assert output_path.exists()

        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_pipeline_different_resolutions(self, tmp_path, sample_image, mock_successful_api_call):
        """Test pipeline with different resolution settings."""
        input_path = tmp_path / 'resolution_input.png'
        sample_image.save(input_path)

        resolutions = ['16', '32', '64']

        for resolution in resolutions:
            output_path = tmp_path / f'output_{resolution}.stl'

            env_vars = {
                'MODEL_NAME': 'test-model',
                'IMAGE_PATH': str(input_path),
                'OUTPUT_PATH': str(output_path),
                'RESOLUTION': resolution
            }

            for key, value in env_vars.items():
                os.environ[key] = value

            try:
                result = generate_3d()
                assert result == str(output_path)
                assert output_path.exists()

                # Higher resolution should generally produce larger files
                # (though this isn't guaranteed due to compression)
                file_size = output_path.stat().st_size
                assert file_size > 100  # Minimum reasonable size

            finally:
                for key in env_vars:
                    if key in os.environ:
                        del os.environ[key]

    @pytest.mark.slow
    def test_pipeline_large_image(self, tmp_path, mock_successful_api_call):
        """Test pipeline with a larger image."""
        # Create a larger test image
        large_image = Image.new('RGB', (256, 256), color='white')

        # Add some patterns
        pixels = large_image.load()
        for i in range(256):
            for j in range(256):
                # Create a more complex pattern
                intensity = int(128 + 64 * ((i % 32) / 32) * ((j % 32) / 32))
                pixels[i, j] = (intensity, intensity, intensity)

        input_path = tmp_path / 'large_input.png'
        output_path = tmp_path / 'large_output.stl'
        large_image.save(input_path)

        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path),
            'RESOLUTION': '64'
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = generate_3d()
            assert result == str(output_path)
            assert output_path.exists()

            # Larger image should produce more triangles
            content = output_path.read_text()
            triangle_count = content.count('facet normal')
            assert triangle_count > 100  # Should have many triangles

        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_pipeline_error_recovery(self, tmp_path, sample_image, mock_failed_api_call):
        """Test pipeline behavior when API calls fail."""
        input_path = tmp_path / 'error_input.png'
        output_path = tmp_path / 'error_output.stl'
        sample_image.save(input_path)

        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path)
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            # Should raise an error due to API failure
            with pytest.raises(RuntimeError, match="Failed to generate 3D model"):
                generate_3d()

            # Output file should not be created
            assert not output_path.exists()

        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]

    def test_pipeline_missing_environment_variables(self, tmp_path, sample_image, monkeypatch):
        """Test pipeline behavior with missing required environment variables."""
        input_path = tmp_path / 'missing_env_input.png'
        sample_image.save(input_path)

        # Mock load_dotenv to prevent loading from .env file
        monkeypatch.setattr('art_tactile_transform.main.load_dotenv', lambda: None)

        # Clear any existing environment variables
        env_vars_to_clear = [
            'MODEL_NAME', 'IMAGE_PATH', 'OUTPUT_PATH', 'RESOLUTION',
            'MIN_HEIGHT_MM', 'MAX_HEIGHT_MM', 'BASE_THICKNESS_MM',
            'PIXEL_SCALE_MM', 'GAUSSIAN_BLUR_RADIUS', 'CLAMP_MIN',
            'CLAMP_MAX', 'BORDER_PIXELS', 'INVERT_HEIGHTS', 'HF_API_TOKEN'
        ]

        for var in env_vars_to_clear:
            monkeypatch.delenv(var, raising=False)

        # Should raise ValueError for missing required variables
        with pytest.raises(ValueError, match="MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set"):
            generate_3d()

    def test_pipeline_output_directory_creation(self, tmp_path, sample_image, mock_successful_api_call):
        """Test that the pipeline creates output directories as needed."""
        input_path = tmp_path / 'dir_input.png'
        # Create nested output path
        output_path = tmp_path / 'nested' / 'subdirectory' / 'output.stl'
        sample_image.save(input_path)

        # Ensure the nested directory doesn't exist
        assert not output_path.parent.exists()

        env_vars = {
            'MODEL_NAME': 'test-model',
            'IMAGE_PATH': str(input_path),
            'OUTPUT_PATH': str(output_path)
        }

        for key, value in env_vars.items():
            os.environ[key] = value

        try:
            result = generate_3d()

            # Directory should be created and file should exist
            assert result == str(output_path)
            assert output_path.exists()
            assert output_path.parent.exists()

        finally:
            for key in env_vars:
                if key in os.environ:
                    del os.environ[key]