"""Depth estimation using transformer models."""

from typing import Optional

import torch
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
        # Force CPU usage to avoid GPU memory issues
        device = "cpu"
        print(f"Loading depth model: {model_name} (using {device})")

        # Initialize depth estimation pipeline with explicit CPU device
        depth_estimator = pipeline(
            "depth-estimation",
            model=model_name,
            device=device
        )

        # Run inference
        result = depth_estimator(image)

        # Extract depth map from result
        depth_map = result["depth"]

        return depth_map
    except torch.cuda.OutOfMemoryError as e:
        raise RuntimeError(
            f"GPU out of memory. This application is configured to use CPU. "
            f"Please restart the application to clear GPU memory. Error: {e}"
        ) from e
    except Exception as e:
        raise RuntimeError(f"Failed to run depth estimation: {e}") from e
