"""
Data validation utilities
"""
from typing import Dict, Any

class DataValidator:
    """Validate input data"""
    
    @staticmethod
    def validate_sensor_data(data: Dict[str, Any]) -> bool:
        """Validate sensor data format"""
        required_fields = ['acceleration', 'gyroscope']
        
        if not all(field in data for field in required_fields):
            return False
        
        # Check if acceleration and gyroscope are lists/arrays of length 3
        accel = data.get('acceleration', [])
        gyro = data.get('gyroscope', [])
        
        return len(accel) == 3 and len(gyro) == 3
    
    @staticmethod
    def validate_user_data(data: Dict[str, Any]) -> bool:
        """Validate user health data format"""
        required_fields = ['age', 'heart_rate', 'blood_pressure']
        
        for field in required_fields:
            if field not in data:
                return False
        
        # Validate age
        if not isinstance(data.get('age'), (int, float)) or data['age'] < 0:
            return False
        
        # Validate heart rate
        if not isinstance(data.get('heart_rate'), (int, float)) or data['heart_rate'] <= 0:
            return False
        
        return True
    
    @staticmethod
    def validate_text(text: str, min_length: int = 1, max_length: int = 5000) -> bool:
        """Validate text input"""
        if not isinstance(text, str):
            return False
        
        return min_length <= len(text) <= max_length
