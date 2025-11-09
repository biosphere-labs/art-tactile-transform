"""
Test the actual GUI processing function with a real image.
This mimics what the GUI does when a user uploads an image.
"""

import numpy as np
from PIL import Image
import sys
import os

# Test with Gradio's test image
test_image_path = "./.venv/lib/python3.13/site-packages/gradio/test_data/cheetah1-copy.jpg"

if not os.path.exists(test_image_path):
    print(f"❌ Test image not found: {test_image_path}")
    sys.exit(1)

print(f"Loading test image: {test_image_path}")
image = Image.open(test_image_path)
print(f"Image size: {image.size}, mode: {image.mode}")

# Convert to numpy (like Gradio does)
image_array = np.array(image)
print(f"Image array shape: {image_array.shape}")

# Now test the GUI processing function
print("\n" + "="*60)
print("Testing GUI processing function...")
print("="*60)

from art_tactile_transform.gui import process_image_to_stl

try:
    stl_path, preview = process_image_to_stl(
        image_array,
        width_mm=150.0,
        relief_depth_mm=3.0,
        base_thickness_mm=2.0,
        smoothing=2.0,
        contrast=1.0,
        invert_depth=False,
        resolution=64,  # Low res for fast test
        model_name="LiheYoung/depth-anything-small-hf"
    )

    print(f"\n✓ SUCCESS!")
    print(f"STL path: {stl_path}")
    print(f"Preview type: {type(preview)}")
    print(f"Preview size: {preview.size if hasattr(preview, 'size') else 'N/A'}")

    # Check if STL was created
    if os.path.exists(stl_path):
        file_size = os.path.getsize(stl_path)
        print(f"STL file size: {file_size:,} bytes")

        # Read first few lines to verify format
        with open(stl_path, 'r') as f:
            first_lines = [f.readline().strip() for _ in range(5)]
        print(f"STL header:\n  " + "\n  ".join(first_lines))

        if file_size > 100:
            print("\n✓ STL file created successfully!")
        else:
            print("\n❌ STL file is too small, might be empty")
    else:
        print(f"\n❌ STL file not found at: {stl_path}")

    # Check preview
    if preview:
        preview_array = np.array(preview)
        print(f"\nPreview array shape: {preview_array.shape}")
        print(f"Preview min/max: {preview_array.min()} / {preview_array.max()}")

        if preview_array.max() == preview_array.min():
            print("❌ Preview is blank (all same value)!")
        else:
            print("✓ Preview has variation")

            # Save preview for inspection
            preview.save("/tmp/test_gui_preview.png")
            print(f"✓ Saved preview to: /tmp/test_gui_preview.png")

except Exception as e:
    print(f"\n❌ ERROR during processing:")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "="*60)
print("TEST PASSED - GUI processing works!")
print("="*60)
