# Main Application Window - Wireframe

**Component**: Main Application Layout
**Version**: 2.0.0
**Last Updated**: 2025-11-08

---

## Overview

The main application window uses a three-column layout optimized for the tactile art transformation workflow. The design prioritizes real-time feedback with the 3D preview taking center stage.

---

## Full Application Layout (Desktop - 1440px)

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│  ╔════════════════════════════════════════════════════════════════════════════╗   │
│  ║  🎨 Tactile Art Transform v2.0              ☀️/🌙  ⚙️  ❓  👤              ║   │
│  ╚════════════════════════════════════════════════════════════════════════════╝   │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│  ┌──────────────────┬─────────────────────────────────┬─────────────────────────┐ │
│  │                  │                                 │                         │ │
│  │  LEFT PANEL      │     CENTER PANEL                │     RIGHT PANEL         │ │
│  │  (360px)         │     (720px)                     │     (360px)             │ │
│  │                  │                                 │                         │ │
│  ├──────────────────┤                                 │                         │ │
│  │                  │                                 │                         │ │
│  │ ┌──────────────┐ │  ┌─────────────────────────┐   │  ┌────────────────────┐ │ │
│  │ │  📁 UPLOAD   │ │  │                         │   │  │   ⚙️ PARAMETERS    │ │ │
│  │ │              │ │  │    3D PREVIEW           │   │  │                    │ │ │
│  │ │ ┌──────────┐ │ │  │    (WebGL Viewport)     │   │  │  Physical          │ │ │
│  │ │ │          │ │ │  │                         │   │  │  ▔▔▔▔▔▔▔▔          │ │ │
│  │ │ │  Drag &  │ │ │  │                         │   │  │  Width (mm)        │ │ │
│  │ │ │   Drop   │ │ │  │     [3D Model]          │   │  │  [─────●──────] 150│ │ │
│  │ │ │          │ │ │  │                         │   │  │                    │ │ │
│  │ │ │  or      │ │ │  │                         │   │  │  Relief Depth (mm) │ │ │
│  │ │ │          │ │ │  │                         │   │  │  [───●────────] 3.0│ │ │
│  │ │ │ [Browse] │ │ │  │                         │   │  │                    │ │ │
│  │ │ └──────────┘ │ │  │                         │   │  │  Base Thickness    │ │ │
│  │ │              │ │  │                         │   │  │  [────●───────] 2.0│ │ │
│  │ │ PNG, JPG,    │ │  └─────────────────────────┘   │  │                    │ │ │
│  │ │ TIFF, BMP    │ │                                 │  │  ☑ Auto Aspect     │ │ │
│  │ │ Max: 20MB    │ │  ┌─────────────────────────┐   │  │                    │ │ │
│  │ └──────────────┘ │  │  🎮 VIEWPORT CONTROLS   │   │  ├────────────────────┤ │ │
│  │                  │  │                         │   │  │  Processing        │ │ │
│  │ ┌──────────────┐ │  │  [🔄 Reset View]       │   │  │  ▔▔▔▔▔▔▔▔▔▔        │ │ │
│  │ │  📋 MODE     │ │  │  [📐 Grid] [🔲 Wire]   │   │  │  Resolution        │ │ │
│  │ │              │ │  │  [📏 Measure] [🔆 Sun] │   │  │  [─────●──────] 128│ │ │
│  │ │ ● Portrait   │ │  │  [▶️ Rotate: OFF]      │   │  │                    │ │ │
│  │ │   /People    │ │  │                         │   │  │  Smoothing         │ │ │
│  │ │              │ │  └─────────────────────────┘   │  │  [──●─────────]  2 │ │ │
│  │ │ ○ Landscape  │ │                                 │  │                    │ │ │
│  │ │   /Scenery   │ │  ┌─────────────────────────┐   │  │  Edge Strength     │ │ │
│  │ │              │ │  │  🖼️  ORIGINAL IMAGE     │   │  │  [─────●──────] 60%│ │ │
│  │ │ ○ Text       │ │  │                         │   │  │                    │ │ │
│  │ │   /Document  │ │  │  ┌───────────────────┐ │   │  │  Contrast          │ │ │
│  │ │              │ │  │  │                   │ │   │  │  [──────●─────] 100%│││
│  │ │ ○ Diagram    │ │  │  │   [Thumbnail]     │ │   │  │                    │ │ │
│  │ │   /Technical │ │  │  │                   │ │   │  ├────────────────────┤ │ │
│  │ │              │ │  │  │   mona_lisa.jpg   │ │   │  │  Semantic          │ │ │
│  │ │ ○ Custom     │ │  │  │   1024 × 768      │ │   │  │  ▔▔▔▔▔▔▔▔          │ │ │
│  │ │   /Advanced  │ │  │  │                   │ │   │  │  Subject Emphasis  │ │ │
│  │ │              │ │  │  └───────────────────┘ │   │  │  [───────●────] 120%│││
│  │ └──────────────┘ │  │                         │   │  │                    │ │ │
│  │                  │  │  Detected:              │   │  │  Background        │ │ │
│  │ ┌──────────────┐ │  │  ✓ Face found          │   │  │  Suppression       │ │ │
│  │ │  💾 PRESETS  │ │  │  Mode: Portrait ✓      │   │  │  [───●────────] 40%│ │ │
│  │ │              │ │  │                         │   │  │                    │ │ │
│  │ │ [▼ Select]   │ │  └─────────────────────────┘   │  │  Feature Sharpness │ │ │
│  │ │              │ │                                 │  │  [─────●──────] 70%│ │ │
│  │ │ Portrait -   │ │                                 │  │                    │ │ │
│  │ │ High Detail  │ │                                 │  └────────────────────┘ │ │
│  │ │              │ │                                 │                         │ │
│  │ │ [💾 Save]    │ │                                 │                         │ │
│  │ │ [📥 Load]    │ │                                 │                         │ │
│  │ └──────────────┘ │                                 │                         │ │
│  │                  │                                 │                         │ │
│  └──────────────────┴─────────────────────────────────┴─────────────────────────┘ │
│                                                                                    │
├────────────────────────────────────────────────────────────────────────────────────┤
│  ╔════════════════════════════════════════════════════════════════════════════╗   │
│  ║  📊 Status: Model ready • 7,234 triangles • 1.2 MB • Est. print time: 45min║   │
│  ║                                                                            ║   │
│  ║  Preview Quality:  ● High  ○ Medium  ○ Low                                ║   │
│  ║                                                                            ║   │
│  ║  [⬇️ Export STL]  [💾 Save Parameters]  [⚠️ Validate Mesh]               ║   │
│  ╚════════════════════════════════════════════════════════════════════════════╝   │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Panel Specifications

