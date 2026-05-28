"""
Routes for Risk Prediction module
"""
from flask import request, jsonify
from . import risk_prediction_bp
from modules.risk_prediction.predictor import RiskPredictor

@risk_prediction_bp.route('/predict', methods=['POST'])
def predict_risk():
    """
    Predict health risk from user data
    Expected JSON: {'age': ..., 'heart_rate': ..., 'blood_pressure': ..., etc}
    """
    try:
        data = request.get_json()
        predictor = RiskPredictor()
        risk_score = predictor.predict(data)
        
        return jsonify({
            'success': True,
            'risk_score': float(risk_score),
            'risk_level': 'high' if risk_score > 0.7 else 'medium' if risk_score > 0.4 else 'low'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@risk_prediction_bp.route('/status', methods=['GET'])
def status():
    """Get risk prediction module status"""
    return jsonify({
        'module': 'Risk Prediction',
        'status': 'active',
        'version': '1.0.0'
    }), 200