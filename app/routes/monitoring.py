"""
Monitoring endpoints for Smart Elderly Care System
Handles the complete workflow: fall detection, NLP analysis, and risk prediction
"""
from flask import request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from . import monitoring_bp
from modules.fall_detection.image_detector import ImageFallDetector
from modules.nlp_analysis.analyzer import NLPAnalyzer
from modules.risk_prediction.enhanced_predictor import EnhancedRiskPredictor
from utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize modules
fall_detector = ImageFallDetector()
nlp_analyzer = NLPAnalyzer()
risk_predictor = EnhancedRiskPredictor()

# Configuration
UPLOAD_FOLDER = 'data/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@monitoring_bp.route('/', methods=['GET'])
def dashboard():
    """Main monitoring dashboard"""
    return render_template('monitoring_dashboard.html')

@monitoring_bp.route('/analysis', methods=['GET'])
def analysis_page():
    """Full analysis page with form"""
    return render_template('analysis_form.html')

@monitoring_bp.route('/api/upload-image', methods=['POST'])
def upload_image():
    """
    API endpoint to upload patient image for fall detection
    """
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No image selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Use: png, jpg, jpeg, gif, bmp'}), 400
        
        # Save file
        filename = secure_filename(f"fall_detection_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze image
        fall_result = fall_detector.analyze_image(image_path=filepath)
        
        logger.info(f"Fall detection analysis completed: {fall_result['posture']}")
        
        return jsonify({
            'success': True,
            'fall_detection': fall_result,
            'image_path': filepath,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in image upload: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/api/analyze-report', methods=['POST'])
def analyze_report():
    """
    API endpoint to analyze caretaker health report
    """
    try:
        data = request.get_json()
        
        if not data or 'report' not in data:
            return jsonify({'error': 'Report text is required'}), 400
        
        report_text = data['report'].strip()
        if not report_text:
            return jsonify({'error': 'Report cannot be empty'}), 400
        
        # Analyze report with NLP
        nlp_result = nlp_analyzer.analyze(report_text)
        
        logger.info(f"NLP analysis completed. Symptoms detected: {nlp_result['extracted_symptoms']}")
        
        return jsonify({
            'success': True,
            'nlp_analysis': nlp_result,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in NLP analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/api/complete-assessment', methods=['POST'])
def complete_assessment():
    """
    API endpoint for complete health assessment
    Combines fall detection and NLP analysis for risk prediction
    """
    try:
        data = request.get_json()
        
        # Validate inputs
        if not data or ('fall_detection' not in data and 'report' not in data):
            return jsonify({'error': 'Either fall detection image or health report is required'}), 400
        
        fall_result = data.get('fall_detection', {
            'posture': 'Normal Standing',
            'confidence': 0.0,
            'emergency_status': False
        })
        
        # Analyze report if provided
        nlp_result = {}
        if 'report' in data and data['report'].strip():
            nlp_result = nlp_analyzer.analyze(data['report'])
        else:
            nlp_result = {
                'extracted_symptoms': [],
                'health_sentiment': 'Neutral',
                'severity_level': 'Low',
                'severity_score': 0.0,
                'keywords': []
            }
        
        # Get user health data if provided
        user_health = data.get('user_health', {})
        
        # Perform comprehensive risk prediction
        risk_result = risk_predictor.predict_comprehensive_risk(
            fall_data=fall_result,
            nlp_data=nlp_result,
            user_health_data=user_health
        )
        
        logger.info(f"Complete assessment done. Risk Level: {risk_result['risk_category']}")
        
        return jsonify({
            'success': True,
            'fall_detection': fall_result,
            'nlp_analysis': nlp_result,
            'risk_prediction': risk_result,
            'assessment_timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in complete assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/api/quick-assessment', methods=['POST'])
def quick_assessment():
    """
    Quick assessment endpoint - analyze just the report
    """
    try:
        data = request.get_json()
        
        if not data or 'report' not in data:
            return jsonify({'error': 'Report is required'}), 400
        
        report = data['report'].strip()
        if not report:
            return jsonify({'error': 'Report cannot be empty'}), 400
        
        # Analyze
        nlp_result = nlp_analyzer.analyze(report)
        
        # Quick risk assessment based only on NLP
        risk_result = risk_predictor.predict_comprehensive_risk(
            fall_data={'posture': 'Normal Standing', 'confidence': 0.0, 'emergency_status': False},
            nlp_data=nlp_result,
            user_health_data={}
        )
        
        return jsonify({
            'success': True,
            'nlp_analysis': nlp_result,
            'risk_prediction': risk_result,
            'timestamp': datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Error in quick assessment: {str(e)}")
        return jsonify({'error': str(e)}), 500

@monitoring_bp.route('/api/health-check', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring service"""
    return jsonify({
        'status': 'operational',
        'service': 'Smart Elderly Care Monitoring',
        'modules': {
            'fall_detection': 'v2.0.0',
            'nlp_analysis': 'v2.0.0',
            'risk_prediction': 'v2.0.0'
        },
        'timestamp': datetime.now().isoformat()
    }), 200