### Header Bar (Top)

**Dimensions**: Full width × 64px
**Background**: Primary-500 (brand blue)
**Text Color**: White

**Elements** (left to right):
1. **App Title & Logo** (left)
   - Icon: 🎨 (32px)
   - Text: "Tactile Art Transform v2.0" (20px, semi-bold)
   - Spacing: 16px padding

2. **Utility Controls** (right, 16px gap)
   - Theme Toggle: Sun/Moon icon button (32px)
   - Settings: Gear icon button (32px)
   - Help: Question mark icon button (32px)
   - User Profile: Avatar or user icon (32px, circular)

**Accessibility**:
- All icon buttons have aria-labels
- Keyboard navigable (Tab order)
- Focus indicators visible (white ring)

---

### Left Panel (360px width)

**Background**: Gray-50 (light) / Dark-800 (dark)
**Padding**: 24px
**Border Right**: 1px solid Gray-300

#### Upload Section

**Dimensions**: 360px × 280px (including padding)
**Background**: White card with dashed border (Gray-400)
**Border Radius**: 8px

**Drag & Drop Zone**:
- Active state: Solid border (Primary-500), light blue background
- Hover: Border color darkens
- Icon: 📁 (48px, centered)
- Text: "Drag & Drop" (16px, centered)
- Subtext: "or" (14px, gray-600)
- Button: "Browse" (Primary button, centered)
- Format info: "PNG, JPG, TIFF, BMP" (12px, gray-600)
- Size limit: "Max: 20MB" (12px, gray-600)

#### Mode Selection

**Dimensions**: 360px × auto
**Spacing**: 24px from Upload section

**Radio Group**:
- Label: "Processing Mode" (16px, semi-bold)
- Options: 5 radio buttons (vertical stack, 16px gap)
  1. ● Portrait/People
  2. ○ Landscape/Scenery
  3. ○ Text/Document
  4. ○ Diagram/Technical
  5. ○ Custom/Advanced

