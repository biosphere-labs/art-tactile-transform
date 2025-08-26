import os
import numpy as np
from PIL import Image, ImageFilter
from stl import mesh
from dotenv import load_dotenv

# Optional import of Hugging Face transformers. If it (or torch/timm) is not available
# or fails to import (e.g., due to CUDA/PyTorch build issues like _has_magma), we
# gracefully disable HF depth features by setting hf_pipeline to None.
hf_pipeline = None
try:
    from transformers import pipeline as _hf_pipeline
    hf_pipeline = _hf_pipeline
except Exception:
    hf_pipeline = None

def bool_from_env(val: str, default: bool = False) -> bool:
    if val is None:
        return default
    return str(val).strip().lower() in {"1", "true", "yes", "y", "on"}


def generate_depth_map_hf(
    input_image_path: str,
    output_depth_png_path: str = "depth.png",
    model_id: str = "Intel/dpt-hybrid-midas",
) -> str:
    """
    Generate a depth map using a Hugging Face depth-estimation model and save as 8-bit PNG.

    Returns the path to the saved depth PNG.
    """
    if hf_pipeline is None:
        raise RuntimeError(
            "Hugging Face transformers is not installed. Please install 'transformers', 'torch', and 'timm' or set USE_HF_DEPTH=false."
        )

    pipe = hf_pipeline("depth-estimation", model=model_id)

    # Open image with PIL to ensure compatibility
    img = Image.open(input_image_path).convert("RGB")
    result = pipe(img)

    # result["depth"] is a PIL Image (float32), larger resolution depending on model
    depth_pil = result["depth"]

    # Convert to numpy for normalization to 0..255
    depth_np = np.array(depth_pil, dtype=np.float32)

    # Normalize: closer = brighter or invert? We'll keep larger depth darker (typical),
    # and let the existing pipeline's invert_heights control if needed.
    # Scale to 0..255 robustly using percentiles to avoid outliers
    p2 = float(np.percentile(depth_np, 2))
    p98 = float(np.percentile(depth_np, 98))
    if p98 <= p2:
        p2, p98 = float(depth_np.min()), float(depth_np.max())
    depth_np = np.clip((depth_np - p2) / max(p98 - p2, 1e-6), 0.0, 1.0)

    depth_uint8 = (depth_np * 255.0).astype(np.uint8)
    out_img = Image.fromarray(depth_uint8, mode="L")
    out_img.save(output_depth_png_path)
    return output_depth_png_path


