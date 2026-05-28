"""
Blueprint modules for the application routes
"""
from flask import Blueprint

main_bp = Blueprint('main', __name__)
fall_detection_bp = Blueprint('fall_detection', __name__, url_prefix='/api/fall-detection')
nlp_bp = Blueprint('nlp', __name__, url_prefix='/api/nlp')
risk_prediction_bp = Blueprint('risk_prediction', __name__, url_prefix='/api/risk-prediction')
monitoring_bp = Blueprint('monitoring', __name__, url_prefix='/monitoring')

from app.routes import main, fall_detection, nlp_analysis, risk_prediction, monitoring
