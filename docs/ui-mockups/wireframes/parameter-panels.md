# Parameter Panels - Mode-Specific Wireframes

**Component**: Parameter Panels for Each Processing Mode
**Version**: 2.0.0
**Last Updated**: 2025-11-08

---

## Overview

Each processing mode (Portrait, Landscape, Text, Diagram, Custom) has a customized parameter panel that exposes the most relevant controls for that type of image. This document details the specific parameters and layout for each mode.

---

## Common Elements (All Modes)

### Physical Parameters Section
**Always present, always expanded by default**

```
┌─────────────────────────────────────┐
│  ⚙️ Physical Parameters         [−] │
├─────────────────────────────────────┤
│                                     │
│  Width (mm)                         │
│  50                      [─●──] 300 │
│         Current: 150mm              │
│                                     │
│  Height (mm)                        │
│  50                      [─●──] 300 │
│         Current: 112mm              │
│  ☑ Auto Aspect Ratio                │
│                                     │
│  Base Thickness (mm)                │
│  0.5                     [──●─] 5.0 │
│         Current: 2.0mm              │
│                                     │
│  Relief Depth (mm)                  │
│  0.5                     [──●─] 10  │
│         Current: 3.0mm              │
│                                     │
│  Edge Wall Thickness (mm)           │
│  1                       [──●─] 10  │
│         Current: 3mm                │
│                                     │
│  ℹ️ Output dimensions:              │
│     150mm × 112mm × 5mm (W×H×Total) │
│     Print volume: ~100 cm³          │
└─────────────────────────────────────┘
```

**Interactions**:
- **Auto Aspect**: When checked, height slider is disabled and auto-calculated
- **Real-time calculation**: Total height = Base + Relief Depth
- **Warnings**: If dimensions exceed common printer build volumes (200mm), show warning icon
- **Info panel**: Shows calculated total dimensions and estimated volume

---

## Mode 1: Portrait/People

**Purpose**: Emphasize faces and people over backgrounds
**Key Features**: Face detection, facial feature enhancement, person segmentation

```
┌─────────────────────────────────────┐
│  🎭 Portrait Parameters          [−]│
├─────────────────────────────────────┤
│                                     │
│  👤 Face Emphasis                   │
│  0%                     [────●] 200%│
│         Current: 150%               │
│  ℹ️ How much higher faces appear   │
│     compared to background          │
│                                     │
│  👁️ Facial Feature Sharpness       │
│  0%                     [───●─] 100%│
│         Current: 70%                │
│  ℹ️ Emphasis on eyes, nose, mouth   │
│                                     │
│  🧍 Body/Person Emphasis            │
│  0%                     [──●──] 200%│
│         Current: 100%               │
│  ℹ️ Raise entire person silhouette  │
│                                     │
│  🌄 Background Suppression          │
│  0%                     [───●─] 100%│
│         Current: 60%                │
│  ℹ️ Flatten background elements     │
│                                     │
│  🔍 Face Detection Settings         │
│  ─────────────────────────────────  │
│                                     │
│  Detected Faces: 1                  │
│  ☑ Auto-center on primary face     │
│  ☐ Emphasize all faces equally      │
│  ☑ Enhance facial landmarks         │
│                                     │
│  [🎯 Manually Select Faces...]      │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🎨 Processing Parameters        [+]│  (Collapsed)
├─────────────────────────────────────┤
│  (Click to expand)                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🔧 Advanced Options             [+]│  (Collapsed)
├─────────────────────────────────────┤
│  (Click to expand)                  │
└─────────────────────────────────────┘
```

### Expanded: Processing Parameters (Portrait)

```
┌─────────────────────────────────────┐
│  🎨 Processing Parameters        [−]│
├─────────────────────────────────────┤
│                                     │
│  Resolution (vertices/side)         │
│  32                      [────●] 256│
│         Current: 128                │
│  ℹ️ Higher = more detail, slower    │
│                                     │
│  Smoothing                          │
│  0                       [──●─] 10  │
│         Current: 2                  │
│  ℹ️ Gaussian blur radius            │
│                                     │
│  Edge Strength                      │
│  0%                     [────●] 100%│
│         Current: 70%                │
│  ℹ️ Emphasize outlines and contours │
│                                     │
│  Contrast Enhancement               │
│  0%                     [─────●]200%│
│         Current: 110%               │
│  ℹ️ Overall height map contrast     │
│                                     │
│  Minimum Feature Size (mm)          │
│  1                       [─●──] 20  │
│         Current: 3mm                │
│  ℹ️ Filter details smaller than this│
│                                     │
└─────────────────────────────────────┘
```

