"""
Main entry point for the Smart Elderly Care Monitoring System
"""
from app import create_app
from config.settings import DevelopmentConfig

if __name__ == '__main__':
    app = create_app(DevelopmentConfig)
    app.run(debug=True, host='0.0.0.0', port=5000)
