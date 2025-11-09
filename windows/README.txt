================================================================================
                    Art Tactile Transform - Windows Edition
                          AI-Powered 3D Tactile Art Generator
================================================================================

Transform any image into a 3D printable tactile representation using
state-of-the-art AI depth estimation!

================================================================================
QUICK START
================================================================================

1. Install Python 3.10 or later (if not already installed):
   https://www.python.org/downloads/

   IMPORTANT: Check "Add Python to PATH" during installation!

2. Double-click: install.bat
   - Creates virtual environment
   - Installs dependencies (~100MB)
   - Creates desktop shortcut

3. Double-click: "Art Tactile Transform" on your desktop
   - First run: Downloads AI models (~2GB, 5-10 min)
   - Opens web browser automatically
   - Subsequent runs are instant!

================================================================================
WHAT IT DOES
================================================================================

Converts images into 3D printable STL files:
- Upload ANY image (portraits, landscapes, objects, etc.)
- AI analyzes and creates depth map automatically
- Adjust contrast, smoothing, and physical dimensions
- Preview in 3D before downloading
- Export STL file for 3D printing

Perfect for:
- Creating tactile art for blind/visually impaired users
- 3D printing relief sculptures from photos
- Generating decorative wall art
- Educational tactile diagrams

================================================================================
SYSTEM REQUIREMENTS
================================================================================

- Windows 10 or later
- Python 3.10+ (with pip)
- 4GB RAM minimum (8GB recommended)
- 5GB free disk space
- Internet connection (for initial setup only)

================================================================================
FILE STRUCTURE
================================================================================

windows/
├── install.bat             <- Run this first (one-time setup)
├── launcher.bat            <- Launches the GUI
├── requirements-core.txt   <- Core dependencies (~100MB)
├── requirements-pytorch.txt <- AI dependencies (~2GB, auto-downloaded)
└── README.txt             <- This file

After installation:
├── venv/                   <- Python virtual environment
└── outputs/                <- Generated STL files

================================================================================
USAGE
================================================================================

1. Launch Application:
   - Double-click desktop shortcut OR
   - Run launcher.bat from this folder

2. Browser Opens:
   - http://localhost:7860
   - If browser doesn't open automatically, copy this URL

3. Upload Image:
   - Drag & drop or click to upload
   - Supports: JPG, PNG, BMP, etc.

4. Adjust Parameters:
   - Physical: Width, relief depth, base thickness
   - Processing: Smoothing, resolution
   - AI: Depth contrast, invert depth

5. Generate Model:
   - Click "Generate 3D Model with AI"
   - Wait for processing (10-30 seconds)
   - Preview in 3D viewer

6. Download STL:
   - Click download button below 3D preview
   - Open in your 3D printing slicer software

================================================================================
PARAMETERS EXPLAINED
================================================================================

Physical Parameters:
  - Width: Final model width in millimeters (50-300mm)
  - Relief Depth: Maximum height of raised features (0.5-10mm)
  - Base Thickness: Thickness of base plate (0.5-5mm)

Processing Parameters:
  - Smoothing: Gaussian blur for smooth surfaces (0=sharp, 10=very smooth)
  - Resolution: Mesh detail (64=low, 256=high, larger file)

AI Depth Parameters:
  - Depth Contrast: Adjust depth strength (1.0=normal, 2.0=very strong)
  - Invert Depth: Swap near/far if background appears raised

================================================================================
TROUBLESHOOTING
================================================================================

"Python not found":
  → Install Python 3.10+ from python.org
  → Make sure "Add to PATH" was checked during installation
  → Restart computer after Python installation

"Failed to install dependencies":
  → Check your internet connection
  → Temporarily disable antivirus
  → Run install.bat as Administrator

"Browser doesn't open":
  → Manually open: http://localhost:7860
  → Check Windows Firewall isn't blocking Python

"AI model download slow":
  → First run downloads ~500MB depth model
  → Can take 5-10 minutes on slow connections
  → Subsequent runs use cached model (instant)

"Out of memory error":
  → Use lower resolution (64 or 128)
  → Close other applications
  → Reduce image size before uploading

"Port 7860 already in use":
  → Another instance is running, close it first
  → Or change port in gui.py (line 399)

================================================================================
FIRST RUN PROCESS
================================================================================

1. Run launcher.bat
2. Checks if PyTorch installed
3. If not: Downloads PyTorch (~1.5GB)
4. Downloads transformers library (~200MB)
5. Launches GUI
6. On first image processing: Downloads depth model (~500MB)
7. Total first run: 5-15 minutes (depending on internet speed)
8. Subsequent runs: Instant launch!

================================================================================
ADVANCED USAGE
================================================================================

Command Line (for batch processing):
  venv\Scripts\python -m art_tactile_transform.cli

Custom Configuration:
  - Edit .env file in project root
  - Change default model, resolution, etc.

Multiple Models:
  - Edit DEFAULT_MODEL in src/art_tactile_transform/gui.py
  - Try different HuggingFace depth models

================================================================================
UNINSTALL
================================================================================

1. Delete desktop shortcut
2. Delete this entire folder
3. (Optional) Uninstall Python if not needed for other programs

No registry changes, no system files modified!

================================================================================
TECHNICAL DETAILS
================================================================================

AI Model: depth-anything-small-hf (HuggingFace)
  - State-of-the-art monocular depth estimation
  - Trained on millions of images
  - No GPU required (CPU version)

Processing Pipeline:
  1. Load image with PIL
  2. Run through depth estimation transformer
  3. Process depth map (contrast, smoothing)
  4. Resize to target resolution
  5. Convert to heightmap (0-1 normalized)
  6. Generate STL file with proper normals
  7. Add base plate for stability

Output Format: ASCII STL
  - Universal 3D printing format
  - Compatible with all slicers
  - Proper surface normals
  - Physical dimensions in millimeters

================================================================================
TIPS FOR BEST RESULTS
================================================================================

For Portraits:
  - Use high contrast photos with clear faces
  - Try Depth Contrast: 1.2-1.5
  - Enable "Invert Depth" if face appears sunken
  - Smoothing: 2-3 for natural skin texture

For Landscapes:
  - Use images with clear foreground/background
  - Depth Contrast: 1.5-2.0 for dramatic relief
  - Resolution: 128-256 for detail
  - Smoothing: 1-2 to preserve fine details

For Text/Diagrams:
  - High contrast black & white images work best
  - Smoothing: 0-1 for sharp edges
  - Invert Depth if text appears recessed

================================================================================
SUPPORT & FEEDBACK
================================================================================

Issues: https://github.com/fluidnotions/art-tactile-transform/issues
Email: justin.g.robinson@gmail.com

================================================================================

Built with:
  - Python 3.13
  - PyTorch (CPU)
  - HuggingFace Transformers
  - Gradio Web UI
  - OpenCV for image processing

Developed for accessibility - making visual art accessible through touch.

================================================================================
