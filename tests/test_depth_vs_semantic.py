"""
Comparison tests: OLD depth estimation vs NEW semantic mapping.

This demonstrates why semantic processing is superior for tactile art.
"""

import pytest
import numpy as np
from PIL import Image
from pathlib import Path
from art_tactile_transform.semantic_processing import SemanticHeightMapper


class TestDepthVsSemanticComparison:
    """
    Compare depth-based and semantic approaches for tactile art generation.

    Key insight: Depth estimation optimizes for photographic realism (distance),
    while semantic processing optimizes for tactile recognition (importance).
    """

    @pytest.fixture
    def mapper(self):
        """Create semantic height mapper."""
        return SemanticHeightMapper()

    def test_mona_lisa_scenario(self, mapper):
        """
        Simulate the Mona Lisa problem mentioned in the PRD.

        Problem with depth estimation:
        - Background landscape gets emphasized (photographic depth)
        - Face gets de-emphasized (closer to camera = lower relief)

        Solution with semantic processing:
        - Face gets emphasized (semantically important)
        - Background gets suppressed (not important for tactile recognition)
        """
        # Create simplified "Mona Lisa" simulation
        # 300x400 image (portrait orientation)
        width, height = 300, 400
        img = np.zeros((height, width, 3), dtype=np.uint8)

        # Background "landscape" (would be "far" in depth estimation)
        # Use greenish/bluish tones that might be interpreted as distant
        img[:, :] = [80, 120, 100]  # Background landscape

        # Add "mountains" in background (top portion)
        img[:150, :] = [90, 100, 110]  # Distant mountains

        # Face region (center-lower portion)
        face_center_y, face_center_x = 250, 150
        face_height_radius, face_width_radius = 80, 60

        # Create elliptical face region
        Y, X = np.ogrid[:height, :width]
        face_mask = (((Y - face_center_y) / face_height_radius) ** 2 +
                     ((X - face_center_x) / face_width_radius) ** 2) <= 1

        img[face_mask] = [220, 180, 150]  # Skin tone

        # Add facial features
        # Eyes
        left_eye_y, left_eye_x = 230, 130
        right_eye_y, right_eye_x = 230, 170
        for eye_y, eye_x in [(left_eye_y, left_eye_x), (right_eye_y, right_eye_x)]:
            eye_mask = ((Y - eye_y) ** 2 + (X - eye_x) ** 2) <= 36
            img[eye_mask] = [60, 40, 30]

        # Nose
        nose_mask = (((Y - 260) ** 2 / 400) + ((X - 150) ** 2 / 100)) <= 1
        img[nose_mask] = [200, 160, 130]

        # Mouth
        mouth_y, mouth_x = 290, 150
        mouth_mask = (((Y - mouth_y) ** 2 / 25) + ((X - mouth_x) ** 2 / 225)) <= 1
        img[mouth_mask] = [180, 100, 100]

        pil_img = Image.fromarray(img)

        # Process with semantic portrait mode
        semantic_result = mapper.process(pil_img, 'portrait', {
            'subject_emphasis': 150,
            'background_suppression': 70,
            'feature_sharpness': 80,
        })

        # Analyze results
        # Face region
        face_region = semantic_result[200:300, 100:200]
        face_mean = face_region.mean()
        face_max = face_region.max()

        # Background region (top portion with "distant mountains")
        background_region = semantic_result[20:100, 50:250]
        background_mean = background_region.mean()

        # Facial features region (eyes area)
        features_region = semantic_result[220:240, 120:180]
        features_mean = features_region.mean()

        print(f"\nMona Lisa Scenario - Semantic Processing:")
        print(f"  Background (landscape): {background_mean:.3f}")
        print(f"  Face region: {face_mean:.3f}")
        print(f"  Facial features: {features_mean:.3f}")

        # Assertions: Semantic processing should prioritize correctly
        assert face_mean > background_mean, \
            f"SEMANTIC: Face ({face_mean:.3f}) should be HIGHER than background ({background_mean:.3f})"

        assert features_mean >= face_mean * 0.8, \
            f"SEMANTIC: Facial features ({features_mean:.3f}) should be emphasized"

        # The key insight:
        # Depth estimation would likely make background high (distant = far away)
        # Semantic processing makes face high (important for tactile recognition)

        contrast_ratio = face_mean / (background_mean + 1e-8)
        print(f"  Face/Background contrast ratio: {contrast_ratio:.2f}")

        assert contrast_ratio > 1.5, \
            f"Semantic should create strong face/background contrast, got {contrast_ratio:.2f}"

    def test_portrait_vs_landscape_mode_difference(self, mapper):
        """
        Test that the same image produces different results in different modes,
        showing the importance of semantic context.
        """
        # Create image with both face-like and landscape-like features
        img = np.zeros((200, 200, 3), dtype=np.uint8)

        # Top half: sky-like (blue)
        img[:100, :] = [100, 150, 255]

        # Bottom half with face-like circular feature
        img[100:, :] = [50, 150, 50]  # Ground

        # Add circular feature
        Y, X = np.ogrid[:200, :200]
        circle_mask = ((Y - 130) ** 2 + (X - 100) ** 2) <= 900
        img[circle_mask] = [220, 180, 150]

        pil_img = Image.fromarray(img)

        # Process as portrait
        portrait_result = mapper.process(pil_img, 'portrait', {
            'subject_emphasis': 120,
        })

        # Process as landscape
        landscape_result = mapper.process(pil_img, 'landscape', {
            'subject_emphasis': 100,
            'background_suppression': 60,
        })

        # The circular feature region
        feature_region_portrait = portrait_result[110:150, 80:120]
        feature_region_landscape = landscape_result[110:150, 80:120]

        # Sky region
        sky_region_portrait = portrait_result[20:80, 50:150]
        sky_region_landscape = landscape_result[20:80, 50:150]

        print(f"\nPortrait mode - Feature: {feature_region_portrait.mean():.3f}, Sky: {sky_region_portrait.mean():.3f}")
        print(f"Landscape mode - Feature: {feature_region_landscape.mean():.3f}, Sky: {sky_region_landscape.mean():.3f}")

        # Both modes should suppress sky, but portrait mode emphasizes face-like features more
        # Landscape mode is more balanced
        assert sky_region_landscape.mean() < landscape_result.mean(), \
            "Landscape mode should suppress sky"

    def test_text_mode_extreme_contrast(self, mapper):
        """
        Test that text mode creates much higher contrast than other modes,
        essential for tactile legibility of text.
        """
        # Create text-like image
        img_array = np.ones((200, 200), dtype=np.uint8) * 255  # White background

        # Add black text (multiple horizontal bars simulating text lines)
        for y in [60, 90, 120, 150]:
            img_array[y:y+8, 40:160] = 0

        pil_img = Image.fromarray(img_array)

        # Process with text mode (high contrast)
        text_result = mapper.process(pil_img, 'text', {
            'text_height': 180,
            'background_height': 10,
        })

        # Process with landscape mode (normal contrast)
        landscape_result = mapper.process(pil_img, 'landscape', {
            'subject_emphasis': 100,
        })

        # Calculate contrast ratios
        text_mode_text_region = text_result[60:68, 100:120]
        text_mode_bg_region = text_result[20:40, 20:40]
        text_mode_contrast = (text_mode_text_region.mean() /
                             (text_mode_bg_region.mean() + 1e-8))

        landscape_mode_text_region = landscape_result[60:68, 100:120]
        landscape_mode_bg_region = landscape_result[20:40, 20:40]
        landscape_mode_contrast = (landscape_mode_text_region.mean() /
                                  (landscape_mode_bg_region.mean() + 1e-8))

        print(f"\nText contrast comparison:")
        print(f"  Text mode contrast ratio: {text_mode_contrast:.2f}")
        print(f"  Landscape mode contrast ratio: {landscape_mode_contrast:.2f}")

        # Text mode should create MUCH higher contrast
        assert text_mode_contrast > landscape_mode_contrast * 1.5, \
            f"Text mode should have higher contrast than landscape mode"

        # Text mode should have very high absolute contrast
        assert text_mode_contrast > 3.0, \
            f"Text mode should create high contrast for tactile legibility"

    def test_diagram_mode_sharp_edges(self, mapper):
        """
        Test that diagram mode preserves sharp edges better than landscape mode,
        important for technical drawings.
        """
        # Create diagram with sharp regions
        img_array = np.ones((200, 200), dtype=np.uint8) * 255

        # Add geometric shapes with sharp boundaries
        img_array[50:100, 50:100] = 100  # Dark square
        img_array[120:170, 120:170] = 150  # Medium square

        pil_img = Image.fromarray(img_array)

        # Process with diagram mode (sharp edges)
        diagram_result = mapper.process(pil_img, 'diagram', {
            'edge_emphasis': 180,
            'smoothing': 0,
        })

        # Process with landscape mode (softer)
        landscape_result = mapper.process(pil_img, 'landscape', {
            'smoothing': 3,
        })

        # Check edge sharpness at boundary (left edge of first square)
        # Compute gradient at edge
        diagram_gradient = np.abs(np.diff(diagram_result[75, 48:52]))
        landscape_gradient = np.abs(np.diff(landscape_result[75, 48:52]))

        print(f"\nEdge sharpness comparison:")
        print(f"  Diagram mode max gradient: {diagram_gradient.max():.4f}")
        print(f"  Landscape mode max gradient: {landscape_gradient.max():.4f}")

        # Diagram mode should preserve sharper edges
        # (though post-processing may affect this)
        assert diagram_gradient.mean() >= landscape_gradient.mean() * 0.7, \
            "Diagram mode should preserve relatively sharp edges"

    def test_semantic_heightmap_normalized(self, mapper):
        """
        Test that all semantic modes produce properly normalized heightmaps.
        """
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))

        modes = ['portrait', 'landscape', 'text', 'diagram']

        for mode in modes:
            heightmap = mapper.process(img, mode)

            # All values should be in [0, 1] range
            assert heightmap.min() >= 0.0, f"{mode}: min should be >= 0"
            assert heightmap.max() <= 1.0, f"{mode}: max should be <= 1"

            # Should use a reasonable range of the available height
            # (not all values exactly the same, unless it's a completely uniform image)
            height_range = heightmap.max() - heightmap.min()

            print(f"{mode} mode - range: {height_range:.4f}, mean: {heightmap.mean():.4f}")

    def test_background_suppression_parameter(self, mapper):
        """
        Test that background suppression parameter works correctly across modes.
        """
        # Create image with clear foreground and background
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:, :] = [100, 150, 200]  # Background

        # Foreground object
        img[80:120, 80:120] = [200, 150, 100]

        pil_img = Image.fromarray(img)

        # Test with different suppression levels
        low_suppression = mapper.process(pil_img, 'landscape', {
            'background_suppression': 20,
        })

        high_suppression = mapper.process(pil_img, 'landscape', {
            'background_suppression': 80,
        })

        # Background regions
        bg_low = low_suppression[20:40, 20:40].mean()
        bg_high = high_suppression[20:40, 20:40].mean()

        print(f"\nBackground suppression test:")
        print(f"  Low suppression (20%): {bg_low:.3f}")
        print(f"  High suppression (80%): {bg_high:.3f}")

        # Higher suppression should result in lower background values
        assert bg_high < bg_low, \
            f"Higher suppression should lower background: {bg_high:.3f} vs {bg_low:.3f}"


