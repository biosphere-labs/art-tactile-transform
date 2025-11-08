# Upload Dialog Component Specification

**Component**: Image Upload Interface
**Version**: 2.0.0
**Last Updated**: 2025-11-08

---

## Overview

The upload component provides drag-and-drop and file browser functionality for loading images into the application. It includes validation, progress feedback, and image preview.

---

## Visual Design

### Default State (Empty)

```
┌─────────────────────────────────────────────────┐
│  📁 Upload Image                                │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │           📂                              │ │
│  │                                           │ │
│  │     Drag & Drop your image here          │ │
│  │              or                           │ │
│  │        [Browse Files]                     │ │
│  │                                           │ │
│  │   Supported: PNG, JPG, TIFF, BMP          │ │
│  │   Maximum size: 20 MB                     │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
│  💡 Quick Start:                                │
│  Try a sample: [Mona Lisa] [Landscape] [Text]  │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Styling**:
- Drop zone: Dashed border (2px, Gray-400)
- Background: White (light) / Dark-800 (dark)
- Padding: 32px
- Border radius: 8px
- Min height: 280px

---

### Drag Over State (Active)

```
┌─────────────────────────────────────────────────┐
│  📁 Upload Image                                │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │           📂↓                             │ │
│  │                                           │ │
│  │        Drop image here                    │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Styling Changes**:
- Border: Solid (3px, Primary-500)
- Background: Primary-50 (light blue tint)
- Icon: Animated downward arrow
- Cursor: copy

---

### Uploading State (Progress)

```
┌─────────────────────────────────────────────────┐
│  📁 Uploading Image...                          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │  portrait.jpg (2.3 MB)                    │ │
│  │                                           │ │
│  │  [████████████████░░░░░░] 67%             │ │
│  │                                           │ │
│  │  Uploading... 1.5 MB / 2.3 MB             │ │
│  │                                           │ │
│  │              [Cancel]                     │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Progress Bar**:
- Height: 8px
- Background: Gray-200
- Fill: Primary-500
- Animation: Smooth transition
- Update frequency: Every 100ms

---

### Uploaded State (Success)

```
┌─────────────────────────────────────────────────┐
│  📁 Image Loaded                                │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │  ┌─────────────────────────┐             │ │
│  │  │                         │             │ │
│  │  │   [Image Thumbnail]     │             │ │
│  │  │                         │             │ │
│  │  └─────────────────────────┘             │ │
│  │                                           │ │
│  │  portrait.jpg                             │ │
│  │  1024 × 768 pixels                        │ │
│  │  2.3 MB                                   │ │
│  │                                           │ │
│  │  ✓ Valid image                            │ │
│  │                                           │ │
│  │     [Change Image]  [Remove]              │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Thumbnail**:
- Max size: 200px × 150px (maintain aspect)
- Border: 1px solid Gray-300
- Shadow: shadow-sm
- Object-fit: contain

---

## Validation & Error States

### File Too Large Error

```
┌─────────────────────────────────────────────────┐
│  ⚠️ File Too Large                              │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │  ❌ large_image.jpg (25 MB)                │ │
│  │                                           │ │
│  │  This file exceeds the 20 MB limit.       │ │
│  │                                           │ │
│  │  💡 Solutions:                             │ │
│  │  • Resize image to smaller dimensions     │ │
│  │    (recommended max: 2048px)              │ │
│  │  • Compress image using an editor         │ │
│  │  • Convert to more efficient format       │ │
│  │                                           │ │
│  │           [Try Another File]              │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

### Invalid Format Error

```
┌─────────────────────────────────────────────────┐
│  ❌ Unsupported Format                          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │  document.pdf                             │ │
│  │                                           │ │
│  │  This file type is not supported.         │ │
│  │                                           │ │
│  │  ✓ Supported formats:                     │ │
│  │  • PNG (.png)                             │ │
│  │  • JPEG (.jpg, .jpeg)                     │ │
│  │  • TIFF (.tiff, .tif)                     │ │
│  │  • BMP (.bmp)                             │ │
│  │                                           │ │
│  │  💡 Tip: Convert PDF to image format      │ │
│  │                                           │ │
│  │           [Choose Different File]         │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

### Corrupted File Error

