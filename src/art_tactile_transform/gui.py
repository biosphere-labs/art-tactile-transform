"""
Gradio GUI for Tactile Art Transform - Phase 1 MVP

This module provides a web-based interface for converting images into 3D printable
tactile representations using semantic height mapping with portrait mode emphasis.

Key innovation: Faces and features are RAISED, backgrounds are LOWERED
(opposite of photographic depth estimation)
"""

import tempfile
from pathlib import Path
from typing import Optional, Tuple

import cv2
import gradio as gr
import numpy as np
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

from art_tactile_transform.main import heightmap_to_stl

# Download Haar Cascade for face detection (included with OpenCV)
FACE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
EYE_CASCADE = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)


def detect_faces_and_features(image: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Detect faces and facial features using OpenCV Haar Cascades.

    Returns:
        Tuple of (face_mask, feature_mask) where masks are normalized 0-1
    """
    # Convert to grayscale for detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = image.shape[:2]

    # Create masks
    face_mask = np.zeros((h, w), dtype=np.float32)
    feature_mask = np.zeros((h, w), dtype=np.float32)

    # Detect faces
    faces = FACE_CASCADE.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    for (x, y, fw, fh) in faces:
        # Create face region mask with gradient falloff
        face_region = np.zeros((h, w), dtype=np.float32)

        # Create elliptical mask for more natural face shape
        center_x = x + fw // 2
        center_y = y + fh // 2

        # Create coordinate grids
        y_coords, x_coords = np.ogrid[:h, :w]

        # Elliptical distance
        ellipse_dist = (
            ((x_coords - center_x) / (fw * 0.6))**2 +
            ((y_coords - center_y) / (fh * 0.6))**2
        )

        # Create smooth falloff
        face_region = np.exp(-ellipse_dist)
        face_region = np.clip(face_region, 0, 1)

        # Accumulate face regions
        face_mask = np.maximum(face_mask, face_region)

        # Detect eyes within face region
        roi_gray = gray[y:y+fh, x:x+fw]
        eyes = EYE_CASCADE.detectMultiScale(
            roi_gray,
            scaleFactor=1.1,
            minNeighbors=3,
            minSize=(15, 15)
        )

        for (ex, ey, ew, eh) in eyes:
            # Convert to full image coordinates
            eye_x = x + ex + ew // 2
            eye_y = y + ey + eh // 2

            # Create circular region around eye
            y_coords, x_coords = np.ogrid[:h, :w]
            dist = np.sqrt((x_coords - eye_x)**2 + (y_coords - eye_y)**2)
            eye_region = np.exp(-dist**2 / (2 * (ew * 0.6)**2))
            feature_mask = np.maximum(feature_mask, eye_region)

        # Add nose region (approximate center-bottom of face)
        nose_x = center_x
        nose_y = center_y + int(fh * 0.15)
        y_coords, x_coords = np.ogrid[:h, :w]
        dist = np.sqrt((x_coords - nose_x)**2 + (y_coords - nose_y)**2)
        nose_region = np.exp(-dist**2 / (2 * (fw * 0.15)**2))
        feature_mask = np.maximum(feature_mask, nose_region)

        # Add mouth region (approximate bottom of face)
        mouth_x = center_x
        mouth_y = center_y + int(fh * 0.35)
        dist = np.sqrt((x_coords - mouth_x)**2 + (y_coords - mouth_y)**2)
        mouth_region = np.exp(-dist**2 / (2 * (fw * 0.2)**2))
        feature_mask = np.maximum(feature_mask, mouth_region)

    # Normalize masks
    if face_mask.max() > 0:
        face_mask = face_mask / face_mask.max()
    if feature_mask.max() > 0:
        feature_mask = feature_mask / feature_mask.max()

    return face_mask, feature_mask


def create_edge_mask(image: np.ndarray, strength: float = 1.0) -> np.ndarray:
    """
    Create edge detection mask for feature enhancement.

    Args:
        image: Input image as numpy array
        strength: Edge strength multiplier (0-2)

    Returns:
        Edge mask normalized 0-1
    """
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Dilate edges slightly for better visibility
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)

    # Normalize and apply strength
    edge_mask = edges.astype(np.float32) / 255.0
    edge_mask = edge_mask * strength

    # Smooth edges
    edge_mask = gaussian_filter(edge_mask, sigma=1.0)

    return edge_mask


def create_semantic_heightmap(
    image: np.ndarray,
    subject_emphasis: float = 120.0,
    background_suppression: float = 40.0,
    feature_sharpness: float = 70.0,
    edge_strength: float = 60.0,
    smoothing: float = 2.0
) -> np.ndarray:
    """
    Create semantic heightmap where faces are HIGH and background is LOW.

    This is the key innovation: height represents IMPORTANCE, not photographic depth.

    Args:
        image: Input image as numpy array (BGR format)
        subject_emphasis: How much to raise main subject (0-200%)
        background_suppression: How much to flatten background (0-100%)
        feature_sharpness: Edge vs smooth transitions (0-100%)
        edge_strength: Edge detection intensity (0-100%)
        smoothing: Gaussian blur radius for smoothing

    Returns:
        Heightmap normalized to 0-1 range
    """
    h, w = image.shape[:2]

    # Detect faces and features
    face_mask, feature_mask = detect_faces_and_features(image)

    # Create edge mask
    edge_mask = create_edge_mask(image, edge_strength / 100.0)

    # Initialize heightmap with base level
    heightmap = np.ones((h, w), dtype=np.float32) * 0.3  # Base background height

    # Apply background suppression (lower the non-face areas)
    background_level = (100.0 - background_suppression) / 100.0 * 0.3
    heightmap = heightmap * (1.0 - face_mask) * background_level + heightmap * face_mask

    # Add face regions (raise faces)
    face_height = subject_emphasis / 100.0
    heightmap += face_mask * face_height

    # Add feature emphasis (raise facial features even more)
    feature_height = (feature_sharpness / 100.0) * 0.3
    heightmap += feature_mask * feature_height

    # Add edge enhancement
    edge_height = (edge_strength / 100.0) * 0.2
    heightmap += edge_mask * edge_height

    # Apply smoothing
    if smoothing > 0:
        heightmap = gaussian_filter(heightmap, sigma=smoothing)

    # Normalize to 0-1 range
    heightmap = np.clip(heightmap, 0, None)
    if heightmap.max() > 0:
        heightmap = heightmap / heightmap.max()

    return heightmap


def process_portrait_to_stl(
    image: np.ndarray,
    width_mm: float = 150.0,
    relief_depth_mm: float = 3.0,
    base_thickness_mm: float = 2.0,
    smoothing: float = 2.0,
    subject_emphasis: float = 120.0,
    background_suppression: float = 40.0,
    feature_sharpness: float = 70.0,
    edge_strength: float = 60.0,
    resolution: int = 128
) -> Tuple[str, Image.Image]:
    """
    Process image and generate STL file with preview.

    Returns:
        Tuple of (stl_path, preview_image)
    """
    # Create semantic heightmap
    heightmap = create_semantic_heightmap(
        image,
        subject_emphasis=subject_emphasis,
        background_suppression=background_suppression,
        feature_sharpness=feature_sharpness,
        edge_strength=edge_strength,
        smoothing=smoothing
    )

    # Resize heightmap to target resolution
    heightmap_resized = cv2.resize(
        heightmap,
        (resolution, resolution),
        interpolation=cv2.INTER_LANCZOS4
    )

    # Calculate pixel scale to achieve target width
    pixel_scale_mm = width_mm / resolution

    # Generate STL file
    temp_dir = Path(tempfile.gettempdir()) / "tactile_art"
    temp_dir.mkdir(exist_ok=True)
    stl_path = str(temp_dir / "output.stl")

    heightmap_to_stl(
        heightmap_resized,
        stl_path,
        min_height_mm=0.0,
        max_height_mm=relief_depth_mm,
        base_thickness_mm=base_thickness_mm,
        pixel_scale_mm=pixel_scale_mm
    )

    # Create preview image (visualize heightmap)
    preview = (heightmap * 255).astype(np.uint8)
    preview_colored = cv2.applyColorMap(preview, cv2.COLORMAP_VIRIDIS)
    preview_image = Image.fromarray(cv2.cvtColor(preview_colored, cv2.COLOR_BGR2RGB))

    return stl_path, preview_image


def process_image_wrapper(
    image,
    width_mm,
    relief_depth_mm,
    base_thickness_mm,
    smoothing,
    subject_emphasis,
    background_suppression,
    feature_sharpness,
    edge_strength,
    resolution
):
    """
    Wrapper for Gradio interface.
    """
    if image is None:
        return None, None, "Please upload an image first."

    try:
        # Convert PIL Image to numpy array (Gradio provides PIL Image)
        image_array = np.array(image)

        # Convert RGB to BGR for OpenCV
        image_bgr = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)

        # Process image
        stl_path, preview = process_portrait_to_stl(
            image_bgr,
            width_mm=width_mm,
            relief_depth_mm=relief_depth_mm,
            base_thickness_mm=base_thickness_mm,
            smoothing=smoothing,
            subject_emphasis=subject_emphasis,
            background_suppression=background_suppression,
            feature_sharpness=feature_sharpness,
            edge_strength=edge_strength,
            resolution=int(resolution)
        )

        # Calculate approximate dimensions
        height_mm = width_mm  # Square output
        total_height_mm = relief_depth_mm + base_thickness_mm

        info = f"""
        ### Model Information
        - Width: {width_mm:.1f} mm
        - Height: {height_mm:.1f} mm
        - Relief depth: {relief_depth_mm:.1f} mm
        - Base thickness: {base_thickness_mm:.1f} mm
        - Total thickness: {total_height_mm:.1f} mm
        - Resolution: {resolution}x{resolution} vertices

        **STL file ready for download!**
        """

        return stl_path, preview, info

    except Exception as e:
        return None, None, f"Error processing image: {str(e)}"


def create_gui():
    """
    Create and configure the Gradio interface.
    """
    with gr.Blocks(title="Tactile Art Transform - Portrait Mode") as demo:
        gr.Markdown(
            """
            # Tactile Art Transform - Portrait Mode

            Convert portraits into 3D printable tactile representations where **faces are raised**
            and **backgrounds are lowered** - optimized for touch perception.

            ### How it works:
            1. Upload a portrait image (faces will be detected automatically)
            2. Adjust parameters to control the tactile representation
            3. Preview the heightmap (brighter = higher)
            4. Download the STL file for 3D printing

            **Key Innovation**: Height represents semantic importance, not photographic depth!
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                # Image upload
                image_input = gr.Image(
                    label="Upload Portrait Image",
                    type="pil",
                    height=400
                )

                # Physical parameters
                gr.Markdown("### Physical Parameters")
                width_slider = gr.Slider(
                    minimum=50,
                    maximum=300,
                    value=150,
                    step=5,
                    label="Width (mm)",
                    info="Physical width of the model"
                )

                relief_depth_slider = gr.Slider(
                    minimum=0.5,
                    maximum=10,
                    value=3,
                    step=0.5,
                    label="Relief Depth (mm)",
                    info="Maximum height of raised features"
                )

                base_thickness_slider = gr.Slider(
                    minimum=0.5,
                    maximum=5,
                    value=2,
                    step=0.5,
                    label="Base Thickness (mm)",
                    info="Thickness of the base plate"
                )

                # Processing parameters
                gr.Markdown("### Processing Parameters")
                smoothing_slider = gr.Slider(
                    minimum=0,
                    maximum=10,
                    value=2,
                    step=0.5,
                    label="Smoothing",
                    info="Gaussian blur radius (0=sharp, 10=very smooth)"
                )

                resolution_slider = gr.Slider(
                    minimum=64,
                    maximum=256,
                    value=128,
                    step=32,
                    label="Resolution",
                    info="Mesh resolution (higher=more detail, larger file)"
                )

            with gr.Column(scale=1):
                # Semantic parameters
                gr.Markdown("### Semantic Parameters")
                subject_emphasis_slider = gr.Slider(
                    minimum=0,
                    maximum=200,
                    value=120,
                    step=10,
                    label="Subject Emphasis (%)",
                    info="How much to raise faces (higher=more pronounced)"
                )

                background_suppression_slider = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=40,
                    step=5,
                    label="Background Suppression (%)",
                    info="How much to flatten background (higher=flatter)"
                )

                feature_sharpness_slider = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=70,
                    step=5,
                    label="Feature Sharpness (%)",
                    info="Emphasis on facial features (eyes, nose, mouth)"
                )

                edge_strength_slider = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=60,
                    step=5,
                    label="Edge Strength (%)",
                    info="Edge detection intensity for boundaries"
                )

                # Process button
                process_btn = gr.Button(
                    "Generate 3D Model",
                    variant="primary",
                    size="lg"
                )

        with gr.Row():
            with gr.Column(scale=1):
                # Preview
                preview_output = gr.Image(
                    label="Heightmap Preview (Brighter = Higher)",
                    type="pil"
                )

            with gr.Column(scale=1):
                # 3D Model output
                model_output = gr.Model3D(
                    label="3D Preview",
                    clear_color=[0.2, 0.2, 0.2, 1.0],
                    height=400
                )

        # Info output
        info_output = gr.Markdown()

        # Connect processing function
        process_btn.click(
            fn=process_image_wrapper,
            inputs=[
                image_input,
                width_slider,
                relief_depth_slider,
                base_thickness_slider,
                smoothing_slider,
                subject_emphasis_slider,
                background_suppression_slider,
                feature_sharpness_slider,
                edge_strength_slider,
                resolution_slider
            ],
            outputs=[model_output, preview_output, info_output]
        )

        # Example
        gr.Markdown(
            """
            ### Tips:
            - **For portraits**: Keep subject emphasis high (100-150%) and background suppression moderate (30-50%)
            - **For detailed faces**: Increase feature sharpness and edge strength
            - **For smooth results**: Increase smoothing value
            - **For faster preview**: Use lower resolution (64-128), increase for final export
            """
        )

    return demo


def main():
    """
    Main entry point for the GUI application.
    """
    demo = create_gui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )


if __name__ == "__main__":
    main()
