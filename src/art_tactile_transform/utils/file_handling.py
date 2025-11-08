"""File handling utilities."""

from pathlib import Path
from typing import List, Optional

from PIL import Image


SUPPORTED_IMAGE_FORMATS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif"}


def validate_image_file(filepath: str) -> Path:
    """Validate that a file exists and is a supported image format.

    Args:
        filepath: Path to image file

    Returns:
        Path object for the validated file

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
    """
    path = Path(filepath)

    if not path.exists():
        raise FileNotFoundError(f"Image file not found: {filepath}")

    if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
        supported = ", ".join(SUPPORTED_IMAGE_FORMATS)
        raise ValueError(
            f"Unsupported image format: {path.suffix}. Supported formats: {supported}"
        )

    return path


def ensure_output_dir(filepath: str) -> Path:
    """Ensure the output directory exists for a file path.

    Args:
        filepath: Output file path

    Returns:
        Path object for the output file

    Raises:
        OSError: If directory cannot be created
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def get_output_filename(
    input_path: str, output_dir: Optional[str] = None, suffix: str = "_tactile"
) -> str:
    """Generate an output filename based on the input filename.

    Args:
        input_path: Input file path
        output_dir: Optional output directory (defaults to input file's directory)
        suffix: Suffix to add before extension

    Returns:
        Output file path as string
    """
    input_file = Path(input_path)
    stem = input_file.stem

    if output_dir:
        output_path = Path(output_dir) / f"{stem}{suffix}.stl"
    else:
        output_path = input_file.parent / f"{stem}{suffix}.stl"

    return str(output_path)


def list_image_files(directory: str) -> List[Path]:
    """List all supported image files in a directory.

    Args:
        directory: Directory path to search

    Returns:
        List of Path objects for image files

    Raises:
        NotADirectoryError: If path is not a directory
    """
    dir_path = Path(directory)

    if not dir_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    image_files = []
    for ext in SUPPORTED_IMAGE_FORMATS:
        image_files.extend(dir_path.glob(f"*{ext}"))
        image_files.extend(dir_path.glob(f"*{ext.upper()}"))

    return sorted(image_files)


def load_image(filepath: str) -> Image.Image:
    """Load and validate an image file.

    Args:
        filepath: Path to image file

    Returns:
        PIL Image object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is not supported
        IOError: If image cannot be loaded
    """
    path = validate_image_file(filepath)

    try:
        image = Image.open(path)
        image.load()  # Force load to catch any errors
        return image
    except Exception as e:
        raise IOError(f"Failed to load image {filepath}: {e}") from e
