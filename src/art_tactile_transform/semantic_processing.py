"""
Semantic height mapping algorithms for tactile art generation.

This module implements context-aware processing modes that map semantic importance
to tactile height, rather than using photographic depth estimation.

Key insight: Tactile art should represent WHAT IS IMPORTANT, not what is far/near.
"""

import numpy as np
from PIL import Image
from typing import Dict, Any, Optional, Tuple
import cv2
from scipy.ndimage import gaussian_filter, sobel
from scipy.ndimage import binary_dilation, binary_erosion


class PortraitProcessor:
    """
    Process portrait images with face and feature detection.

    Height mapping strategy:
    - Background: LOW (minimal relief)
    - Face region: HIGH (raised for recognition)
    - Facial features (eyes, nose, mouth, ears): HIGHEST (maximum emphasis)
    """

    def __init__(self):
        """Initialize face detection with MediaPipe."""
        try:
            import mediapipe as mp
            self.mp_face_detection = mp.solutions.face_detection
            self.mp_face_mesh = mp.solutions.face_mesh
            self.face_detection = self.mp_face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5
            )
            self.face_mesh = self.mp_face_mesh.FaceMesh(
                static_image_mode=True,
                max_num_faces=5,
                min_detection_confidence=0.5
            )
            self.has_mediapipe = True
        except ImportError:
            print("Warning: MediaPipe not available, falling back to OpenCV")
            self.has_mediapipe = False
            # Load OpenCV's pre-trained face detector
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            self.eye_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_eye.xml'
            )

    def process(self, image: Image.Image, params: Dict[str, Any]) -> np.ndarray:
        """
        Process portrait image to create semantic heightmap.

        Args:
            image: Input PIL Image
            params: Processing parameters
                - subject_emphasis: 0-200% (default: 120)
                - background_suppression: 0-100% (default: 40)
                - feature_sharpness: 0-100% (default: 70)
                - smoothing: 0-10 (default: 2)
                - edge_strength: 0-100% (default: 60)

        Returns:
            Heightmap as numpy array (0-1 normalized)
        """
        # Convert PIL to numpy/OpenCV format
        img_array = np.array(image)
        if len(img_array.shape) == 2:
            # Grayscale
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            # RGBA
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        else:
            img_rgb = img_array.copy()

        height, width = img_rgb.shape[:2]

        # Extract parameters with defaults
        subject_emphasis = params.get('subject_emphasis', 120) / 100.0
        background_suppression = params.get('background_suppression', 40) / 100.0
        feature_sharpness = params.get('feature_sharpness', 70) / 100.0

        # Initialize heightmap with background level
        heightmap = np.ones((height, width), dtype=np.float32) * (1.0 - background_suppression)

        if self.has_mediapipe:
            heightmap = self._process_with_mediapipe(img_rgb, heightmap, subject_emphasis, feature_sharpness)
        else:
            heightmap = self._process_with_opencv(img_rgb, heightmap, subject_emphasis, feature_sharpness)

        return heightmap

    def _process_with_mediapipe(self, img_rgb: np.ndarray, heightmap: np.ndarray,
                                 subject_emphasis: float, feature_sharpness: float) -> np.ndarray:
        """Process using MediaPipe face detection and mesh."""
        height, width = img_rgb.shape[:2]

        # Detect faces
        face_results = self.face_detection.process(img_rgb)

        if face_results.detections:
            for detection in face_results.detections:
                # Get bounding box
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)

                # Ensure bounds are valid
                x = max(0, x)
                y = max(0, y)
                w = min(w, width - x)
                h = min(h, height - y)

                # Create smooth face mask with falloff
                face_mask = self._create_smooth_region_mask(height, width, x, y, w, h)
                heightmap += face_mask * subject_emphasis

        # Detect facial landmarks for feature emphasis
        mesh_results = self.face_mesh.process(img_rgb)

        if mesh_results.multi_face_landmarks:
            for face_landmarks in mesh_results.multi_face_landmarks:
                # Create feature mask for eyes, nose, mouth
                feature_mask = self._create_feature_mask(
                    face_landmarks, height, width, feature_sharpness
                )
                heightmap += feature_mask

        return np.clip(heightmap, 0, 1)

    def _process_with_opencv(self, img_rgb: np.ndarray, heightmap: np.ndarray,
                            subject_emphasis: float, feature_sharpness: float) -> np.ndarray:
        """Fallback processing using OpenCV Haar cascades."""
        height, width = img_rgb.shape[:2]
        gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

        # Detect faces
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            # Create smooth face mask
            face_mask = self._create_smooth_region_mask(height, width, x, y, w, h)
            heightmap += face_mask * subject_emphasis

            # Detect eyes within face region
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)

            for (ex, ey, ew, eh) in eyes:
                # Convert eye coordinates to full image coordinates
                eye_x, eye_y = x + ex, y + ey
                eye_mask = self._create_smooth_region_mask(
                    height, width, eye_x, eye_y, ew, eh, sigma_scale=0.5
                )
                heightmap += eye_mask * feature_sharpness

        return np.clip(heightmap, 0, 1)

    def _create_smooth_region_mask(self, height: int, width: int,
                                    x: int, y: int, w: int, h: int,
                                    sigma_scale: float = 1.0) -> np.ndarray:
        """Create a smooth Gaussian mask for a region."""
        mask = np.zeros((height, width), dtype=np.float32)

        # Create mesh grid centered on region
        center_x = x + w // 2
        center_y = y + h // 2

        Y, X = np.ogrid[:height, :width]

        # Gaussian falloff from center
        sigma_x = (w / 4) * sigma_scale
        sigma_y = (h / 4) * sigma_scale

        dist_sq = ((X - center_x) / sigma_x) ** 2 + ((Y - center_y) / sigma_y) ** 2
        mask = np.exp(-dist_sq / 2)

        return mask

    def _create_feature_mask(self, face_landmarks, height: int, width: int,
                            feature_sharpness: float) -> np.ndarray:
        """Create mask emphasizing facial features from landmarks."""
        mask = np.zeros((height, width), dtype=np.float32)

        # MediaPipe face mesh landmark indices for key features
        # Left eye: 33, 133, 159, 145
        # Right eye: 362, 263, 386, 374
        # Nose tip: 1
        # Mouth: 61, 291, 17, 314

        feature_indices = [
            # Left eye contour
            33, 133, 159, 145, 160, 144,
            # Right eye contour
            362, 263, 386, 374, 385, 373,
            # Nose
            1, 2, 98, 327,
            # Mouth
            61, 291, 17, 314, 78, 308, 13, 14
        ]

        points = []
        for idx in feature_indices:
            if idx < len(face_landmarks.landmark):
                landmark = face_landmarks.landmark[idx]
                x = int(landmark.x * width)
                y = int(landmark.y * height)
                points.append((x, y))

        # Create Gaussian blobs around each feature point
        for (x, y) in points:
            if 0 <= x < width and 0 <= y < height:
                Y, X = np.ogrid[:height, :width]
                sigma = min(width, height) * 0.01  # Small, sharp features
                dist_sq = ((X - x) / sigma) ** 2 + ((Y - y) / sigma) ** 2
                mask += np.exp(-dist_sq / 2) * feature_sharpness

        return mask