```
┌─────────────────────────────────────────────────┐
│  ❌ Cannot Read File                            │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │                                           │ │
│  │  corrupted_image.jpg                      │ │
│  │                                           │ │
│  │  Unable to read this file.                │ │
│  │  The file may be corrupted or incomplete. │ │
│  │                                           │ │
│  │  💡 Troubleshooting:                       │ │
│  │  • Re-download the image                  │ │
│  │  • Try opening in image editor first      │ │
│  │  • Use a different image                  │ │
│  │                                           │ │
│  │           [Try Another File]              │ │
│  │                                           │ │
│  └───────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## Implementation Details

### File Validation

```javascript
const ACCEPTED_FORMATS = [
  'image/png',
  'image/jpeg',
  'image/jpg',
  'image/tiff',
  'image/bmp'
];

const MAX_FILE_SIZE = 20 * 1024 * 1024;  // 20 MB in bytes

function validateFile(file) {
  const errors = [];

  // Check file type
  if (!ACCEPTED_FORMATS.includes(file.type)) {
    errors.push({
      type: 'INVALID_FORMAT',
      message: `Unsupported file type: ${file.type}`,
      suggestions: [
        'Convert to PNG, JPEG, TIFF, or BMP',
        'Use an image editor to export in supported format'
      ]
    });
  }

  // Check file size
  if (file.size > MAX_FILE_SIZE) {
    errors.push({
      type: 'FILE_TOO_LARGE',
      message: `File size (${formatBytes(file.size)}) exceeds ${formatBytes(MAX_FILE_SIZE)} limit`,
      suggestions: [
        'Resize image to smaller dimensions (max 2048px recommended)',
        'Compress image using image editor',
        'Convert to more efficient format (PNG or JPEG)'
      ]
    });
  }

  return {
    valid: errors.length === 0,
    errors
  };
}
```

### Drag & Drop Implementation

```javascript
function setupDragAndDrop(dropZone) {
  // Prevent default browser behavior
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Visual feedback
  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.add('drag-over');  // Active state
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
      dropZone.classList.remove('drag-over');
    }, false);
  });

  // Handle drop
  dropZone.addEventListener('drop', (e) => {
    const files = e.dataTransfer.files;
    handleFiles(files);
  }, false);
}
```

### File Upload with Progress

```javascript
async function uploadFile(file) {
  // Validate first
  const validation = validateFile(file);
  if (!validation.valid) {
    showError(validation.errors[0]);
    return;
  }

  // Show progress UI
  showUploadProgress(true);

  // Simulate upload progress (in real app, would track actual upload)
  // For local processing, this reads the file
  const reader = new FileReader();

  reader.onprogress = (event) => {
    if (event.lengthComputable) {
      const percentComplete = (event.loaded / event.total) * 100;
      updateProgress(percentComplete);
    }
  };

  reader.onload = (event) => {
    const imageData = event.target.result;
    onUploadComplete(file, imageData);
  };

  reader.onerror = (error) => {
    showError({
      type: 'READ_ERROR',
      message: 'Failed to read file',
      suggestions: ['Try a different file', 'Check file is not corrupted']
    });
  };

  reader.readAsDataURL(file);
}
```

### Image Preview Generation

```javascript
function generateThumbnail(imageData) {
  return new Promise((resolve, reject) => {
    const img = new Image();

    img.onload = () => {
      // Create canvas for thumbnail
      const maxWidth = 200;
      const maxHeight = 150;

      let width = img.width;
      let height = img.height;

      // Maintain aspect ratio
      if (width > height) {
        if (width > maxWidth) {
          height *= maxWidth / width;
          width = maxWidth;
        }
      } else {
        if (height > maxHeight) {
          width *= maxHeight / height;
          height = maxHeight;
        }
      }

      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext('2d');
      ctx.drawImage(img, 0, 0, width, height);

      resolve({
        thumbnail: canvas.toDataURL(),
        dimensions: {
          original: { width: img.width, height: img.height },
          thumbnail: { width, height }
        }
      });
    };

    img.onerror = reject;
    img.src = imageData;
  });
}
```

---

## Sample Images Feature

### Quick Start with Samples

```
┌─────────────────────────────────────────────────┐
│  💡 Quick Start: Try a sample image             │
│                                                 │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐       │
│  │[Img] │  │[Img] │  │[Img] │  │[Img] │       │
│  │Mona  │  │Land- │  │Text  │  │Dia-  │       │
│  │Lisa  │  │scape │  │Sign  │  │gram  │       │
│  └──────┘  └──────┘  └──────┘  └──────┘       │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Sample Images**:
1. **Mona Lisa** - Portrait example (classic artwork)
2. **Landscape** - Nature scene with sky/foreground
3. **Text Sign** - High contrast text ("EMERGENCY EXIT")
4. **Diagram** - Simple floor plan or map