### Expanded: Advanced Options (Portrait)

```
┌─────────────────────────────────────┐
│  🔧 Advanced Options             [−]│
├─────────────────────────────────────┤
│                                     │
│  Face Detection Model               │
│  ┌─────────────────────────────┐   │
│  │ ● MediaPipe (Fast)          │   │
│  │ ○ dlib (Accurate)           │   │
│  │ ○ MTCNN (Robust)            │   │
│  └─────────────────────────────┘   │
│                                     │
│  Segmentation Model                 │
│  ┌─────────────────────────────┐   │
│  │ ● Segformer (Balanced)      │   │
│  │ ○ SAM (Highest Quality)     │   │
│  │ ○ DeepLabv3 (Fast)          │   │
│  └─────────────────────────────┘   │
│                                     │
│  Height Mapping Strategy            │
│  ┌─────────────────────────────┐   │
│  │ ● Semantic (Face highest)   │   │
│  │ ○ Hybrid (Face + depth)     │   │
│  │ ○ Saliency-based            │   │
│  └─────────────────────────────┘   │
│                                     │
│  Edge Detection                     │
│  ┌─────────────────────────────┐   │
│  │ ● Canny                     │   │
│  │ ○ Sobel                     │   │
│  │ ○ Holistically-Nested       │   │
│  └─────────────────────────────┘   │
│                                     │
│  ☑ Invert height map                │
│  ☐ Mirror horizontally              │
│  ☐ Add text label (braille/visual) │
│                                     │
│  [🔄 Reset to Defaults]             │
│                                     │
└─────────────────────────────────────┘
```

**Preset Recommendations** (Portrait):
- "Portrait - High Detail" (face: 180%, features: 90%, background: 80%)
- "Portrait - Simple" (face: 120%, features: 50%, background: 60%)
- "Portrait - Dramatic" (face: 200%, features: 100%, background: 90%)
- "Portrait - Soft" (face: 100%, smoothing: 5, edge: 30%)

---

## Mode 2: Landscape/Scenery

**Purpose**: Emphasize foreground objects, flatten distant elements
**Key Features**: Semantic segmentation, saliency mapping, depth ordering

```
┌─────────────────────────────────────┐
│  🌄 Landscape Parameters         [−]│
├─────────────────────────────────────┤
│                                     │
│  🎯 Foreground Emphasis             │
│  0%                     [────●] 200%│
│         Current: 140%               │
│  ℹ️ Raise near objects and subjects │
│                                     │
│  🌤️ Background/Sky Suppression      │
│  0%                     [────●] 100%│
│         Current: 70%                │
│  ℹ️ Flatten distant sky/mountains   │
│                                     │
│  🌳 Object Separation               │
│  0%                     [──●──] 100%│
│         Current: 50%                │
│  ℹ️ Height gap between depth layers │
│                                     │
│  ⭐ Saliency Strength                │
│  0%                     [───●─] 100%│
│         Current: 60%                │
│  ℹ️ Emphasize visually interesting  │
│     elements (people, animals, etc.)│
│                                     │
│  🔲 Edge Preservation               │
│  0%                     [───●─] 100%│
│         Current: 60%                │
│  ℹ️ Sharpen object boundaries       │
│                                     │
│  📊 Detected Elements:              │
│  ─────────────────────────────────  │
│  ✓ Sky (suppressed)                 │
│  ✓ Trees (foreground)               │
│  ✓ Building (mid-ground)            │
│  ✓ Person (emphasized)              │
│                                     │
│  [🎯 Manually Adjust Regions...]    │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🎨 Processing Parameters        [+]│
│  🔧 Advanced Options             [+]│
└─────────────────────────────────────┘
```

### Advanced: Landscape