def png_to_3d_stl(
    input_png: str,
    output_stl: str,
    min_height_mm: float = 0.2,
    max_height_mm: float = 2.0,
    base_thickness_mm: float = 1.0,
    pixel_scale_mm: float = 0.2,
    invert_heights: bool = False,
    gaussian_blur_radius: float = 0.0,
    clamp_min: int = 0,
    clamp_max: int = 255,
    border_pixels: int = 0,
):
    """
    Convert a grayscale PNG into a solid STL suitable for tactile printing.

    - The top surface height is mapped from grayscale to [min_height_mm, max_height_mm]
      (after optional clamp/normalize and invert), then added on top of a base of
      thickness base_thickness_mm.
    - The model includes a bottom plate and side walls to make it a watertight solid.

    Parameters are in millimeters for Z and XY scales.
    """
    # Load the image in grayscale
    img = Image.open(input_png).convert('L')

    # Optional blur to smooth noise
    if gaussian_blur_radius and gaussian_blur_radius > 0:
        img = img.filter(ImageFilter.GaussianBlur(radius=gaussian_blur_radius))

    img_array = np.array(img).astype(np.float32)  # 0..255

    # Optional border: pad the image with constant background (use the min after clamp)
    if border_pixels and border_pixels > 0:
        pad_val = float(clamp_min)
        img_array = np.pad(
            img_array,
            ((border_pixels, border_pixels), (border_pixels, border_pixels)),
            mode='constant',
            constant_values=pad_val,
        )

    # Clamp then normalize to 0..1
    clamp_min_f = float(clamp_min)
    clamp_max_f = float(clamp_max)
    clamp_max_f = max(clamp_max_f, clamp_min_f + 1.0)  # avoid divide by zero
    img_array = np.clip(img_array, clamp_min_f, clamp_max_f)
    norm = (img_array - clamp_min_f) / (clamp_max_f - clamp_min_f)

    if invert_heights:
        norm = 1.0 - norm

    # Map to heights (mm)
    heights = min_height_mm + norm * (max_height_mm - min_height_mm)

    # Dimensions
    height_px, width_px = heights.shape

    # Construct vertices: top grid and bottom grid
    # Top Z includes base thickness
    top_z = base_thickness_mm + heights
    bottom_z = 0.0

    vertices = []
    faces = []

    # Helper to index top and bottom vertex indices
    def t_index(i, j):
        return i * width_px + j

    def b_index(i, j):
        return width_px * height_px + i * width_px + j

    # Create vertices for each grid point (top first, then bottom)
    for i in range(height_px):
        for j in range(width_px):
            x = j * pixel_scale_mm
            y = i * pixel_scale_mm
            z = float(top_z[i, j])
            vertices.append([x, y, z])  # top vertex

    for i in range(height_px):
        for j in range(width_px):
            x = j * pixel_scale_mm
            y = i * pixel_scale_mm
            z = bottom_z
            vertices.append([x, y, z])  # bottom vertex

    # Top faces (two triangles per cell)
    for i in range(height_px - 1):
        for j in range(width_px - 1):
            v1 = t_index(i, j)
            v2 = t_index(i, j + 1)
            v3 = t_index(i + 1, j)
            v4 = t_index(i + 1, j + 1)
            faces.append([v1, v2, v3])
            faces.append([v2, v4, v3])

    # Bottom faces (two triangles per cell), reverse winding to face outward
    for i in range(height_px - 1):
        for j in range(width_px - 1):
            v1 = b_index(i, j)
            v2 = b_index(i, j + 1)
            v3 = b_index(i + 1, j)
            v4 = b_index(i + 1, j + 1)
            faces.append([v3, v2, v1])
            faces.append([v3, v4, v2])

    # Side walls around the perimeter (quads split into triangles)
    # Left edge (j = 0)
    j = 0
    for i in range(height_px - 1):
        tt1 = t_index(i, j)
        tt2 = t_index(i + 1, j)
        bb1 = b_index(i, j)
        bb2 = b_index(i + 1, j)
        faces.append([tt1, bb1, tt2])
        faces.append([tt2, bb1, bb2])

    # Right edge (j = width_px - 1)
    j = width_px - 1
    for i in range(height_px - 1):
        tt1 = t_index(i, j)
        tt2 = t_index(i + 1, j)
        bb1 = b_index(i, j)
        bb2 = b_index(i + 1, j)
        faces.append([tt2, bb1, tt1])
        faces.append([tt2, bb2, bb1])

    # Top edge (i = 0)
    i = 0
    for j in range(width_px - 1):
        tt1 = t_index(i, j)
        tt2 = t_index(i, j + 1)
        bb1 = b_index(i, j)
        bb2 = b_index(i, j + 1)
        faces.append([tt1, tt2, bb1])
        faces.append([tt2, bb2, bb1])

    # Bottom edge (i = height_px - 1)
    i = height_px - 1
    for j in range(width_px - 1):
        tt1 = t_index(i, j)
        tt2 = t_index(i, j + 1)
        bb1 = b_index(i, j)
        bb2 = b_index(i, j + 1)
        faces.append([tt2, tt1, bb1])
        faces.append([bb2, tt2, bb1])

    # Convert to numpy arrays
    vertices = np.array(vertices, dtype=np.float32)
    faces = np.array(faces, dtype=np.int32)

    # Create the mesh
    model = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))

    # Add faces to the mesh
    for i_f, face in enumerate(faces):
        for j_v in range(3):
            model.vectors[i_f][j_v] = vertices[face[j_v]]

    # Save the mesh to file
    model.save(output_stl)