class LandscapeProcessor:
    """
    Process landscape/scenery images with semantic segmentation.

    Height mapping strategy:
    - Sky/background: LOW (minimal relief)
    - Foreground objects: HIGH (raised for prominence)
    - Salient regions: HIGHEST (maximum emphasis)
    """

    def __init__(self):
        """Initialize semantic segmentation and saliency detection."""
        self.segmentation_model = None
        self.has_transformers = False

        try:
            from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation
            self.has_transformers = True
            # We'll lazy-load the model when needed
            self.AutoImageProcessor = AutoImageProcessor
            self.AutoModelForSemanticSegmentation = AutoModelForSemanticSegmentation
        except ImportError:
            print("Warning: transformers not available, using simpler segmentation")

    def process(self, image: Image.Image, params: Dict[str, Any]) -> np.ndarray:
        """
        Process landscape image to create semantic heightmap.

        Args:
            image: Input PIL Image
            params: Processing parameters
                - subject_emphasis: 0-200% (default: 100)
                - background_suppression: 0-100% (default: 60)
                - smoothing: 0-10 (default: 3)

        Returns:
            Heightmap as numpy array (0-1 normalized)
        """
        img_array = np.array(image)
        if len(img_array.shape) == 2:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
        elif img_array.shape[2] == 4:
            img_rgb = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
        else:
            img_rgb = img_array.copy()

        height, width = img_rgb.shape[:2]

        # Extract parameters
        subject_emphasis = params.get('subject_emphasis', 100) / 100.0
        background_suppression = params.get('background_suppression', 60) / 100.0

        # Compute saliency map
        saliency_map = self._compute_saliency(img_rgb)

        # Simple semantic segmentation (sky detection)
        sky_mask = self._detect_sky(img_rgb)

        # Create heightmap
        heightmap = np.ones((height, width), dtype=np.float32) * 0.3

        # Suppress sky/background
        heightmap[sky_mask] *= (1.0 - background_suppression)

        # Emphasize salient regions
        heightmap += saliency_map * subject_emphasis

        return np.clip(heightmap, 0, 1)

    def _compute_saliency(self, img_rgb: np.ndarray) -> np.ndarray:
        """Compute saliency map using spectral residual method."""
        # Convert to LAB color space
        img_lab = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2LAB)

        # Use OpenCV's saliency detection
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        (success, saliency_map) = saliency.computeSaliency(img_rgb)

        if success:
            return saliency_map
        else:
            # Fallback: use simple contrast-based saliency
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            blurred = cv2.GaussianBlur(gray, (21, 21), 0)
            saliency_map = np.abs(gray.astype(float) - blurred.astype(float)) / 255.0
            return saliency_map

    def _detect_sky(self, img_rgb: np.ndarray) -> np.ndarray:
        """Simple sky detection based on color and position."""
        height, width = img_rgb.shape[:2]

        # Convert to HSV
        img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)

        # Sky is typically blue and in upper portion of image
        # Blue hue range in HSV
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])

        blue_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

        # Weight by vertical position (sky is typically at top)
        y_weight = np.linspace(1.0, 0.0, height).reshape(-1, 1)
        y_weight = np.tile(y_weight, (1, width))

        weighted_mask = (blue_mask / 255.0) * y_weight
        sky_mask = weighted_mask > 0.3

        return sky_mask


