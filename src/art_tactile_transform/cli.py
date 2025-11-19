"""Command-line interface for art-tactile-transform."""

import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from PIL import Image

from .core.image_processing import image_to_heightmap, process_image, resize_to_resolution
from .core.mesh_generation import heightmap_to_stl
from .processing.depth_estimation import query_depth_model
from .utils.file_handling import ensure_output_dir, validate_image_file
from .utils.logging import get_logger, setup_logging


def generate_3d() -> str:
    """Load image, query model, and generate STL file.

    This function maintains backwards compatibility with the original implementation.
    It reads configuration from environment variables.

    Returns:
        Path to the generated STL file

    Raises:
        ValueError: If required environment variables are missing
        FileNotFoundError: If input image not found
        RuntimeError: If generation fails
    """
    # Load environment variables
    load_dotenv(override=True)

    # Required parameters
    model_name = os.getenv("MODEL_NAME")
    image_path = os.getenv("IMAGE_PATH")
    output_path = os.getenv("OUTPUT_PATH")

    if not model_name or not image_path or not output_path:
        raise ValueError(
            "MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set in .env file"
        )

    # Optional parameters with defaults
    resolution = int(os.getenv("RESOLUTION", "64"))

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
            depth_image,
            gaussian_blur_radius,
            clamp_min,
            clamp_max,
            border_pixels,
            invert_heights,
        )

        # Resize to target resolution
        processed_image = resize_to_resolution(processed_image, resolution, False)

        # Convert to heightmap
        heightmap = image_to_heightmap(processed_image)

        # Generate STL with proper scaling
        print(f"Generating STL file: {output_path}")
        heightmap_to_stl(
            heightmap,
            output_path,
            min_height_mm,
            max_height_mm,
            base_thickness_mm,
            pixel_scale_mm,
        )

        print(f"✓ Successfully generated tactile model: {output_path}")
        return output_path

    except Exception as e:
        raise RuntimeError(f"Failed to generate 3D model: {e}") from e


def main() -> None:
    """CLI entry point.

    This maintains backwards compatibility with the original CLI interface.
    """
    # Set up basic logging
    setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))
    logger = get_logger("cli")

    try:
        logger.info("Starting tactile art generation")
        output_file = generate_3d()
        logger.info(f"Generated: {output_file}")
        print(f"Generated: {output_file}")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
