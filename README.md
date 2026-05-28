# Smart Elderly Care Monitoring System

A comprehensive Flask-based system for monitoring elderly health with integrated modules for fall detection, NLP analysis, and risk prediction.

## Features

- **Fall Detection Module**: Detects potential falls using accelerometer and gyroscope sensor data
- **NLP Analysis Module**: Analyzes health-related text for sentiment, symptoms, and concerns
- **Risk Prediction Module**: Predicts health risks based on multiple user factors

## Project Structure

```
smart_elderly_care_system/
├── app/
│   ├── routes/              # API route handlers
│   ├── models/              # Database models
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── modules/
│   ├── fall_detection/      # Fall detection module
│   ├── nlp_analysis/        # NLP analysis module
│   └── risk_prediction/     # Risk prediction module
├── config/                  # Configuration settings
├── utils/                   # Utility functions
├── tests/                   # Test files
├── logs/                    # Application logs
├── data/                    # Data storage
└── docs/                    # Documentation
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd smart_elderly_care_system
```

2. Create a virtual environment:
```bash
python -m venv venv
# macOS / Linux
source venv/bin/activate
# Windows PowerShell
.\venv\Scripts\Activate.ps1
# Windows Command Prompt
venv\Scripts\activate.bat
```

3. Install dependencies:
```bash
python -m pip install -r requirements.txt
```

4. Launch the Streamlit frontend (required):
```bash
python -m pip install streamlit
python -m streamlit run streamlit_app.py
```

5. (Optional) Run the Flask application:
```bash
python run.py
```

6. Open the dashboard in your web browser. Do not paste the URL directly into PowerShell as a command.

- For the Flask app, use:
```powershell
start http://localhost:5000/monitoring/
```
- For the Streamlit app, use:
```powershell
start http://localhost:8501
```
- Or open your browser and navigate to the appropriate URL manually.

```
http://localhost:5000/monitoring/  # Flask
http://localhost:8501/             # Streamlit
```

If the application is running, the monitoring dashboard will load at the above URL.

## API Endpoints

### Fall Detection
- `POST /api/fall-detection/detect` - Detect fall from sensor data
- `GET /api/fall-detection/status` - Get module status

### NLP Analysis
- `POST /api/nlp/analyze` - Analyze text
- `POST /api/nlp/sentiment` - Analyze sentiment
- `GET /api/nlp/status` - Get module status

### Risk Prediction
- `POST /api/risk-prediction/predict` - Predict risk
- `GET /api/risk-prediction/factors/<user_id>` - Get risk factors
- `GET /api/risk-prediction/status` - Get module status

### Health Check
- `GET /api/health` - API health check

## Configuration

Configuration can be set in `config/settings.py`. Three environments are supported:
- **Development**: Debug enabled, SQLite database
- **Testing**: Testing mode enabled, in-memory database
- **Production**: Debug disabled, uses DATABASE_URL environment variable

## Testing

Run tests from the project root:
```bash
pytest tests/
```

## Documentation

See the `docs/` folder for detailed documentation on each module.

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions, please open an issue on the project repository.
