"""
Enhanced Risk Prediction Module
Combines fall detection, NLP analysis, and health metrics for comprehensive risk assessment
"""
import numpy as np
from typing import Dict, Any, List

class EnhancedRiskPredictor:
    """
    Enhanced risk prediction that combines multiple data sources
    """
    
    def __init__(self):
        self.model_version = '2.0.0'
    
    def predict_comprehensive_risk(self, 
                                   fall_data: Dict[str, Any],
                                   nlp_data: Dict[str, Any],
                                   user_health_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Predict comprehensive risk combining all data sources
        
        Args:
            fall_data: Fall detection results
            nlp_data: NLP analysis results
            user_health_data: Additional user health metrics
            
        Returns:
            Dictionary with comprehensive risk assessment
        """
        
        # Calculate risk scores from different sources
        fall_risk_score = self._calculate_fall_risk_score(fall_data)
        nlp_risk_score = self._calculate_nlp_risk_score(nlp_data)
        health_risk_score = self._calculate_health_risk_score(user_health_data or {})
        
        # Weighted combination
        weights = {
            'fall': 0.40,
            'nlp': 0.40,
            'health': 0.20
        }
        
        final_risk_score = (
            fall_risk_score * weights['fall'] +
            nlp_risk_score * weights['nlp'] +
            health_risk_score * weights['health']
        )
        
        final_risk_score = min(1.0, max(0.0, final_risk_score))
        
        # Determine risk category
        risk_category = self._categorize_risk(final_risk_score, fall_data, nlp_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            risk_category, fall_data, nlp_data
        )
        
        return {
            'final_risk_score': float(final_risk_score),
            'risk_category': risk_category,
            'fall_risk_component': float(fall_risk_score),
            'nlp_risk_component': float(nlp_risk_score),
            'health_risk_component': float(health_risk_score),
            'confidence': float(self._calculate_confidence(fall_data, nlp_data)),
            'recommendations': recommendations,
            'alert_status': self._determine_alert_status(risk_category),
            'medical_action': self._determine_medical_action(risk_category)
        }
    
    def _calculate_fall_risk_score(self, fall_data: Dict[str, Any]) -> float:
        """Calculate risk score from fall detection"""
        if fall_data.get('emergency_status'):
            return 0.95
        elif fall_data.get('posture') == 'Fall Detected':
            return 0.90
        elif fall_data.get('posture') == 'Emergency Posture':
            return 0.70
        elif fall_data.get('posture') == 'Unconscious Condition':
            return 0.98
        elif fall_data.get('posture') == 'Normal Standing':
            return 0.10
        elif fall_data.get('posture') == 'Sitting':
            return 0.15
        else:
            confidence = fall_data.get('confidence', 0.5)
            return 0.3 if confidence > 0.8 else 0.2
    
    def _calculate_nlp_risk_score(self, nlp_data: Dict[str, Any]) -> float:
        """Calculate risk score from NLP analysis"""
        base_score = 0.0
        
        # Severity component
        severity_level = nlp_data.get('severity_level', 'Low')
        severity_map = {'Low': 0.2, 'Medium': 0.6, 'High': 0.9}
        base_score += severity_map.get(severity_level, 0.3) * 0.5
        
        # Symptom component
        symptoms = nlp_data.get('extracted_symptoms', [])
        critical_symptoms = ['Chest Pain', 'Breathing', 'Unconsciousness', 'Falls']
        critical_count = sum(1 for s in symptoms if any(c in s for c in critical_symptoms))
        
        symptom_score = min(0.95, critical_count * 0.25)
        base_score += symptom_score * 0.4
        
        # Sentiment component
        sentiment = nlp_data.get('health_sentiment', 'Neutral')
        if 'Negative' in sentiment:
            base_score += 0.15 * 0.1
        
        return min(1.0, max(0.0, base_score))
    
    def _calculate_health_risk_score(self, health_data: Dict[str, Any]) -> float:
        """Calculate risk score from general health data"""
        risk_score = 0.3  # Default baseline
        
        if not health_data:
            return risk_score
        
        # Age factor
        age = health_data.get('age', 75)
        if age > 85:
            risk_score += 0.2
        elif age > 75:
            risk_score += 0.1
        
        # Existing conditions
        conditions = health_data.get('conditions', [])
        condition_risk_map = {
            'diabetes': 0.15,
            'hypertension': 0.15,
            'heart_disease': 0.25,
            'stroke_history': 0.20,
            'osteoporosis': 0.10
        }
        
        for condition, risk in condition_risk_map.items():
            if condition in [c.lower() for c in conditions]:
                risk_score += risk
        
        return min(1.0, max(0.0, risk_score))
    
    def _categorize_risk(self, risk_score: float, fall_data: Dict, nlp_data: Dict) -> str:
        """Categorize risk level"""
        
        # Emergency conditions override score
        if fall_data.get('emergency_status') or fall_data.get('posture') == 'Unconscious Condition':
            return 'Emergency Critical'
        
        emergency_symptoms = ['Unconsciousness', 'Chest Pain', 'Breathing']
        symptoms = nlp_data.get('extracted_symptoms', [])
        if any(s in symptoms for s in emergency_symptoms):
            return 'Emergency Critical'
        
        # Score-based categorization
        if risk_score >= 0.75:
            return 'Emergency Critical'
        elif risk_score >= 0.55:
            return 'High Risk'
        elif risk_score >= 0.35:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    def _generate_recommendations(self, risk_category: str, fall_data: Dict, nlp_data: Dict) -> List[str]:
        """Generate recommendations based on risk category"""
        recommendations = []
        
        if risk_category == 'Emergency Critical':
            recommendations.extend([
                'Emergency response required immediately',
                'Call emergency services (Ambulance)',
                'Immediate medical evaluation needed',
                'Patient requires hospitalization assessment'
            ])
        elif risk_category == 'High Risk':
            recommendations.extend([
                'Immediate caretaker and medical attention required',
                'Contact healthcare provider urgently',
                'Close monitoring recommended',
                'Patient should not be left unattended'
            ])
        elif risk_category == 'Medium Risk':
            recommendations.extend([
                'Caretaker attention recommended',
                'Schedule doctor appointment within 24 hours',
                'Monitor patient condition regularly',
                'Increase supervision level'
            ])
        else:  # Low Risk
            recommendations.extend([
                'Patient condition appears stable',
                'Continue routine monitoring',
                'Maintain regular health check-ups',
                'No immediate medical action required'
            ])
        
        # Add specific recommendations based on symptoms
        symptoms = nlp_data.get('extracted_symptoms', [])
        if 'Falls' in symptoms or fall_data.get('posture') == 'Fall Detected':
            recommendations.append('Assess for injuries from fall')
            recommendations.append('Consider fall prevention measures')
        
        if 'Breathing' in symptoms:
            recommendations.append('Monitor oxygen saturation levels')
        
        if 'Chest Pain' in symptoms:
            recommendations.append('Consider cardiac evaluation')
        
        return recommendations
    
    def _calculate_confidence(self, fall_data: Dict, nlp_data: Dict) -> float:
        """Calculate overall confidence in prediction"""
        fall_confidence = fall_data.get('confidence', 0.5)
        severity_score = nlp_data.get('severity_score', 0.5)
        
        # Higher confidence when data points agree
        average_confidence = (fall_confidence + severity_score) / 2
        
        return min(1.0, average_confidence + 0.1)  # Boost overall confidence slightly
    
    def _determine_alert_status(self, risk_category: str) -> str:
        """Determine alert status color/level"""
        alert_map = {
            'Emergency Critical': 'RED_ALERT',
            'High Risk': 'ORANGE_ALERT',
            'Medium Risk': 'YELLOW_ALERT',
            'Low Risk': 'GREEN_SAFE'
        }
        return alert_map.get(risk_category, 'YELLOW_ALERT')
    
    def _determine_medical_action(self, risk_category: str) -> str:
        """Determine recommended medical action"""
        action_map = {
            'Emergency Critical': 'Emergency Response Required Immediately',
            'High Risk': 'Immediate Medical Consultation Required',
            'Medium Risk': 'Schedule Medical Consultation Within 24 Hours',
            'Low Risk': 'Continue Routine Monitoring'
        }
        return action_map.get(risk_category, 'Continue Monitoring')