def read_env_and_run():
    load_dotenv()
    # Input/Output
    # If using HF depth, INPUT_IMAGE can be any RGB image; otherwise INPUT_PNG should be a grayscale PNG.
    input_image = os.getenv('INPUT_IMAGE')  # used when USE_HF_DEPTH=true
    input_png = os.getenv('INPUT_PNG', '../data/pic1.png')
    output_file = os.getenv('OUTPUT_STL', '../data/output.stl')

    # Heights and base
    min_height_mm = float(os.getenv('MIN_HEIGHT_MM', '0.2'))
    max_height_mm = float(os.getenv('MAX_HEIGHT_MM', '2.0'))
    base_thickness_mm = float(os.getenv('BASE_THICKNESS_MM', '1.0'))

    # XY scaling
    pixel_scale_mm = float(os.getenv('PIXEL_SCALE_MM', '0.2'))

    # Options
    invert_heights = bool_from_env(os.getenv('INVERT_HEIGHTS', 'false'), default=False)
    gaussian_blur_radius = float(os.getenv('GAUSSIAN_BLUR_RADIUS', '0.0'))
    clamp_min = int(os.getenv('CLAMP_MIN', '0'))
    clamp_max = int(os.getenv('CLAMP_MAX', '255'))
    border_pixels = int(os.getenv('BORDER_PIXELS', '0'))

    # HF depth options
    use_hf_depth = bool_from_env(os.getenv('USE_HF_DEPTH', 'true'), default=False)
    depth_model = os.getenv('DEPTH_MODEL', 'Intel/dpt-hybrid-midas')
    depth_png_path = os.getenv('DEPTH_PNG', 'depth.png')

    # If transformers (and its torch deps) failed to import, force-disable HF depth to avoid crashes
    if use_hf_depth and hf_pipeline is None:
        print("Warning: transformers/torch not available or failed to import. Disabling USE_HF_DEPTH.")
        use_hf_depth = False

    print('Generating STL with parameters:')
    print(f'  USE_HF_DEPTH={use_hf_depth}')
    if use_hf_depth:
        print(f'  INPUT_IMAGE={input_image if input_image else input_png}')
        print(f'  DEPTH_MODEL={depth_model}')
        print(f'  DEPTH_PNG(out)={depth_png_path}')
    else:
        print(f'  INPUT_PNG={input_png}')
    print(f'  OUTPUT_STL={output_file}')
    print(f'  MIN_HEIGHT_MM={min_height_mm}, MAX_HEIGHT_MM={max_height_mm}')
    print(f'  BASE_THICKNESS_MM={base_thickness_mm}')
    print(f'  PIXEL_SCALE_MM={pixel_scale_mm}')
    print(f'  INVERT_HEIGHTS={invert_heights}')
    print(f'  GAUSSIAN_BLUR_RADIUS={gaussian_blur_radius}')
    print(f'  CLAMP_MIN={clamp_min}, CLAMP_MAX={clamp_max}')
    print(f'  BORDER_PIXELS={border_pixels}')

    # If requested, create a depth map from an image via Hugging Face, then feed it
    stl_input_png = input_png
    if use_hf_depth:
        source_img = input_image if input_image else input_png
        if not os.path.exists(source_img):
            raise FileNotFoundError(f"Source image not found: {source_img}")
        print('  Running Hugging Face depth-estimation to produce heightmap...')
        stl_input_png = generate_depth_map_hf(
            input_image_path=source_img,
            output_depth_png_path=depth_png_path,
            model_id=depth_model,
        )
        print(f'  Depth map saved to: {stl_input_png}')

    png_to_3d_stl(
        input_png=stl_input_png,
        output_stl=output_file,
        min_height_mm=min_height_mm,
        max_height_mm=max_height_mm,
        base_thickness_mm=base_thickness_mm,
        pixel_scale_mm=pixel_scale_mm,
        invert_heights=invert_heights,
        gaussian_blur_radius=gaussian_blur_radius,
        clamp_min=clamp_min,
        clamp_max=clamp_max,
        border_pixels=border_pixels,
    )


# Example usage
if __name__ == "__main__":
    read_env_and_run()