class TextProcessor:
    """
    Process text/document images with OCR and character detection.

    Height mapping strategy:
    - Background: VERY LOW (nearly flat)
    - Text characters: VERY HIGH (maximum relief for legibility)
    - Sharp edges for tactile reading
    """

    def __init__(self):
        """Initialize OCR engine."""
        self.has_tesseract = False
        self.has_easyocr = False

        try:
            import pytesseract
            self.pytesseract = pytesseract
            self.has_tesseract = True
        except ImportError:
            pass

        try:
            import easyocr
            self.easyocr = easyocr
            self.has_easyocr = True
        except ImportError:
            pass

        if not self.has_tesseract and not self.has_easyocr:
            print("Warning: No OCR engine available, using simple threshold")

    def process(self, image: Image.Image, params: Dict[str, Any]) -> np.ndarray:
        """
        Process text image to create semantic heightmap.

        Args:
            image: Input PIL Image
            params: Processing parameters
                - text_height: 0-200% (default: 150)
                - background_height: 0-100% (default: 5)
                - edge_strength: 0-100% (default: 90)

        Returns:
            Heightmap as numpy array (0-1 normalized)
        """
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array.copy()

        height, width = gray.shape

        # Extract parameters
        text_height = params.get('text_height', 150) / 100.0
        background_height = params.get('background_height', 5) / 100.0

        # Create text mask using adaptive thresholding
        # This works well even without OCR
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 11, 2
        )

        # Detect text regions if OCR available
        if self.has_tesseract or self.has_easyocr:
            text_mask = self._detect_text_regions(image, binary)
        else:
            text_mask = binary / 255.0

        # Create heightmap
        heightmap = np.ones((height, width), dtype=np.float32) * background_height
        heightmap += text_mask * text_height

        return np.clip(heightmap, 0, 1)

    def _detect_text_regions(self, image: Image.Image, binary: np.ndarray) -> np.ndarray:
        """Detect text regions using OCR."""
        if self.has_tesseract:
            try:
                # Get bounding boxes for text
                data = self.pytesseract.image_to_data(
                    image, output_type=self.pytesseract.Output.DICT
                )

                height, width = binary.shape
                mask = np.zeros((height, width), dtype=np.float32)

                n_boxes = len(data['text'])
                for i in range(n_boxes):
                    if int(data['conf'][i]) > 30:  # Confidence threshold
                        (x, y, w, h) = (data['left'][i], data['top'][i],
                                       data['width'][i], data['height'][i])
                        if w > 0 and h > 0:
                            x, y = max(0, x), max(0, y)
                            w = min(w, width - x)
                            h = min(h, height - y)
                            mask[y:y+h, x:x+w] = 1.0

                return mask if mask.sum() > 0 else binary / 255.0
            except Exception as e:
                print(f"OCR failed: {e}, using threshold")
                return binary / 255.0
        else:
            return binary / 255.0


