"""
Gradio GUI for Tactile Art Transform - AI Depth Estimation

This module provides a web-based interface for converting images into 3D printable
tactile representations using AI-powered depth estimation.

Uses HuggingFace transformers for state-of-the-art depth mapping.
"""

import base64
import os
import tempfile
import textwrap
from datetime import datetime
from pathlib import Path
from typing import Tuple

import cv2
import gradio as gr
import numpy as np
from PIL import Image, ImageFilter

from art_tactile_transform.core.mesh_generation import heightmap_to_stl
from art_tactile_transform.processing.depth_estimation import query_depth_model

# Default model from environment or fallback
# Using Depth Anything V2 Large for better quality depth estimation
DEFAULT_MODEL = os.getenv("MODEL_NAME", "depth-anything/Depth-Anything-V2-Large-hf")


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
    print(f"\n[GUI] Running AI depth estimation with {model_name}...")
    print(f"[GUI] Image size: {pil_image.size}")
    depth_image = query_depth_model(pil_image, model_name)
    print(f"[GUI] Depth estimation complete. Depth map size: {depth_image.size}")

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

    # Generate STL file with datetime
    temp_dir = Path(tempfile.gettempdir()) / "tactile_art"
    temp_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stl_filename = f"tactile_relief_{timestamp}.stl"
    stl_path = str(temp_dir / stl_filename)

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