- Each option: 20px radio + 12px gap + label (14px)
- Active: Primary-500, semi-bold text
- Inactive: Gray-600, regular text

**Behavior**:
- Single selection
- Auto-select based on image analysis
- Changing mode updates parameter defaults

#### Presets Section

**Dimensions**: 360px × auto
**Spacing**: 24px from Mode section

**Dropdown**:
- Label: "Presets" (16px, semi-bold)
- Select: Full width, 40px height
- Options: Built-in presets (Portrait - High Detail, etc.)
- Placeholder: "Select a preset..."

**Buttons** (horizontal, 12px gap):
- [💾 Save]: Save current parameters
- [📥 Load]: Load preset file

---

### Center Panel (720px width)

**Background**: Gray-100 (light) / Dark-900 (dark)
**Padding**: 24px

#### 3D Preview Viewport

**Dimensions**: 720px × 540px
**Background**: Dark gradient (for contrast)
**Border**: 1px solid Gray-300
**Border Radius**: 8px

**3D Canvas**:
- WebGL rendering
- Default view: Isometric, 45° rotation
- Lighting: Three-point lighting setup
- Grid: Optional, toggleable
- Axes: Optional, XYZ colored

**Interactions**:
- **Orbit**: Left-click drag (cursor: grab → grabbing)
- **Zoom**: Mouse wheel (scale: 0.5x - 5x)
- **Pan**: Shift + drag or middle-mouse drag
- **Touch** (mobile): 1-finger rotate, 2-finger pinch zoom, 2-finger pan

**Overlay Elements**:
- Measurements (if enabled): Dimensions in mm, yellow text
- Performance: FPS counter (top-left, 12px, gray-400)

#### Viewport Controls

**Dimensions**: 720px × 60px
**Background**: White card
**Border Radius**: 6px
**Padding**: 12px
**Spacing**: 12px gap between buttons

**Buttons** (horizontal layout):
1. [🔄 Reset View]: Return to default camera position
2. [📐 Grid]: Toggle reference grid (active state: Primary-500)
3. [🔲 Wireframe]: Toggle wireframe overlay (active state: Primary-500)
4. [📏 Measure]: Toggle measurement display (active state: Primary-500)
5. [🔆 Lighting]: Adjust lighting intensity (slider popover)
6. [▶️ Rotate]: Toggle auto-rotation (active state: Primary-500, shows "ON")

**Button Size**: 40px height, auto width, 12px padding

#### Original Image Panel

**Dimensions**: 720px × 320px
**Background**: White card
**Border Radius**: 8px
**Padding**: 16px
**Spacing**: 24px from viewport controls

**Image Preview**:
- Thumbnail: Centered, max 280px × 200px (maintain aspect)
- Border: 1px solid Gray-300
- Shadow: shadow-sm

**Metadata** (below image):
- Filename: "mona_lisa.jpg" (14px, semi-bold)
- Dimensions: "1024 × 768" (12px, gray-600)
- File size: "2.3 MB" (12px, gray-600)

**Analysis Results**:
- Badge: "✓ Face found" (success badge, green)
- Suggested mode: "Mode: Portrait ✓" (12px, primary-500)
- Confidence: "95% confident" (12px, gray-600)

---

### Right Panel (360px width)

**Background**: Gray-50 (light) / Dark-800 (dark)
**Padding**: 24px
**Border Left**: 1px solid Gray-300
**Scroll**: Vertical scroll if content exceeds viewport

#### Parameters Section (Collapsible Groups)

Each parameter group is collapsible for progressive disclosure.

**Physical Parameters** (Expanded by default)
- Header: "Physical" (16px, semi-bold) + collapse icon
- Spacing: 20px between sliders

Sliders (each):
1. **Width (mm)**
   - Range: 50-300mm
   - Default: 150mm
   - Step: 5mm
   - Label: Above slider (14px)
   - Current value: Above thumb (14px, semi-bold, primary-500)
   - Min/Max: At track ends (11px, gray-600)

2. **Relief Depth (mm)**
   - Range: 0.5-10mm
   - Default: 3.0mm
   - Step: 0.1mm

3. **Base Thickness (mm)**
   - Range: 0.5-5mm
   - Default: 2.0mm
   - Step: 0.1mm

4. **Auto Aspect Ratio** (Checkbox)
   - Label: "Auto Aspect" (14px)
   - Checked by default
   - When checked: Height auto-calculated

