"""Preset management for tactile art generation."""

import json
from pathlib import Path
from typing import Dict, List, Optional

from .parameters import AllParams, PhysicalParams, ProcessingParams, SemanticParams


# Built-in presets
BUILTIN_PRESETS: Dict[str, Dict] = {
    "portrait_high_detail": {
        "name": "Portrait - High Detail",
        "description": "Fine facial features with strong emphasis on details",
        "physical": {
            "width_mm": 150.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 4.0,
            "pixel_scale_mm": 0.15,
        },
        "processing": {
            "resolution": 256,
            "smoothing": 1.5,
            "edge_strength": 75.0,
            "contrast": 120.0,
            "gaussian_blur_radius": 1,
        },
        "semantic": {
            "subject_emphasis": 150.0,
            "background_suppression": 60.0,
            "feature_sharpness": 85.0,
            "mode": "portrait",
        },
    },
    "portrait_simple": {
        "name": "Portrait - Simple",
        "description": "Basic face shape with gentle features",
        "physical": {
            "width_mm": 150.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 3.0,
            "pixel_scale_mm": 0.2,
        },
        "processing": {
            "resolution": 128,
            "smoothing": 3.0,
            "edge_strength": 50.0,
            "contrast": 90.0,
            "gaussian_blur_radius": 2,
        },
        "semantic": {
            "subject_emphasis": 110.0,
            "background_suppression": 50.0,
            "feature_sharpness": 60.0,
            "mode": "portrait",
        },
    },
    "landscape_dramatic": {
        "name": "Landscape - Dramatic",
        "description": "Strong foreground/background contrast for scenery",
        "physical": {
            "width_mm": 200.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 5.0,
            "pixel_scale_mm": 0.2,
        },
        "processing": {
            "resolution": 192,
            "smoothing": 2.0,
            "edge_strength": 65.0,
            "contrast": 130.0,
            "gaussian_blur_radius": 1,
        },
        "semantic": {
            "subject_emphasis": 140.0,
            "background_suppression": 70.0,
            "feature_sharpness": 70.0,
            "mode": "landscape",
        },
    },
    "text_maximum_legibility": {
        "name": "Text - Maximum Legibility",
        "description": "Very sharp, high relief for text and characters",
        "physical": {
            "width_mm": 150.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 4.0,
            "pixel_scale_mm": 0.15,
        },
        "processing": {
            "resolution": 256,
            "smoothing": 0.5,
            "edge_strength": 95.0,
            "contrast": 150.0,
            "gaussian_blur_radius": 0,
            "invert_heights": True,
        },
        "semantic": {
            "subject_emphasis": 180.0,
            "background_suppression": 90.0,
            "feature_sharpness": 95.0,
            "mode": "text",
        },
    },
    "diagram_technical": {
        "name": "Diagram - Technical",
        "description": "Sharp edges and flat regions for diagrams and maps",
        "physical": {
            "width_mm": 150.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 3.5,
            "pixel_scale_mm": 0.18,
        },
        "processing": {
            "resolution": 192,
            "smoothing": 1.0,
            "edge_strength": 85.0,
            "contrast": 140.0,
            "gaussian_blur_radius": 0,
        },
        "semantic": {
            "subject_emphasis": 130.0,
            "background_suppression": 80.0,
            "feature_sharpness": 90.0,
            "mode": "diagram",
        },
    },
    "art_impressionist": {
        "name": "Art - Impressionist",
        "description": "Soft, flowing features for artistic representations",
        "physical": {
            "width_mm": 150.0,
            "base_thickness_mm": 2.0,
            "relief_depth_mm": 3.0,
            "pixel_scale_mm": 0.2,
        },
        "processing": {
            "resolution": 128,
            "smoothing": 4.0,
            "edge_strength": 40.0,
            "contrast": 95.0,
            "gaussian_blur_radius": 3,
        },
        "semantic": {
            "subject_emphasis": 100.0,
            "background_suppression": 30.0,
            "feature_sharpness": 50.0,
            "mode": "custom",
        },
    },
}


def get_builtin_preset(preset_name: str) -> AllParams:
    """Get a built-in preset by name.

    Args:
        preset_name: Name of the preset (key from BUILTIN_PRESETS)

    Returns:
        AllParams object with preset values

    Raises:
        KeyError: If preset name not found
    """
    if preset_name not in BUILTIN_PRESETS:
        available = ", ".join(BUILTIN_PRESETS.keys())
        raise KeyError(
            f"Preset '{preset_name}' not found. Available presets: {available}"
        )

    preset_data = BUILTIN_PRESETS[preset_name]
    return AllParams.from_dict(preset_data)


def list_builtin_presets() -> List[Dict[str, str]]:
    """List all built-in presets with their descriptions.

    Returns:
        List of dictionaries with preset info (id, name, description)
    """
    return [
        {
            "id": key,
            "name": preset["name"],
            "description": preset["description"],
        }
        for key, preset in BUILTIN_PRESETS.items()
    ]


class PresetManager:
    """Manage custom presets (save/load/list)."""

    def __init__(self, presets_dir: Optional[Path] = None):
        """Initialize preset manager.

        Args:
            presets_dir: Directory to store custom presets.
                        Defaults to ~/.art-tactile-transform/presets
        """
        if presets_dir is None:
            self.presets_dir = Path.home() / ".art-tactile-transform" / "presets"
        else:
            self.presets_dir = Path(presets_dir)

        self.presets_dir.mkdir(parents=True, exist_ok=True)

    def save_preset(
        self, name: str, params: AllParams, description: str = ""
    ) -> Path:
        """Save a preset to disk.

        Args:
            name: Preset name (will be used as filename)
            params: AllParams object to save
            description: Optional description

        Returns:
            Path to saved preset file

        Raises:
            ValueError: If name is invalid
        """
        if not name or "/" in name or "\\" in name:
            raise ValueError("Invalid preset name")

        preset_data = params.to_dict()
        preset_data["name"] = name
        preset_data["description"] = description

        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = self.presets_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(preset_data, f, indent=2)

        return filepath

    def load_preset(self, name: str) -> AllParams:
        """Load a preset from disk.

        Args:
            name: Preset name (or filename without .json)

        Returns:
            AllParams object

        Raises:
            FileNotFoundError: If preset not found
        """
        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = self.presets_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Preset not found: {name}")

        with open(filepath, "r", encoding="utf-8") as f:
            preset_data = json.load(f)

        return AllParams.from_dict(preset_data)

    def list_presets(self) -> List[Dict[str, str]]:
        """List all custom presets.

        Returns:
            List of dictionaries with preset info (id, name, description)
        """
        presets = []
        for filepath in self.presets_dir.glob("*.json"):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                presets.append(
                    {
                        "id": filepath.stem,
                        "name": data.get("name", filepath.stem),
                        "description": data.get("description", ""),
                    }
                )
            except Exception:
                # Skip invalid preset files
                continue

        return presets

    def delete_preset(self, name: str) -> None:
        """Delete a custom preset.

        Args:
            name: Preset name to delete

        Raises:
            FileNotFoundError: If preset not found
        """
        filename = f"{name.lower().replace(' ', '_')}.json"
        filepath = self.presets_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Preset not found: {name}")

        filepath.unlink()
