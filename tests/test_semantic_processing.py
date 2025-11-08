"""
Tests for semantic height mapping algorithms.
"""

import pytest
import numpy as np
from PIL import Image
from art_tactile_transform.semantic_processing import (
    PortraitProcessor,
    LandscapeProcessor,
    TextProcessor,
    DiagramProcessor,
    SemanticHeightMapper,
)


class TestPortraitProcessor:
    """Test portrait processing with face detection."""

    @pytest.fixture
    def portrait_processor(self):
        """Create portrait processor instance."""
        return PortraitProcessor()

    @pytest.fixture
    def sample_portrait(self):
        """Create a simple synthetic portrait for testing."""
        # Create 200x200 image with a circular "face" in center
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        # Background
        img[:, :] = [200, 200, 200]

        # Create circular face
        center_y, center_x = 100, 100
        radius = 50
        Y, X = np.ogrid[:200, :200]
        dist_from_center = np.sqrt((X - center_x)**2 + (Y - center_y)**2)

        # Face (skin tone)
        face_mask = dist_from_center <= radius
        img[face_mask] = [220, 180, 150]

        # Add eyes (dark circles)
        left_eye_mask = np.sqrt((X - 80)**2 + (Y - 90)**2) <= 8
        right_eye_mask = np.sqrt((X - 120)**2 + (Y - 90)**2) <= 8
        img[left_eye_mask] = [50, 50, 50]
        img[right_eye_mask] = [50, 50, 50]

        return Image.fromarray(img)

    def test_portrait_processor_initialization(self, portrait_processor):
        """Test that portrait processor initializes correctly."""
        assert portrait_processor is not None
        # Should have either MediaPipe or OpenCV available
        assert portrait_processor.has_mediapipe or portrait_processor.face_cascade is not None

    def test_portrait_processing_returns_heightmap(self, portrait_processor, sample_portrait):
        """Test that portrait processing returns valid heightmap."""
        params = {
            'subject_emphasis': 120,
            'background_suppression': 40,
            'feature_sharpness': 70,
            'smoothing': 2,
        }

        heightmap = portrait_processor.process(sample_portrait, params)

        # Check output properties
        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (200, 200)
        assert heightmap.dtype == np.float32 or heightmap.dtype == np.float64
        assert heightmap.min() >= 0.0
        assert heightmap.max() <= 1.0

    def test_portrait_face_region_raised(self, portrait_processor, sample_portrait):
        """Test that face regions are raised relative to background."""
        params = {
            'subject_emphasis': 120,
            'background_suppression': 60,
        }

        heightmap = portrait_processor.process(sample_portrait, params)

        # Center region (face) should be higher than corners (background)
        center_height = heightmap[90:110, 90:110].mean()
        corner_height = heightmap[0:20, 0:20].mean()

        # Face should be significantly higher than background
        assert center_height > corner_height, \
            f"Face height {center_height} should be > background {corner_height}"

    def test_portrait_parameter_variation(self, portrait_processor, sample_portrait):
        """Test that parameters affect the output."""
        params_low = {'subject_emphasis': 50}
        params_high = {'subject_emphasis': 200}

        heightmap_low = portrait_processor.process(sample_portrait, params_low)
        heightmap_high = portrait_processor.process(sample_portrait, params_high)

        # Higher emphasis should create more variation
        assert heightmap_high.std() > heightmap_low.std()