**Implementation**:
```javascript
const SAMPLE_IMAGES = [
  {
    name: 'Mona Lisa',
    url: '/samples/mona_lisa.jpg',
    mode: 'portrait',
    description: 'Classic portrait artwork'
  },
  {
    name: 'Landscape',
    url: '/samples/landscape.jpg',
    mode: 'landscape',
    description: 'Nature scene with mountains'
  },
  {
    name: 'Text Sign',
    url: '/samples/text_sign.jpg',
    mode: 'text',
    description: 'High contrast text'
  },
  {
    name: 'Diagram',
    url: '/samples/diagram.jpg',
    mode: 'diagram',
    description: 'Simple floor plan'
  }
];

function loadSampleImage(sample) {
  fetch(sample.url)
    .then(response => response.blob())
    .then(blob => {
      const file = new File([blob], sample.name + '.jpg', { type: 'image/jpeg' });
      handleFiles([file]);
      // Auto-select recommended mode
      setMode(sample.mode);
    });
}
```

---

## Accessibility

### Keyboard Support

```javascript
// Make drop zone keyboard accessible
<div
  className="drop-zone"
  tabIndex="0"
  role="button"
  aria-label="Upload image. Press Enter or Space to open file browser, or drag and drop an image file here."
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();  // Open file browser
    }
  }}
>
```

### Screen Reader Announcements

```html
<!-- Live region for status updates -->
<div aria-live="polite" aria-atomic="true" className="sr-only">
  {/* Dynamically update with status */}
  {status === 'uploading' && `Uploading ${fileName}, ${progress}% complete`}
  {status === 'success' && `Image uploaded successfully: ${fileName}, ${width} by ${height} pixels`}
  {status === 'error' && `Error: ${errorMessage}`}
</div>
```

### ARIA Labels

```html
<input
  type="file"
  id="file-input"
  accept=".png,.jpg,.jpeg,.tiff,.tif,.bmp"
  aria-label="Choose image file to upload"
  onChange={handleFileSelect}
/>

<button
  type="button"
  aria-label="Remove uploaded image"
  onClick={removeImage}
>
  Remove
</button>
```

---

## Mobile Considerations

### Mobile Upload UI

```
┌─────────────────────────┐
│  📁 Upload Image        │
│                         │
│  ┌───────────────────┐  │
│  │                   │  │
│  │   📂 Tap to       │  │
│  │   select image    │  │
│  │                   │  │
│  │   [Choose File]   │  │
│  │                   │  │
│  │   or              │  │
│  │                   │  │
│  │   [📷 Take Photo] │  │
│  │                   │  │
│  └───────────────────┘  │
│                         │
│  PNG, JPG, TIFF, BMP    │
│  Max 20 MB              │
│                         │
└─────────────────────────┘
```

**Features**:
- Larger touch targets (minimum 44px)
- Camera option (if device has camera)
- Simplified drag-and-drop (tap to browse instead)
- Bottom sheet for file picker

### Camera Capture (Mobile)

```html
<input
  type="file"
  accept="image/*"
  capture="environment"
  aria-label="Take photo with camera"
/>
```

---

## Component API (React Example)

```typescript
interface UploadDialogProps {
  onFileSelect: (file: File) => void;
  onError: (error: ValidationError) => void;
  maxFileSize?: number;  // bytes
  acceptedFormats?: string[];
  showSamples?: boolean;
  sampleImages?: SampleImage[];
}

interface SampleImage {
  name: string;
  url: string;
  mode: ProcessingMode;
  description: string;
}

interface ValidationError {
  type: 'INVALID_FORMAT' | 'FILE_TOO_LARGE' | 'READ_ERROR';
  message: string;
  suggestions: string[];
}

function UploadDialog(props: UploadDialogProps) {
  // Implementation
}

// Usage:
<UploadDialog
  onFileSelect={handleFileUpload}
  onError={handleError}
  maxFileSize={20 * 1024 * 1024}
  acceptedFormats={['image/png', 'image/jpeg', 'image/tiff', 'image/bmp']}
  showSamples={true}
/>
```

---

## Performance Considerations

### Large File Handling

```javascript
// For very large files, show warning
function checkFileSize(file) {
  if (file.size > 10 * 1024 * 1024) {  // > 10 MB
    showWarning({
      message: 'Large file detected. Processing may take longer.',
      dismissible: true
    });
  }
}

// Progressive thumbnail loading
async function loadLargeImage(file) {
  // Load low-res preview first
  const lowResPreview = await createDownsampledPreview(file, 256);
  showThumbnail(lowResPreview);

  // Then load full resolution
  const fullImage = await loadFullImage(file);
  updateThumbnail(fullImage);
}
```

---

**End of Upload Dialog Component Specification**