**Processing Parameters** (Collapsed by default)
- Header: "Processing" + collapse icon
- Same slider layout

1. **Resolution**: 32-256 (default: 128)
2. **Smoothing**: 0-10 (default: 2)
3. **Edge Strength**: 0-100% (default: 60%)
4. **Contrast**: 0-200% (default: 100%)

**Semantic Parameters** (Expanded, mode-dependent)
- Header: "Semantic" + collapse icon
- Changes based on selected mode

1. **Subject Emphasis**: 0-200% (default: 120%)
2. **Background Suppression**: 0-100% (default: 40%)
3. **Feature Sharpness**: 0-100% (default: 70%)

**Slider Specifications**:
- Track height: 4px
- Thumb size: 20px diameter
- Active track: Primary-500
- Inactive track: Gray-300
- Hover: Thumb scale 1.1
- Focus: 3px focus ring

---

### Status Bar (Bottom)

**Dimensions**: Full width × 120px
**Background**: White (light) / Dark-800 (dark)
**Border Top**: 1px solid Gray-300
**Padding**: 20px

**Top Row**: Status Information
- Icon: 📊 (24px)
- Text: "Model ready • 7,234 triangles • 1.2 MB • Est. print time: 45min"
- Font: 14px, regular
- Color: Gray-700

**Middle Row**: Preview Quality Toggle
- Label: "Preview Quality:" (14px, gray-600)
- Radio group (horizontal):
  - ● High
  - ○ Medium
  - ○ Low
- Affects 3D viewport resolution

**Bottom Row**: Action Buttons (horizontal, right-aligned, 16px gap)
1. **[⬇️ Export STL]** (Primary button, large)
   - Most prominent action
   - Icon + text
   - Keyboard shortcut: Ctrl+E

2. **[💾 Save Parameters]** (Secondary button)
   - Save current settings as JSON
   - Keyboard shortcut: Ctrl+S

3. **[⚠️ Validate Mesh]** (Secondary button)
   - Check mesh integrity before export
   - Shows validation results in modal

---

## Responsive Behavior

### Tablet (768px - 1024px)

```
┌─────────────────────────────────────────┐
│  Header (full width)                    │
├─────────────────────────────────────────┤
│  ┌───────────┬─────────────────────┐   │
│  │ Left Panel│   Center Panel      │   │
│  │ (300px)   │   (468px)           │   │
│  │           │                     │   │
│  │ Upload    │   3D Preview        │   │
│  │ Mode      │   (larger)          │   │
│  │ Presets   │                     │   │
│  │           │   Controls          │   │
│  │           │   Original Image    │   │
│  └───────────┴─────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Parameters (full width, below)  │   │
│  │ (collapsible accordion)         │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  Status Bar (full width)                │
└─────────────────────────────────────────┘
```

**Changes**:
- Two-column layout (left + center)
- Parameters move below as accordion
- Reduced panel widths
- Smaller 3D viewport (468px)

### Mobile (<768px)

```
┌──────────────────────────┐
│  Header (compact)        │
├──────────────────────────┤
│  Upload Section          │
│  (full width)            │
├──────────────────────────┤
│  Mode Selection          │
│  (horizontal tabs)       │
├──────────────────────────┤
│  3D Preview              │
│  (full width, 4:3)       │
│  Controls (bottom bar)   │
├──────────────────────────┤
│  Original Image          │
│  (thumbnail + info)      │
├──────────────────────────┤
│  Parameters              │
│  (bottom sheet, slide up)│
│  Essential only          │
├──────────────────────────┤
│  Action Buttons          │
│  (fixed bottom)          │
└──────────────────────────┘
```

**Changes**:
- Single column, vertical stack
- Upload area collapsed by default (show when no image)
- Mode selection: Horizontal tabs instead of radio
- 3D viewport: Full width, 4:3 aspect ratio
- Touch gestures for 3D control
- Parameters: Bottom sheet (swipe up to reveal)
- Reduced parameter count (essential only)
- Action buttons: Fixed position bottom bar

---

## Keyboard Navigation Flow

**Tab Order** (desktop):
1. Theme toggle
2. Settings button
3. Help button
4. User profile
5. Upload button
6. Mode radio group (5 items)
7. Preset dropdown
8. Save preset button
9. Load preset button
10. 3D viewport (focus for keyboard controls)
11. Viewport control buttons (6 items)
12. All parameter sliders (sequential)
13. Preview quality radio (3 items)
14. Export button
15. Save parameters button
16. Validate mesh button