```
┌─────────────────────────────────────┐
│  🔧 Advanced Options             [−]│
├─────────────────────────────────────┤
│                                     │
│  Segmentation Strategy              │
│  ┌─────────────────────────────┐   │
│  │ ● Semantic (category-based) │   │
│  │ ○ Instance (object-based)   │   │
│  │ ○ Panoptic (combined)       │   │
│  └─────────────────────────────┘   │
│                                     │
│  Height Assignment                  │
│  ┌─────────────────────────────┐   │
│  │ ● Semantic priority         │   │
│  │ ○ Saliency priority         │   │
│  │ ○ Depth estimation hybrid   │   │
│  └─────────────────────────────┘   │
│                                     │
│  Depth Layers                       │
│  ┌─────────────────────────────┐   │
│  │ ● 3 layers (simple)         │   │
│  │ ○ 5 layers (detailed)       │   │
│  │ ○ 7+ layers (very detailed) │   │
│  └─────────────────────────────┘   │
│                                     │
│  Sky Handling                       │
│  ┌─────────────────────────────┐   │
│  │ ● Flat (lowest level)       │   │
│  │ ○ Textured (subtle clouds)  │   │
│  │ ○ Removed (transparent)     │   │
│  └─────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

**Preset Recommendations** (Landscape):
- "Landscape - Dramatic" (foreground: 160%, background: 80%, separation: 70%)
- "Landscape - Gentle" (foreground: 110%, background: 40%, separation: 30%)
- "Landscape - Layers" (3+ depth layers, clear separation)

---

## Mode 3: Text/Document

**Purpose**: Maximum text legibility, high contrast characters
**Key Features**: OCR, character detection, extreme height contrast

```
┌─────────────────────────────────────┐
│  📝 Text Parameters              [−]│
├─────────────────────────────────────┤
│                                     │
│  🔤 Text Height                     │
│  0.5mm                  [─────●] 10 │
│         Current: 4.0mm              │
│  ℹ️ How high text characters raise  │
│                                     │
│  📐 Character Edge Sharpness        │
│  0%                     [─────●]100%│
│         Current: 95%                │
│  ℹ️ Sharp edges for clear letters   │
│                                     │
│  🎯 Background Suppression          │
│  0%                     [─────●]100%│
│         Current: 100%               │
│  ℹ️ Flatten non-text areas          │
│                                     │
│  📏 Minimum Character Size (mm)     │
│  1                       [──●─] 10  │
│         Current: 3mm                │
│  ℹ️ Filter text smaller than this   │
│                                     │
│  🔄 Invert Colors                   │
│  ┌─────────────────────────────┐   │
│  │ ● Dark text on light        │   │
│  │ ○ Light text on dark        │   │
│  │ ○ Auto-detect               │   │
│  └─────────────────────────────┘   │
│                                     │
│  📊 OCR Results:                    │
│  ─────────────────────────────────  │
│  Detected Text: "EMERGENCY EXIT"    │
│  Confidence: 98%                    │
│  Language: English                  │
│  Characters: 13                     │
│                                     │
│  ☑ Add Braille version below        │
│  ☐ Add visual border around text    │
│  ☐ Mirror text (for mold making)    │
│                                     │
│  [✏️ Edit Detected Text...]         │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🎨 Processing Parameters        [+]│
│  🔧 Advanced Options             [+]│
└─────────────────────────────────────┘
```

### Advanced: Text

```
┌─────────────────────────────────────┐
│  🔧 Advanced Options             [−]│
├─────────────────────────────────────┤
│                                     │
│  OCR Engine                         │
│  ┌─────────────────────────────┐   │
│  │ ● Tesseract (open source)   │   │
│  │ ○ EasyOCR (deep learning)   │   │
│  │ ○ Manual text input         │   │
│  └─────────────────────────────┘   │
│                                     │
│  Text Preprocessing                 │
│  ┌─────────────────────────────┐   │
│  │ ☑ Deskew/rotation           │   │
│  │ ☑ Noise reduction           │   │
│  │ ☑ Contrast enhancement      │   │
│  │ ☐ Binarization              │   │
│  └─────────────────────────────┘   │
│                                     │
│  Character Rendering                │
│  ┌─────────────────────────────┐   │
│  │ ● Original font (detected)  │   │
│  │ ○ Sans-serif (simple)       │   │
│  │ ○ High-contrast (maximum)   │   │
│  └─────────────────────────────┘   │
│                                     │
│  Braille Settings (if enabled)      │
│  ─────────────────────────────────  │
│  Braille Grade: ● 1  ○ 2            │
│  Dot Height: [──●─] 0.5mm           │
│  Dot Spacing: [──●─] 2.5mm          │
│                                     │
│  Position: ● Below  ○ Above         │
│                                     │
└─────────────────────────────────────┘
```

**Preset Recommendations** (Text):
- "Text - Maximum Legibility" (height: 5mm, sharpness: 100%, no smoothing)
- "Text - Braille + Visual" (text + braille, optimized spacing)
- "Text - Sign" (large text, high contrast, border)

---

## Mode 4: Diagram/Technical

**Purpose**: Sharp edges, clear regions, technical precision
**Key Features**: Edge detection, region segmentation, geometric clarity

```
┌─────────────────────────────────────┐
│  📐 Diagram Parameters           [−]│
├─────────────────────────────────────┤
│                                     │
│  📏 Edge/Line Emphasis              │
│  0%                     [─────●]100%│
│         Current: 90%                │
│  ℹ️ Raise all lines and boundaries  │
│                                     │
│  🔲 Region Height Variation         │
│  0%                     [───●─] 100%│
│         Current: 60%                │
│  ℹ️ Height difference between areas │
│                                     │
│  ⚡ Edge Sharpness                   │
│  0%                     [─────●]100%│
│         Current: 95%                │
│  ℹ️ Crisp boundaries (no blur)      │
│                                     │
│  🎨 Region Smoothing                │
│  0                       [─●──] 10  │
│         Current: 1                  │
│  ℹ️ Smooth within regions only      │
│                                     │
│  📊 Line Thickness (mm)             │
│  0.5                     [──●─] 5.0 │
│         Current: 1.5mm              │
│  ℹ️ Width of detected lines         │
│                                     │
│  🔍 Detected Elements:              │
│  ─────────────────────────────────  │
│  ✓ 12 lines/edges                   │
│  ✓ 5 distinct regions               │
│  ✓ 3 text labels                    │
│                                     │
│  ☑ Emphasize text labels            │
│  ☑ Preserve geometric shapes        │
│  ☐ Add grid reference               │
│                                     │
│  [🎯 Manually Edit Regions...]      │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🎨 Processing Parameters        [+]│
│  🔧 Advanced Options             [+]│
└─────────────────────────────────────┘
```

### Advanced: Diagram

```
┌─────────────────────────────────────┐
│  🔧 Advanced Options             [−]│
├─────────────────────────────────────┤
│                                     │
│  Edge Detection Algorithm           │
│  ┌─────────────────────────────┐   │
│  │ ● Canny (standard)          │   │
│  │ ○ Hough Lines (geometric)   │   │
│  │ ○ Holistically-Nested (AI)  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Line Processing                    │
│  ┌─────────────────────────────┐   │
│  │ ☑ Connect broken lines      │   │
│  │ ☑ Remove noise/artifacts    │   │
│  │ ☑ Extend to edges           │   │
│  │ ☐ Vectorize (perfect lines) │   │
│  └─────────────────────────────┘   │
│                                     │
│  Region Assignment                  │
│  ┌─────────────────────────────┐   │
│  │ ● Automatic (segmentation)  │   │
│  │ ○ Color-based               │   │
│  │ ○ Manual selection          │   │
│  └─────────────────────────────┘   │
│                                     │
│  Height Distribution                │
│  ┌─────────────────────────────┐   │
│  │ ● Stepped (discrete levels) │   │
│  │ ○ Gradient (smooth)         │   │
│  │ ○ Binary (2 levels only)    │   │
│  └─────────────────────────────┘   │
│                                     │
│  Text Label Handling                │
│  ─────────────────────────────────  │
│  Text Height: [────●─] +2mm         │
│  ☑ OCR text labels                  │
│  ☑ Emphasize labels                 │
│                                     │
└─────────────────────────────────────┘
```

**Preset Recommendations** (Diagram):
- "Diagram - Technical" (edges: 95%, sharp: 100%, stepped heights)
- "Diagram - Map" (regions at different heights, clear boundaries)
- "Diagram - Floor Plan" (binary heights, very sharp edges)

---

## Mode 5: Custom/Advanced

**Purpose**: Maximum control, hybrid processing, experimentation
**Key Features**: Manual region selection, multiple strategies, full parameter access

```
┌─────────────────────────────────────┐
│  🎛️ Custom Parameters            [−]│
├─────────────────────────────────────┤
│                                     │
│  Processing Strategy                │
│  ┌─────────────────────────────┐   │
│  │ Select multiple:            │   │
│  │ ☑ Semantic segmentation     │   │
│  │ ☑ Edge detection            │   │
│  │ ☐ Saliency mapping          │   │
│  │ ☐ Depth estimation          │   │
│  │ ☐ Face detection            │   │
│  │ ☐ Text/OCR                  │   │
│  └─────────────────────────────┘   │
│                                     │
│  Strategy Weights                   │
│  ─────────────────────────────────  │
│  Semantic:  [────●─] 50%            │
│  Edges:     [────●─] 50%            │
│  Saliency:  [──────] 0%             │
│                                     │
│  🖌️ Manual Region Editor            │
│  [🎨 Open Region Editor...]         │
│  ℹ️ Paint regions and assign heights│
│                                     │
│  Current Regions: 0                 │
│  (No manual regions defined)        │
│                                     │
│  [+ Add Region]                     │
│                                     │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🎨 All Processing Parameters    [−]│
├─────────────────────────────────────┤
│  (Full list of all parameters)      │
│  (Similar to other modes)           │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  🔧 All Advanced Options         [−]│
├─────────────────────────────────────┤
│  (All advanced controls exposed)    │
└─────────────────────────────────────┘
```

### Manual Region Editor (Modal)

```
┌──────────────────────────────────────────────────────────┐
│  🎨 Manual Region Editor                         [X]     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────────┬───────────────────────────────────┐ │
│  │  Tools         │   Canvas (Image + Mask)           │ │
│  │                │                                   │ │
│  │ ○ Select       │   ┌─────────────────────────┐    │ │
│  │ ● Brush        │   │                         │    │ │
│  │ ○ Eraser       │   │                         │    │ │
│  │ ○ Fill         │   │   [Original Image       │    │ │
│  │ ○ Lasso        │   │    with colored         │    │ │
│  │                │   │    region overlays]     │    │ │
│  │ Brush Size:    │   │                         │    │ │
│  │ [───●──] 20px  │   │                         │    │ │
│  │                │   │                         │    │ │
│  │ Opacity:       │   └─────────────────────────┘    │ │
│  │ [────●─] 50%   │                                   │ │
│  │                │   Zoom: [─●──] 100%               │ │
│  │ [Undo] [Redo]  │   [Fit] [100%] [200%]            │ │
│  │                │                                   │ │
│  └────────────────┴───────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Regions & Heights                                 │ │
│  ├────────────────────────────────────────────────────┤ │
│  │  Region 1: Background [🎨 Blue]   Height: 0mm     │ │
│  │  Region 2: Face       [🎨 Red]    Height: 4mm     │ │
│  │  Region 3: Features   [🎨 Yellow] Height: 5mm     │ │
│  │                                                    │ │
│  │  [+ Add New Region]                                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [Cancel]  [Reset]  [Apply & Close]                     │
└──────────────────────────────────────────────────────────┘
```

**Features**:
- Paint directly on image to define regions
- Assign specific height to each region
- Color-coded overlay for visual clarity
- Support for multiple tools (brush, fill, lasso)
- Real-time 3D preview updates as regions are painted

---

## Responsive Parameter Panels (Mobile)

### Mobile Layout (< 768px)

```
┌─────────────────────────────┐
│  ⚙️ Parameters   [Collapse ▼]│
├─────────────────────────────┤
│                             │
│  Essential parameters only  │
│  (Top 3-5 most important)   │
│                             │
│  Width (mm)                 │
│  [────●────] 150            │
│                             │
│  Relief Depth (mm)          │
│  [───●─────] 3.0            │
│                             │
│  Subject Emphasis           │
│  [─────●───] 120%           │
│                             │
│  [Show All Parameters...]   │
│                             │
└─────────────────────────────┘
```

**Mobile Optimizations**:
- Show only 3-5 essential parameters by default
- "Show All" expands full list
- Larger slider thumbs (28px for touch)
- Simplified labels (shorter text)
- Collapsible by default to save screen space
- Swipe up gesture to reveal from bottom

---

## Parameter Validation & Warnings

### Real-time Validation

**Physical Constraints**:
```
⚠️ Warning: Width (250mm) exceeds typical printer bed (220mm)
   Consider reducing size or splitting model.

