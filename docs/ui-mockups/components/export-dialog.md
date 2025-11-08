# Export Dialog Component Specification

**Component**: STL Export Interface with Validation
**Version**: 2.0.0
**Last Updated**: 2025-11-08

---

## Overview

The export dialog is the final step before generating the STL file. It provides file format options, validation warnings, estimates, and metadata options to ensure successful 3D printing.

---

## Visual Design

### Export Dialog (Main)

```
┌──────────────────────────────────────────────────────────┐
│  Export STL File                                    [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  File Information                                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │  File name:                                        │ │
│  │  [portrait_tactile                  ] .stl         │ │
│  │                                                    │ │
│  │  Save location:                                    │ │
│  │  [~/Downloads/              ] [Browse...]          │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Format Options                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  ● STL Binary (recommended - smaller file size)   │ │
│  │  ○ STL ASCII (human-readable, larger file)        │ │
│  │                                                    │ │
│  │  ☑ Include parameter metadata in STL comments     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Validation Results                                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │  ✓ Mesh is manifold (watertight)                  │ │
│  │  ✓ No inverted normals                            │ │
│  │  ✓ No self-intersections                          │ │
│  │  ✓ All features above minimum size (2.5mm)        │ │
│  │  ✓ Dimensions within common printer limits        │ │
│  │                                                    │ │
│  │  All checks passed! Ready to export. ✅           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Export Estimates                                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Estimated file size:      1.2 MB                  │ │
│  │  Triangle count:           7,234 triangles         │ │
│  │  Model dimensions:         150 × 112 × 5 mm        │ │
│  │                                                    │ │
│  │  📊 Print Estimates (FDM, 0.2mm layer):            │ │
│  │     Print time:            ~45 minutes             │ │
│  │     Filament needed:       ~15g PLA                │ │
│  │     Material cost:         ~$0.30 USD              │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  💡 Next Steps After Export:                       │ │
│  │  1. Load STL into slicer (Cura, PrusaSlicer, etc.)│ │
│  │  2. Configure printer settings (0.2mm recommended)│ │
│  │  3. Generate G-code and print!                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
├──────────────────────────────────────────────────────────┤
│                              [Cancel]  [Export STL]     │
└──────────────────────────────────────────────────────────┘
```

**Dialog Size**: 600px width × auto height
**Modal**: Yes (blocks interaction with main window)
**Backdrop**: Semi-transparent dark overlay (rgba(0,0,0,0.6))

---

## Validation States

### All Checks Pass (Success)

```
┌────────────────────────────────────────────────────┐
│  Validation Results                                │
│  ┌──────────────────────────────────────────────┐ │
│  │  ✓ Mesh is manifold (watertight)            │ │
│  │  ✓ No inverted normals                      │ │
│  │  ✓ No self-intersections                    │ │
│  │  ✓ All features above minimum size (2.5mm)  │ │
│  │  ✓ Dimensions within common printer limits  │ │
│  │                                              │ │
│  │  ✅ All checks passed! Ready to export.     │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

**Visual**:
- Green checkmarks (Success-500)
- Green success banner
- "Export STL" button enabled (Primary-500)

---

### Warnings (Non-Critical)

```
┌────────────────────────────────────────────────────┐
│  Validation Results                                │
│  ┌──────────────────────────────────────────────┐ │
│  │  ✓ Mesh is manifold (watertight)            │ │
│  │  ✓ No inverted normals                      │ │
│  │  ✓ No self-intersections                    │ │
│  │  ⚠️ Some features small (1.8mm)              │ │
│  │     May not print clearly on FDM printers    │ │
│  │     Recommended minimum: 2-3mm               │ │
│  │  ⚠️ Width (250mm) exceeds typical bed (220mm)│ │
│  │     Consider reducing size or using larger   │ │
│  │     printer                                  │ │
│  │                                              │ │
│  │  ⚠️ 2 warnings found. Export with caution.  │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘

  [Go Back to Adjust]  [Export Anyway]
