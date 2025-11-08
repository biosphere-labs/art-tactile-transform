import os
import sys
from io import BytesIO
from pathlib import Path
from typing import Optional

import numpy as np
from dotenv import load_dotenv
from PIL import Image, ImageFilter
from transformers import pipeline


def query_depth_model(image: Image.Image, model_name: str) -> Image.Image:
    """Use transformers pipeline for local depth estimation."""
    try:
        # Initialize depth estimation pipeline
        print(f"Loading depth model: {model_name}")
        depth_estimator = pipeline("depth-estimation", model=model_name)

        # Run inference
        result = depth_estimator(image)

        # Extract depth map from result
        depth_map = result["depth"]

        return depth_map
    except Exception as e:
        raise RuntimeError(f"Failed to run depth estimation: {e}") from e


def calculate_normals(z00: float, z10: float, z01: float, z11: float,
                     i: int, j: int, pixel_scale: float) -> tuple[float, float, float]:
    """Calculate proper surface normals for STL triangles."""
    # Create vectors for the triangle surface
    v1 = np.array([pixel_scale, 0.0, z10 - z00])
    v2 = np.array([0.0, pixel_scale, z01 - z00])

    # Cross product gives normal vector
    normal = np.cross(v1, v2)
    length = np.linalg.norm(normal)

    if length > 0:
        normal = normal / length
    else:
        normal = np.array([0.0, 0.0, 1.0])

    return tuple(normal)


def heightmap_to_stl(heightmap: np.ndarray, output_path: str,
                    min_height_mm: float = 0.2, max_height_mm: float = 2.0,
                    base_thickness_mm: float = 1.0, pixel_scale_mm: float = 0.2) -> None:
    """Save an enhanced ASCII STL derived from the heightmap with proper scaling."""
    height, width = heightmap.shape

    # Normalize heightmap to physical dimensions
    normalized_heights = (heightmap * (max_height_mm - min_height_mm) +
                         min_height_mm + base_thickness_mm)

    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("solid tactile_model\n")

        # Generate top surface triangles
        for i in range(height - 1):
            for j in range(width - 1):
                z00 = normalized_heights[i, j]
                z10 = normalized_heights[i + 1, j]
                z01 = normalized_heights[i, j + 1]
                z11 = normalized_heights[i + 1, j + 1]

                x0, x1 = i * pixel_scale_mm, (i + 1) * pixel_scale_mm
                y0, y1 = j * pixel_scale_mm, (j + 1) * pixel_scale_mm

                # First triangle
                normal = calculate_normals(z00, z10, z01, z11, i, j, pixel_scale_mm)
                f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
                f.write("    outer loop\n")
                f.write(f"      vertex {x0:.3f} {y0:.3f} {z00:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y0:.3f} {z10:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y1:.3f} {z11:.3f}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")

                # Second triangle
                f.write(f"  facet normal {normal[0]:.6f} {normal[1]:.6f} {normal[2]:.6f}\n")
                f.write("    outer loop\n")
                f.write(f"      vertex {x0:.3f} {y0:.3f} {z00:.3f}\n")
                f.write(f"      vertex {x1:.3f} {y1:.3f} {z11:.3f}\n")
                f.write(f"      vertex {x0:.3f} {y1:.3f} {z01:.3f}\n")
                f.write("    endloop\n")
                f.write("  endfacet\n")

        # Add base plate (bottom surface)
        max_x = (height - 1) * pixel_scale_mm
        max_y = (width - 1) * pixel_scale_mm
        base_z = base_thickness_mm

        # Base rectangle (two triangles)
        f.write("  facet normal 0.0 0.0 -1.0\n")
        f.write("    outer loop\n")
        f.write(f"      vertex 0.0 0.0 {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} {max_y:.3f} {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} 0.0 {base_z:.3f}\n")
        f.write("    endloop\n")
        f.write("  endfacet\n")

        f.write("  facet normal 0.0 0.0 -1.0\n")
        f.write("    outer loop\n")
        f.write(f"      vertex 0.0 0.0 {base_z:.3f}\n")
        f.write(f"      vertex 0.0 {max_y:.3f} {base_z:.3f}\n")
        f.write(f"      vertex {max_x:.3f} {max_y:.3f} {base_z:.3f}\n")
        f.write("    endloop\n")
        f.write("  endfacet\n")

        f.write("endsolid tactile_model\n")


