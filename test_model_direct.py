"""
Direct test of depth estimation model to verify it works.
Uses a sample image to test the full pipeline.
"""

from PIL import Image
import numpy as np
from transformers import pipeline

# Create a simple test image (gradient for easy visual verification)
print("Creating test image...")
img = Image.new('RGB', (256, 256))
pixels = img.load()
for i in range(256):
    for j in range(256):
        # Create a diagonal gradient
        intensity = int((i + j) / 2)
        pixels[i, j] = (intensity, intensity, intensity)

print(f"Test image size: {img.size}, mode: {img.mode}")

# Test depth estimation
print("\nLoading depth estimation model...")
model_name = "LiheYoung/depth-anything-small-hf"
depth_estimator = pipeline("depth-estimation", model=model_name)

print(f"Model loaded: {model_name}")
print(f"Model device: {depth_estimator.device}")
print(f"Model type: {type(depth_estimator.model).__name__}")

# Run inference
print("\nRunning depth estimation...")
result = depth_estimator(img)

print(f"\nResult type: {type(result)}")
print(f"Result keys: {result.keys()}")

# Extract depth map
depth_map = result["depth"]
print(f"Depth map type: {type(depth_map)}")
print(f"Depth map size: {depth_map.size}")
print(f"Depth map mode: {depth_map.mode}")

# Convert to numpy for analysis
depth_array = np.array(depth_map)
print(f"\nDepth array shape: {depth_array.shape}")
print(f"Depth array dtype: {depth_array.dtype}")
print(f"Depth min: {depth_array.min()}")
print(f"Depth max: {depth_array.max()}")
print(f"Depth mean: {depth_array.mean():.2f}")
print(f"Depth std: {depth_array.std():.2f}")

# Check if depth map is all zeros (blank)
if depth_array.max() == depth_array.min():
    print("\n❌ ERROR: Depth map is blank (all same value)!")
else:
    print("\n✓ Depth map has variation (good!)")

# Save outputs
print("\nSaving test outputs...")
img.save("/tmp/test_input.png")
depth_map.save("/tmp/test_depth.png")
print("✓ Saved: /tmp/test_input.png")
print("✓ Saved: /tmp/test_depth.png")

print("\n" + "="*60)
print("TEST SUMMARY")
print("="*60)
print(f"Model: {model_name}")
print(f"Input: 256x256 gradient image")
print(f"Output: {depth_array.shape} depth map")
print(f"Value range: {depth_array.min()} - {depth_array.max()}")
print(f"Has variation: {'YES ✓' if depth_array.max() > depth_array.min() else 'NO ❌'}")
print("="*60)
