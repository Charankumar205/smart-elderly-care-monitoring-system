"""
Risk prediction model for elderly care
Predicts health risks based on various factors
"""
import numpy as np
from typing import Dict, Any, List

class RiskPredictor:
    """
    Risk predictor for health monitoring
    Evaluates multiple risk factors and provides risk scores
    """
    
    def __init__(self):
        self.model_version = '1.0.0'
        self.risk_factors = {
            'age': 0.15,
            'heart_rate': 0.20,
            'blood_pressure': 0.20,
            'activity_level': 0.15,
            'sleep_quality': 0.15,
            'medication_adherence': 0.10,
            'mental_health': 0.05
        }
    
    def predict(self, user_data: Dict[str, Any]) -> float:
        """
        Predict risk score for a user
        
        Args:
            user_data: Dictionary containing user health metrics
            
        Returns:
            float: Risk score between 0 and 1
        """
        if not user_data:
            raise ValueError("User data cannot be empty")
        
        risk_score = 0.0
        
        # Calculate weighted risk score
        for factor, weight in self.risk_factors.items():
            if factor in user_data:
                factor_risk = self._calculate_factor_risk(factor, user_data[factor])
                risk_score += factor_risk * weight
        
        return min(1.0, max(0.0, risk_score))
    
    def _calculate_factor_risk(self, factor: str, value: Any) -> float:
        """Calculate risk for a specific factor"""
        if factor == 'age':
            # Higher risk with advanced age
            age = value
            return min(1.0, (age - 60) / 40) if age > 60 else 0.2
        
        elif factor == 'heart_rate':
            # Normal range: 60-100 bpm
            return self._calculate_deviation_risk(value, 60, 100)
        
        elif factor == 'blood_pressure':
            # Normal: systolic < 120, diastolic < 80
            systolic = value.get('systolic', 120)
            diastolic = value.get('diastolic', 80)
            return (self._calculate_deviation_risk(systolic, 90, 120) + 
                   self._calculate_deviation_risk(diastolic, 60, 80)) / 2
        
        elif factor == 'activity_level':
            # Higher activity = lower risk
            return max(0, 1 - value / 10000)
        
        elif factor == 'sleep_quality':
            # 0-10 scale, higher is better
            return max(0, 1 - value / 10)
        
        elif factor == 'medication_adherence':
            # 0-100%, higher is better
            return max(0, 1 - value / 100)
        
        elif factor == 'mental_health':
            # 0-10 scale, higher is better
            return max(0, 1 - value / 10)
        
        return 0.5
    
    def _calculate_deviation_risk(self, value: float, lower: float, upper: float) -> float:
        """Calculate risk based on deviation from ideal range"""
        if lower <= value <= upper:
            return 0.1
        elif value < lower:
            return (lower - value) / lower * 0.5
        else:
            return (value - upper) / upper * 0.5
    
    def get_factors(self, user_id: str) -> Dict[str, Any]:
        """Get detailed risk factors for a user"""
        return {
            'user_id': user_id,
            'factors': self.risk_factors,
            'last_updated': '2026-02-20',
            'model_version': self.model_version
        }
