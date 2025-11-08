# Product Requirements Document: Tactile Art Transform GUI v2.0

**Status**: Draft
**Created**: 2025-11-08
**Author**: System Analysis
**Target Users**: Blind and visually impaired individuals, educators, museums, accessibility advocates

---

## 1. Executive Summary

### Problem Statement

**Current Implementation Failure**: The existing CLI application uses photographic depth estimation, which fundamentally fails at creating meaningful tactile representations for blind users.

**Why it fails**:
- Depth estimation prioritizes photographic perspective (distant mountains appear "far")
- For the Mona Lisa example: the background landscape gets emphasized over facial features
- Blind users need SEMANTIC importance (face, people, key objects raised), not photographic depth
- No way to preview or adjust results before 3D printing (costly failure)

**Core Insight**: Tactile art is NOT about photographic realism—it's about semantic saliency and recognizability through touch.

### Proposed Solution

A GUI-based application that:
1. Uses **semantic segmentation** + **edge detection** + **saliency mapping** instead of depth estimation
2. Provides **real-time 3D preview** with orbit controls
3. Allows **interactive parameter adjustment** for different image types (portraits, landscapes, text, diagrams)
4. Generates properly scaled STL files for 3D printing
5. Supports different processing modes optimized for tactile perception

---

## 2. User Stories

### Primary User: Blind/Visually Impaired Person
> "As a blind person, I want to feel the Mona Lisa's face and expression, not the photographic depth of the background landscape"

> "As a teacher for blind students, I want to convert diagrams into tactile representations where important elements are raised and clear"

### Secondary User: Museum/Educator
> "As a museum curator, I want to create tactile versions of artwork that emphasize the subject matter, not camera perspective"

> "As an accessibility professional, I need to preview and adjust tactile models before committing to expensive 3D printing"

### Tertiary User: Researcher
> "As a researcher, I want to experiment with different height mapping strategies to understand what works best for tactile perception"

---

## 3. Core Functionality Requirements

### 3.1 Processing Modes

#### Mode 1: Portrait/People
- **Primary**: Face detection with feature emphasis (eyes, nose, mouth, ears raised)
- **Secondary**: Person segmentation (body raised, background lowered)
- **Edge enhancement**: Strong emphasis on facial boundaries and features
- **Use case**: Portraits, family photos, historical figures

#### Mode 2: Landscape/Scenery
- **Primary**: Semantic segmentation (foreground objects raised, sky/background flat)
- **Secondary**: Saliency-based (interesting objects emphasized)
- **Edge enhancement**: Moderate emphasis on object boundaries
- **Use case**: Nature scenes, cityscapes, artwork

#### Mode 3: Text/Document
- **Primary**: OCR + character detection (text highly raised)
- **Secondary**: High contrast conversion (black = raised, white = flat)
- **Edge enhancement**: Maximum sharpness for character definition
- **Use case**: Signs, documents, educational materials

#### Mode 4: Diagram/Technical
- **Primary**: Edge detection (lines and boundaries emphasized)
- **Secondary**: Region segmentation (different areas at different heights)
- **Edge enhancement**: Sharp boundaries between regions
- **Use case**: Maps, charts, technical diagrams, floor plans

#### Mode 5: Custom/Advanced
- **User-defined**: Manual region selection with height assignment
- **Hybrid processing**: Combine multiple modes
- **Fine-tuning**: All parameters exposed
- **Use case**: Complex images, artistic experimentation

### 3.2 Image Upload & Preview
- **Supported formats**: PNG, JPG, JPEG, BMP, TIFF
- **Max file size**: 20MB
- **Preview**: Side-by-side original and processed view
- **Drag-and-drop**: Support for easy file upload

### 3.3 Parameter Controls (Real-time Adjustment)

#### Physical Parameters
- **Width (mm)**: 50-300mm (default: 150mm)
- **Height (mm)**: 50-300mm (default: auto-maintain aspect ratio)
- **Base thickness (mm)**: 0.5-5mm (default: 2mm)
- **Relief depth (mm)**: 0.5-10mm (default: 3mm)
- **Edge wall thickness (mm)**: 1-10mm (default: 3mm)

#### Processing Parameters
- **Resolution**: 32-256 vertices per side (default: 128)
- **Smoothing**: 0-10 (Gaussian blur radius)
- **Edge strength**: 0-100% (edge detection intensity)
- **Contrast**: 0-200% (heightmap contrast)
- **Minimum feature size**: 1-20mm (filter small details)

