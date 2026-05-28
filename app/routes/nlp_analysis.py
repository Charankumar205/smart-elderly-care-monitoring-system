"""
Routes for NLP analysis module
"""
from flask import request, jsonify
from . import nlp_bp
from modules.nlp_analysis.analyzer import NLPAnalyzer

@nlp_bp.route('/analyze', methods=['POST'])
def analyze_text():
    """
    Analyze text using NLP
    Expected JSON: {'text': '...', 'user_id': '...'}
    """
    try:
        data = request.get_json()
        analyzer = NLPAnalyzer()
        result = analyzer.analyze(data.get('text'))
        
        return jsonify({
            'success': True,
            'analysis': result,
            'user_id': data.get('user_id')
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@nlp_bp.route('/sentiment', methods=['POST'])
def sentiment_analysis():
    """Analyze sentiment from text"""
    try:
        data = request.get_json()
        analyzer = NLPAnalyzer()
        sentiment = analyzer.get_sentiment(data.get('text'))
        
        return jsonify({
            'success': True,
            'sentiment': sentiment
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@nlp_bp.route('/status', methods=['GET'])
def status():
    """Get NLP module status"""
    return jsonify({
        'module': 'NLP Analysis',
        'status': 'active',
        'version': '1.0.0'
    }), 200
