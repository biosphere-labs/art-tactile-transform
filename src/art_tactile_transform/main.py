import argparse
import os
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Callable, Optional

import numpy as np
import requests
from dotenv import dotenv_values, load_dotenv
from PIL import Image, ImageFilter
from scipy.ndimage import gaussian_filter

try:
    from colorama import Fore, Style, init as colorama_init
except ImportError:  # pragma: no cover - fallback when colorama isn't installed
    class _FallbackFore:
        CYAN = "\033[36m"
        GREEN = "\033[32m"
        RED = "\033[31m"
        YELLOW = "\033[33m"

    class _FallbackStyle:
        RESET_ALL = "\033[0m"

    def colorama_init(*_args: object, **_kwargs: object) -> None:
        return None

    Fore = _FallbackFore()  # type: ignore[assignment]
    Style = _FallbackStyle()  # type: ignore[assignment]


API_URL = "https://api-inference.huggingface.co/models/{model_name}"


@dataclass
class EnvSetting:
    """Metadata describing an environment variable used by the CLI."""

    key: str
    description: str
    required: bool = False
    default: Optional[str] = None


ENV_SETTINGS: list[EnvSetting] = [
    EnvSetting("MODEL_NAME", "Hugging Face model name", required=True),
    EnvSetting("IMAGE_PATH", "Path to the input image", required=True),
    EnvSetting("OUTPUT_PATH", "Output STL file path", required=True),
    EnvSetting("RESOLUTION", "Output resolution (pixels)", default="64"),
    EnvSetting("HF_API_TOKEN", "Hugging Face API token (optional)", default=""),
    EnvSetting("MIN_HEIGHT_MM", "Minimum height in millimetres", default="0.2"),
    EnvSetting("MAX_HEIGHT_MM", "Maximum height in millimetres", default="2.0"),
    EnvSetting("BASE_THICKNESS_MM", "Base thickness in millimetres", default="1.0"),
    EnvSetting("PIXEL_SCALE_MM", "Pixel scale in millimetres", default="0.2"),
    EnvSetting("INVERT_HEIGHTS", "Invert heights? (true/false)", default="false"),
    EnvSetting("GAUSSIAN_BLUR_RADIUS", "Gaussian blur radius", default="0"),
    EnvSetting("CLAMP_MIN", "Clamp minimum value", default="0"),
    EnvSetting("CLAMP_MAX", "Clamp maximum value", default="255"),
    EnvSetting("BORDER_PIXELS", "Border pixels to pad", default="0"),
]


def _resolve_default(setting: EnvSetting, defaults: dict[str, str]) -> tuple[Optional[str], Optional[str]]:
    """Return the default to apply and the value to display to the user."""

    raw_default = defaults.get(setting.key)
    if raw_default in (None, ""):
        raw_default = os.environ.get(setting.key)
    if raw_default is None:
        raw_default = setting.default

    apply_default = raw_default
    if setting.required and (apply_default is None or apply_default == ""):
        apply_default = None

    display_default = raw_default if raw_default not in (None, "") else None
    return apply_default, display_default


def prompt_for_env_values(
    env_file: str | Path = ".env",
    input_func: Callable[[str], str] | None = None,
) -> dict[str, str]:
    """Interactively ask the user for environment values and set them."""

    defaults = dotenv_values(env_file)
    colorama_init(autoreset=True)

    input_func = input if input_func is None else input_func
    results: dict[str, str] = {}

    for setting in ENV_SETTINGS:
        apply_default, display_default = _resolve_default(setting, defaults)

        while True:
            prompt = f"{Fore.CYAN}{setting.description} ({setting.key})"
            if display_default is not None:
                prompt += f" [{display_default}]"
            prompt += f": {Style.RESET_ALL}"

            response = input_func(prompt).strip()

            if not response:
                if apply_default is not None:
                    value = apply_default
                elif setting.required:
                    print(
                        f"{Fore.RED}A value is required for {setting.key}.{Style.RESET_ALL}"
                    )
                    continue
                else:
                    value = ""
            else:
                value = response

            results[setting.key] = value
            os.environ[setting.key] = value
            break

    return results


def interactive_cli(
    env_file: str | Path = ".env",
    input_func: Callable[[str], str] | None = None,
) -> str:
    """Run the interactive CLI to collect environment variables and generate output."""

    colorama_init(autoreset=True)
    print(f"{Fore.GREEN}Art Tactile Transform interactive setup{Style.RESET_ALL}")

    prompt_for_env_values(env_file=env_file, input_func=input_func)

    print(f"{Fore.YELLOW}Generating tactile model…{Style.RESET_ALL}")
    result = generate_3d(env_file=env_file)
    print(f"{Fore.GREEN}✓ Generated tactile model: {result}{Style.RESET_ALL}")
    return result


def query_hf_api(image_bytes: bytes, model_name: str, api_token: Optional[str] = None) -> bytes:
    """Send image bytes to the Hugging Face inference API and return depth map bytes."""
    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}

    try:
        response = requests.post(
            API_URL.format(model_name=model_name),
            headers=headers,
            data=image_bytes,
            timeout=30
        )
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to query Hugging Face API: {e}") from e
    except Exception as e:  # pragma: no cover - safety net for unexpected errors
        raise RuntimeError(f"Failed to query Hugging Face API: {e}") from e


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


def generate_3d(env_file: str | Path | None = None) -> str:
    """Load image, query model, and generate STL file."""
    # Load environment variables
    if env_file is not None:
        load_dotenv(env_file)
    else:
        load_dotenv()

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
        # Load and preprocess image
        with open(image_path, "rb") as img_file:
            image_bytes = img_file.read()

        # Query depth estimation model
        print(f"Querying depth model: {model_name}")
        depth_bytes = query_hf_api(image_bytes, model_name, api_token)

        # Process depth map
        depth_image = Image.open(BytesIO(depth_bytes))
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


def main(argv: Optional[list[str]] = None) -> None:
    """CLI entry point."""

    parser = argparse.ArgumentParser(
        description="Generate tactile STL models from flat images"
    )
    parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Launch an interactive prompt to configure environment settings.",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Path to a .env file providing default configuration values.",
    )
    args = parser.parse_args(argv)

    try:
        if args.interactive:
            interactive_cli(env_file=args.env_file)
        else:
            output_file = generate_3d(env_file=args.env_file)
            print(f"Generated: {output_file}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()