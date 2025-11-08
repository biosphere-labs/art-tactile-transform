# 3D Viewer Component Specification

**Component**: 3D Preview Viewport with Interactive Controls
**Version**: 2.0.0
**Last Updated**: 2025-11-08
**Technology**: Three.js (WebGL)

---

## Table of Contents

1. [Overview](#overview)
2. [Visual Layout](#visual-layout)
3. [Camera Controls](#camera-controls)
4. [Lighting Setup](#lighting-setup)
5. [Material & Shading](#material--shading)
6. [Measurement Tools](#measurement-tools)
7. [Grid & Axis Helpers](#grid--axis-helpers)
8. [Interaction States](#interaction-states)
9. [Performance Optimization](#performance-optimization)
10. [Accessibility](#accessibility)

---

## Overview

The 3D viewer is the central component for previewing tactile art models before export. It provides real-time visualization with orbit controls, multiple shading modes, and measurement tools to verify the model is ready for 3D printing.

**Key Features**:
- Real-time WebGL rendering (60 FPS target)
- Orbit/pan/zoom camera controls
- Multiple visualization modes (solid, wireframe, heightmap)
- Measurement overlays
- Grid and axis helpers
- Auto-rotation option
- Screenshot capability

---

## Visual Layout

### Viewport Container

```
┌─────────────────────────────────────────────────────────────────┐
│  3D Preview                                          [📷] [⚙️]  │  (Header)
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                                                                 │
│         ┌───────────────────────────────────────────┐          │
│         │                                           │          │
│         │                                           │          │
│         │            [3D Model]                     │          │
│         │                                           │          │
│         │         Y↑                                │          │
│         │         │                                 │          │
│         │         │                                 │          │
│         │         └─────→ X                         │          │
│         │        ╱                                  │          │
│         │       Z                                   │          │
│         │                                           │          │
│         │                                           │          │
│         │                                           │          │
│         └───────────────────────────────────────────┘          │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  FPS: 60 │ Tris: 7,234 │ Zoom: 100% │ Info: 150×112×5mm│  │  (Status bar)
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  [🔄 Reset] [📐 Grid] [🔲 Wire] [📏 Measure] [🔆 Light] [▶️ Rotate]│  (Controls)
└─────────────────────────────────────────────────────────────────┘
```

**Dimensions**:
- Desktop: 720px × 540px (4:3 aspect ratio)
- Tablet: 600px × 450px
- Mobile: Full width × 4:3 aspect ratio

**Background**:
- Gradient: Dark top (#1a1a1a) to lighter bottom (#2a2a2a)
- Alternative: Solid dark gray (#1e1e1e)
- Light mode: Light gradient (#f0f0f0 to #ffffff)

**Border**:
- 1px solid Gray-300
- Slight shadow (shadow-sm)
- Rounded corners (8px)

---

## Camera Controls

### Default Camera Setup

```javascript
// Initial camera position (Three.js)
camera = new THREE.PerspectiveCamera(
  50,              // FOV (degrees)
  aspect,          // aspect ratio
  0.1,             // near clipping plane
  1000             // far clipping plane
);

// Default position: Isometric-like view
camera.position.set(
  150,  // X: to the right
  100,  // Y: above
  150   // Z: in front
);
camera.lookAt(0, 0, 0);  // Look at center
```

### Orbit Controls

**Mouse/Desktop**:
```
Left-click + drag:     Orbit (rotate around model)
Scroll wheel:          Zoom in/out
Middle-click + drag:   Pan (move camera laterally)
Shift + left-drag:     Pan (alternative)
Right-click + drag:    Pan (alternative)
Double-click:          Auto-center on click point
```

**Touch/Mobile**:
```
One-finger drag:       Orbit
Two-finger pinch:      Zoom
Two-finger drag:       Pan
Double-tap:            Reset view
```

**Keyboard** (for accessibility):
```
Arrow keys:            Orbit (5° increments)
+ / -:                 Zoom in/out
Shift + Arrows:        Pan
Home:                  Reset to default view
Space:                 Toggle auto-rotation
```

### Camera Constraints

```javascript
// Orbit constraints
controls.minDistance = 50;   // Minimum zoom (close)
controls.maxDistance = 500;  // Maximum zoom (far)
controls.minPolarAngle = 0;  // Can view from directly above
controls.maxPolarAngle = Math.PI;  // Can view from below

// Damping (smooth motion)
controls.enableDamping = true;
controls.dampingFactor = 0.05;

// Auto-rotate (optional)
controls.autoRotate = false;  // Off by default
controls.autoRotateSpeed = 1.0;  // Revolutions per minute
```

### Camera Presets

**Preset Views** (quick access buttons):
```
[Top View]     - Camera at (0, 200, 0), looking down
[Front View]   - Camera at (0, 0, 200), looking at front
[Side View]    - Camera at (200, 0, 0), looking from side
[Isometric]    - Default (150, 100, 150)
```

---

## Lighting Setup

### Three-Point Lighting System

```javascript
// 1. Key Light (main illumination)
const keyLight = new THREE.DirectionalLight(0xffffff, 1.0);
keyLight.position.set(100, 100, 100);
keyLight.castShadow = true;
scene.add(keyLight);

// 2. Fill Light (soften shadows)
const fillLight = new THREE.DirectionalLight(0xffffff, 0.5);
fillLight.position.set(-50, 50, -50);
scene.add(fillLight);

// 3. Rim/Back Light (edge definition)
const rimLight = new THREE.DirectionalLight(0xffffff, 0.3);
rimLight.position.set(0, 100, -100);
scene.add(rimLight);

// 4. Ambient Light (overall illumination)
const ambientLight = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambientLight);
```

### Shadow Configuration

```javascript
// Enable shadows for depth perception
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;

// Key light shadow settings
keyLight.shadow.camera.left = -200;
keyLight.shadow.camera.right = 200;
keyLight.shadow.camera.top = 200;
keyLight.shadow.camera.bottom = -200;
keyLight.shadow.camera.near = 0.5;
keyLight.shadow.camera.far = 500;
keyLight.shadow.mapSize.width = 2048;  // Shadow quality
keyLight.shadow.mapSize.height = 2048;
```

### Adjustable Lighting Control

**Lighting Panel** (popover from [🔆 Light] button):
```
┌────────────────────────────────┐
│  Lighting Controls             │
├────────────────────────────────┤
│                                │
│  Overall Brightness            │
│  [───────●────] 100%           │
│                                │
│  Shadow Intensity              │
│  [─────●──────] 60%            │
│                                │
│  Ambient Light                 │
│  [────●───────] 40%            │
│                                │
│  ☑ Enable shadows              │
│  ☐ High quality shadows        │
│    (slower performance)        │
│                                │
│  [Reset to Defaults]           │
│                                │
└────────────────────────────────┘
```

---

## Material & Shading

### Material Definitions

**Standard Material** (default):
```javascript
const material = new THREE.MeshStandardMaterial({
  color: 0x8a8a8a,         // Neutral gray
  roughness: 0.7,          // Slightly rough (realistic plastic)
  metalness: 0.0,          // Non-metallic
  flatShading: false,      // Smooth shading
  side: THREE.DoubleSide,  // Render both sides
});
```

**Height-Colored Material** (shows height variation):
```javascript
// Gradient from low (blue) to high (red)
const colorRamp = [
  { height: 0.0, color: new THREE.Color(0x1a1a5a) },   // Deep blue
  { height: 0.25, color: new THREE.Color(0x0066cc) },  // Blue
  { height: 0.50, color: new THREE.Color(0x00aa44) },  // Green
  { height: 0.75, color: new THREE.Color(0xffaa00) },  // Orange
  { height: 1.0, color: new THREE.Color(0xdd0000) }    // Red
];

// Apply vertex colors based on height
geometry.setAttribute('color',
  new THREE.BufferAttribute(computeVertexColors(geometry), 3)
);

const material = new THREE.MeshStandardMaterial({
  vertexColors: true,
  roughness: 0.7,
  metalness: 0.0
});
```

### Visualization Modes

**Mode Toggle** (radio group in controls):
```
● Solid       - Standard shaded view
○ Height Map  - Color-coded by height
○ Wireframe   - Edge mesh only
○ Both        - Wireframe overlay on solid
```

**Wireframe Material**:
```javascript
const wireframeMaterial = new THREE.LineBasicMaterial({
  color: 0x00ff00,     // Green lines
  linewidth: 1,        // Pixel width
  transparent: true,
  opacity: 0.5         // Semi-transparent
});
```

**Combined View** (solid + wireframe):
```javascript
// Two meshes: one solid, one wireframe
const solidMesh = new THREE.Mesh(geometry, solidMaterial);
const wireframeMesh = new THREE.LineSegments(
  new THREE.EdgesGeometry(geometry),
  wireframeMaterial
);

group.add(solidMesh);
group.add(wireframeMesh);
```

---

## Measurement Tools

### Dimension Annotations

**Measurement Overlay** (when enabled):
```
       ↔────── 150mm ──────↕
       ┌──────────────────┐ │
       │                  │ │
       │                  │ 112mm
       │     [Model]      │ │
       │                  │ │
       └──────────────────┘ │
                            ↕

       Height: 5mm (base: 2mm + relief: 3mm)
```

**Implementation**:
```javascript
// Create text sprites for measurements
function createMeasurementLabel(text, position) {
  const canvas = document.createElement('canvas');
  const context = canvas.getContext('2d');
  canvas.width = 256;
  canvas.height = 64;

  // Draw text
  context.fillStyle = '#FFD700';  // Gold color
  context.font = 'Bold 24px Arial';
  context.textAlign = 'center';
  context.fillText(text, 128, 40);

  // Create texture and sprite
  const texture = new THREE.CanvasTexture(canvas);
  const spriteMaterial = new THREE.SpriteMaterial({ map: texture });
  const sprite = new THREE.Sprite(spriteMaterial);
  sprite.position.copy(position);
  sprite.scale.set(20, 5, 1);  // Billboard size

  return sprite;
}

// Add dimension lines and labels
const widthLabel = createMeasurementLabel(
  `${width}mm`,
  new THREE.Vector3(0, height + 10, 0)
);
scene.add(widthLabel);
```

### Interactive Measurement Tool

**Click-to-Measure Mode**:
```
User flow:
1. Click [📏 Measure] button
2. Cursor changes to crosshair
3. Click two points on model
4. Distance line appears between points
5. Distance label shows measurement in mm
6. Click [📏 Measure] again to deactivate
```

**Measurement Line Rendering**:
```javascript
function addMeasurementLine(pointA, pointB) {
  const distance = pointA.distanceTo(pointB);

  // Create line
  const geometry = new THREE.BufferGeometry().setFromPoints([pointA, pointB]);
  const material = new THREE.LineBasicMaterial({
    color: 0xFFD700,  // Gold
    linewidth: 2
  });
  const line = new THREE.Line(geometry, material);
  scene.add(line);

  // Add distance label at midpoint
  const midpoint = new THREE.Vector3().lerpVectors(pointA, pointB, 0.5);
  const label = createMeasurementLabel(
    `${distance.toFixed(2)}mm`,
    midpoint
  );
  scene.add(label);
}
```

---

## Grid & Axis Helpers

### Reference Grid

**Ground Grid** (when enabled):
```javascript
const gridSize = 200;       // Total size
const gridDivisions = 20;   // Number of divisions
const gridHelper = new THREE.GridHelper(
  gridSize,
  gridDivisions,
  0x444444,  // Center line color
  0x222222   // Grid line color
);
gridHelper.position.y = -baseThickness;  // Below model
scene.add(gridHelper);
```

**Visual Appearance**:
```
Grid spacing: 10mm (200mm / 20 divisions)
Center lines: Slightly brighter
Grid color: Dark gray (subtle, not distracting)
Transparency: Optional (50% opacity)
```

### Axis Helper

**XYZ Axis Indicator**:
```javascript
const axisHelper = new THREE.AxesHelper(50);  // 50mm long arrows
scene.add(axisHelper);

// Standard coloring:
// Red: X-axis (left/right)
// Green: Y-axis (up/down)
// Blue: Z-axis (forward/back)
```

**Labeled Axes** (custom implementation):
```
         Y
         ↑ (Green)
         │
         │
         └─────→ X (Red)
        ╱
       ╱
      Z (Blue)

With labels: "X", "Y", "Z" at arrow tips
```

### Measurement Grid Overlay

**Optional: Print Bed Outline**:
```javascript
// Show common printer bed sizes for reference
function addPrinterBedOutline(size = 220) {  // 220mm = common Ender 3
  const shape = new THREE.Shape();
  shape.moveTo(-size/2, -size/2);
  shape.lineTo(size/2, -size/2);
  shape.lineTo(size/2, size/2);
  shape.lineTo(-size/2, size/2);
  shape.lineTo(-size/2, -size/2);

  const geometry = new THREE.ShapeGeometry(shape);
  const material = new THREE.LineBasicMaterial({
    color: 0xff8800,  // Orange (warning if exceeds)
    linewidth: 2
  });
  const outline = new THREE.Line(geometry, material);
  outline.rotation.x = -Math.PI / 2;  // Rotate to horizontal
  outline.position.y = -baseThickness - 0.5;
  scene.add(outline);
}
```

---

## Interaction States

### Hover State

**On Viewport Hover**:
```css
cursor: grab;  /* Show grabbable cursor */
```

**While Dragging**:
```css
cursor: grabbing;  /* Show grabbing cursor */
```

**Measurement Mode**:
```css
cursor: crosshair;  /* Show measurement cursor */
```

### Loading State

**While Processing**:
```
┌─────────────────────────────────────┐
│                                     │
│          [Spinner Animation]        │
│                                     │
│       Generating 3D preview...      │
│                                     │
│       [████████░░] 80%              │
│                                     │
└─────────────────────────────────────┘
```

**Progressive Rendering**:
1. Show low-res preview first (32×32 grid) - immediate
2. Refine to medium (64×64) - 200ms later
3. Final high-res (128×128 or user setting) - 500ms later

### Empty State

**No Model Loaded**:
```
┌─────────────────────────────────────┐
│                                     │
│            [📦 Icon]                │
│                                     │
│      No model loaded yet            │
│                                     │
│   Upload an image to see 3D preview │
│                                     │
└─────────────────────────────────────┘
```

### Error State

**Processing Failed**:
```
┌─────────────────────────────────────┐
│                                     │
│            [⚠️ Icon]                │
│                                     │
│     Failed to generate preview      │
│                                     │
│         [Retry]  [Report]           │
│                                     │
└─────────────────────────────────────┘
```

---

## Performance Optimization

### Level of Detail (LOD)

```javascript
// Use lower resolution during interaction, high-res when still
let interactionTimeout;
let isInteracting = false;

controls.addEventListener('change', () => {
  if (!isInteracting) {
    // Switch to low-res model
    switchToLOD('low');
    isInteracting = true;
  }

  clearTimeout(interactionTimeout);
  interactionTimeout = setTimeout(() => {
    // Switch back to high-res after 500ms of no interaction
    switchToLOD('high');
    isInteracting = false;
  }, 500);
});
```

### Frame Rate Management

```javascript
// Adaptive quality based on FPS
let fps = 60;
let frameCount = 0;
let lastTime = performance.now();

function monitorFPS() {
  frameCount++;
  const currentTime = performance.now();

  if (currentTime >= lastTime + 1000) {
    fps = frameCount;
    frameCount = 0;
    lastTime = currentTime;

    // If FPS drops below 30, reduce quality
    if (fps < 30) {
      renderer.setPixelRatio(1);  // Lower pixel ratio
      reduceQuality();
    } else if (fps > 55) {
      renderer.setPixelRatio(window.devicePixelRatio);
      restoreQuality();
    }
  }
}
```

### Rendering Optimizations

```javascript
// Only render when needed (not continuously)
let needsRender = false;

controls.addEventListener('change', () => {
  needsRender = true;
});

function animate() {
  requestAnimationFrame(animate);

  if (needsRender || controls.autoRotate) {
    controls.update();
    renderer.render(scene, camera);
    needsRender = false;
  }
}
```

### Memory Management

```javascript
// Dispose of old geometry when loading new model
function disposeModel(model) {
  model.traverse((object) => {
    if (object.geometry) {
      object.geometry.dispose();
    }
    if (object.material) {
      if (Array.isArray(object.material)) {
        object.material.forEach(material => material.dispose());
      } else {
        object.material.dispose();
      }
    }
  });
}
```

---

## Accessibility

### Keyboard Navigation

**Full keyboard control** (see [Camera Controls](#camera-controls)):
- Arrow keys: Orbit
- +/-: Zoom
- Shift+Arrows: Pan
- Space: Toggle auto-rotate
- Home: Reset view
- Tab: Focus next control button

### Screen Reader Support

**ARIA Labels**:
```html
<div
  role="img"
  aria-label="3D preview of tactile art model. Use arrow keys to rotate, plus and minus to zoom."
  tabindex="0"
>
  <canvas id="3d-viewport"></canvas>
</div>

<!-- Control buttons -->
<button aria-label="Reset camera to default view">Reset View</button>
<button aria-label="Toggle grid overlay" aria-pressed="false">Grid</button>
<button aria-label="Toggle wireframe mode" aria-pressed="false">Wireframe</button>
```

**Live Region Announcements**:
```html
<div aria-live="polite" aria-atomic="true" class="sr-only">
  <!-- Announce changes -->
  Model loaded successfully. 7,234 triangles. Dimensions: 150 by 112 by 5 millimeters.
</div>
```

### Focus Indicators

```css
/* Viewport focus ring */
.viewport:focus {
  outline: 3px solid #0066cc;
  outline-offset: 2px;
}

/* Control buttons */
.viewport-control:focus {
  box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.4);
}
```

### Alternative Text Descriptions

**Describe model state**:
- "3D model of portrait, face raised 4 millimeters above 2 millimeter base"
- "Heightmap visualization, colors range from blue (low) to red (high)"
- "Wireframe mode active, showing triangular mesh structure"

---

## Screenshot Capability

### Capture Current View

```javascript
function captureScreenshot() {
  // Render at higher resolution
  const originalSize = renderer.getSize(new THREE.Vector2());
  const screenshotWidth = 1920;
  const screenshotHeight = 1080;

  renderer.setSize(screenshotWidth, screenshotHeight);
  renderer.render(scene, camera);

  // Get image data
  const dataURL = renderer.domElement.toDataURL('image/png');

  // Restore original size
  renderer.setSize(originalSize.x, originalSize.y);

  // Trigger download
  const link = document.createElement('a');
  link.download = 'tactile-art-preview.png';
  link.href = dataURL;
  link.click();
}
```

**Screenshot Button** (header):
```
[📷 Screenshot]
- Click to capture current view
- Saves as PNG (1920×1080)
- Filename: tactile-art-preview.png
```

---

## Advanced Features

### Auto-Rotation

```javascript
// Toggle with [▶️ Rotate] button
controls.autoRotate = true;
controls.autoRotateSpeed = 1.0;  // RPM

// Pause on user interaction
controls.addEventListener('start', () => {
  controls.autoRotate = false;
});
```

### Model Slicing Plane

**Optional: Cross-section view**:
```javascript
// Show internal structure
const slicePlane = new THREE.Plane(new THREE.Vector3(0, 1, 0), 0);
renderer.clippingPlanes = [slicePlane];
renderer.localClippingEnabled = true;

// UI: Slider to move slice plane up/down
```

### Comparison View

**Split screen: Before/After**:
```
┌─────────────────┬─────────────────┐
│  Original Image │  3D Model       │
│                 │                 │
│  [2D Preview]   │  [3D Preview]   │
│                 │                 │
└─────────────────┴─────────────────┘
```

---

## Component API (React Example)

```typescript
interface Viewer3DProps {
  model: THREE.Mesh | null;
  width: number;
  height: number;
  onModelClick?: (point: THREE.Vector3) => void;
  showGrid?: boolean;
  showAxes?: boolean;
  showMeasurements?: boolean;
  visualizationMode?: 'solid' | 'heightmap' | 'wireframe' | 'both';
  autoRotate?: boolean;
  backgroundColor?: string;
}

function Viewer3D(props: Viewer3DProps) {
  // Implementation
}

// Usage:
<Viewer3D
  model={generatedMesh}
  width={720}
  height={540}
  showGrid={true}
  visualizationMode="heightmap"
  autoRotate={false}
/>
```

---

**End of 3D Viewer Component Specification**
