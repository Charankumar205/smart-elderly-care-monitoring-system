"""
Routes for Fall Detection module
"""
from flask import request, jsonify
from . import fall_detection_bp
from modules.fall_detection.detector import FallDetectionModel

@fall_detection_bp.route('/detect', methods=['POST'])
def detect_fall():
    """
    Detect fall from sensor data
    Expected JSON: {'acceleration': ..., 'gyroscope': ...}
    """
    try:
        data = request.get_json()
        detector = FallDetectionModel()
        result = detector.predict(data)
        
        return jsonify({
            'success': True,
            'fall_detected': result,
            'confidence': 0.95
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@fall_detection_bp.route('/status', methods=['GET'])
def status():
    """Get fall detection module status"""
    return jsonify({
        'module': 'Fall Detection',
        'status': 'active',
        'version': '1.0.0'
    }), 200