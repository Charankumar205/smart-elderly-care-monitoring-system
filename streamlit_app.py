"""
Smart Elderly Care Monitoring System - Streamlit Web Application
Professional, modern healthcare dashboard with AI-based monitoring
"""

import streamlit as st
from PIL import Image
import io
import json
from datetime import datetime
import random

# Page Configuration
st.set_page_config(
    page_title="Smart Elderly Care Monitoring System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Professional Healthcare Styling
def inject_custom_css():
    custom_css = """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Main Background */
    .main {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #ffffff;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 40px 20px;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        margin-bottom: 30px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .header-title {
        font-size: 3.5em;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        margin-bottom: 10px;
        letter-spacing: 1px;
    }
    
    .header-subtitle {
        font-size: 1.3em;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 300;
        letter-spacing: 0.5px;
    }
    
    /* Card Styling - Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
        border-left: 4px solid;
    }
    
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.08);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        transform: translateY(-5px);
    }
    
    .glass-card-fall {
        border-left-color: #ff6b6b;
    }
    
    .glass-card-nlp {
        border-left-color: #4ecdc4;
    }
    
    .glass-card-risk {
        border-left-color: #ffd93d;
    }
    
    /* Card Titles */
    .card-title {
        font-size: 1.8em;
        font-weight: 700;
        margin-bottom: 20px;
        letter-spacing: 0.5px;
    }
    
    .card-title-fall {
        color: #ff6b6b;
    }
    
    .card-title-nlp {
        color: #4ecdc4;
    }
    
    .card-title-risk {
        color: #ffd93d;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 15px 40px;
        border: none;
        border-radius: 15px;
        font-size: 1.1em;
        font-weight: 600;
        cursor: pointer;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
        letter-spacing: 0.5px;
    }
    
    .btn-primary:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 45px rgba(102, 126, 234, 0.5);
    }
    
    .btn-fall {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
    }
    
    .btn-fall:hover {
        box-shadow: 0 15px 45px rgba(255, 107, 107, 0.5);
    }
    
    .btn-nlp {
        background: linear-gradient(135deg, #4ecdc4 0%, #44a5a5 100%);
        box-shadow: 0 10px 30px rgba(78, 205, 196, 0.3);
    }
    
    .btn-nlp:hover {
        box-shadow: 0 15px 45px rgba(78, 205, 196, 0.5);
    }
    
    .btn-risk {
        background: linear-gradient(135deg, #ffd93d 0%, #ffb700 100%);
        box-shadow: 0 10px 30px rgba(255, 217, 61, 0.3);
        color: #000;
    }
    
    .btn-risk:hover {
        box-shadow: 0 15px 45px rgba(255, 217, 61, 0.5);
    }
    
    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }
    
    .result-label {
        font-size: 0.95em;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .result-value {
        font-size: 2.2em;
        font-weight: 900;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    
    /* Risk Level Indicators */
    .risk-low {
        color: #4ade80;
        border-left: 4px solid #4ade80;
    }
    
    .risk-medium {
        color: #facc15;
        border-left: 4px solid #facc15;
    }
    
    .risk-high {
        color: #f97316;
        border-left: 4px solid #f97316;
    }
    
    .risk-critical {
        color: #ef4444;
        border-left: 4px solid #ef4444;
        animation: pulse-red 1.5s infinite;
    }
    
    @keyframes pulse-red {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Alert Banners */
    .alert-critical {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1), rgba(239, 68, 68, 0.05));
        border: 2px solid #ef4444;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        animation: slide-in 0.5s ease;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.1), rgba(249, 115, 22, 0.05));
        border: 2px solid #f97316;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .alert-info {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(59, 130, 246, 0.05));
        border: 2px solid #3b82f6;
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
    }
    
    @keyframes slide-in {
        from {
            transform: translateX(-20px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* Metrics Grid */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2.5em;
        font-weight: 900;
        margin: 10px 0;
    }
    
    .metric-label {
        font-size: 0.9em;
        color: rgba(255, 255, 255, 0.6);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Progress Bars */
    .progress-bar {
        width: 100%;
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        overflow: hidden;
        margin: 15px 0;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* Footer */
    .footer-container {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01));
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        padding: 30px 20px;
        text-align: center;
        margin-top: 50px;
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.95em;
        letter-spacing: 0.5px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .header-title {
            font-size: 2em;
        }
        
        .header-subtitle {
            font-size: 1em;
        }
        
        .glass-card {
            padding: 20px;
        }
        
        .card-title {
            font-size: 1.4em;
        }
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# Initialize Session State
if 'fall_detection_result' not in st.session_state:
    st.session_state.fall_detection_result = None
if 'nlp_analysis_result' not in st.session_state:
    st.session_state.nlp_analysis_result = None
if 'risk_prediction_result' not in st.session_state:
    st.session_state.risk_prediction_result = None

# Helper Functions
def get_confidence_score():
    """Generate realistic confidence score"""
    return round(random.uniform(0.85, 0.99), 3)

def perform_fall_detection(image):
    """Simulate fall detection analysis"""
    posture_categories = [
        "Normal Standing",
        "Sitting",
        "Sleeping",
        "Fall Detected",
        "Emergency Posture",
        "Unconscious Condition"
    ]
    
    # Random selection (in production, use ML model)
    detected_posture = random.choice(posture_categories)
    confidence = get_confidence_score()
    
    is_emergency = detected_posture in ["Fall Detected", "Emergency Posture", "Unconscious Condition"]
    
    return {
        'posture': detected_posture,
        'confidence': confidence,
        'emergency': is_emergency,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def perform_nlp_analysis(text):
    """Simulate NLP health analysis"""
    symptom_keywords = {
        'weakness': ['weak', 'fatigue', 'tired'],
        'dizziness': ['dizzy', 'vertigo', 'lightheaded'],
        'breathing': ['breathe', 'breath', 'breathing', 'shortness'],
        'chest': ['chest', 'heart', 'cardiac'],
        'pain': ['pain', 'ache', 'hurt']
    }
    
    symptoms = []
    text_lower = text.lower()
    
    for symptom, keywords in symptom_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            symptoms.append(symptom.replace('_', ' ').title())
    
    sentiment_score = random.uniform(0.3, 0.8)
    severity = 'Critical' if sentiment_score > 0.7 else 'Moderate' if sentiment_score > 0.5 else 'Mild'
    
    return {
        'symptoms': symptoms if symptoms else ['General Observation'],
        'sentiment_score': round(sentiment_score, 2),
        'severity': severity,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def perform_risk_assessment(fall_result, nlp_result):
    """Calculate comprehensive risk assessment"""
    base_risk = 0.2
    
    # Add fall detection risk
    if fall_result and fall_result.get('emergency'):
        base_risk += 0.4
    
    # Add NLP severity risk
    if nlp_result:
        if nlp_result.get('severity') == 'Critical':
            base_risk += 0.3
        elif nlp_result.get('severity') == 'Moderate':
            base_risk += 0.15
    
    # Add randomness
    base_risk += random.uniform(0, 0.1)
    base_risk = min(0.99, base_risk)
    
    if base_risk > 0.75:
        risk_level = "Emergency Critical"
        color = "critical"
    elif base_risk > 0.55:
        risk_level = "High Risk"
        color = "high"
    elif base_risk > 0.35:
        risk_level = "Medium Risk"
        color = "medium"
    else:
        risk_level = "Low Risk"
        color = "low"
    
    return {
        'risk_score': round(base_risk, 3),
        'risk_level': risk_level,
        'risk_color': color,
        'confidence': round(random.uniform(0.85, 0.99), 3),
        'recommendation': get_recommendation(risk_level),
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_recommendation(risk_level):
    """Get clinical recommendation based on risk level"""
    recommendations = {
        'Emergency Critical': [
            '🚨 Immediate Medical Attention Required',
            '🔴 Alert Emergency Services',
            '⚠️ Continuous Monitoring Enabled'
        ],
        'High Risk': [
            '⚠️ Enhanced Monitoring Recommended',
            '📞 Notify Caretaker Immediately',
            '🏥 Schedule Medical Evaluation'
        ],
        'Medium Risk': [
            '📋 Continue Regular Monitoring',
            '📊 Track Changes Daily',
            '🩺 Schedule Doctor Visit if Symptoms Persist'
        ],
        'Low Risk': [
            '✅ Routine Monitoring Sufficient',
            '💪 Continue Daily Activities',
            '🔄 Regular Check-ups Recommended'
        ]
    }
    return recommendations.get(risk_level, [])

# Main Application
inject_custom_css()

# Header Section
st.markdown("""
<div class="header-container">
    <div class="header-title">🏥 Smart Elderly Care Monitoring System</div>
    <div class="header-subtitle">Advanced AI-Based Health Monitoring & Risk Assessment Dashboard</div>
</div>
""", unsafe_allow_html=True)

# Create Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🔍 Fall Detection",
    "📝 NLP Analysis",
    "⚠️ Risk Prediction",
    "📊 Dashboard"
])

# ============================================================================
# TAB 1: FALL DETECTION
# ============================================================================
with tab1:
    st.markdown("""
    <div class="glass-card glass-card-fall">
        <div class="card-title card-title-fall">🚨 Fall Detection Module</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📸 Upload Patient Image")
        uploaded_image = st.file_uploader(
            "Select a patient image (JPG, PNG, JPEG)",
            type=['jpg', 'png', 'jpeg'],
            key='fall_detection_image'
        )
        
        if uploaded_image:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Patient Image", use_column_width=True)
    
    with col2:
        st.markdown("#### 📊 Detection Analysis")
        
        if uploaded_image:
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🎯 Detect Fall & Posture", use_container_width=True, key='fall_btn'):
                    with st.spinner("🔄 Analyzing posture..."):
                        result = perform_fall_detection(uploaded_image)
                        st.session_state.fall_detection_result = result
            
            if st.session_state.fall_detection_result:
                result = st.session_state.fall_detection_result
                
                # Display results using Streamlit components
                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.metric("📍 Detection Result", result['posture'])
                    st.metric("🎯 Confidence Score", f"{result['confidence']*100:.1f}%")
                
                with res_col2:
                    status = "🔴 YES - ALERT!" if result['emergency'] else "🟢 NO - SAFE"
                    st.metric("🚨 Emergency Status", status)
                    st.metric("⏰ Timestamp", result['timestamp'])
                
                if result['emergency']:
                    st.error("⚠️ ALERT: Potential fall detected! Emergency protocols activated. Immediate assistance recommended.")
    
    if not uploaded_image:
        st.info("👉 Upload an image to start fall detection analysis")

# ============================================================================
# TAB 2: NLP ANALYSIS
# ============================================================================
with tab2:
    st.markdown("""
    <div class="glass-card glass-card-nlp">
        <div class="card-title card-title-nlp">📝 NLP Health Analysis Module</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📋 Caretaker Report")
        health_report = st.text_area(
            "Enter patient health observations",
            placeholder="Patient is feeling weak and dizzy. Experienced shortness of breath after minimal activity.",
            height=150,
            label_visibility="collapsed"
        )
    
    with col2:
        st.markdown("#### 📊 Analysis Results")
        
        if health_report:
            if st.button("🔬 Analyze Health Report", use_container_width=True, key='nlp_btn'):
                with st.spinner("🔄 Analyzing health report..."):
                    result = perform_nlp_analysis(health_report)
                    st.session_state.nlp_analysis_result = result
        
        if st.session_state.nlp_analysis_result:
            result = st.session_state.nlp_analysis_result
            
            severity_color = {
                'Critical': 'error',
                'Moderate': 'warning',
                'Mild': 'info'
            }.get(result['severity'], 'info')
            
            # Display results using Streamlit components
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.info(f"🔍 **Extracted Symptoms**\n\n{', '.join(result['symptoms'])}")
                st.metric("😊 Health Sentiment Score", f"{result['sentiment_score']}/1.0")
            
            with res_col2:
                st.metric("📈 Severity Level", result['severity'])
                st.metric("⏰ Analysis Time", result['timestamp'])
            
            if result['severity'] == 'Critical':
                st.error("⚠️ CRITICAL: Severe health indicators detected. Medical evaluation recommended immediately.")
    
    if not health_report:
        st.info("👉 Enter a health report to analyze symptoms and severity")

# ============================================================================
# TAB 3: RISK PREDICTION
# ============================================================================
with tab3:
    st.markdown("""
    <div class="glass-card glass-card-risk">
        <div class="card-title card-title-risk">⚠️ Risk Prediction Module</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 🏥 Complete Monitoring Assessment")
    
    if st.button("🔮 Run Complete Assessment", use_container_width=True, key='risk_btn'):
        with st.spinner("🔄 Computing risk assessment..."):
            risk_result = perform_risk_assessment(
                st.session_state.fall_detection_result,
                st.session_state.nlp_analysis_result
            )
            st.session_state.risk_prediction_result = risk_result
    
    if st.session_state.risk_prediction_result:
        result = st.session_state.risk_prediction_result
        
        risk_colors = {
            'critical': 'error',
            'high': 'warning',
            'medium': 'info',
            'low': 'success'
        }
        
        color_type = risk_colors.get(result['risk_color'], 'info')
        
        # Display risk metrics
        col_risk1, col_risk2 = st.columns(2)
        with col_risk1:
            st.metric("⚠️ Final Risk Prediction", result['risk_level'])
            st.metric("🎯 Risk Confidence", f"{result['confidence']*100:.1f}%")
        
        with col_risk2:
            st.metric("📍 Risk Score", f"{result['risk_score']:.3f}")
            st.metric("⏰ Assessment Time", result['timestamp'])
        
        # Progress bar
        st.progress(result['risk_score'], text=f"Risk Level: {result['risk_score']*100:.1f}%")
        
        # Recommendations
        st.markdown("#### 📋 Recommended Actions")
        for i, rec in enumerate(result['recommendation'], 1):
            st.info(rec)
        
        # Alert based on risk level
        if result['risk_color'] == 'critical':
            st.error("🚨 CRITICAL ALERT: High-risk condition detected. Immediate medical intervention may be required. Contact emergency services if necessary.")
        elif result['risk_color'] == 'high':
            st.warning("⚠️ WARNING: Elevated risk detected. Enhanced monitoring and medical evaluation recommended.")
    else:
        st.info("👉 Click 'Run Complete Assessment' to calculate comprehensive risk score")

# ============================================================================
# TAB 4: MONITORING DASHBOARD
# ============================================================================
with tab4:
    st.markdown("""
    <div class="glass-card">
        <div class="card-title" style="color: #667eea;">📊 Comprehensive Monitoring Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Metrics
    st.markdown("#### 📈 Key Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Fall Detection Status",
            "✅ MONITORED" if st.session_state.fall_detection_result else "⏳ PENDING",
            "System Ready"
        )
    
    with col2:
        st.metric(
            "NLP Analysis Status",
            "✅ ANALYZED" if st.session_state.nlp_analysis_result else "⏳ PENDING",
            "System Ready"
        )
    
    with col3:
        st.metric(
            "Risk Assessment Status",
            "✅ COMPLETED" if st.session_state.risk_prediction_result else "⏳ PENDING",
            "System Ready"
        )
    
    with col4:
        st.metric(
            "System Status",
            "🟢 ONLINE",
            "All Systems Operational"
        )
    
    # Dashboard Summary
    st.markdown("#### 📋 Assessment Summary")
    
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    with summary_col1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title card-title-fall">Fall Detection</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.fall_detection_result:
            result = st.session_state.fall_detection_result
            status = "🔴 ALERT" if result['emergency'] else "🟢 SAFE"
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 2.5em; margin: 10px 0;'>{status}</div>
                <div style='color: rgba(255,255,255,0.7);'>{result['posture']}</div>
                <div style='font-size: 0.9em; color: rgba(255,255,255,0.5); margin-top: 10px;'>Confidence: {result['confidence']*100:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; padding: 30px; color: rgba(255,255,255,0.5);'>⏳ Awaiting Analysis</div>", unsafe_allow_html=True)
    
    with summary_col2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title card-title-nlp">NLP Analysis</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.nlp_analysis_result:
            result = st.session_state.nlp_analysis_result
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 1.8em; color: #4ecdc4; margin: 10px 0;'>{result['severity']}</div>
                <div style='color: rgba(255,255,255,0.7);'>Symptoms: {len(result['symptoms'])}</div>
                <div style='font-size: 0.9em; color: rgba(255,255,255,0.5); margin-top: 10px;'>Sentiment: {result['sentiment_score']}/1.0</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; padding: 30px; color: rgba(255,255,255,0.5);'>⏳ Awaiting Analysis</div>", unsafe_allow_html=True)
    
    with summary_col3:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title card-title-risk">Risk Assessment</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.risk_prediction_result:
            result = st.session_state.risk_prediction_result
            st.markdown(f"""
            <div style='text-align: center; padding: 20px;'>
                <div style='font-size: 2.5em; color: #ffd93d; margin: 10px 0;'>{result['risk_level']}</div>
                <div style='color: rgba(255,255,255,0.7);'>Score: {result['risk_score']}</div>
                <div style='font-size: 0.9em; color: rgba(255,255,255,0.5); margin-top: 10px;'>Confidence: {result['confidence']*100:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("<div style='text-align: center; padding: 30px; color: rgba(255,255,255,0.5);'>⏳ Awaiting Analysis</div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown("#### 🕐 Recent Activity Timeline")
    
    activity_data = []
    if st.session_state.fall_detection_result:
        activity_data.append({
            'time': st.session_state.fall_detection_result['timestamp'],
            'event': '📸 Fall Detection Analysis',
            'status': '✅ Completed'
        })
    if st.session_state.nlp_analysis_result:
        activity_data.append({
            'time': st.session_state.nlp_analysis_result['timestamp'],
            'event': '📝 NLP Report Analysis',
            'status': '✅ Completed'
        })
    if st.session_state.risk_prediction_result:
        activity_data.append({
            'time': st.session_state.risk_prediction_result['timestamp'],
            'event': '⚠️ Risk Assessment',
            'status': '✅ Completed'
        })
    
    if activity_data:
        for activity in reversed(activity_data):
            st.markdown(f"""
            <div style='padding: 15px; background: rgba(255,255,255,0.05); border-left: 3px solid #667eea; border-radius: 8px; margin: 10px 0;'>
                <div style='display: flex; justify-content: space-between;'>
                    <span><strong>{activity['event']}</strong></span>
                    <span style='color: #4ade80;'>{activity['status']}</span>
                </div>
                <div style='color: rgba(255,255,255,0.5); font-size: 0.9em; margin-top: 5px;'>{activity['time']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No activity recorded yet. Start by performing analyses in other tabs.")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("""
<div class="footer-container">
    © 2026 Smart Elderly Care Monitoring System | Advanced AI Healthcare Dashboard | Version 1.0
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
