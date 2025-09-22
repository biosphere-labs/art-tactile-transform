# Testing Guide

This document explains how to run and understand the test suite for the art-tactile-transform project.

## Quick Start

```bash
# Install dependencies (first time setup)
poetry install

# Run all tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=src/art_tactile_transform --cov-report=html

# Run specific test categories
poetry run pytest -m unit          # Unit tests only
poetry run pytest -m integration   # Integration tests only
poetry run pytest -m "not slow"    # Exclude slow tests
```

## Test Organization

### Test Categories (Markers)

- `@pytest.mark.unit` - Fast unit tests for individual functions
- `@pytest.mark.integration` - End-to-end pipeline tests
- `@pytest.mark.api` - Tests requiring external API mocking
- `@pytest.mark.slow` - Tests that take longer to run
- `@pytest.mark.requires_env` - Tests requiring environment variables

### Test Files

- `test_main.py` - Core functionality tests
- `test_image_processing.py` - Image processing pipeline tests
- `test_stl_generation.py` - STL file generation tests
- `test_integration.py` - End-to-end integration tests

## Running Tests

### Using Poetry

```bash
# Basic test run
poetry run pytest

# Verbose output
poetry run pytest -v

# Run tests in parallel
poetry run pytest -n 4

# Run specific test file
poetry run pytest tests/test_main.py

# Run specific test function
poetry run pytest -k "test_process_image"

# Run with coverage report
poetry run pytest --cov=src/art_tactile_transform --cov-report=term-missing --cov-report=html
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run unit tests only
python run_tests.py --unit

# Run with coverage and HTML report
python run_tests.py --coverage --html-coverage

# Run tests in parallel
python run_tests.py --parallel 4

# Run specific file
python run_tests.py --file test_main.py

# Run tests matching pattern
python run_tests.py --function "test_process_image"
```

## Test Configuration

### pytest.ini

The `pytest.ini` file configures:
- Test discovery patterns
- Output formatting
- Coverage settings
- Test markers
- Warning filters

### conftest.py

Provides shared fixtures:
- `sample_image` - Test RGB image with patterns
- `sample_grayscale_image` - Test grayscale image
- `sample_heightmap` - Test NumPy heightmap array
- `mock_env_vars` - Mock environment variables
- `mock_hf_api_response` - Mock API responses
- `temp_dir` - Temporary directory for test files

## Test Data and Fixtures

Test fixtures are defined in `conftest.py` and provide:

- Sample images of various types and sizes
- Mock API responses for Hugging Face
- Temporary directories for file operations
- Environment variable mocking
- Pre-configured test data

## Coverage Reports

### Terminal Report
```bash
poetry run pytest --cov=src/art_tactile_transform --cov-report=term-missing
```

### HTML Report
```bash
poetry run pytest --cov=src/art_tactile_transform --cov-report=html
# Open htmlcov/index.html in browser
```

### XML Report (for CI)
```bash
poetry run pytest --cov=src/art_tactile_transform --cov-report=xml
```

## Writing New Tests

### Test Structure

```python
import pytest
from art_tactile_transform.main import function_to_test

@pytest.mark.unit
def test_function_behavior(sample_fixture):
    \"\"\"Test description.\"\"\"
    # Arrange
    input_data = sample_fixture
    expected_result = "expected"

    # Act
    result = function_to_test(input_data)

    # Assert
    assert result == expected_result
```

### Best Practices

1. **Use descriptive test names**: `test_process_image_with_border_addition`
2. **Add appropriate markers**: `@pytest.mark.unit`, `@pytest.mark.integration`
3. **Use fixtures for test data**: Defined in `conftest.py`
4. **Test edge cases**: Empty inputs, extreme values, error conditions
5. **Mock external dependencies**: API calls, file system operations
6. **Keep tests isolated**: Each test should be independent
7. **Use parametrized tests**: For testing multiple inputs

### Testing External Dependencies

For API calls:
```python
def test_api_call(monkeypatch, mock_hf_api_response):
    def mock_post(*args, **kwargs):
        return MockResponse(mock_hf_api_response)

    monkeypatch.setattr('requests.post', mock_post)
    # Test your function
```

For environment variables:
```python
def test_with_env_vars(monkeypatch):
    monkeypatch.setenv('MODEL_NAME', 'test-model')
    # Test your function
```

## Continuous Integration

The test suite is designed to work with CI systems:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    poetry install
    poetry run pytest --cov=src/art_tactile_transform --cov-report=xml
```

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure `poetry install` has been run
2. **Missing fixtures**: Check `conftest.py` for fixture definitions
3. **Environment variable conflicts**: Tests clean up env vars automatically
4. **API mocking issues**: Verify mock setup in test functions

### Debug Mode

Run tests with extra debugging:
```bash
poetry run pytest -v -s --tb=long
```

### Test Discovery Issues

If tests aren't being discovered:
```bash
poetry run pytest --collect-only
```

## Performance

- Unit tests should complete in < 1 second each
- Integration tests may take 5-10 seconds
- Slow tests are marked and can be excluded
- Use parallel execution for large test suites

## Test Metrics

Current test coverage targets:
- Overall coverage: > 90%
- Critical functions: 100%
- Error handling: > 95%

Run coverage report to see current metrics:
```bash
poetry run pytest --cov=src/art_tactile_transform --cov-report=term-missing
```