class DiagramProcessor:
    """
    Process diagram/technical images with edge and region detection.

    Height mapping strategy:
    - Distinct heights for different regions
    - Sharp boundaries between regions
    - Edges and lines emphasized
    """

    def __init__(self):
        """Initialize edge and region detection."""
        pass

    def process(self, image: Image.Image, params: Dict[str, Any]) -> np.ndarray:
        """
        Process diagram image to create semantic heightmap.

        Args:
            image: Input PIL Image
            params: Processing parameters
                - edge_emphasis: 0-200% (default: 150)
                - region_contrast: 0-100% (default: 80)
                - smoothing: 0-10 (default: 0)

        Returns:
            Heightmap as numpy array (0-1 normalized)
        """
        img_array = np.array(image)
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array.copy()

        height, width = gray.shape

        # Extract parameters
        edge_emphasis = params.get('edge_emphasis', 150) / 100.0
        region_contrast = params.get('region_contrast', 80) / 100.0

        # Detect edges using Canny
        edges = cv2.Canny(gray, 50, 150)
        edge_map = edges / 255.0

        # Segment regions using watershed or simple threshold
        regions = self._segment_regions(gray)

        # Create heightmap with distinct region heights
        heightmap = regions * region_contrast

        # Add edge emphasis
        heightmap += edge_map * edge_emphasis

        return np.clip(heightmap, 0, 1)

    def _segment_regions(self, gray: np.ndarray) -> np.ndarray:
        """Segment image into distinct regions."""
        # Use Otsu's thresholding to find regions
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Find connected components
        num_labels, labels = cv2.connectedComponents(binary)

        # Normalize labels to 0-1 range with distinct values
        if num_labels > 1:
            region_map = labels.astype(float) / (num_labels - 1)
        else:
            region_map = np.zeros_like(gray, dtype=float)

        return region_map