#### Semantic Parameters (Mode-dependent)
- **Subject emphasis**: 0-200% (how much to raise main subject)
- **Background suppression**: 0-100% (how much to flatten background)
- **Feature sharpness**: 0-100% (edge vs smooth transitions)

### 3.4 3D Preview with Orbit Controls

#### Viewport Features
- **Orbit rotation**: Click-drag to rotate around model
- **Zoom**: Scroll to zoom in/out
- **Pan**: Shift-drag to pan view
- **Reset view**: Button to return to default viewpoint
- **Lighting**: Adjustable lighting to show surface detail

#### Visualization Options
- **Shading mode**: Solid, wireframe, or both
- **Show grid**: Reference grid for scale
- **Show measurements**: Display physical dimensions
- **Color mapping**: Height-based color gradient for clarity
- **Rotation animation**: Auto-rotate toggle

#### Preview Performance
- **Live updates**: Changes reflect in preview within 500ms
- **Progressive rendering**: Low-res preview, then high-res refinement
- **Quality toggle**: Preview quality vs performance

### 3.5 Export & Download
- **Format**: STL (ASCII and binary options)
- **Validation**: Check for non-manifold edges, holes, inverted normals
- **File size estimate**: Show expected file size before export
- **Metadata**: Embed processing parameters in STL comments
- **Batch export**: Save multiple parameter variations

---

## 4. Technical Architecture

### 4.1 Technology Stack

#### Backend (Python)
```
- Image Processing: OpenCV, scikit-image
- Semantic Segmentation: transformers (Segformer, SAM)
- Face Detection: MediaPipe, face_recognition
- Saliency Detection: cv2.saliency
- 3D Generation: NumPy, trimesh
- OCR: pytesseract, EasyOCR
```

#### Frontend (GUI)
```
Option A: Gradio (Fastest to implement)
- Built-in components for sliders, upload, 3D viewer
- Auto-generated web interface
- Good for MVP

Option B: Electron + Three.js (Most powerful)
- Custom UI/UX control
- Better 3D performance (Three.js)
- Native desktop app feel

Option C: PyQt/PySide + VTK (Desktop native)
- True desktop application
- Professional appearance
- Better for offline use
```

**Recommended**: Start with **Gradio** for rapid prototyping, migrate to **Electron + Three.js** for production.

### 4.2 Processing Pipeline

```
1. Image Upload
   └─> Load & Validate

2. Mode Selection
   └─> Configure processing pipeline

3. Preprocessing
   ├─> Resize/normalize
   ├─> Color correction
   └─> Noise reduction

4. Semantic Analysis (Mode-dependent)
   ├─> Portrait: Face detection + feature extraction
   ├─> Landscape: Semantic segmentation
   ├─> Text: OCR + character detection
   ├─> Diagram: Edge detection + region segmentation
   └─> Custom: User-defined regions

5. Height Mapping
   ├─> Assign heights based on semantic importance
   ├─> Apply edge enhancement
   ├─> Smooth according to parameters
   └─> Clamp to physical constraints

6. 3D Generation
   ├─> Create vertex grid
   ├─> Generate triangulated mesh
   ├─> Add base plate and walls
   ├─> Calculate normals
   └─> Validate mesh integrity

7. Preview Rendering
   └─> WebGL/Three.js visualization

8. Export
   └─> Generate STL with proper scaling
```

### 4.3 Key Algorithms

#### Semantic Height Assignment
```python
def calculate_semantic_heights(image, mode, params):
    """
    Assign heights based on semantic importance, not depth
    """
    if mode == "portrait":
        face_mask = detect_faces(image)
        face_features = detect_facial_landmarks(image)
        # Faces high, features highest, background low
        heightmap = base_height(params.background_height)
        heightmap += face_mask * params.subject_emphasis
        heightmap += face_features * params.feature_sharpness

    elif mode == "landscape":
        segments = semantic_segmentation(image)
        saliency = compute_saliency_map(image)
        # Important objects high, sky/background low
        heightmap = map_segments_to_heights(segments, saliency)

    elif mode == "text":
        text_mask = detect_text_regions(image)
        characters = detect_characters(image)
        # Text very high, background very low
        heightmap = params.min_height
        heightmap += characters * params.max_height

    # Apply edge enhancement
    edges = detect_edges(image, params.edge_strength)
    heightmap += edges * params.edge_emphasis

    # Smooth and normalize
    heightmap = gaussian_filter(heightmap, params.smoothing)
    heightmap = normalize_to_physical_range(heightmap, params)

    return heightmap
```

---

## 5. User Interface Design

