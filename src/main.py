import os
from io import BytesIO

import numpy as np
import requests
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/{model_name}"


def query_hf_api(image_bytes: bytes, model_name: str, api_token: str | None = None) -> bytes:
    """Send image bytes to the Hugging Face inference API and return depth map bytes."""
    headers = {"Authorization": f"Bearer {api_token}"} if api_token else {}
    response = requests.post(API_URL.format(model_name=model_name), headers=headers, data=image_bytes)
    response.raise_for_status()
    return response.content


def heightmap_to_stl(heightmap: np.ndarray, output_path: str) -> None:
    """Save a simple ASCII STL derived from the heightmap."""
    height, width = heightmap.shape
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("solid model\n")
        for i in range(height - 1):
            for j in range(width - 1):
                z00 = heightmap[i, j]
                z10 = heightmap[i + 1, j]
                z01 = heightmap[i, j + 1]
                z11 = heightmap[i + 1, j + 1]
                f.write("  facet normal 0 0 1\n    outer loop\n")
                f.write(f"      vertex {i} {j} {z00}\n")
                f.write(f"      vertex {i + 1} {j} {z10}\n")
                f.write(f"      vertex {i + 1} {j + 1} {z11}\n")
                f.write("    endloop\n  endfacet\n")
                f.write("  facet normal 0 0 1\n    outer loop\n")
                f.write(f"      vertex {i} {j} {z00}\n")
                f.write(f"      vertex {i + 1} {j + 1} {z11}\n")
                f.write(f"      vertex {i} {j + 1} {z01}\n")
                f.write("    endloop\n  endfacet\n")
        f.write("endsolid model\n")


def generate_3d() -> str:
    """Load image, query model, and generate STL file."""
    model_name = os.getenv("MODEL_NAME")
    image_path = os.getenv("IMAGE_PATH")
    output_path = os.getenv("OUTPUT_PATH")
    resolution = int(os.getenv("RESOLUTION", "64"))
    api_token = os.getenv("HF_API_TOKEN")

    if not model_name or not image_path or not output_path:
        raise ValueError("MODEL_NAME, IMAGE_PATH and OUTPUT_PATH must be set")

    with open(image_path, "rb") as img_file:
        image_bytes = img_file.read()

    depth_bytes = query_hf_api(image_bytes, model_name, api_token)
    depth_image = Image.open(BytesIO(depth_bytes)).convert("L").resize((resolution, resolution))
    heightmap = np.array(depth_image, dtype=float) / 255.0
    heightmap_to_stl(heightmap, output_path)
    return output_path


if __name__ == "__main__":
    generate_3d()
