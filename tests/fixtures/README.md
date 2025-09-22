# Test Fixtures

This directory contains test data and fixtures used by the test suite.

## Contents

- Sample images for testing image processing
- Expected output files for validation
- Test configuration files

## Usage

Test fixtures are automatically loaded by the test suite using pytest fixtures defined in `conftest.py`.

## Adding New Fixtures

When adding new test data:

1. Place files in appropriate subdirectories
2. Keep file sizes small (< 100KB when possible)
3. Use descriptive names
4. Document the purpose in this README

## Test Data Types

- **images/**: Sample input images (PNG, JPG)
- **heightmaps/**: Pre-generated heightmap arrays
- **stl/**: Expected STL output files for validation
- **configs/**: Test configuration files