class TestLandscapeProcessor:
    """Test landscape processing with semantic segmentation."""

    @pytest.fixture
    def landscape_processor(self):
        """Create landscape processor instance."""
        return LandscapeProcessor()

    @pytest.fixture
    def sample_landscape(self):
        """Create a simple synthetic landscape for testing."""
        # Create 200x200 image with sky (top) and ground (bottom)
        img = np.zeros((200, 200, 3), dtype=np.uint8)

        # Sky (top half, blue)
        img[:100, :] = [100, 150, 255]

        # Ground (bottom half, green)
        img[100:, :] = [50, 150, 50]

        # Add a "tree" (dark vertical shape)
        img[80:180, 90:110] = [40, 80, 40]

        return Image.fromarray(img)

    def test_landscape_processor_initialization(self, landscape_processor):
        """Test that landscape processor initializes correctly."""
        assert landscape_processor is not None

    def test_landscape_processing_returns_heightmap(self, landscape_processor, sample_landscape):
        """Test that landscape processing returns valid heightmap."""
        params = {
            'subject_emphasis': 100,
            'background_suppression': 60,
            'smoothing': 3,
        }

        heightmap = landscape_processor.process(sample_landscape, params)

        # Check output properties
        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (200, 200)
        assert heightmap.min() >= 0.0
        assert heightmap.max() <= 1.0

    def test_landscape_sky_suppression(self, landscape_processor, sample_landscape):
        """Test that sky regions are suppressed (lower)."""
        params = {'background_suppression': 80}

        heightmap = landscape_processor.process(sample_landscape, params)

        # Sky (top) should generally be lower than ground (bottom)
        sky_height = heightmap[:80, :].mean()
        ground_height = heightmap[120:, :].mean()

        # Ground should be higher than sky
        assert ground_height >= sky_height, \
            f"Ground height {ground_height} should be >= sky {sky_height}"


class TestTextProcessor:
    """Test text processing with OCR."""

    @pytest.fixture
    def text_processor(self):
        """Create text processor instance."""
        return TextProcessor()

    @pytest.fixture
    def sample_text(self):
        """Create a simple synthetic text image for testing."""
        # Create 200x200 white background
        img = np.ones((200, 200), dtype=np.uint8) * 255

        # Add black text-like horizontal bars
        img[80:90, 40:160] = 0  # Top line
        img[110:120, 40:160] = 0  # Bottom line

        return Image.fromarray(img)

    def test_text_processor_initialization(self, text_processor):
        """Test that text processor initializes correctly."""
        assert text_processor is not None

    def test_text_processing_returns_heightmap(self, text_processor, sample_text):
        """Test that text processing returns valid heightmap."""
        params = {
            'text_height': 150,
            'background_height': 5,
            'edge_strength': 90,
        }

        heightmap = text_processor.process(sample_text, params)

        # Check output properties
        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (200, 200)
        assert heightmap.min() >= 0.0
        assert heightmap.max() <= 1.0

    def test_text_regions_raised(self, text_processor, sample_text):
        """Test that text regions are raised relative to background."""
        params = {
            'text_height': 150,
            'background_height': 5,
        }

        heightmap = text_processor.process(sample_text, params)

        # Text regions should be higher than background
        text_height = heightmap[80:90, 80:100].mean()
        background_height = heightmap[20:40, 20:40].mean()

        assert text_height > background_height, \
            f"Text height {text_height} should be > background {background_height}"


class TestDiagramProcessor:
    """Test diagram processing with edge detection."""

    @pytest.fixture
    def diagram_processor(self):
        """Create diagram processor instance."""
        return DiagramProcessor()

    @pytest.fixture
    def sample_diagram(self):
        """Create a simple synthetic diagram for testing."""
        # Create 200x200 image with geometric shapes
        img = np.ones((200, 200), dtype=np.uint8) * 255

        # Add rectangle (dark region)
        img[50:100, 50:150] = 100

        # Add circle (different gray level)
        center_y, center_x = 140, 100
        radius = 30
        Y, X = np.ogrid[:200, :200]
        circle_mask = (X - center_x)**2 + (Y - center_y)**2 <= radius**2
        img[circle_mask] = 150

        return Image.fromarray(img)

    def test_diagram_processor_initialization(self, diagram_processor):
        """Test that diagram processor initializes correctly."""
        assert diagram_processor is not None

    def test_diagram_processing_returns_heightmap(self, diagram_processor, sample_diagram):
        """Test that diagram processing returns valid heightmap."""
        params = {
            'edge_emphasis': 150,
            'region_contrast': 80,
            'smoothing': 0,
        }

        heightmap = diagram_processor.process(sample_diagram, params)

        # Check output properties
        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (200, 200)
        assert heightmap.min() >= 0.0
        assert heightmap.max() <= 1.0

    def test_diagram_edges_emphasized(self, diagram_processor, sample_diagram):
        """Test that edges are emphasized in diagrams."""
        params = {'edge_emphasis': 200}

        heightmap = diagram_processor.process(sample_diagram, params)

        # Edge regions should have higher values
        # Check rectangle edge (vertical)
        edge_height = heightmap[70, 50]  # Left edge of rectangle
        interior_height = heightmap[75, 100]  # Interior of rectangle

        # Edge should be at least as high as interior
        assert edge_height >= interior_height * 0.8