### 5.1 Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Tactile Art Transform - v2.0                     [_ □ X]   │
├─────────────────────────────────────────────────────────────┤
│ ┌─────────────────┐  ┌─────────────────────────────────┐   │
│ │  Upload Image   │  │    Processing Mode              │   │
│ │                 │  │  ○ Portrait/People              │   │
│ │  [Drag & Drop]  │  │  ○ Landscape/Scenery            │   │
│ │   or Click      │  │  ○ Text/Document                │   │
│ │                 │  │  ○ Diagram/Technical            │   │
│ └─────────────────┘  │  ○ Custom/Advanced              │   │
│                      └─────────────────────────────────┘   │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────┐  ┌──────────────────────────────┐ │
│ │  Original Image      │  │  3D Preview (Orbit Controls) │ │
│ │                      │  │                              │ │
│ │                      │  │   [3D Model Rendering]       │ │
│ │                      │  │                              │ │
│ │                      │  │  [Reset] [Wireframe] [Grid]  │ │
│ └──────────────────────┘  └──────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│  Parameters (Live Preview)                                  │
│                                                             │
│  Physical:                                                  │
│  Width (mm):     [────●────────] 150    Auto Aspect: ☑     │
│  Relief Depth:   [──●──────────] 3.0                       │
│  Base Thickness: [───●─────────] 2.0                       │
│                                                             │
│  Processing:                                                │
│  Resolution:     [──────●──────] 128                       │
│  Smoothing:      [──●──────────] 2                         │
│  Edge Strength:  [──────●──────] 60%                       │
│                                                             │
│  Semantic:                                                  │
│  Subject Emphasis:      [────────●─] 120%                  │
│  Background Suppression:[───●──────] 40%                   │
│  Feature Sharpness:     [──────●───] 70%                   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  Status: Model ready - 7,234 triangles, 1.2 MB            │
│  [Preview Quality: ● High ○ Medium ○ Low]                  │
│  [Export STL] [Save Parameters] [Load Preset]              │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Interaction Flow

1. **User uploads image** → Auto-detect suggested mode (face detection, text detection, etc.)
2. **Select mode** → Parameters update to mode-appropriate defaults
3. **Adjust parameters** → 3D preview updates in real-time
4. **Orbit/inspect** → Rotate model to verify quality
5. **Export STL** → Download file for 3D printing

### 5.3 Presets System

**Built-in Presets**:
- "Portrait - High Detail" (fine facial features)
- "Portrait - Simple" (basic face shape)
- "Landscape - Dramatic" (strong foreground/background contrast)
- "Text - Maximum Legibility" (very sharp, high characters)
- "Diagram - Technical" (sharp edges, flat regions)
- "Art - Impressionist" (soft, flowing)

**Custom Presets**:
- Save current parameters as preset
- Export/import preset files (JSON)
- Community preset sharing

---

## 6. Success Metrics

### 6.1 Functional Metrics
- **Processing time**: < 10 seconds for 1024px image
- **Preview responsiveness**: < 500ms parameter update
- **STL validation**: 100% manifold, watertight meshes
- **File size**: < 5MB for typical 150mm × 150mm model

### 6.2 User Experience Metrics
- **First tactile print satisfaction**: > 80% "usable without adjustment"
- **Parameter adjustment frequency**: Average < 5 tweaks per image
- **Mode selection accuracy**: Auto-suggest correct in > 90% of cases
- **Time to successful print**: < 15 minutes (upload to STL)

### 6.3 Accessibility Impact Metrics
- **Tactile recognition rate**: Blind users identify subject > 70% of time
- **Feature clarity**: Can distinguish facial features, objects, text
- **Print cost efficiency**: < 2 attempts needed for satisfactory result

---

## 7. Implementation Phases

### Phase 1: MVP - Gradio Prototype (2-3 weeks)
**Goal**: Prove the concept with basic functionality

**Features**:
- ✓ Image upload (drag-and-drop)
- ✓ Portrait mode only (face detection + emphasis)
- ✓ Basic parameters (5-7 sliders)
- ✓ 3D preview (Gradio 3D component)
- ✓ STL export

**Success Criteria**:
- Can process Mona Lisa with face emphasized over background
- Preview shows 3D model with orbit controls
- STL prints successfully on standard 3D printer

### Phase 2: Multi-Mode (3-4 weeks)
**Goal**: Support different image types

**Features**:
- ✓ Landscape mode (semantic segmentation)
- ✓ Text mode (OCR + high relief)
- ✓ Diagram mode (edge detection)
- ✓ Mode auto-detection
- ✓ Extended parameters per mode

