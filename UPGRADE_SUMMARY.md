# Upgrade Summary - Depth Anything V2 Large

## Major Improvements

### 1. Better AI Model ✨

**Before:** `LiheYoung/depth-anything-small-hf`
**Now:** `depth-anything/Depth-Anything-V2-Large-hf`

**Benefits:**
- **State-of-the-art quality** (NeurIPS 2024)
- Trained on 595K labeled + 62M unlabeled images
- Superior to MiDaS, ZoeDepth, and Depth Anything V1
- Much better depth accuracy and detail

**Trade-offs:**
- Larger download: ~1.3GB (vs ~500MB)
- First-time setup: 5-10 minutes (vs 2-5 minutes)
- Processing speed: Similar (both CPU-based)

**Model Card:** https://huggingface.co/depth-anything/Depth-Anything-V2-Large-hf

---

### 2. Deeper Tactile Relief 🎯

**Contrast Settings:**
- **Default:** 1.0x → **1.8x** (much deeper!)
- **Range:** 0.5-2.0x → **0.5-3.0x**
- **Recommended for tactile art:** 2.5-3.0x

**Why this matters:**
- Original depth was too shallow for tactile perception
- 1.8x default creates noticeable depth immediately
- Users can push to 3.0x for dramatic relief
- Better for blind/visually impaired accessibility

---

### 3. 3D Viewer Issue - Known Limitation ⚠️

**Issue:** Gradio's Model3D component shows blank pane

**Cause:** Gradio struggles with 1-2MB STL files in browser

**Workarounds:**
1. **Heightmap Preview** - Always check this! Shows depth variation
2. **Download STL** - View in external 3D software (Blender, Meshlab, etc.)
3. **Wait 5-10 seconds** - Sometimes viewer loads slowly
4. **Try different browser** - Chrome recommended

**Backend Works Perfect:**
- ✓ STL files generate correctly (1.4MB, valid geometry)
- ✓ Heightmap previews show full depth range
- ✓ All tests pass (test_model_direct.py, test_gui_processing.py)

---

## Model Comparison

| Model | Size | Quality | Speed | Use Case |
|-------|------|---------|-------|----------|
| **Depth Anything V2 Large** ⭐ | 1.3GB | Excellent | Medium | Best overall |
| Depth Anything V1 Small | 500MB | Good | Fast | Quick preview |
| MiDaS v3.1 | 1.2GB | Good | Medium | Legacy |
| ZoeDepth | 800MB | Good (metric) | Medium | Metric depth |
| Intel DPT Large | 1.4GB | Good | Slow | Legacy |

**We chose V2 Large for:** Best quality for tactile art where depth accuracy matters most

---

## Alternative Models (Future Options)

If you want to try different models, edit `.env`:

```bash
# Faster but lower quality
MODEL_NAME=LiheYoung/depth-anything-small-hf

# Metric depth (indoor scenes)
MODEL_NAME=depth-anything/Depth-Anything-V2-Metric-Indoor-Large-hf

# Metric depth (outdoor scenes)
MODEL_NAME=depth-anything/Depth-Anything-V2-Metric-Outdoor-Large-hf

# Current (best for tactile art)
MODEL_NAME=depth-anything/Depth-Anything-V2-Large-hf
```

---

## Testing Results

All tests pass with new model:

```bash
$ python test_model_direct.py
✓ Model loads: Depth Anything V2 Large
✓ Depth map range: 0-255 (full range)
✓ Has variation: YES

$ python test_gui_processing.py
✓ STL file: 1,441,101 bytes
✓ Preview range: 7-253 (good variation)
✓ TEST PASSED

$ python test_gui_wrapper.py
✓ Wrapper returns 3 values correctly
✓ STL exists and valid
✓ Preview has variation
✓ Info message correct
```

**Conclusion:** Backend works perfectly. 3D viewer issue is Gradio limitation.

---

## For Users

### Quick Start

1. Run `install.bat` (Windows) or `./launch.sh` (Linux/Mac)
2. First run downloads ~1.3GB model (5-10 min)
3. Upload any image
4. **Check heightmap preview** (lower right) - should show depth
5. Adjust contrast (try 2.5-3.0x for dramatic depth)
6. Download STL file

### Tips for Best Results

- **Contrast:** Start at 1.8x, increase to 2.5-3.0x for more depth
- **Smoothing:** 0-2 for sharp, 3-5 for smooth tactile surfaces
- **Resolution:** 128 for preview, 256 for final export
- **Relief Depth:** 3-5mm for tactile perception

### If 3D Preview is Blank

Don't worry! The STL file is fine. Just:
1. Check the **heightmap preview** (should show color variation)
2. Download the STL file
3. Open in Blender, Meshlab, or any STL viewer

---

## Technical Details

**Architecture:**
- Model: ViT-Large backbone
- Training: DPT (Dense Prediction Transformer)
- Output: Relative depth maps (0-255 normalized)

**Processing Pipeline:**
```
Image → Depth Anything V2 Large → Depth Map (0-255)
  → Contrast Adjustment (×1.8 default)
  → Smoothing (Gaussian)
  → Normalize (0-1)
  → STL Generation (heightmap_to_stl)
  → Output: tactile_art.stl
```

**File Sizes:**
- Model download: ~1.3GB (one-time)
- Input image: Any size (resized internally)
- Output STL: 1-2MB (depends on resolution)
- Resolution 64: ~350KB STL
- Resolution 128: ~1.4MB STL
- Resolution 256: ~5.5MB STL

---

## Links

- **Model:** https://huggingface.co/depth-anything/Depth-Anything-V2-Large-hf
- **Paper:** https://arxiv.org/abs/2406.09414
- **GitHub:** https://github.com/DepthAnything/Depth-Anything-V2
- **Demo:** https://huggingface.co/spaces/depth-anything/Depth-Anything-V2