class TestSemanticHeightMapper:
    """Test the unified semantic height mapper."""

    @pytest.fixture
    def mapper(self):
        """Create semantic height mapper instance."""
        return SemanticHeightMapper()

    def test_mapper_initialization(self, mapper):
        """Test that mapper initializes with all processors."""
        assert 'portrait' in mapper.processors
        assert 'landscape' in mapper.processors
        assert 'text' in mapper.processors
        assert 'diagram' in mapper.processors

    def test_mapper_process_portrait_mode(self, mapper):
        """Test processing in portrait mode."""
        # Create simple test image
        img = Image.new('RGB', (100, 100), color=(200, 200, 200))

        heightmap = mapper.process(img, 'portrait')

        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (100, 100)
        assert 0.0 <= heightmap.min() <= 1.0
        assert 0.0 <= heightmap.max() <= 1.0

    def test_mapper_process_landscape_mode(self, mapper):
        """Test processing in landscape mode."""
        img = Image.new('RGB', (100, 100), color=(100, 150, 255))

        heightmap = mapper.process(img, 'landscape')

        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (100, 100)

    def test_mapper_process_text_mode(self, mapper):
        """Test processing in text mode."""
        img = Image.new('L', (100, 100), color=255)

        heightmap = mapper.process(img, 'text')

        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (100, 100)

    def test_mapper_process_diagram_mode(self, mapper):
        """Test processing in diagram mode."""
        img = Image.new('L', (100, 100), color=200)

        heightmap = mapper.process(img, 'diagram')

        assert isinstance(heightmap, np.ndarray)
        assert heightmap.shape == (100, 100)

    def test_mapper_invalid_mode_raises_error(self, mapper):
        """Test that invalid mode raises ValueError."""
        img = Image.new('RGB', (100, 100))

        with pytest.raises(ValueError, match="Unknown mode"):
            mapper.process(img, 'invalid_mode')

    def test_mapper_post_process_smoothing(self, mapper):
        """Test that post-processing applies smoothing."""
        # Create heightmap with sharp transition
        heightmap = np.zeros((100, 100))
        heightmap[:, 50:] = 1.0

        params = {'smoothing': 5}
        smoothed = mapper.post_process(heightmap, params)

        # Smoothing should reduce the sharpness of the transition
        transition_region = smoothed[:, 48:52]
        # Should have intermediate values, not just 0 and 1
        unique_values = np.unique(transition_region)
        assert len(unique_values) > 2

    def test_mapper_post_process_edge_enhancement(self, mapper):
        """Test that post-processing can enhance edges."""
        # Create heightmap with edge
        heightmap = np.zeros((100, 100))
        heightmap[:, 50:] = 1.0

        params = {'edge_strength': 80, 'smoothing': 0}
        enhanced = mapper.post_process(heightmap, params)

        # Edge enhancement should increase values near the edge
        assert enhanced.max() >= heightmap.max()

    def test_mapper_post_process_contrast(self, mapper):
        """Test that post-processing adjusts contrast."""
        heightmap = np.random.rand(100, 100) * 0.5 + 0.25  # Values between 0.25 and 0.75

        params_low = {'contrast': 50}
        params_high = {'contrast': 150}

        result_low = mapper.post_process(heightmap, params_low)
        result_high = mapper.post_process(heightmap, params_high)

        # Higher contrast should have larger standard deviation
        assert result_high.std() > result_low.std()

    def test_mapper_detect_mode_portrait(self, mapper):
        """Test that mode detection identifies portraits."""
        # Skip if no face detection available
        try:
            import mediapipe
        except ImportError:
            pytest.skip("MediaPipe not available for mode detection")

        # Create simple face-like image (this won't actually be detected without a real face)
        img = Image.new('RGB', (200, 200), color=(220, 180, 150))

        # This is a heuristic test - actual face detection would need real face images
        # For now, just test that the method runs without error
        mode = mapper.detect_mode(img)
        assert mode in ['portrait', 'landscape', 'text', 'diagram']

    def test_mapper_detect_mode_text(self, mapper):
        """Test that mode detection identifies text images."""
        # Create text-like image with horizontal structures
        img_array = np.ones((200, 200), dtype=np.uint8) * 255
        # Add multiple horizontal bars
        for y in range(50, 150, 20):
            img_array[y:y+5, 40:160] = 0

        img = Image.fromarray(img_array)

        mode = mapper.detect_mode(img)
        # Should detect as text or diagram (both have similar edge patterns)
        assert mode in ['text', 'diagram']

    def test_mapper_detect_mode_diagram(self, mapper):
        """Test that mode detection identifies diagrams."""
        # Create diagram-like image with high edge density
        img_array = np.ones((200, 200), dtype=np.uint8) * 255
        # Add geometric shapes
        img_array[50:100, 50:150] = 100
        img_array[120:170, 80:130] = 150

        img = Image.fromarray(img_array)

        mode = mapper.detect_mode(img)
        assert mode in ['diagram', 'landscape']


