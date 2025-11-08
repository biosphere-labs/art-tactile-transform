"""Parameter classes for tactile art generation."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PhysicalParams:
    """Physical parameters for 3D model generation.

    All measurements are in millimeters.
    """

    width_mm: float = 150.0
    height_mm: Optional[float] = None  # Auto-calculated if None
    base_thickness_mm: float = 2.0
    relief_depth_mm: float = 3.0
    pixel_scale_mm: float = 0.2
    edge_wall_thickness_mm: float = 3.0

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if self.width_mm <= 0:
            raise ValueError("width_mm must be positive")
        if self.height_mm is not None and self.height_mm <= 0:
            raise ValueError("height_mm must be positive if specified")
        if self.base_thickness_mm <= 0:
            raise ValueError("base_thickness_mm must be positive")
        if self.relief_depth_mm <= 0:
            raise ValueError("relief_depth_mm must be positive")
        if self.pixel_scale_mm <= 0:
            raise ValueError("pixel_scale_mm must be positive")
        if self.edge_wall_thickness_mm <= 0:
            raise ValueError("edge_wall_thickness_mm must be positive")

    def get_min_height_mm(self) -> float:
        """Get minimum height (base only)."""
        return self.base_thickness_mm

    def get_max_height_mm(self) -> float:
        """Get maximum height (base + relief)."""
        return self.base_thickness_mm + self.relief_depth_mm


@dataclass
class ProcessingParams:
    """Image processing parameters."""

    resolution: int = 128
    smoothing: float = 2.0
    edge_strength: float = 60.0
    contrast: float = 100.0
    minimum_feature_size_mm: float = 1.0
    gaussian_blur_radius: int = 0
    clamp_min: int = 0
    clamp_max: int = 255
    border_pixels: int = 0
    invert_heights: bool = False

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if self.resolution <= 0:
            raise ValueError("resolution must be positive")
        if self.smoothing < 0:
            raise ValueError("smoothing must be non-negative")
        if not 0 <= self.edge_strength <= 100:
            raise ValueError("edge_strength must be between 0 and 100")
        if not 0 <= self.contrast <= 200:
            raise ValueError("contrast must be between 0 and 200")
        if self.minimum_feature_size_mm < 0:
            raise ValueError("minimum_feature_size_mm must be non-negative")
        if self.gaussian_blur_radius < 0:
            raise ValueError("gaussian_blur_radius must be non-negative")
        if not 0 <= self.clamp_min <= 255:
            raise ValueError("clamp_min must be between 0 and 255")
        if not 0 <= self.clamp_max <= 255:
            raise ValueError("clamp_max must be between 0 and 255")
        if self.clamp_min >= self.clamp_max:
            raise ValueError("clamp_min must be less than clamp_max")
        if self.border_pixels < 0:
            raise ValueError("border_pixels must be non-negative")


@dataclass
class SemanticParams:
    """Semantic processing parameters for advanced height mapping."""

    subject_emphasis: float = 120.0
    background_suppression: float = 40.0
    feature_sharpness: float = 70.0
    mode: str = "portrait"

    def __post_init__(self) -> None:
        """Validate parameters after initialization."""
        if not 0 <= self.subject_emphasis <= 200:
            raise ValueError("subject_emphasis must be between 0 and 200")
        if not 0 <= self.background_suppression <= 100:
            raise ValueError("background_suppression must be between 0 and 100")
        if not 0 <= self.feature_sharpness <= 100:
            raise ValueError("feature_sharpness must be between 0 and 100")

        valid_modes = ["portrait", "landscape", "text", "diagram", "custom"]
        if self.mode not in valid_modes:
            raise ValueError(f"mode must be one of {valid_modes}")


@dataclass
class AllParams:
    """Complete parameter set for tactile art generation."""

    physical: PhysicalParams = field(default_factory=PhysicalParams)
    processing: ProcessingParams = field(default_factory=ProcessingParams)
    semantic: SemanticParams = field(default_factory=SemanticParams)

    def to_dict(self) -> dict:
        """Convert all parameters to a dictionary."""
        return {
            "physical": {
                "width_mm": self.physical.width_mm,
                "height_mm": self.physical.height_mm,
                "base_thickness_mm": self.physical.base_thickness_mm,
                "relief_depth_mm": self.physical.relief_depth_mm,
                "pixel_scale_mm": self.physical.pixel_scale_mm,
                "edge_wall_thickness_mm": self.physical.edge_wall_thickness_mm,
            },
            "processing": {
                "resolution": self.processing.resolution,
                "smoothing": self.processing.smoothing,
                "edge_strength": self.processing.edge_strength,
                "contrast": self.processing.contrast,
                "minimum_feature_size_mm": self.processing.minimum_feature_size_mm,
                "gaussian_blur_radius": self.processing.gaussian_blur_radius,
                "clamp_min": self.processing.clamp_min,
                "clamp_max": self.processing.clamp_max,
                "border_pixels": self.processing.border_pixels,
                "invert_heights": self.processing.invert_heights,
            },
            "semantic": {
                "subject_emphasis": self.semantic.subject_emphasis,
                "background_suppression": self.semantic.background_suppression,
                "feature_sharpness": self.semantic.feature_sharpness,
                "mode": self.semantic.mode,
            },
        }

    @classmethod
    def from_dict(cls, data: dict) -> "AllParams":
        """Create AllParams from a dictionary."""
        physical = PhysicalParams(**data.get("physical", {}))
        processing = ProcessingParams(**data.get("processing", {}))
        semantic = SemanticParams(**data.get("semantic", {}))
        return cls(physical=physical, processing=processing, semantic=semantic)