def _build_stl_viewer_html(stl_path: str) -> str:
    """Create an embeddable HTML viewer for STL data using three.js."""
    with open(stl_path, "rb") as stl_file:
        stl_bytes = stl_file.read()

    stl_b64 = base64.b64encode(stl_bytes).decode("utf-8")

    # The wrapper div is the previous sibling of the script tag, so we can safely
    # reference it from within the script without needing global identifiers.
    return textwrap.dedent(
        f"""
        <div class="stl-viewer-wrapper" style="display:flex;flex-direction:column;gap:10px;font-family:Inter,system-ui,Segoe UI,Helvetica,Arial,sans-serif;color:#eaeaea;">
            <div class="stl-viewer-canvas" style="height:440px;border-radius:12px;border:1px solid #2f2f2f;background:radial-gradient(circle at 20% 20%, #222 0%, #111 45%, #0b0b0b 100%);overflow:hidden;position:relative;"></div>
            <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;font-size:14px;opacity:0.9;">
                <strong>Interactive 3D preview</strong>
                <span style="opacity:0.8;">Pan with left click, zoom with scroll, rotate with right click.</span>
                <a data-role="download-stl" style="padding:6px 10px;border-radius:8px;background:#2a6df4;color:#fff;text-decoration:none;font-weight:600;">Download STL</a>
            </div>
        </div>
        <script type="module">
            import * as THREE from "https://unpkg.com/three@0.165.0/build/three.module.js";
            import {{ OrbitControls }} from "https://unpkg.com/three@0.165.0/examples/jsm/controls/OrbitControls.js";
            import {{ STLLoader }} from "https://unpkg.com/three@0.165.0/examples/jsm/loaders/STLLoader.js";

            const wrapper = document.currentScript.previousElementSibling;
            const container = wrapper.querySelector('.stl-viewer-canvas');
            const downloadLink = wrapper.querySelector('a[data-role="download-stl"]');

            const downloadUrl = 'data:application/sla;base64,{stl_b64}';
            downloadLink.href = downloadUrl;
            downloadLink.download = 'tactile-relief.stl';

            // Convert base64 STL to a blob for the loader
            const binary = atob('{stl_b64}');
            const buffer = new Uint8Array(binary.length);
            for (let i = 0; i < binary.length; i++) {{
                buffer[i] = binary.charCodeAt(i);
            }}
            const blob = new Blob([buffer], {{ type: 'application/sla' }});
            const url = URL.createObjectURL(blob);

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x0b0b0b);

            const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 1000);
            camera.position.set(1.5, 1.5, 1.5);

            const renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(container.clientWidth, container.clientHeight);
            container.innerHTML = '';
            container.appendChild(renderer.domElement);

            const light = new THREE.HemisphereLight(0xffffff, 0x111111, 1.2);
            scene.add(light);
            const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
            dirLight.position.set(2, 4, 2);
            scene.add(dirLight);

            const loader = new STLLoader();
            loader.load(url, (geometry) => {{
                geometry.computeBoundingBox();
                geometry.computeVertexNormals();

                const material = new THREE.MeshStandardMaterial({{
                    color: 0x5a9bff,
                    roughness: 0.35,
                    metalness: 0.15,
                    flatShading: false,
                }});

                const mesh = new THREE.Mesh(geometry, material);
                scene.add(mesh);

                const bbox = geometry.boundingBox;
                const size = new THREE.Vector3();
                bbox.getSize(size);
                const maxDim = Math.max(size.x, size.y, size.z);
                const scale = 1.4 / maxDim;
                mesh.scale.setScalar(scale);
                bbox.getCenter(mesh.position).multiplyScalar(-1 * scale);

                const controls = new OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.screenSpacePanning = false;
                controls.target.set(0, 0, 0);

                camera.position.set(2, 1.2, 2);
                camera.lookAt(new THREE.Vector3(0, 0, 0));

                const animate = () => {{
                    requestAnimationFrame(animate);
                    controls.update();
                    renderer.render(scene, camera);
                }};
                animate();
            }});

            const resizeObserver = new ResizeObserver(() => {{
                const rect = container.getBoundingClientRect();
                camera.aspect = rect.width / rect.height;
                camera.updateProjectionMatrix();
                renderer.setSize(rect.width, rect.height);
            }});
            resizeObserver.observe(container);
        </script>
        """
    )


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
        - **AI Model**: Depth Anything V2 Large
        - Width: {width_mm:.1f} mm × Height: {height_mm:.1f} mm
        - Relief depth: {relief_depth_mm:.1f} mm
        - Base thickness: {base_thickness_mm:.1f} mm
        - Total thickness: {total_height_mm:.1f} mm
        - Resolution: {resolution}x{resolution} vertices
        - Depth contrast: {contrast:.1f}x

        **STL file ready for download!**

        **Tip**: Check the heightmap preview (should show depth variation)
        """

        return preview, stl_path, info

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

            **Powered by**: Depth Anything V2 Large (NeurIPS 2024) - [Model Card](https://huggingface.co/depth-anything/Depth-Anything-V2-Large-hf)
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
                    maximum=1000,
                    value=300,
                    step=10,
                    label="Width (mm)",
                    info="Physical width of the model"
                )

                relief_depth_slider = gr.Slider(
                    minimum=0.5,
                    maximum=50,
                    value=10,
                    step=0.5,
                    label="Relief Depth (mm)",
                    info="Maximum height of raised features"
                )

                base_thickness_slider = gr.Slider(
                    minimum=0.5,
                    maximum=20,
                    value=5,
                    step=0.5,
                    label="Base Thickness (mm)",
                    info="Thickness of the base plate"
                )

                # Processing parameters
                gr.Markdown("### Processing Parameters")
                smoothing_slider = gr.Slider(
                    minimum=0,
                    maximum=20,
                    value=0,
                    step=0.5,
                    label="Smoothing",
                    info="Gaussian blur radius (0=sharp, 20=very smooth)"
                )

                resolution_slider = gr.Slider(
                    minimum=64,
                    maximum=1024,
                    value=256,
                    step=64,
                    label="Resolution",
                    info="Mesh resolution (256=good, 512=high, 1024=extreme detail but huge files)"
                )

            with gr.Column(scale=1):
                # AI Depth Parameters
                gr.Markdown("### AI Depth Parameters")
                contrast_slider = gr.Slider(
                    minimum=0.5,
                    maximum=10.0,
                    value=3.0,
                    step=0.1,
                    label="Depth Contrast",
                    info="Adjust depth contrast (1.0=normal, 3.0=strong, 10.0=extreme)"
                )

                invert_depth_checkbox = gr.Checkbox(
                    label="Invert Depth",
                    value=True,
                    info="Swap near/far (default ON for relief to pop out)"
                )

                gr.Markdown("""
                ### About AI Depth Estimation

                Uses **Depth Anything V2 Large** (NeurIPS 2024) - state-of-the-art depth model.

                **First run**: Downloads AI model (~1.3GB) - takes 5-10 minutes
                **Subsequent runs**: Cached, processes in seconds

                **Models**:
                - [Depth Anything V2 Large](https://huggingface.co/depth-anything/Depth-Anything-V2-Large-hf)
                - Trained on 595K labeled + 62M unlabeled images
                - Superior to MiDaS, ZoeDepth, and V1

                **Tips**:
                - Default contrast (1.8x) creates pronounced depth
                - Increase to 2.5-3.0x for dramatic tactile relief
                - Enable "Invert Depth" if background is raised
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

        # Download + Info output
        stl_file_output = gr.File(label="Download STL")
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
            outputs=[preview_output, stl_file_output, info_output]
        )

        # Tips
        gr.Markdown(
            """
            ### Tips for Best Results:
            - **Depth Contrast**: Default 1.8x creates good depth. Increase to 2.5-3.0x for dramatic tactile relief
            - **Invert Depth**: Enable if background appears raised instead of subject
            - **Smoothing**: 0-2 for sharp details, 3-5 for smooth tactile surfaces, 5-10 for very smooth
            - **Resolution**: 64-128 for fast preview, 256 for final export
            - **Relief Depth**: 2-3mm for subtle, 5-10mm for pronounced tactile features

            **Model Info**: Depth Anything V2 Large outperforms MiDaS and older models significantly
            """
        )

    return demo


def main():
    """
    Main entry point for the GUI application.
    """
    demo = create_gui()
    print("\n" + "="*60)
    print("Launching Gradio GUI...")
    print("="*60)
    print("Access the GUI at: http://localhost:7860")
    print("\nIf the 3D preview appears blank:")
    print("  1. Wait 5-10 seconds for the viewer to load")
    print("  2. Try a different browser (Chrome recommended)")
    print("  3. Check the heightmap preview (should show depth)")
    print("  4. Download the STL and view in a 3D viewer")
    print("="*60 + "\n")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=True  # Enable debug mode for better error messages
    )


if __name__ == "__main__":
    main()
