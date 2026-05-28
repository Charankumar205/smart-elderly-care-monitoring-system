"""
Tests for NLP analysis module
"""
import pytest
from modules.nlp_analysis.analyzer import NLPAnalyzer

class TestNLPAnalyzer:
    """Test NLP analyzer"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = NLPAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        assert self.analyzer.model_version == '1.0.0'
        assert 'pain' in self.analyzer.health_keywords
    
    def test_sentiment_analysis(self):
        """Test sentiment analysis"""
        text = "I feel good and happy today"
        sentiment = self.analyzer.get_sentiment(text)
        
        assert 'positive' in sentiment
        assert 'negative' in sentiment
        assert 'neutral' in sentiment
        assert sentiment['positive'] > sentiment['negative']
    
    def test_health_concern_extraction(self):
        """Test health concern extraction"""
        text = "I have pain in my chest and I feel dizzy"
        concerns = self.analyzer.extract_health_concerns(text)
        
        assert 'pain' in concerns
        assert 'dizziness' in concerns
    
    def test_keyword_extraction(self):
        """Test keyword extraction"""
        text = "I have severe headache and feeling tired"
        keywords = self.analyzer.extract_keywords(text)
        
        assert len(keywords) > 0
        assert 'severe' in keywords
    
    def test_analyze_text(self):
        """Test complete text analysis"""
        text = "I have been feeling good lately"
        result = self.analyzer.analyze(text)
        
        assert 'sentiment' in result
        assert 'health_concerns' in result
        assert 'keywords' in result
        assert 'text_length' in result
    
    def test_empty_text_raises_error(self):
        """Test that empty text raises error"""
        with pytest.raises(ValueError):
            self.analyzer.analyze("")