**Keyboard Shortcuts**:
- `Tab`: Next element
- `Shift+Tab`: Previous element
- `Enter/Space`: Activate button/toggle
- `Arrow keys`: Navigate sliders, radio groups
- `Esc`: Close modals, deselect
- `Ctrl+O`: Open file dialog
- `Ctrl+E`: Export STL
- `Ctrl+S`: Save parameters

---

## State Management

### Application States

1. **Empty State** (no image loaded)
   - Upload area prominent
   - 3D viewport shows placeholder
   - Parameters disabled (grayed out)
   - Export button disabled

2. **Loading State** (image processing)
   - Upload area shows progress
   - 3D viewport shows spinner
   - Parameters disabled
   - Status: "Processing..."

3. **Ready State** (image processed)
   - 3D model visible
   - Parameters enabled
   - Export button enabled
   - Status shows model info

4. **Error State** (processing failed)
   - Error message in viewport
   - Retry button
   - Upload area available
   - Status shows error details

5. **Exporting State** (generating STL)
   - Modal overlay with progress
   - "Generating STL..." message
   - Cancel button
   - Estimated time remaining

---

## Interactions & Animations

### Upload Interaction
1. User drags file over drop zone
2. Border changes to solid Primary-500
3. Background changes to Primary-50
4. On drop: Upload animation (progress bar)
5. Success: Fade to image preview + analysis

### Mode Change
1. User selects different mode
2. Parameters fade out (200ms)
3. New parameters fade in (200ms)
4. 3D model regenerates (preview quality)
5. Full quality render after 500ms

### Parameter Adjustment
1. User drags slider
2. Value updates in real-time (on thumb)
3. Debounce: Wait 300ms after last change
4. Generate low-res preview (100ms)
5. Generate high-res preview (500ms)
6. 3D viewport smoothly updates

### 3D Viewport Interaction
1. Hover: Cursor changes to grab
2. Mouse down: Cursor changes to grabbing
3. Drag: Model rotates smoothly (60fps)
4. Release: Momentum continues briefly (easing)
5. Zoom: Smooth scale transition (200ms)

---

## Accessibility Features

### Screen Reader Announcements

- **Image uploaded**: "Image uploaded successfully: mona_lisa.jpg, 1024 by 768 pixels"
- **Mode changed**: "Processing mode changed to Portrait. Parameters updated."
- **Parameter adjusted**: "Width set to 150 millimeters"
- **Model updated**: "3D model updated. 7,234 triangles."
- **Export started**: "Exporting STL file. Please wait."
- **Export complete**: "STL file exported successfully. File size: 1.2 megabytes."

### High Contrast Mode

- Respect Windows High Contrast settings
- Increase border weights
- Force high contrast colors
- Remove subtle shadows
- Stronger focus indicators

### Keyboard-Only Operation

- Full functionality without mouse
- Clear focus indicators (3px blue ring)
- Skip links ("Skip to preview", "Skip to parameters")
- Focus trap in modals
- Logical tab order

---

## Performance Targets

- **Initial load**: < 2 seconds
- **Image upload**: < 1 second for 5MB file
- **Image processing**: < 5 seconds for 1024px image
- **3D preview generation**: < 500ms (low quality), < 2s (high quality)
- **Parameter change**: < 300ms to see effect
- **STL export**: < 5 seconds for 150mm model
- **60 FPS**: 3D viewport during interaction
- **Memory**: < 500MB RAM for typical workflow

---

## Error Handling

### Upload Errors
- **File too large**: "File exceeds 20MB limit. Please use a smaller image."
- **Invalid format**: "Unsupported file format. Please use PNG, JPG, TIFF, or BMP."
- **Corrupted file**: "Unable to read file. File may be corrupted."

### Processing Errors
- **No face found** (Portrait mode): "No face detected. Try Landscape mode or Custom mode."
- **Processing failed**: "Processing failed. Please try again or contact support."

### Export Errors
- **Non-manifold mesh**: "Mesh contains errors. Click 'Validate Mesh' to see details."
- **File system error**: "Unable to save file. Check disk space and permissions."

### Display
- Toast notifications for non-critical errors
- Modal dialogs for critical errors requiring action
- Inline validation messages for form inputs

---

**End of Main Application Wireframe**
