"""
NLP analysis for health-related text
Analyzes sentiment, symptoms, and health concerns from user text
"""
from typing import Dict, Any, List
from textblob import TextBlob

class NLPAnalyzer:
    """
    NLP analyzer for health-related text
    Provides sentiment analysis, symptom extraction, and health concern detection
    """
    
    def __init__(self):
        self.model_version = '2.0.0'
        self.health_keywords = {
            'weakness': ['weak', 'weakness', 'strength loss', 'feeble', 'fragile'],
            'fever': ['fever', 'temperature', 'hot', 'warm', 'chills'],
            'dizziness': ['dizzy', 'dizziness', 'vertigo', 'lightheaded', 'spinning'],
            'chest_pain': ['chest pain', 'chest', 'heart', 'palpitation', 'tightness'],
            'fatigue': ['tired', 'fatigue', 'exhausted', 'fatigue', 'energy loss'],
            'breathing': ['breathless', 'shortness of breath', 'wheezing', 'dyspnea', 'difficulty breathing'],
            'unconsciousness': ['unconscious', 'faint', 'passed out', 'blacked out', 'unresponsive'],
            'anxiety': ['anxiety', 'anxious', 'nervous', 'worried', 'stress', 'panic'],
            'pain': ['pain', 'ache', 'hurt', 'sore', 'discomfort'],
            'nausea': ['nausea', 'nauseous', 'vomiting', 'sick', 'queasy'],
            'headache': ['headache', 'migraine', 'head pain', 'head ache'],
            'confusion': ['confused', 'confusion', 'disoriented', 'memory loss', 'forgetful'],
            'falls': ['fall', 'fell', 'trip', 'stumble', 'lost balance'],
            'injury': ['injury', 'hurt', 'injured', 'trauma', 'accident']
        }
        
        # Severity indicators
        self.high_severity_keywords = [
            'emergency', 'critical', 'severe', 'urgent', 'immediately',
            'unconscious', 'not responding', 'cannot', 'unable', 'stopped'
        ]
        
        self.medium_severity_keywords = [
            'difficulty', 'trouble', 'pain', 'problem', 'concern', 'worried'
        ]
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze text for health concerns
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        extracted_symptoms = self.extract_health_concerns(text)
        sentiment = self.get_sentiment(text)
        severity = self.calculate_severity(text, extracted_symptoms)
        
        return {
            'extracted_symptoms': extracted_symptoms,
            'health_sentiment': sentiment['label'],
            'sentiment_score': sentiment['polarity'],
            'severity_score': severity['score'],
            'severity_level': severity['level'],
            'text_length': len(text),
            'keywords': self.extract_keywords(text),
            'risk_factors': self._identify_risk_factors(extracted_symptoms, severity)
        }
    
    def get_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using TextBlob
        
        Returns:
            Dictionary with sentiment scores and label
        """
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 (negative) to 1 (positive)
            subjectivity = blob.sentiment.subjectivity
            
            # Convert polarity to label
            if polarity < -0.1:
                label = 'Negative'
            elif polarity > 0.1:
                label = 'Positive'
            else:
                label = 'Neutral'
            
            # Context-based adjustment for health reports
            text_lower = text.lower()
            if any(kw in text_lower for kw in ['normal', 'fine', 'okay', 'good', 'healthy']):
                label = 'Positive Health Condition'
            elif any(kw in text_lower for kw in ['sick', 'ill', 'bad', 'worse', 'pain', 'suffer']):
                label = 'Negative Health Condition'
            else:
                label = 'Mixed Health Status'
            
            return {
                'label': label,
                'polarity': float(polarity),
                'subjectivity': float(subjectivity)
            }
        except Exception as e:
            return {
                'label': 'Neutral',
                'polarity': 0.0,
                'subjectivity': 0.5
            }
    
    def extract_health_concerns(self, text: str) -> List[str]:
        """Extract health concerns from text"""
        text_lower = text.lower()
        concerns = []
        
        for concern, keywords in self.health_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                concerns.append(concern.replace('_', ' ').title())
        
        return concerns
    
    def calculate_severity(self, text: str, symptoms: List[str]) -> Dict[str, Any]:
        """
        Calculate severity level based on keywords and symptoms
        
        Returns:
            Dictionary with severity score and level
        """
        text_lower = text.lower()
        severity_score = 0.0
        
        # Check for high severity indicators
        high_severity_count = sum(1 for kw in self.high_severity_keywords if kw in text_lower)
        severity_score += high_severity_count * 0.25
        
        # Check for medium severity indicators
        medium_severity_count = sum(1 for kw in self.medium_severity_keywords if kw in text_lower)
        severity_score += medium_severity_count * 0.15
        
        # Symptoms contribute to severity
        critical_symptoms = ['unconsciousness', 'chest_pain', 'breathing', 'falls']
        high_symptom_count = sum(1 for s in symptoms if any(c in s.lower() for c in critical_symptoms))
        severity_score += high_symptom_count * 0.2
        
        severity_score = min(1.0, severity_score)
        
        # Determine level
        if severity_score >= 0.7:
            level = 'High'
        elif severity_score >= 0.4:
            level = 'Medium'
        else:
            level = 'Low'
        
        return {
            'score': float(severity_score),
            'level': level
        }
    
    def _identify_risk_factors(self, symptoms: List[str], severity: Dict[str, Any]) -> List[str]:
        """Identify risk factors based on symptoms and severity"""
        risk_factors = []
        
        critical_symptoms = ['Chest Pain', 'Breathing', 'Unconsciousness', 'Falls']
        
        for symptom in symptoms:
            if symptom in critical_symptoms:
                risk_factors.append(f'Critical: {symptom} detected')
        
        if severity['level'] == 'High':
            risk_factors.append('High Severity Condition')
        elif severity['level'] == 'Medium':
            risk_factors.append('Moderate Health Concern')
        
        if len(symptoms) >= 3:
            risk_factors.append('Multiple Symptoms Reported')
        
        return risk_factors
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract important keywords from text"""
        # Simple keyword extraction (tokenization)
        words = text.lower().split()
        # Remove common words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        keywords = [w for w in words if w not in stop_words and len(w) > 3]
        return list(set(keywords))[:10]
