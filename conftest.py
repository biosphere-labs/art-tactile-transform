"""Pytest configuration and shared fixtures for art_tactile_transform tests."""

import os
import tempfile
from pathlib import Path
from typing import Generator

import pytest
from PIL import Image
import numpy as np


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def sample_image() -> Image.Image:
    """Create a sample RGB image for testing."""
    img = Image.new('RGB', (64, 64), color='white')
    # Add some simple patterns for depth variation
    pixels = img.load()
    for i in range(64):
        for j in range(64):
            # Create a gradient pattern
            intensity = int(255 * (i + j) / 128)
            pixels[i, j] = (intensity, intensity, intensity)
    return img


@pytest.fixture
def sample_grayscale_image() -> Image.Image:
    """Create a sample grayscale image for testing."""
    img = Image.new('L', (32, 32), color=128)
    # Add some geometric patterns
    pixels = img.load()
    center_x, center_y = 16, 16
    for i in range(32):
        for j in range(32):
            # Create concentric circles
            dist = ((i - center_x) ** 2 + (j - center_y) ** 2) ** 0.5
            intensity = max(0, min(255, int(255 - dist * 8)))
            pixels[i, j] = intensity
    return img


@pytest.fixture
def sample_heightmap() -> np.ndarray:
    """Create a sample heightmap for testing STL generation."""
    # Create a 8x8 heightmap with interesting features
    heightmap = np.zeros((8, 8))

    # Add a pyramid in the center
    center = 4
    for i in range(8):
        for j in range(8):
            dist = np.sqrt((i - center) ** 2 + (j - center) ** 2)
            heightmap[i, j] = max(0, 1 - dist / center)

    return heightmap


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    test_env = {
        'MODEL_NAME': 'test-model',
        'IMAGE_PATH': 'test_input.png',
        'OUTPUT_PATH': 'test_output.stl',
        'RESOLUTION': '32',
        'MIN_HEIGHT_MM': '0.5',
        'MAX_HEIGHT_MM': '2.0',
        'BASE_THICKNESS_MM': '1.0',
        'PIXEL_SCALE_MM': '0.2',
        'GAUSSIAN_BLUR_RADIUS': '2',
        'CLAMP_MIN': '0',
        'CLAMP_MAX': '255',
        'BORDER_PIXELS': '5',
        'INVERT_HEIGHTS': 'false'
    }

    for key, value in test_env.items():
        monkeypatch.setenv(key, value)

    return test_env


@pytest.fixture
def mock_hf_api_response():
    """Create a mock Hugging Face API response."""
    # Create a simple depth map image
    depth_img = Image.new('L', (32, 32), color=128)
    # Add some depth variation
    pixels = depth_img.load()
    for i in range(32):
        for j in range(32):
            # Simple gradient
            pixels[i, j] = int(128 + 64 * np.sin(i/5) * np.cos(j/5))

    from io import BytesIO
    buf = BytesIO()
    depth_img.save(buf, format='PNG')
    return buf.getvalue()


class MockResponse:
    """Mock HTTP response for testing API calls."""

    def __init__(self, content: bytes, status_code: int = 200):
        self.content = content
        self.status_code = status_code

    def raise_for_status(self) -> None:
        """Simulate requests.Response.raise_for_status()."""
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


@pytest.fixture
def mock_successful_api_call(monkeypatch, mock_hf_api_response):
    """Mock a successful API call to Hugging Face."""
    def mock_post(*args, **kwargs):
        return MockResponse(mock_hf_api_response)

    monkeypatch.setattr('art_tactile_transform.main.requests.post', mock_post)
    return mock_post


@pytest.fixture
def mock_failed_api_call(monkeypatch):
    """Mock a failed API call to Hugging Face."""
    def mock_post(*args, **kwargs):
        return MockResponse(b'', status_code=500)

    monkeypatch.setattr('art_tactile_transform.main.requests.post', mock_post)
    return mock_post


@pytest.fixture(autouse=True)
def clean_env_vars():
    """Clean up environment variables after each test."""
    # Store original values
    original_env = {}
    test_vars = [
        'MODEL_NAME', 'IMAGE_PATH', 'OUTPUT_PATH', 'RESOLUTION',
        'MIN_HEIGHT_MM', 'MAX_HEIGHT_MM', 'BASE_THICKNESS_MM',
        'PIXEL_SCALE_MM', 'GAUSSIAN_BLUR_RADIUS', 'CLAMP_MIN',
        'CLAMP_MAX', 'BORDER_PIXELS', 'INVERT_HEIGHTS', 'HF_API_TOKEN'
    ]

    for var in test_vars:
        if var in os.environ:
            original_env[var] = os.environ[var]

    yield

    # Clean up test environment variables
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]

    # Restore original values
    for var, value in original_env.items():
        os.environ[var] = value


# Pytest configuration hooks
def pytest_configure(config):
    """Configure pytest with custom settings."""
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    )
    config.addinivalue_line(
        "markers", "api: mark test as requiring external API"
    )
    config.addinivalue_line(
        "markers", "requires_env: mark test as requiring environment variables"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark API tests
        if 'api' in item.name or 'hf' in item.name:
            item.add_marker(pytest.mark.api)

        # Mark integration tests
        if 'integration' in item.name or 'full_pipeline' in item.name:
            item.add_marker(pytest.mark.integration)

        # Mark unit tests (default for most tests)
        if not any(marker.name in ['api', 'integration', 'slow'] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.unit)