"""Image processing and preprocessing for tactile art generation."""

from typing import Optional

import numpy as np
from PIL import Image, ImageFilter


def process_image(
    image: Image.Image,
    gaussian_blur_radius: int = 0,
    clamp_min: int = 0,
    clamp_max: int = 255,
    border_pixels: int = 0,
    invert_heights: bool = False,
) -> Image.Image:
    """Apply image processing pipeline to enhance tactile representation.

    Args:
        image: Input PIL Image
        gaussian_blur_radius: Radius for Gaussian blur (0 = no blur)
        clamp_min: Minimum value for clamping (0-255)
        clamp_max: Maximum value for clamping (0-255)
        border_pixels: Number of pixels to add as border
        invert_heights: Whether to invert the height values

    Returns:
        Processed PIL Image in grayscale mode

    Raises:
        ValueError: If parameters are invalid
    """
    if clamp_min < 0 or clamp_min > 255:
        raise ValueError("clamp_min must be between 0 and 255")
    if clamp_max < 0 or clamp_max > 255:
        raise ValueError("clamp_max must be between 0 and 255")
    if clamp_min >= clamp_max:
        raise ValueError("clamp_min must be less than clamp_max")
    if gaussian_blur_radius < 0:
        raise ValueError("gaussian_blur_radius must be non-negative")
    if border_pixels < 0:
        raise ValueError("border_pixels must be non-negative")

    # Convert to grayscale
    if image.mode != "L":
        image = image.convert("L")

    # Add border if specified
    if border_pixels > 0:
        width, height = image.size
        new_image = Image.new(
            "L", (width + 2 * border_pixels, height + 2 * border_pixels), clamp_min
        )
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

    return Image.fromarray((img_array * 255).astype(np.uint8), "L")


def resize_to_resolution(
    image: Image.Image, resolution: int, maintain_aspect: bool = True
) -> Image.Image:
    """Resize image to target resolution.

    Args:
        image: Input PIL Image
        resolution: Target resolution (width in pixels)
        maintain_aspect: Whether to maintain aspect ratio

    Returns:
        Resized PIL Image

    Raises:
        ValueError: If resolution is invalid
    """
    if resolution <= 0:
        raise ValueError("Resolution must be positive")

    if maintain_aspect:
        width, height = image.size
        aspect_ratio = height / width
        new_height = int(resolution * aspect_ratio)
        return image.resize((resolution, new_height), Image.Resampling.LANCZOS)
    else:
        return image.resize((resolution, resolution), Image.Resampling.LANCZOS)


def image_to_heightmap(image: Image.Image) -> np.ndarray:
    """Convert a grayscale image to a normalized heightmap.

    Args:
        image: Input grayscale PIL Image

    Returns:
        2D numpy array with values normalized to 0.0-1.0

    Raises:
        ValueError: If image is not grayscale
    """
    if image.mode != "L":
        raise ValueError("Image must be in grayscale mode ('L')")

    heightmap = np.array(image, dtype=float) / 255.0
    return heightmap
