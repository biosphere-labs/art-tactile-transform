#!/usr/bin/env python3
"""
Verification script for semantic processing implementation.

This script can run without the full test suite to verify the implementation.
"""

import sys

print("Verifying semantic processing implementation...")
print("=" * 70)

# Check imports
print("\n1. Checking imports...")
try:
    import numpy as np
    print("   ✓ numpy")
except ImportError as e:
    print(f"   ✗ numpy: {e}")
    sys.exit(1)

try:
    from PIL import Image
    print("   ✓ PIL")
except ImportError as e:
    print(f"   ✗ PIL: {e}")
    sys.exit(1)

try:
    from scipy.ndimage import gaussian_filter, sobel
    print("   ✓ scipy")
except ImportError as e:
    print(f"   ✗ scipy: {e}")
    sys.exit(1)

try:
    import cv2
    print(f"   ✓ opencv (version: {cv2.__version__})")
except ImportError as e:
    print(f"   ✗ opencv: {e}")
    print("   Note: Run 'uv pip install opencv-python-headless' to install")
    sys.exit(1)

try:
    from art_tactile_transform.semantic_processing import (
        PortraitProcessor,
        LandscapeProcessor,
        TextProcessor,
        DiagramProcessor,
        SemanticHeightMapper,
    )
    print("   ✓ semantic_processing module")
except ImportError as e:
    print(f"   ✗ semantic_processing: {e}")
    sys.exit(1)

# Check processor initialization
print("\n2. Checking processor initialization...")
try:
    portrait = PortraitProcessor()
    print(f"   ✓ PortraitProcessor (MediaPipe: {portrait.has_mediapipe})")
except Exception as e:
    print(f"   ✗ PortraitProcessor: {e}")
    sys.exit(1)

try:
    landscape = LandscapeProcessor()
    print(f"   ✓ LandscapeProcessor (Transformers: {landscape.has_transformers})")
except Exception as e:
    print(f"   ✗ LandscapeProcessor: {e}")
    sys.exit(1)

try:
    text = TextProcessor()
    print(f"   ✓ TextProcessor (Tesseract: {text.has_tesseract}, EasyOCR: {text.has_easyocr})")
except Exception as e:
    print(f"   ✗ TextProcessor: {e}")
    sys.exit(1)

try:
    diagram = DiagramProcessor()
    print("   ✓ DiagramProcessor")
except Exception as e:
    print(f"   ✗ DiagramProcessor: {e}")
    sys.exit(1)

try:
    mapper = SemanticHeightMapper()
    print("   ✓ SemanticHeightMapper")
except Exception as e:
    print(f"   ✗ SemanticHeightMapper: {e}")
    sys.exit(1)

# Test basic processing
print("\n3. Testing basic processing...")

# Create test image
test_img = Image.new('RGB', (100, 100), color=(128, 128, 128))

modes = ['portrait', 'landscape', 'text', 'diagram']
for mode in modes:
    try:
        heightmap = mapper.process(test_img, mode)
        assert isinstance(heightmap, np.ndarray), f"Expected np.ndarray, got {type(heightmap)}"
        assert heightmap.shape == (100, 100), f"Expected (100, 100), got {heightmap.shape}"
        assert 0.0 <= heightmap.min() <= 1.0, f"Min out of range: {heightmap.min()}"
        assert 0.0 <= heightmap.max() <= 1.0, f"Max out of range: {heightmap.max()}"
        print(f"   ✓ {mode} mode (range: [{heightmap.min():.3f}, {heightmap.max():.3f}])")
    except Exception as e:
        print(f"   ✗ {mode} mode: {e}")
        sys.exit(1)

# Test mode detection
print("\n4. Testing mode detection...")
try:
    detected_mode = mapper.detect_mode(test_img)
    assert detected_mode in modes, f"Invalid mode: {detected_mode}"
    print(f"   ✓ Auto-detection working (detected: {detected_mode})")
except Exception as e:
    print(f"   ✗ Mode detection: {e}")
    sys.exit(1)

# Test post-processing
print("\n5. Testing post-processing...")
try:
    test_heightmap = np.random.rand(100, 100)
    params = {'smoothing': 2, 'edge_strength': 50, 'contrast': 100}
    processed = mapper.post_process(test_heightmap, params)
    assert processed.shape == (100, 100), f"Shape changed: {processed.shape}"
    assert 0.0 <= processed.min() <= 1.0, f"Min out of range: {processed.min()}"
    assert 0.0 <= processed.max() <= 1.0, f"Max out of range: {processed.max()}"
    print(f"   ✓ Post-processing (range: [{processed.min():.3f}, {processed.max():.3f}])")
except Exception as e:
    print(f"   ✗ Post-processing: {e}")
    sys.exit(1)

# Test Mona Lisa scenario
print("\n6. Testing Mona Lisa scenario (semantic correctness)...")
try:
    # Create portrait with face and background
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = [80, 120, 100]  # Background

    # Face region
    Y, X = np.ogrid[:200, :200]
    face_mask = ((Y - 100) ** 2 + (X - 100) ** 2) <= 1600
    img[face_mask] = [220, 180, 150]

    test_img = Image.fromarray(img)

    result = mapper.process(test_img, 'portrait', {
        'subject_emphasis': 150,
        'background_suppression': 70,
    })

    face_height = result[80:120, 80:120].mean()
    background_height = result[0:30, 0:30].mean()

    if face_height > background_height:
        ratio = face_height / (background_height + 1e-8)
        print(f"   ✓ Semantic correctness verified!")
        print(f"      Face height: {face_height:.3f}")
        print(f"      Background height: {background_height:.3f}")
        print(f"      Contrast ratio: {ratio:.2f}x")
    else:
        print(f"   ✗ FAIL: Face ({face_height:.3f}) not higher than background ({background_height:.3f})")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Mona Lisa scenario: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 70)
print("✓ ALL VERIFICATION TESTS PASSED!")
print("\nImplementation is correct and ready for integration.")
print("\nNext steps:")
print("  1. Install dependencies: uv pip install opencv-python-headless scikit-image")
print("  2. Run full test suite: pytest tests/test_semantic_processing.py -v")
print("  3. Run comparison tests: pytest tests/test_depth_vs_semantic.py -v")
print("  4. Integrate with GUI (Gradio)")
print("  5. Test with real images (Mona Lisa, landscapes, text, diagrams)")
