"""
Tests for risk prediction module
"""
import pytest
from modules.risk_prediction.predictor import RiskPredictor

class TestRiskPredictor:
    """Test risk predictor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.predictor = RiskPredictor()
    
    def test_predictor_initialization(self):
        """Test predictor initialization"""
        assert self.predictor.model_version == '1.0.0'
        assert 'age' in self.predictor.risk_factors
        assert 'heart_rate' in self.predictor.risk_factors
    
    def test_risk_score_in_valid_range(self):
        """Test that risk score is between 0 and 1"""
        user_data = {
            'age': 70,
            'heart_rate': 75,
            'blood_pressure': {'systolic': 130, 'diastolic': 85},
            'activity_level': 5000,
            'sleep_quality': 7,
            'medication_adherence': 90,
            'mental_health': 8
        }
        
        score = self.predictor.predict(user_data)
        assert 0 <= score <= 1
    
    def test_high_age_increases_risk(self):
        """Test that higher age increases risk"""
        data_young = {'age': 65}
        data_old = {'age': 85}
        
        score_young = self.predictor._calculate_factor_risk('age', 65)
        score_old = self.predictor._calculate_factor_risk('age', 85)
        
        assert score_old > score_young
    
    def test_abnormal_heart_rate_increases_risk(self):
        """Test that abnormal heart rate increases risk"""
        score_normal = self.predictor._calculate_factor_risk('heart_rate', 75)
        score_high = self.predictor._calculate_factor_risk('heart_rate', 120)
        
        assert score_high > score_normal
    
    def test_get_factors(self):
        """Test getting risk factors"""
        factors = self.predictor.get_factors('user123')
        
        assert 'user_id' in factors
        assert factors['user_id'] == 'user123'
        assert 'factors' in factors
        assert 'model_version' in factors
    
    def test_empty_user_data_raises_error(self):
        """Test that empty user data raises error"""
        with pytest.raises(ValueError):
            self.predictor.predict({})