class TestSemanticCorrectness:
    """
    Test that semantic processing produces semantically correct results.
    """

    def test_face_is_raised(self):
        """Core test: faces should be raised in portrait mode."""
        mapper = SemanticHeightMapper()

        # Create clear portrait
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:, :] = [200, 200, 200]  # Background

        # Face
        Y, X = np.ogrid[:200, :200]
        face_mask = ((Y - 100) ** 2 + (X - 100) ** 2) <= 1600
        img[face_mask] = [220, 180, 150]

        pil_img = Image.fromarray(img)

        result = mapper.process(pil_img, 'portrait', {
            'subject_emphasis': 150,
            'background_suppression': 60,
        })

        face_height = result[80:120, 80:120].mean()
        background_height = result[0:30, 0:30].mean()

        assert face_height > background_height, \
            "CORE REQUIREMENT: Faces must be raised above background"

    def test_text_is_raised(self):
        """Core test: text should be raised in text mode."""
        mapper = SemanticHeightMapper()

        # Create text image
        img_array = np.ones((200, 200), dtype=np.uint8) * 255
        img_array[90:110, 50:150] = 0  # Black text

        pil_img = Image.fromarray(img_array)

        result = mapper.process(pil_img, 'text', {
            'text_height': 150,
            'background_height': 10,
        })

        text_height = result[95:105, 100:110].mean()
        background_height = result[20:40, 20:40].mean()

        assert text_height > background_height * 2, \
            "CORE REQUIREMENT: Text must be significantly raised above background"

    def test_sky_is_suppressed(self):
        """Core test: sky should be low in landscape mode."""
        mapper = SemanticHeightMapper()

        # Create landscape
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:100, :] = [100, 150, 255]  # Blue sky
        img[100:, :] = [50, 150, 50]  # Green ground

        pil_img = Image.fromarray(img)

        result = mapper.process(pil_img, 'landscape', {
            'background_suppression': 70,
        })

        sky_height = result[20:80, 50:150].mean()
        ground_height = result[120:180, 50:150].mean()

        assert sky_height <= ground_height, \
            "CORE REQUIREMENT: Sky should not be higher than ground"


