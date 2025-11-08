"""Depth estimation using transformer models."""

from typing import Optional

from PIL import Image
from transformers import pipeline


def query_depth_model(image: Image.Image, model_name: str) -> Image.Image:
    """Use transformers pipeline for local depth estimation.

    Args:
        image: Input PIL Image
        model_name: Name of the depth estimation model to use

    Returns:
        Depth map as PIL Image

    Raises:
        RuntimeError: If depth estimation fails
        ValueError: If image or model_name is invalid
    """
    if image is None:
        raise ValueError("Image cannot be None")
    if not model_name:
        raise ValueError("Model name cannot be empty")

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