```

**Visual**:
- Orange warning icons (Warning-500)
- Yellow warning banner
- "Export Anyway" button available but secondary
- "Go Back to Adjust" button suggested

---

### Errors (Critical)

```
┌────────────────────────────────────────────────────┐
│  Validation Results                                │
│  ┌──────────────────────────────────────────────┐ │
│  │  ❌ Mesh has 3 non-manifold edges             │ │
│  │     STL may not print correctly              │ │
│  │  ❌ Found 1 hole in surface                   │ │
│  │     Mesh is not watertight                   │ │
│  │  ✓ No inverted normals                      │ │
│  │  ✓ No self-intersections                    │ │
│  │                                              │ │
│  │  ❌ Errors must be fixed before export.      │ │
│  │                                              │ │
│  │  💡 Suggested fixes:                         │ │
│  │  • Increase smoothing to reduce noise        │ │
│  │  • Increase minimum feature size             │ │
│  │  • Use auto-repair (may alter model)         │ │
│  └──────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────┘

  [Auto-Repair Mesh]  [Adjust Parameters]  [Cancel]
```

**Visual**:
- Red error icons (Error-500)
- Red error banner
- "Export STL" button disabled
- "Auto-Repair" button available
- "Adjust Parameters" returns to main app

---

## Auto-Repair Flow

### Repair Process

```
┌──────────────────────────────────────────────────────────┐
│  Auto-Repair Mesh                                   [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  🔧 Repairing mesh...                                    │
│                                                          │
│  Progress: [████████████████░░░░] 80%                    │
│                                                          │
│  Current step: Closing holes...                          │
│                                                          │
│  Repairs applied:                                        │
│  ✓ Fixed 3 non-manifold edges                           │
│  🔄 Closing 1 hole... (in progress)                      │
│  ⏳ Re-validating mesh... (pending)                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Repair Complete

```
┌──────────────────────────────────────────────────────────┐
│  Auto-Repair Complete                               [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ✅ Mesh repaired successfully!                          │
│                                                          │
│  Repairs applied:                                        │
│  ✓ Fixed 3 non-manifold edges                           │
│  ✓ Closed 1 hole                                        │
│  ✓ Re-validated mesh                                    │
│                                                          │
│  ⚠️ Note: Auto-repair may slightly alter the model.     │
│     Review 3D preview to confirm result.                │
│                                                          │
│  New validation:                                         │
│  ✓ All checks passed                                    │
│                                                          │
│  [Review Changes]  [Continue to Export]                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Export Progress

### Generating STL

```
┌──────────────────────────────────────────────────────────┐
│  Exporting STL...                                   [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  🔄 Generating STL file...                               │
│                                                          │
│  Progress: [████████████████████] 100%                   │
│                                                          │
│  Stage: Writing file to disk...                          │
│                                                          │
│  portrait_tactile.stl                                    │
│  1.2 MB / 1.2 MB                                         │
│                                                          │
│  Elapsed: 2.3s                                           │
│  Estimated remaining: 0s                                 │
│                                                          │
│  [Cancel]                                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Progress Stages**:
1. Preparing mesh data (10%)
2. Converting to STL format (40%)
3. Generating triangles (70%)
4. Writing file (90%)
5. Finalizing (100%)

---

## Export Success

### Success Dialog

```
┌──────────────────────────────────────────────────────────┐
│  Export Successful!                                 [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ✅ STL file exported successfully!                      │
│                                                          │
│  File Details:                                           │
│  📁 portrait_tactile.stl                                 │
│  📂 ~/Downloads/portrait_tactile.stl                     │
│  💾 1.2 MB                                               │
│  🕐 Created: 2025-11-08 14:30:45                         │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  💡 Next Steps:                                    │ │
│  │                                                    │ │
│  │  1. Open your slicer software:                    │ │
│  │     • Cura                                        │ │
│  │     • PrusaSlicer                                 │ │
│  │     • Simplify3D                                  │ │
│  │                                                    │ │
│  │  2. Import portrait_tactile.stl                   │ │
│  │                                                    │ │
│  │  3. Recommended settings:                         │ │
│  │     • Layer height: 0.2mm                         │ │
│  │     • Infill: 20%                                 │ │
│  │     • Supports: Not needed (flat base)            │ │
│  │     • Rafts/brims: Optional for adhesion          │ │
│  │                                                    │ │
│  │  4. Generate G-code and print!                    │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  [📂 Open Folder]  [🖨️ Print Guide]  [🔄 Export Another]│
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │  💾 Save these settings as a preset?              │ │
│  │                                                    │ │
│  │  Preset name: [My Portrait Settings]              │ │
│  │  [Skip]  [Save Preset]                            │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Actions Available**:
1. **Open Folder**: Opens file location in system file browser
2. **Print Guide**: Opens documentation on printing tips
3. **Export Another**: Closes dialog, keeps same image/settings
4. **Save Preset**: Saves current parameters for reuse

---

## Advanced Export Options

### Advanced Options Panel (Collapsed by default)

```
┌────────────────────────────────────────────────────┐
│  🔧 Advanced Options                           [+] │
└────────────────────────────────────────────────────┘

(Click to expand)
```

### Expanded Advanced Options

```
┌────────────────────────────────────────────────────┐
│  🔧 Advanced Options                           [−] │
├────────────────────────────────────────────────────┤
│                                                    │
│  STL Precision                                     │
│  ● Standard (6 decimal places)                     │
│  ○ High (9 decimal places - larger file)           │
│  ○ Low (3 decimal places - smaller file)           │
│                                                    │
│  Coordinate System                                 │
│  ● Z-up (standard for most slicers)                │
│  ○ Y-up (for some CAD software)                    │
│                                                    │
│  Units                                             │
│  ● Millimeters (standard)                          │
│  ○ Inches                                          │
│                                                    │
│  Metadata                                          │
│  ☑ Include creation date                          │
│  ☑ Include parameter settings                     │
│  ☑ Include software version                       │
│  ☐ Include original image dimensions              │
│                                                    │
│  Mesh Optimization                                 │
│  ☐ Reduce triangle count (experimental)            │
│     Target: [50%  ] of current                     │
│  ☐ Smooth normals for better shading              │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## Validation Details Modal

### Detailed Validation Report

```
┌──────────────────────────────────────────────────────────┐
│  Mesh Validation Report                             [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ✓ Manifold Check                                        │
│    The mesh is watertight with no holes or gaps.        │
│    All edges are connected to exactly 2 faces.          │
│                                                          │
│  ✓ Normal Consistency                                    │
│    All face normals point outward.                       │
│    No inverted or flipped faces detected.               │
│                                                          │
│  ✓ Self-Intersection Check                              │
│    No faces intersect with each other.                   │
│    Mesh is geometrically valid.                          │
│                                                          │
│  ✓ Feature Size Analysis                                 │
│    Minimum feature size: 2.5mm                           │
│    All features above recommended minimum (2mm).         │
│                                                          │
│  ✓ Dimension Check                                       │
│    Width: 150mm (within limits)                          │
│    Height: 112mm (within limits)                         │
│    Depth: 5mm (within limits)                            │
│    Fits on 220mm × 220mm printer bed ✓                  │
│                                                          │
│  Statistics:                                             │
│  ─────────────────────────────────────                  │
│  Vertices:        7,682                                  │
│  Triangles:       7,234                                  │
│  Edges:           11,458                                 │
│  Boundary edges:  0 (watertight ✓)                      │
│  Surface area:    23,456 mm²                             │
│  Volume:          84,000 mm³                             │
│                                                          │
│  [Export Detailed Report]  [Close]                      │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Error Handling

### Export Failed (Disk Full)

```
┌──────────────────────────────────────────────────────────┐
│  Export Failed                                      [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ❌ Failed to export STL file                            │
│                                                          │
│  Error: Insufficient disk space                          │
│                                                          │
│  Required:    1.2 MB                                     │
│  Available:   0.3 MB                                     │
│                                                          │
│  💡 Solutions:                                            │
│  • Free up disk space                                   │
│  • Choose a different save location                     │
│  • Reduce model resolution to decrease file size        │
│                                                          │
│  [Choose Different Location]                             │
│  [Free Disk Space Guide]                                 │
│  [Cancel]                                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Export Failed (Permission Denied)

```
┌──────────────────────────────────────────────────────────┐
│  Export Failed                                      [X]  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ❌ Failed to export STL file                            │
│                                                          │
│  Error: Permission denied                                │
│                                                          │
│  Unable to write to:                                     │
│  ~/Downloads/portrait_tactile.stl                        │
│                                                          │
│  💡 Solutions:                                            │
│  • Choose a different folder                            │
│  • Check folder permissions                             │
│  • Try saving to Desktop or Documents                   │
│                                                          │
│  [Choose Different Location]                             │
│  [Cancel]                                                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Implementation Details

### File Name Auto-Generation

```javascript
function generateFileName(originalFileName, mode) {
  // Remove extension
  const baseName = originalFileName.replace(/\.[^/.]+$/, '');

  // Sanitize (remove special characters)
  const sanitized = baseName.replace(/[^a-zA-Z0-9_-]/g, '_');

  // Add suffix based on mode
  const suffix = '_tactile';

  // Add timestamp if file exists
  let fileName = `${sanitized}${suffix}.stl`;

  if (fileExists(fileName)) {
    const timestamp = new Date().getTime();
    fileName = `${sanitized}${suffix}_${timestamp}.stl`;
  }

  return fileName;
}

// Example:
// "Mona Lisa.jpg" → "Mona_Lisa_tactile.stl"
// "portrait.png" → "portrait_tactile.stl"
```

### Validation Implementation

```javascript
async function validateMesh(mesh) {
  const results = {
    manifold: true,
    invertedNormals: false,
    selfIntersections: false,
    minFeatureSize: Infinity,
    dimensionsOK: true,
    errors: [],
    warnings: []
  };

  // Check manifold (watertight)
  const boundaryEdges = mesh.geometry.getBoundaryEdges();
  if (boundaryEdges.length > 0) {
    results.manifold = false;
    results.errors.push({
      type: 'NON_MANIFOLD',
      message: `Found ${boundaryEdges.length} boundary edges`,
      suggestion: 'Increase smoothing or use auto-repair'
    });
  }

  // Check normals
  const invertedCount = checkNormals(mesh);
  if (invertedCount > 0) {
    results.invertedNormals = true;
    results.errors.push({
      type: 'INVERTED_NORMALS',
      message: `Found ${invertedCount} inverted faces`,
      suggestion: 'Use auto-repair to fix normals'
    });
  }

  // Check dimensions
  const bbox = new THREE.Box3().setFromObject(mesh);
  const size = bbox.getSize(new THREE.Vector3());

  if (size.x > 220 || size.y > 220) {
    results.warnings.push({
      type: 'LARGE_DIMENSIONS',
      message: `Dimensions (${size.x.toFixed(1)} × ${size.y.toFixed(1)}mm) exceed typical printer bed (220mm)`,
      suggestion: 'Reduce width/height or use larger printer'
    });
  }

  // Check feature sizes
  results.minFeatureSize = calculateMinFeatureSize(mesh);
  if (results.minFeatureSize < 2.0) {
    results.warnings.push({
      type: 'SMALL_FEATURES',
      message: `Minimum feature size (${results.minFeatureSize.toFixed(1)}mm) may not print clearly`,
      suggestion: 'Increase minimum feature size to 2-3mm'
    });
  }

  return results;
}
```

### Export Implementation

```javascript
async function exportSTL(mesh, options) {
  const {
    filePath,
    binary = true,
    includeMetadata = true,
    precision = 6
  } = options;

  // Update progress
  updateProgress(0, 'Preparing mesh data...');

  // Create STL exporter
  const exporter = new STLExporter();

  updateProgress(40, 'Converting to STL format...');

  // Generate STL data
  const stlData = exporter.parse(mesh, {
    binary: binary
  });

  updateProgress(70, 'Generating triangles...');

  // Add metadata if requested (ASCII only)
  if (includeMetadata && !binary) {
    const metadata = generateMetadata();
    stlData = addMetadataToSTL(stlData, metadata);
  }

  updateProgress(90, 'Writing file...');

  // Write to file
  await writeFile(filePath, stlData);

  updateProgress(100, 'Complete!');

  return {
    success: true,
    filePath,
    fileSize: stlData.byteLength || stlData.length
  };
}
```

### Print Time Estimation

```javascript
function estimatePrintTime(mesh, options = {}) {
  const {
    layerHeight = 0.2,  // mm
    printSpeed = 50,    // mm/s
    travelSpeed = 150   // mm/s
  } = options;

  // Get bounding box
  const bbox = new THREE.Box3().setFromObject(mesh);
  const size = bbox.getSize(new THREE.Vector3());

  // Estimate layers
  const layers = Math.ceil(size.z / layerHeight);

  // Estimate perimeter per layer (rough approximation)
  const avgPerimeterLength = (size.x + size.y) * 2;

  // Estimate infill area
  const layerArea = size.x * size.y;
  const infillDensity = 0.2;  // 20%
  const infillLength = Math.sqrt(layerArea * infillDensity) * 10;

  // Calculate time per layer
  const perimeterTime = avgPerimeterLength / printSpeed;
  const infillTime = infillLength / printSpeed;
  const travelTime = 10;  // seconds (estimated)

  const timePerLayer = perimeterTime + infillTime + travelTime;

  // Total time
  const totalSeconds = layers * timePerLayer;

  return {
    layers,
    totalMinutes: Math.ceil(totalSeconds / 60),
    formattedTime: formatPrintTime(totalSeconds)
  };
}

function formatPrintTime(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.ceil((seconds % 3600) / 60);

  if (hours > 0) {
    return `~${hours}h ${minutes}m`;
  } else {
    return `~${minutes} minutes`;
  }
}
```

---

## Accessibility

### Keyboard Support

```javascript
// Focus management
onDialogOpen() {
  // Focus first input (file name)
  fileNameInput.focus();
}

// Tab order
1. File name input
2. Browse button
3. Format radio buttons
4. Metadata checkbox
5. Export button
6. Cancel button

// Keyboard shortcuts
Ctrl/Cmd + E: Export (when dialog open)
Escape: Cancel/close dialog
Enter: Export (if validation passed)
```

### Screen Reader Announcements

```html
<div aria-live="polite" aria-atomic="true">
  {validationStatus === 'success' &&
    "All validation checks passed. Ready to export."
  }
  {validationStatus === 'warning' &&
    "Validation completed with 2 warnings. Review warnings before exporting."
  }
  {validationStatus === 'error' &&
    "Validation failed with errors. Mesh must be repaired before export."
  }
</div>
```

---

## Component API (React Example)

```typescript
interface ExportDialogProps {
  mesh: THREE.Mesh;
  originalFileName: string;
  parameters: ProcessingParameters;
  onExport: (options: ExportOptions) => Promise<void>;
  onCancel: () => void;
  isOpen: boolean;
}

interface ExportOptions {
  filePath: string;
  binary: boolean;
  includeMetadata: boolean;
  precision: number;
}

function ExportDialog(props: ExportDialogProps) {
  // Implementation
}

// Usage:
<ExportDialog
  mesh={generatedMesh}
  originalFileName="portrait.jpg"
  parameters={currentParameters}
  onExport={handleExport}
  onCancel={handleCancel}
  isOpen={showExportDialog}
/>
```

---

**End of Export Dialog Component Specification**