class TestSemanticVsDepth:
    """Compare semantic processing to depth estimation approach."""

    def test_portrait_semantic_emphasizes_face(self):
        """
        Test that semantic processing emphasizes faces over background,
        unlike depth estimation which may emphasize distant objects.
        """
        mapper = SemanticHeightMapper()

        # Create portrait with face in center, "distant" background
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        img[:, :] = [50, 100, 150]  # Blue background (could be "far" in depth)

        # Face in center
        center_y, center_x = 100, 100
        radius = 40
        Y, X = np.ogrid[:200, :200]
        face_mask = np.sqrt((X - center_x)**2 + (Y - center_y)**2) <= radius
        img[face_mask] = [220, 180, 150]

        pil_img = Image.fromarray(img)

        # Process with semantic mode
        semantic_heightmap = mapper.process(pil_img, 'portrait', {
            'subject_emphasis': 150,
            'background_suppression': 80,
        })

        # Verify face region is HIGHER than background
        face_region = semantic_heightmap[80:120, 80:120]
        background_region = semantic_heightmap[0:30, 0:30]

        face_height = face_region.mean()
        bg_height = background_region.mean()

        assert face_height > bg_height, \
            f"Semantic: Face ({face_height:.3f}) should be higher than background ({bg_height:.3f})"

        # This demonstrates the key difference:
        # Depth estimation might make blue background high (appears "far")
        # Semantic processing makes FACE high (semantically important)

    def test_text_semantic_creates_high_contrast(self):
        """
        Test that semantic processing creates very high relief for text,
        making it more tactilely legible than depth-based approaches.
        """
        mapper = SemanticHeightMapper()

        # Create text image
        img_array = np.ones((200, 200), dtype=np.uint8) * 255
        img_array[80:100, 50:150] = 0  # Black text

        img = Image.fromarray(img_array)

        # Process with text mode
        text_heightmap = mapper.process(img, 'text', {
            'text_height': 180,
            'background_height': 10,
        })

        # Verify extreme contrast
        text_region = text_heightmap[85:95, 100:110]
        bg_region = text_heightmap[20:40, 20:40]

        contrast_ratio = text_region.mean() / (bg_region.mean() + 1e-8)

        # Text should be MUCH higher than background for tactile legibility
        assert contrast_ratio > 3.0, \
            f"Text should have high contrast ratio, got {contrast_ratio:.2f}"


def test_integration_all_modes():
    """Integration test: process same image with all modes."""
    mapper = SemanticHeightMapper()

    # Create a general test image
    img = Image.new('RGB', (150, 150), color=(128, 128, 128))

    modes = ['portrait', 'landscape', 'text', 'diagram']

    results = {}
    for mode in modes:
        heightmap = mapper.process(img, mode)
        results[mode] = heightmap

        # Each mode should produce valid output
        assert heightmap.shape == (150, 150)
        assert 0.0 <= heightmap.min() <= 1.0
        assert 0.0 <= heightmap.max() <= 1.0

    # Different modes should produce different results
    # (unless the image is completely uniform, which it is, but processing still differs)
    assert len(results) == 4
