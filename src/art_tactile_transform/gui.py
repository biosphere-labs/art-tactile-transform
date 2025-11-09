"""
Gradio GUI for Tactile Art Transform - AI Depth Estimation

This module provides a web-based interface for converting images into 3D printable
tactile representations using AI-powered depth estimation.

Uses HuggingFace transformers for state-of-the-art depth mapping.
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import cv2
import gradio as gr
import numpy as np
from PIL import Image, ImageFilter

from art_tactile_transform.main import heightmap_to_stl
from art_tactile_transform.processing.depth_estimation import query_depth_model

# Default model from environment or fallback
DEFAULT_MODEL = os.getenv("MODEL_NAME", "LiheYoung/depth-anything-small-hf")


def process_depth_map(
    depth_image: Image.Image,
    smoothing: float = 2.0,
    contrast: float = 1.0,
    invert: bool = False,
    clamp_min: int = 0,
    clamp_max: int = 255
) -> np.ndarray:
    """
    Process AI-generated depth map into heightmap.

    Args:
        depth_image: Depth map from AI model (PIL Image)
        smoothing: Gaussian blur radius (0-10)
        contrast: Contrast adjustment (0.5-2.0)
        invert: Invert depth values (far becomes near)
        clamp_min: Minimum value clamp (0-255)
        clamp_max: Maximum value clamp (0-255)

    Returns:
        Heightmap as numpy array normalized 0-1
    """
    # Convert to grayscale if needed
    if depth_image.mode != 'L':
        depth_image = depth_image.convert('L')

    # Convert to numpy array
    depth_array = np.array(depth_image, dtype=np.float32)

    # Apply clamping
    depth_array = np.clip(depth_array, clamp_min, clamp_max)

    # Normalize to 0-1
    if clamp_max > clamp_min:
        depth_array = (depth_array - clamp_min) / (clamp_max - clamp_min)

    # Apply contrast adjustment
    if contrast != 1.0:
        # Adjust around midpoint (0.5)
        depth_array = ((depth_array - 0.5) * contrast) + 0.5
        depth_array = np.clip(depth_array, 0, 1)

    # Invert if requested
    if invert:
        depth_array = 1.0 - depth_array

    # Apply smoothing
    if smoothing > 0:
        from scipy.ndimage import gaussian_filter
        depth_array = gaussian_filter(depth_array, sigma=smoothing)

    # Final normalization
    if depth_array.max() > 0:
        depth_array = depth_array / depth_array.max()

    return depth_array


def process_image_to_stl(
    image: np.ndarray,
    width_mm: float = 150.0,
    relief_depth_mm: float = 3.0,
    base_thickness_mm: float = 2.0,
    smoothing: float = 2.0,
    contrast: float = 1.0,
    invert_depth: bool = False,
    resolution: int = 128,
    model_name: str = DEFAULT_MODEL
) -> Tuple[str, Image.Image]:
    """
    Process image using AI depth estimation and generate STL file.

    Args:
        image: Input image as numpy array (BGR or RGB)
        width_mm: Physical width in millimeters
        relief_depth_mm: Maximum relief height
        base_thickness_mm: Base plate thickness
        smoothing: Gaussian blur radius (0-10)
        contrast: Depth contrast adjustment (0.5-2.0)
        invert_depth: Invert depth (far becomes near)
        resolution: Mesh resolution (vertices per side)
        model_name: HuggingFace model to use

    Returns:
        Tuple of (stl_path, preview_image)
    """
    # Convert numpy array to PIL Image
    if image.shape[2] == 4:  # RGBA
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
    elif image.shape[2] == 3:  # BGR or RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image_rgb = image

    pil_image = Image.fromarray(image_rgb)

    # Run AI depth estimation
    print(f"Running AI depth estimation with {model_name}...")
    depth_image = query_depth_model(pil_image, model_name)

    # Process depth map
    heightmap = process_depth_map(
        depth_image,
        smoothing=smoothing,
        contrast=contrast,
        invert=invert_depth,
        clamp_min=0,
        clamp_max=255
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
    contrast,
    invert_depth,
    resolution
):
    """
    Wrapper for Gradio interface with AI depth estimation.
    """
    if image is None:
        return None, None, "Please upload an image first."

    try:
        # Convert PIL Image to numpy array (Gradio provides PIL Image)
        image_array = np.array(image)

        # Process image with AI depth estimation
        stl_path, preview = process_image_to_stl(
            image_array,
            width_mm=width_mm,
            relief_depth_mm=relief_depth_mm,
            base_thickness_mm=base_thickness_mm,
            smoothing=smoothing,
            contrast=contrast,
            invert_depth=invert_depth,
            resolution=int(resolution),
            model_name=DEFAULT_MODEL
        )

        # Calculate approximate dimensions
        height_mm = width_mm  # Square output
        total_height_mm = relief_depth_mm + base_thickness_mm

        info = f"""
        ### Model Information
        - **AI Model**: {DEFAULT_MODEL}
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
        import traceback
        error_details = traceback.format_exc()
        return None, None, f"Error processing image:\n\n{str(e)}\n\n{error_details}"


def create_gui():
    """
    Create and configure the Gradio interface.
    """
    with gr.Blocks(title="Tactile Art Transform - AI Depth Estimation") as demo:
        gr.Markdown(
            """
            # Tactile Art Transform - AI Depth Estimation

            Convert images into 3D printable tactile representations using state-of-the-art AI.

            ### How it works:
            1. Upload any image (portraits, landscapes, objects, etc.)
            2. AI analyzes the image and generates depth map automatically
            3. Adjust contrast and smoothing to fine-tune the relief
            4. Preview the heightmap (brighter = higher)
            5. Download the STL file for 3D printing

            **Powered by**: HuggingFace Transformers depth-anything-small-hf model
            """
        )

        with gr.Row():
            with gr.Column(scale=1):
                # Image upload
                image_input = gr.Image(
                    label="Upload Image",
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
                # AI Depth Parameters
                gr.Markdown("### AI Depth Parameters")
                contrast_slider = gr.Slider(
                    minimum=0.5,
                    maximum=2.0,
                    value=1.0,
                    step=0.1,
                    label="Depth Contrast",
                    info="Adjust depth contrast (1.0=normal, >1=stronger, <1=softer)"
                )

                invert_depth_checkbox = gr.Checkbox(
                    label="Invert Depth",
                    value=False,
                    info="Swap near/far (try if background is raised)"
                )

                gr.Markdown("""
                ### About AI Depth Estimation

                Uses **depth-anything-small-hf** model for accurate depth mapping.

                **First run**: Downloads AI model (~500MB) - takes 2-5 minutes
                **Subsequent runs**: Instant processing

                **Tip**: If faces appear too flat, increase contrast. If background is raised, enable "Invert Depth".
                """)

                # Process button
                process_btn = gr.Button(
                    "Generate 3D Model with AI",
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
                contrast_slider,
                invert_depth_checkbox,
                resolution_slider
            ],
            outputs=[model_output, preview_output, info_output]
        )

        # Tips
        gr.Markdown(
            """
            ### Tips:
            - **First run**: Wait for AI model download (~500MB, 2-5 min)
            - **Depth Contrast**: Start at 1.0, increase to 1.5-2.0 for stronger relief
            - **Invert Depth**: Enable if background appears raised instead of faces
            - **Smoothing**: Use 0-2 for sharp details, 3-5 for smooth tactile surfaces
            - **Resolution**: Use 64-128 for preview, 256 for final high-quality export
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
