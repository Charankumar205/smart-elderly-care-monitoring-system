"""
Flask application factory for Smart Elderly Care Monitoring System
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app(config_class=None):
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import main_bp, fall_detection_bp, nlp_bp, risk_prediction_bp, monitoring_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(fall_detection_bp)
    app.register_blueprint(nlp_bp)
    app.register_blueprint(risk_prediction_bp)
    app.register_blueprint(monitoring_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