⚠️ Warning: Relief depth (8mm) with base (2mm) = 10mm total height.
   May require significant print time.

✓ Dimensions within safe range for most printers.
```

**Processing Constraints**:
```
⚠️ Warning: Resolution (256) may be slow to process.
   Consider using Preview Quality: Medium during adjustment.

⚠️ Warning: Minimum feature size (1mm) may be too small to print clearly.
   Recommended minimum: 2-3mm for FDM printers.

✓ Parameters optimized for quality and performance.
```

**Semantic Constraints**:
```
⚠️ Warning: No face detected in Portrait mode.
   Consider switching to Landscape or Custom mode.

⚠️ Warning: Background suppression (100%) will create flat background.
   This may affect model stability. Add base thickness.

✓ Semantic analysis successful.
```

---

## Parameter Presets System

### Preset Dropdown Component

```
┌─────────────────────────────────────┐
│  💾 Load Preset                     │
│  ┌───────────────────────────────┐ │
│  │ ▼ Select a preset...          │ │
│  └───────────────────────────────┘ │
│                                     │
│  Built-in Presets:                  │
│  • Portrait - High Detail           │
│  • Portrait - Simple                │
│  • Landscape - Dramatic             │
│  • Text - Maximum Legibility        │
│  • Diagram - Technical              │
│  ─────────────────────────────────  │
│  Custom Presets:                    │
│  • My Portrait Settings             │
│  • Museum Sign Template             │
│  ─────────────────────────────────  │
│  [📥 Import Preset File...]         │
│  [💾 Save Current as Preset...]     │
│                                     │
└─────────────────────────────────────┘
```

### Save Preset Dialog

```
┌────────────────────────────────────┐
│  💾 Save Preset                [X] │
├────────────────────────────────────┤
│                                    │
│  Preset Name:                      │
│  ┌──────────────────────────────┐ │
│  │ My Portrait Settings         │ │
│  └──────────────────────────────┘ │
│                                    │
│  Description (optional):           │
│  ┌──────────────────────────────┐ │
│  │ High detail settings for     │ │
│  │ portrait photos with clear   │ │
│  │ facial features.             │ │
│  └──────────────────────────────┘ │
│                                    │
│  Mode: Portrait                    │
│                                    │
│  Parameters to save:               │
│  ☑ All parameters                  │
│  ☐ Only modified parameters        │
│                                    │
│  Share:                            │
│  ☐ Export as file (.json)          │
│                                    │
│  [Cancel]  [Save Preset]           │
│                                    │
└────────────────────────────────────┘
```

---

## Accessibility Notes

### Screen Reader Support

**Parameter Announcements**:
- "Width slider, current value 150 millimeters, minimum 50, maximum 300"
- "Subject emphasis slider, current value 120 percent, minimum 0, maximum 200 percent"
- "Auto aspect ratio checkbox, checked"

**Mode Changes**:
- "Portrait mode selected. Parameters updated for portrait processing."

**Validation Messages**:
- "Warning: Width exceeds typical printer bed size."

### Keyboard Navigation

**Slider Controls**:
- `Left/Right Arrow`: ±1 unit
- `Shift + Left/Right`: ±10 units
- `Home`: Minimum value
- `End`: Maximum value
- `Page Up/Down`: ±10% of range

**Expand/Collapse**:
- `Enter/Space`: Toggle section
- Focus moves to first control when expanded

---

**End of Parameter Panels Documentation**
