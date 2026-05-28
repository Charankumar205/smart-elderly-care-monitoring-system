"""
Fall detection using accelerometer and gyroscope data
"""
import numpy as np
from typing import Dict, Any

class FallDetectionModel:
    """
    Fall detection model using sensor fusion
    Analyzes accelerometer and gyroscope data to detect potential falls
    """
    
    def __init__(self):
        self.threshold = 2.5
        self.model_version = '1.0.0'
    
    def predict(self, sensor_data: Dict[str, Any]) -> bool:
        """
        Predict if a fall has occurred
        
        Args:
            sensor_data: Dictionary containing accelerometer and gyroscope readings
            
        Returns:
            bool: True if fall detected, False otherwise
        """
        try:
            acceleration = np.array(sensor_data.get('acceleration', [0, 0, 0]))
            gyroscope = np.array(sensor_data.get('gyroscope', [0, 0, 0]))
            
            # Calculate magnitude
            accel_magnitude = np.linalg.norm(acceleration)
            gyro_magnitude = np.linalg.norm(gyroscope)
            
            # Fall detection logic
            fall_detected = accel_magnitude > self.threshold and gyro_magnitude > 1.5
            
            return fall_detected
        except Exception as e:
            raise ValueError(f"Error in fall detection: {str(e)}")
    
    def preprocess_data(self, raw_data: np.ndarray) -> np.ndarray:
        """Preprocess sensor data"""
        return (raw_data - np.mean(raw_data)) / (np.std(raw_data) + 1e-8)
    
    def extract_features(self, sensor_data: Dict) -> Dict:
        """Extract features from sensor data"""
        accel = np.array(sensor_data.get('acceleration', [0, 0, 0]))
        gyro = np.array(sensor_data.get('gyroscope', [0, 0, 0]))
        
        return {
            'accel_magnitude': float(np.linalg.norm(accel)),
            'gyro_magnitude': float(np.linalg.norm(gyro)),
            'accel_variance': float(np.var(accel)),
            'gyro_variance': float(np.var(gyro))
        }
