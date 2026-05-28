"""
Main routes for the application
"""
from flask import jsonify, render_template
from . import main_bp

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Smart Elderly Care Monitoring System'
    }), 200