**Success Criteria**:
- Each mode produces recognizable tactile output
- Auto-detection accuracy > 85%

### Phase 3: Advanced Preview & Polish (2-3 weeks)
**Goal**: Professional user experience

**Features**:
- ✓ Enhanced 3D viewer (better lighting, materials)
- ✓ Measurement tools
- ✓ Preset system
- ✓ Batch processing
- ✓ Progress indicators
- ✓ Error handling & validation

**Success Criteria**:
- User testing shows > 80% satisfaction
- Zero crashes in 100 test sessions

### Phase 4: Production Desktop App (4-6 weeks)
**Goal**: Native desktop application

**Features**:
- ✓ Electron + Three.js frontend
- ✓ Offline functionality
- ✓ Custom UI/UX design
- ✓ Installer packages (Windows, macOS, Linux)
- ✓ Advanced semantic models
- ✓ Plugin system for custom processors

**Success Criteria**:
- Runs smoothly on mid-range hardware
- Professional appearance
- Community adoption

---

## 8. Technical Challenges & Solutions

### Challenge 1: Real-time Preview Performance
**Problem**: Regenerating 3D mesh on every parameter change is slow

**Solution**:
- Use progressive rendering (low-res preview, then refine)
- Debounce parameter changes (wait 300ms after last change)
- Pre-compute semantic maps, only regenerate heights
- WebGL optimization for smooth orbit controls

### Challenge 2: Semantic Segmentation Accuracy
**Problem**: AI models may misidentify subjects

**Solution**:
- Provide manual region selection tool (lasso/brush)
- Multiple model options (user can switch if one fails)
- Confidence indicators (show user where model is uncertain)
- "Invert" button for quick fixes

### Challenge 3: Tactile Design Knowledge Gap
**Problem**: We don't know optimal parameters for blind users

**Solution**:
- Partner with blind user testing groups
- Iterative testing with 3D printed samples
- Document research findings
- Build preset library based on real feedback
- Support community contribution of successful parameters

### Challenge 4: 3D Printing Variability
**Problem**: Different printers, materials, scales affect results

**Solution**:
- Provide printer profiles (FDM vs resin, material types)
- Scale recommendations based on printer resolution
- Validation warnings for features too small to print
- Test print generator (small sample to verify settings)

---

## 9. Dependencies

### Required Libraries (Python Backend)
```toml
dependencies = [
    "numpy>=1.24.0",
    "pillow>=10.0.0",
    "opencv-python>=4.8.0",
    "scikit-image>=0.21.0",
    "transformers>=4.35.0",
    "torch>=2.1.0",
    "trimesh>=4.0.0",
    "scipy>=1.11.0",
    "gradio>=4.0.0",  # Phase 1
    "mediapipe>=0.10.0",  # Face detection
    "pytesseract>=0.3.10",  # OCR
]
```

### Optional (Advanced Features)
```toml
optional-dependencies = [
    "segment-anything",  # Meta's SAM model
    "ultralytics",  # YOLO for object detection
    "face-recognition",  # Advanced face features
    "easyocr",  # Better OCR than tesseract
]
```

---

## 10. Open Questions for User Research

1. **Height Mapping**: Should faces be 3mm or 5mm relief? What's optimal for touch?
2. **Edge Sharpness**: Smooth transitions vs sharp boundaries - which is more recognizable?
3. **Scale**: What physical size range is most useful? (postcard vs poster size?)
4. **Detail Level**: How much detail before it becomes confusing to touch?
5. **Multi-person**: In group photos, should all faces be equal height or nearest highest?
6. **Background**: Complete suppression or gentle texture?
7. **Color mapping**: Should bright colors = higher or darker colors = higher?
8. **Text orientation**: Should braille option be added alongside visual text?

---

## 11. Future Enhancements (Post-v2.0)

- **Multi-material export**: Generate files for dual-extrusion (different textures)
- **Braille integration**: Automatic braille labels for text
- **AR preview**: View model in physical space via phone camera
- **Cloud processing**: Offload heavy computation to cloud for low-end devices
- **Educational mode**: Guided tutorials for creating tactile teaching materials
- **Gallery**: Community-shared successful tactile art with parameters
- **Accessibility**: Full screen reader support, voice control
- **API**: REST API for integration with other accessibility tools

---

## 12. Conclusion

This PRD redefines the tactile art transformation from a technical depth estimation problem to a **semantic accessibility solution**. By prioritizing what blind users need to feel over photographic realism, and providing interactive tools to refine results, we can create truly useful tactile representations of visual art and information.

The key innovation is recognizing that **tactile height should represent importance, not distance**.