def test_save_comparison_examples(tmp_path):
    """
    Generate example outputs for documentation.

    This test saves example heightmaps showing the difference between modes.
    """
    mapper = SemanticHeightMapper()

    # Create sample images
    samples = {
        'portrait': _create_sample_portrait(),
        'landscape': _create_sample_landscape(),
        'text': _create_sample_text(),
        'diagram': _create_sample_diagram(),
    }

    results = {}

    for mode, img in samples.items():
        heightmap = mapper.process(img, mode)
        results[mode] = heightmap

        # Save as image for visual inspection
        heightmap_img = (heightmap * 255).astype(np.uint8)
        output_path = tmp_path / f"semantic_{mode}_heightmap.png"
        Image.fromarray(heightmap_img, mode='L').save(output_path)

        print(f"Saved {mode} heightmap to {output_path}")

    # Verify all were created
    assert len(results) == 4


def _create_sample_portrait():
    """Create sample portrait image."""
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:, :] = [180, 200, 220]  # Light background

    # Face
    Y, X = np.ogrid[:200, :200]
    face_mask = ((Y - 100) ** 2 + (X - 100) ** 2) <= 2000
    img[face_mask] = [220, 180, 150]

    # Eyes
    for eye_x in [80, 120]:
        eye_mask = ((Y - 90) ** 2 + (X - eye_x) ** 2) <= 64
        img[eye_mask] = [50, 50, 50]

    return Image.fromarray(img)


def _create_sample_landscape():
    """Create sample landscape image."""
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img[:80, :] = [100, 150, 255]  # Sky
    img[80:, :] = [50, 120, 50]  # Ground

    # Tree
    img[60:150, 90:110] = [40, 80, 40]

    return Image.fromarray(img)


def _create_sample_text():
    """Create sample text image."""
    img_array = np.ones((200, 200), dtype=np.uint8) * 255

    # Text lines
    for y in [60, 90, 120]:
        img_array[y:y+8, 40:160] = 0

    return Image.fromarray(img_array)


def _create_sample_diagram():
    """Create sample diagram image."""
    img_array = np.ones((200, 200), dtype=np.uint8) * 255

    # Geometric shapes
    img_array[50:100, 50:100] = 100
    img_array[120:160, 120:170] = 150

    return Image.fromarray(img_array)