def process_image(image: Image.Image, gaussian_blur_radius: int = 0,
                 clamp_min: int = 0, clamp_max: int = 255,
                 border_pixels: int = 0, invert_heights: bool = False) -> Image.Image:
    """Apply image processing pipeline to enhance tactile representation."""
    # Convert to grayscale
    if image.mode != 'L':
        image = image.convert('L')

    # Add border if specified
    if border_pixels > 0:
        width, height = image.size
        new_image = Image.new('L',
                             (width + 2 * border_pixels, height + 2 * border_pixels),
                             clamp_min)
        new_image.paste(image, (border_pixels, border_pixels))
        image = new_image

    # Apply Gaussian blur
    if gaussian_blur_radius > 0:
        image = image.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius))

    # Apply clamping
    img_array = np.array(image)
    img_array = np.clip(img_array, clamp_min, clamp_max)

    # Normalize to 0-1 range
    img_array = (img_array - clamp_min) / (clamp_max - clamp_min)

    # Invert if requested
    if invert_heights:
        img_array = 1.0 - img_array

    return Image.fromarray((img_array * 255).astype(np.uint8), mode='L')


def generate_3d() -> str:
    """Load image, query model, and generate STL file."""
    # Load environment variables
    load_dotenv(override=True)

    # Required parameters
    model_name = os.getenv("MODEL_NAME")
    image_path = os.getenv("IMAGE_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    if not model_name or not image_path or not output_path:
        raise ValueError("MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set in .env file")

    # Optional parameters with defaults
    resolution = int(os.getenv("RESOLUTION", "64"))
    api_token = os.getenv("HF_API_TOKEN")

    # Enhanced parameters
    min_height_mm = float(os.getenv("MIN_HEIGHT_MM", "0.2"))
    max_height_mm = float(os.getenv("MAX_HEIGHT_MM", "2.0"))
    base_thickness_mm = float(os.getenv("BASE_THICKNESS_MM", "1.0"))
    pixel_scale_mm = float(os.getenv("PIXEL_SCALE_MM", "0.2"))
    invert_heights = os.getenv("INVERT_HEIGHTS", "false").lower() == "true"
    gaussian_blur_radius = int(os.getenv("GAUSSIAN_BLUR_RADIUS", "0"))
    clamp_min = int(os.getenv("CLAMP_MIN", "0"))
    clamp_max = int(os.getenv("CLAMP_MAX", "255"))
    border_pixels = int(os.getenv("BORDER_PIXELS", "0"))

    # Validate file paths
    if not Path(image_path).exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")

    # Create output directory if needed
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    try:
        # Load input image
        input_image = Image.open(image_path)

        # Run depth estimation with local model
        print(f"Running depth estimation with: {model_name}")
        depth_image = query_depth_model(input_image, model_name)

        # Process depth map
        processed_image = process_image(
            depth_image, gaussian_blur_radius, clamp_min, clamp_max,
            border_pixels, invert_heights
        )

        # Resize to target resolution
        processed_image = processed_image.resize((resolution, resolution), Image.Resampling.LANCZOS)

        # Convert to heightmap
        heightmap = np.array(processed_image, dtype=float) / 255.0

        # Generate STL with proper scaling
        print(f"Generating STL file: {output_path}")
        heightmap_to_stl(
            heightmap, output_path, min_height_mm, max_height_mm,
            base_thickness_mm, pixel_scale_mm
        )

        print(f"✓ Successfully generated tactile model: {output_path}")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to generate 3D model: {e}") from e


def main() -> None:
    """CLI entry point."""
    try:
        output_file = generate_3d()
        print(f"Generated: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()