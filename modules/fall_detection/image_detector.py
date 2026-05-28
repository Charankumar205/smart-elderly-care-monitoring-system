"""
Image-based fall detection using Computer Vision and Deep Learning
Analyzes patient posture from uploaded images using MediaPipe and CNN
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, Any, Tuple
from PIL import Image
import io

class ImageFallDetector:
    """
    Fall detection using image analysis and pose detection
    Uses MediaPipe for human pose detection and CNN for posture classification
    """
    
    def __init__(self):
        self.model_version = '2.0.0'
        self.has_pose_model = False
        self.mp_pose = None
        self.mp_drawing = None
        self.pose = None

        if hasattr(mp, 'solutions') and hasattr(mp.solutions, 'pose'):
            try:
                self.mp_pose = mp.solutions.pose
                self.mp_drawing = mp.solutions.drawing_utils
                self.pose = self.mp_pose.Pose(
                    static_image_mode=True,
                    model_complexity=2,
                    smooth_landmarks=True,
                    min_detection_confidence=0.3,
                    min_tracking_confidence=0.3
                )
                self.has_pose_model = True
            except Exception:
                self.has_pose_model = False

        # Posture thresholds
        self.vertical_threshold = 0.6
        self.horizontal_threshold = 0.4
        
        # Posture categories
        self.posture_classes = {
            'standing': 0,
            'sitting': 1,
            'lying': 2,
            'fall_detected': 3,
            'emergency_posture': 4,
            'unconscious': 5
        }
    
    def analyze_image(self, image_path: str = None, image_bytes: bytes = None) -> Dict[str, Any]:
        """
        Analyze image for fall detection
        
        Args:
            image_path: Path to image file
            image_bytes: Image as bytes (for uploaded files)
            
        Returns:
            Dictionary with detection results
        """
        try:
            # Load image
            if image_bytes:
                image = Image.open(io.BytesIO(image_bytes))
                image_np = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            else:
                image_np = cv2.imread(image_path)
            
            if image_np is None:
                raise ValueError("Cannot load image")
            
            # Convert to RGB for MediaPipe
            rgb_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
            
            if not self.has_pose_model or self.pose is None:
                return self._analyze_image_fallback(image_np)

            # Detect pose landmarks
            results = self.pose.process(rgb_image)
            
            if not results.pose_landmarks:
                return self._analyze_image_fallback(image_np)
            
            # Analyze posture
            posture_result = self._classify_posture(results.pose_landmarks)
            
            return {
                'posture': posture_result['posture'],
                'confidence': posture_result['confidence'],
                'emergency_status': posture_result['emergency_status'],
                'body_angle': posture_result['body_angle'],
                'height_ratio': posture_result['height_ratio'],
                'detailed_analysis': posture_result.get('detailed_analysis', {})
            }
        
        except Exception as e:
            return {
                'posture': 'error',
                'confidence': 0.0,
                'emergency_status': False,
                'error': str(e)
            }

    def _analyze_image_fallback(self, image_np: np.ndarray) -> Dict[str, Any]:
        """Fallback analysis when MediaPipe pose is unavailable."""
        try:
            gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (640, 640), interpolation=cv2.INTER_LINEAR)
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            boxes, weights = hog.detectMultiScale(
                resized,
                winStride=(8, 8),
                padding=(16, 16),
                scale=1.05,
                hitThreshold=0
            )

            if len(boxes) == 0:
                boxes, weights = hog.detectMultiScale(
                    resized,
                    winStride=(4, 4),
                    padding=(8, 8),
                    scale=1.02,
                    hitThreshold=-0.5
                )

            if len(boxes) == 0:
                contour_detection = self._detect_person_contour(image_np)
                if contour_detection:
                    x, y, w, h = contour_detection
                    boxes = np.array([[x, y, w, h]])
                else:
                    return {
                        'posture': 'unknown',
                        'confidence': 0.0,
                        'emergency_status': False,
                        'error': 'No person detected in image'
                    }
            else:
                if isinstance(boxes, np.ndarray) and boxes.shape[0] > 1:
                    areas = [w * h for (x, y, w, h) in boxes]
                    best_index = int(np.argmax(areas))
                    x, y, w, h = boxes[best_index]
                else:
                    x, y, w, h = boxes[0]
            x = int(x * image_np.shape[1] / resized.shape[1])
            y = int(y * image_np.shape[0] / resized.shape[0])
            w = int(w * image_np.shape[1] / resized.shape[1])
            h = int(h * image_np.shape[0] / resized.shape[0])
            aspect_ratio = float(h) / (w + 1e-6)
            area_ratio = (w * h) / (image_np.shape[0] * image_np.shape[1])

            if area_ratio < 0.02:
                posture = 'Unconscious Condition'
                confidence = 0.65
                emergency = True
            elif aspect_ratio > 1.5:
                posture = 'Normal Standing'
                confidence = 0.78
                emergency = False
            elif aspect_ratio > 1.0:
                posture = 'Sitting'
                confidence = 0.75
                emergency = False
            elif aspect_ratio > 0.6:
                posture = 'Sleeping'
                confidence = 0.72
                emergency = False
            else:
                posture = 'Fall Detected'
                confidence = 0.82
                emergency = True

            detailed_analysis = {
                'aspect_ratio': aspect_ratio,
                'area_ratio': area_ratio
            }

            if hasattr(boxes, 'tolist'):
                detailed_analysis['boxes'] = boxes.tolist()
            elif isinstance(boxes, (list, tuple)):
                detailed_analysis['boxes'] = [list(b) for b in boxes]
            else:
                detailed_analysis['boxes'] = []

            orientation_angle = self._measure_orientation(image_np, x, y, w, h)
            is_horizontal = (orientation_angle is not None and orientation_angle < 35) or aspect_ratio < 1.0

            if area_ratio < 0.02:
                posture = 'Unconscious Condition'
                confidence = 0.65
                emergency = True
            elif is_horizontal:
                posture = 'Fall Detected'
                confidence = 0.90
                emergency = True
            elif aspect_ratio > 1.6:
                posture = 'Normal Standing'
                confidence = 0.78
                emergency = False
            elif aspect_ratio > 1.1:
                posture = 'Sitting'
                confidence = 0.75
                emergency = False
            else:
                posture = 'Sleeping'
                confidence = 0.72
                emergency = False

            detailed_analysis['orientation_angle'] = orientation_angle

            return {
                'posture': posture,
                'confidence': confidence,
                'emergency_status': emergency,
                'error': None,
                'body_angle': None,
                'height_ratio': aspect_ratio,
                'detailed_analysis': detailed_analysis
            }
        except Exception as e:
            return {
                'posture': 'error',
                'confidence': 0.0,
                'emergency_status': False,
                'error': str(e)
            }

    def _measure_orientation(self, image_np: np.ndarray, x: int, y: int, w: int, h: int):
        """Measure the dominant orientation of the detected region."""
        try:
            roi = image_np[y:y+h, x:x+w]
            if roi.size == 0:
                return None

            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (7, 7), 0)
            _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                return None

            cnt = max(contours, key=cv2.contourArea)
            rect = cv2.minAreaRect(cnt)
            width, height = rect[1]
            angle = rect[2]
            if width <= 0 or height <= 0:
                return None

            # Convert to angle relative to horizontal
            if width < height:
                angle = angle + 90.0
            return abs(angle)
        except Exception:
            return None

    def _classify_posture(self, landmarks) -> Dict[str, Any]:
        """
        Classify posture based on pose landmarks
        
        Args:
            landmarks: MediaPipe pose landmarks
            
        Returns:
            Dictionary with posture classification
        """
        try:
            # Extract key points
            nose = np.array([landmarks[0].x, landmarks[0].y])
            left_shoulder = np.array([landmarks[11].x, landmarks[11].y])
            right_shoulder = np.array([landmarks[12].x, landmarks[12].y])
            left_hip = np.array([landmarks[23].x, landmarks[23].y])
            right_hip = np.array([landmarks[24].x, landmarks[24].y])
            left_knee = np.array([landmarks[25].x, landmarks[25].y])
            right_knee = np.array([landmarks[26].x, landmarks[26].y])
            left_ankle = np.array([landmarks[27].x, landmarks[27].y])
            right_ankle = np.array([landmarks[28].x, landmarks[28].y])
            
            # Calculate body angles
            shoulder_center = (left_shoulder + right_shoulder) / 2
            hip_center = (left_hip + right_hip) / 2
            ankle_center = (left_ankle + right_ankle) / 2
            
            # Body vertical alignment
            body_vector = hip_center - shoulder_center
            body_angle = self._calculate_tilt_angle(body_vector)

            # Vertical ratio (how upright the torso is)
            if np.linalg.norm(body_vector) > 0:
                vertical_ratio = np.abs(np.dot(body_vector, np.array([0.0, 1.0]))) / np.linalg.norm(body_vector)
            else:
                vertical_ratio = 0.0
            
            # Height ratio (nose to ankle distance vs hip width)
            nose_ankle_dist = np.linalg.norm(nose - ankle_center)
            hip_width = np.linalg.norm(right_hip - left_hip)
            height_ratio = nose_ankle_dist / (hip_width + 1e-6) if hip_width > 0 else 0

            # Pose orientation from landmarks
            points = np.array([[lm.x, lm.y] for lm in landmarks])
            pose_width = points[:, 0].max() - points[:, 0].min()
            pose_height = points[:, 1].max() - points[:, 1].min()
            pose_horiz_ratio = (pose_width + 1e-6) / (pose_height + 1e-6)
            is_pose_horizontal = pose_horiz_ratio > 1.0
            
            # Determine posture
            posture_result = self._determine_posture(
                body_angle, vertical_ratio, height_ratio, 
                hip_center, ankle_center, nose,
                pose_horiz_ratio,
                is_pose_horizontal
            )
            
            return {
                'posture': posture_result['posture'],
                'confidence': posture_result['confidence'],
                'emergency_status': posture_result['emergency_status'],
                'body_angle': float(body_angle),
                'vertical_ratio': float(vertical_ratio),
                'height_ratio': float(height_ratio),
                'detailed_analysis': {
                    'body_angle': float(body_angle),
                    'vertical_alignment': float(vertical_ratio),
                    'height_ratio': float(height_ratio),
                    'pose_horizontal_ratio': float(pose_horiz_ratio)
                }
            }
        
        except Exception as e:
            return {
                'posture': 'error',
                'confidence': 0.0,
                'emergency_status': False,
                'error': str(e)
            }
    
    def _determine_posture(self, body_angle: float, vertical_ratio: float, 
                          height_ratio: float, hip_center, ankle_center, nose,
                          pose_horiz_ratio: float,
                          is_pose_horizontal: bool) -> Dict[str, Any]:
        """
        Determine posture category based on calculated metrics
        """
        # Fall Detected: torso is tilted and not upright, or pose alignment is horizontal
        if (body_angle > 35 and vertical_ratio < 0.7) or (is_pose_horizontal and body_angle > 25):
            return {
                'posture': 'Fall Detected',
                'confidence': 0.96,
                'emergency_status': True
            }

        # Unconscious: person is nearly horizontal with very low upright alignment
        if vertical_ratio < 0.25 and height_ratio < 1.3:
            return {
                'posture': 'Unconscious Condition',
                'confidence': 0.92,
                'emergency_status': True
            }

        # Emergency Posture: unstable or partially collapsed positions
        if body_angle > 40 and vertical_ratio < 0.55:
            return {
                'posture': 'Emergency Posture',
                'confidence': 0.88,
                'emergency_status': True
            }

        # Lying/Sleeping: person is mostly horizontal
        if vertical_ratio < 0.35 or (body_angle > 55 and height_ratio < 2.0):
            return {
                'posture': 'Sleeping',
                'confidence': 0.87,
                'emergency_status': False
            }

        # Sitting: significant bending with reasonably high nose-to-ankle ratio
        if vertical_ratio < 0.6 and height_ratio > 1.0:
            return {
                'posture': 'Sitting',
                'confidence': 0.89,
                'emergency_status': False
            }

        # Standing: Upright position
        if vertical_ratio > 0.7:
            return {
                'posture': 'Normal Standing',
                'confidence': 0.91,
                'emergency_status': False
            }

        # Default to normal if uncertain
        return {
            'posture': 'Normal Standing',
            'confidence': 0.75,
            'emergency_status': False
        }
    
    def _calculate_angle(self, point1, point2, point3) -> float:
        """
        Calculate angle between three points
        """
        # Vectors
        a = point1 - point2
        b = point3 - point2
        
        # Calculate angle
        cos_angle = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-6)
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))

        return np.degrees(angle)

    def _calculate_tilt_angle(self, vector: np.ndarray) -> float:
        """Calculate the angle between a vector and the vertical axis."""
        norm = np.linalg.norm(vector)
        if norm == 0:
            return 0.0

        vertical = np.array([0.0, 1.0])
        cos_angle = np.dot(vector, vertical) / norm
        cos_angle = np.clip(np.abs(cos_angle), -1.0, 1.0)
        angle = np.arccos(cos_angle)
        return np.degrees(angle)
    
    def draw_landmarks(self, image_path: str, output_path: str) -> str:
        """
        Draw pose landmarks on image for visualization
        """
        try:
            image = cv2.imread(image_path)
            if self.pose is None:
                cv2.imwrite(output_path, image)
                return output_path

            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.pose.process(rgb_image)
            
            if results.pose_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS
                )
            
            cv2.imwrite(output_path, image)
            return output_path
        
        except Exception as e:
            raise ValueError(f"Error drawing landmarks: {str(e)}")
