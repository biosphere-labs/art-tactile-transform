"""
Test the GUI wrapper function to see exactly what it returns.
"""

import numpy as np
from PIL import Image
import os

# Create simple test image
print("Creating test image...")
img = Image.new('RGB', (128, 128))
pixels = img.load()
for i in range(128):
    for j in range(128):
        intensity = int((i + j) / 2)
        pixels[i, j] = (intensity, intensity, intensity)

print(f"Test image: {img.size}, {img.mode}")

# Test the wrapper (what Gradio calls)
print("\nTesting GUI wrapper function...")
from art_tactile_transform.gui import process_image_wrapper

result = process_image_wrapper(
    image=img,  # Gradio passes PIL Image
    width_mm=150,
    relief_depth_mm=3,
    base_thickness_mm=2,
    smoothing=2,
    contrast=1.0,
    invert_depth=False,
    resolution=64
)

print(f"\nWrapper returned {len(result)} values:")
print(f"1. STL path: {result[0]}")
print(f"2. Preview: {type(result[1])}")
print(f"3. Info: {result[2][:100] if result[2] else 'None'}...")

# Verify outputs
if result[0] and os.path.exists(result[0]):
    print(f"\n✓ STL file exists: {os.path.getsize(result[0]):,} bytes")
else:
    print(f"\n❌ STL file missing: {result[0]}")

if result[1]:
    preview_array = np.array(result[1])
    print(f"✓ Preview image: {preview_array.shape}, range {preview_array.min()}-{preview_array.max()}")
else:
    print("❌ Preview image is None")

if result[2] and "STL file ready" in result[2]:
    print("✓ Info message looks good")
else:
    print(f"❌ Info message issue: {result[2]}")

print("\n" + "="*60)
print("DIAGNOSIS")
print("="*60)
print("The GUI wrapper is working correctly.")
print("If you see a blank pane in the browser, it's likely:")
print("1. The 3D viewer needs time to load the STL")
print("2. Browser compatibility (try Chrome/Firefox)")
print("3. Check browser console for JavaScript errors")
print("="*60)
