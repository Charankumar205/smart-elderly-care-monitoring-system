import io

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from modules.fall_detection.image_detector import ImageFallDetector
from modules.nlp_analysis.analyzer import NLPAnalyzer
from modules.risk_prediction.enhanced_predictor import EnhancedRiskPredictor

st.set_page_config(page_title='Smart Elderly Care Monitoring', layout='wide')

# Initialize modules
fall_detector = ImageFallDetector()
nlp_analyzer = NLPAnalyzer()
risk_predictor = EnhancedRiskPredictor()

RISK_COLOR = {
    'Emergency Critical': '#ff4d4d',
    'High Risk': '#ff9900',
    'Medium Risk': '#ffcc00',
    'Low Risk': '#2ecc71'
}

STATUS_LABEL = {
    'Emergency Critical': '🔴 EMERGENCY CRITICAL',
    'High Risk': '🟠 HIGH RISK',
    'Medium Risk': '🟡 MEDIUM RISK',
    'Low Risk': '🟢 LOW RISK'
}


def format_percentage(value: float) -> str:
    return f"{int(value * 100)}%"


def render_metric_card(title: str, value: str, delta: str = None):
    if delta:
        st.metric(title, value, delta)
    else:
        st.metric(title, value)


def render_alert_banner(risk_category: str):
    color = RISK_COLOR.get(risk_category, '#ffcc00')
    st.markdown(
        f"<div style='padding: 18px; border-radius: 12px; background: {color}; color: white;'>"
        f"<strong>{STATUS_LABEL.get(risk_category, '⚠️ Risk')}</strong> - {risk_category}</div>",
        unsafe_allow_html=True
    )


def show_symptom_list(symptoms):
    if not symptoms:
        st.write("No symptoms detected.")
        return
    for symptom in symptoms:
        st.write(f"- {symptom}")


st.title("Smart Elderly Care Monitoring System")
st.markdown(
    "This dashboard performs sequential image-based fall detection, caretaker report NLP analysis, and final risk prediction."
)

st.markdown("---")

step1_col, step2_col = st.columns([1, 1])

with step1_col:
    st.header("STEP 1: Upload Patient Image")
    uploaded_file = st.file_uploader("Upload elderly patient image", type=["png", "jpg", "jpeg"])
    image_data = None
    if uploaded_file:
        image_data = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_data))
        st.image(image, caption="Uploaded patient image", use_column_width=True)

    if uploaded_file and st.button("Detect Posture & Fall", key="detect_fall"):
        with st.spinner("Analyzing image for posture and fall detection..."):
            fall_result = fall_detector.analyze_image(image_bytes=image_data)
            st.session_state['fall_result'] = fall_result

    fall_result = st.session_state.get('fall_result')
    if fall_result is not None:
        st.subheader("Fall Detection Result")
        if fall_result.get('error'):
            st.error(fall_result['error'])
        else:
            st.write(f"**Posture:** {fall_result['posture']}")
            st.write(f"**Emergency status:** {'Yes' if fall_result['emergency_status'] else 'No'}")
            st.write(f"**Confidence score:** {format_percentage(fall_result.get('confidence', 0.0))}")
            st.write(f"**Body angle:** {fall_result.get('body_angle', 'N/A')}")
            st.write(f"**Height ratio:** {fall_result.get('height_ratio', 'N/A')}")

with step2_col:
    st.header("STEP 2: Caretaker Report")
    report_text = st.text_area(
        "Enter a short health report from the caretaker",
        placeholder="e.g. Patient is feeling weak and dizzy and is not responding properly.",
        height=240,
    )

    if st.button("Analyze Caretaker Report", key="analyze_report"):
        if not report_text.strip():
            st.warning("Please enter the caretaker report before analysis.")
        else:
            nlp_result = nlp_analyzer.analyze(report_text)
            st.session_state['nlp_result'] = nlp_result

    nlp_result = st.session_state.get('nlp_result')
    if nlp_result is not None:
        st.subheader("NLP Health Analysis")
        st.write("**Extracted Symptoms:**")
        show_symptom_list(nlp_result.get('extracted_symptoms', []))
        st.write(f"**Health Sentiment:** {nlp_result.get('health_sentiment')}")
        st.write(f"**Severity Level:** {nlp_result.get('severity_level')} ({format_percentage(nlp_result.get('severity_score', 0.0))})")
        if nlp_result.get('risk_factors'):
            st.write("**Risk Factors:**")
            show_symptom_list(nlp_result.get('risk_factors'))

st.markdown("---")

st.header("STEP 3: Final Risk Prediction")

if st.button("Run Complete Monitoring Assessment", key="run_assessment"):
    if 'fall_result' not in st.session_state:
        st.warning("Please complete Step 1 (image upload and fall detection) before running the assessment.")
    elif 'nlp_result' not in st.session_state:
        st.warning("Please complete Step 2 (caretaker report analysis) before running the assessment.")
    else:
        with st.spinner("Combining image and report data for risk prediction..."):
            risk_result = risk_predictor.predict_comprehensive_risk(
                fall_data=st.session_state['fall_result'],
                nlp_data=st.session_state['nlp_result'],
                user_health_data={}
            )
            st.session_state['risk_result'] = risk_result

risk_result = st.session_state.get('risk_result')

if risk_result is not None:
    st.subheader("Monitoring Dashboard")
    render_alert_banner(risk_result['risk_category'])
    card_col1, card_col2, card_col3 = st.columns(3)
    with card_col1:
        render_metric_card("Patient Posture", st.session_state['fall_result']['posture'])
        render_metric_card("Emergency Status", 'Yes' if st.session_state['fall_result']['emergency_status'] else 'No')
    with card_col2:
        render_metric_card("Health Sentiment", st.session_state['nlp_result']['health_sentiment'])
        render_metric_card("Severity Level", st.session_state['nlp_result']['severity_level'])
    with card_col3:
        render_metric_card("Risk Category", risk_result['risk_category'])
        render_metric_card("Risk Confidence", format_percentage(risk_result['confidence']))

    st.markdown("### Visual Risk Summary")
    st.write(f"**Final Risk Score:** {format_percentage(risk_result['final_risk_score'])}")
    st.progress(int(risk_result['final_risk_score'] * 100))

    st.markdown("### Recommended Action")
    for action in risk_result['recommendations']:
        st.write(f"- {action}")

    st.markdown("### Full Monitoring Report")
    st.markdown("---")
    st.write(f"**Fall Detection:** {st.session_state['fall_result']['posture']}")
    st.write(f"**Confidence Score:** {format_percentage(st.session_state['fall_result'].get('confidence', 0.0))}")
    st.write("**NLP Extracted Symptoms:**")
    show_symptom_list(st.session_state['nlp_result'].get('extracted_symptoms', []))
    st.write(f"**Health Sentiment:** {st.session_state['nlp_result']['health_sentiment']}")
    st.write(f"**Severity Level:** {st.session_state['nlp_result']['severity_level']}")
    st.write(f"**Final Risk Prediction:** {risk_result['risk_category']}")
    st.write(f"**Recommended Action:** {risk_result['medical_action']}")
    st.write(f"**Dashboard Status:** {risk_result['alert_status']}")