class SemanticHeightMapper:
    """
    Unified interface for semantic height mapping across different image types.
    """

    def __init__(self):
        """Initialize all processors."""
        self.processors = {
            'portrait': PortraitProcessor(),
            'landscape': LandscapeProcessor(),
            'text': TextProcessor(),
            'diagram': DiagramProcessor(),
        }

    def process(self, image: Image.Image, mode: str, params: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Process image with specified mode.

        Args:
            image: Input PIL Image
            mode: Processing mode ('portrait', 'landscape', 'text', 'diagram')
            params: Processing parameters (mode-specific)

        Returns:
            Heightmap as numpy array (0-1 normalized)

        Raises:
            ValueError: If mode is not recognized
        """
        if mode not in self.processors:
            raise ValueError(f"Unknown mode: {mode}. Must be one of {list(self.processors.keys())}")

        if params is None:
            params = {}

        # Get processor and run
        processor = self.processors[mode]
        heightmap = processor.process(image, params)

        # Apply post-processing
        heightmap = self.post_process(heightmap, params)

        return heightmap

    def post_process(self, heightmap: np.ndarray, params: Dict[str, Any]) -> np.ndarray:
        """
        Apply post-processing to heightmap.

        Args:
            heightmap: Raw heightmap from processor
            params: Processing parameters
                - smoothing: 0-10 (Gaussian blur sigma, default: 2)
                - edge_strength: 0-100% (edge enhancement, default: 60)
                - contrast: 0-200% (contrast adjustment, default: 100)

        Returns:
            Post-processed heightmap (0-1 normalized)
        """
        # Apply smoothing
        smoothing = params.get('smoothing', 2)
        if smoothing > 0:
            heightmap = gaussian_filter(heightmap, sigma=smoothing)

        # Apply edge enhancement if specified
        edge_strength = params.get('edge_strength', 60) / 100.0
        if edge_strength > 0:
            # Compute edges using Sobel
            edges_x = sobel(heightmap, axis=1)
            edges_y = sobel(heightmap, axis=0)
            edges = np.sqrt(edges_x**2 + edges_y**2)

            # Normalize and add to heightmap
            edges = edges / (edges.max() + 1e-8)
            heightmap = heightmap + edges * edge_strength * 0.2

        # Apply contrast adjustment
        contrast = params.get('contrast', 100) / 100.0
        if contrast != 1.0:
            mean = heightmap.mean()
            heightmap = (heightmap - mean) * contrast + mean

        # Final normalization
        heightmap = np.clip(heightmap, 0, 1)

        # Normalize to full 0-1 range
        h_min, h_max = heightmap.min(), heightmap.max()
        if h_max > h_min:
            heightmap = (heightmap - h_min) / (h_max - h_min)

        return heightmap

    def detect_mode(self, image: Image.Image) -> str:
        """
        Auto-detect appropriate processing mode for image.

        Args:
            image: Input PIL Image

        Returns:
            Suggested mode ('portrait', 'landscape', 'text', 'diagram')
        """
        img_array = np.array(image)

        # Convert to grayscale for analysis
        if len(img_array.shape) == 3:
            gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        else:
            gray = img_array.copy()

        # Try face detection
        if self._has_faces(img_array):
            return 'portrait'

        # Check for text
        if self._has_text(gray):
            return 'text'

        # Check for diagram characteristics (high edge density, low color variation)
        if self._is_diagram(gray):
            return 'diagram'

        # Default to landscape
        return 'landscape'

    def _has_faces(self, img_rgb: np.ndarray) -> bool:
        """Check if image contains faces."""
        try:
            import mediapipe as mp
            face_detection = mp.solutions.face_detection.FaceDetection(
                model_selection=1, min_detection_confidence=0.5
            )
            results = face_detection.process(img_rgb)
            return results.detections is not None and len(results.detections) > 0
        except ImportError:
            # Fallback to OpenCV
            face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
            gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            return len(faces) > 0

    def _has_text(self, gray: np.ndarray) -> bool:
        """Check if image contains text."""
        # Use edge density and aspect ratio heuristics
        edges = cv2.Canny(gray, 50, 150)
        edge_density = edges.sum() / (gray.shape[0] * gray.shape[1] * 255)

        # Text typically has moderate edge density
        if 0.05 < edge_density < 0.3:
            # Check for horizontal structures (text lines)
            horizontal_profile = edges.sum(axis=1)
            peaks = np.diff(np.sign(np.diff(horizontal_profile)))
            num_peaks = (peaks < 0).sum()

            # Text images have multiple horizontal line structures
            return num_peaks > 5

        return False

    def _is_diagram(self, gray: np.ndarray) -> bool:
        """Check if image is a diagram/technical drawing."""
        # Diagrams typically have:
        # 1. High edge density
        # 2. Low color/grayscale variation
        # 3. Sharp transitions

        edges = cv2.Canny(gray, 50, 150)
        edge_density = edges.sum() / (gray.shape[0] * gray.shape[1] * 255)

        # Check grayscale variation
        std_dev = gray.std()

        # Diagrams have high edge density and often lower color variation
        return edge_density > 0.15 and std_dev < 80
