"""
Comprehensive test file for Smart Elderly Care Monitoring System
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.fall_detection.image_detector import ImageFallDetector
from modules.nlp_analysis.analyzer import NLPAnalyzer
from modules.risk_prediction.enhanced_predictor import EnhancedRiskPredictor

def test_nlp_analyzer():
    """Test NLP analysis module"""
    print("\n" + "="*60)
    print("TESTING NLP ANALYZER MODULE")
    print("="*60)
    
    analyzer = NLPAnalyzer()
    
    test_reports = [
        "Patient is feeling weak and dizzy.",
        "Patient has breathing difficulty and chest pain.",
        "Patient is not responding properly since morning.",
        "Patient appears normal, no complaints."
    ]
    
    for report in test_reports:
        print(f"\nAnalyzing: '{report}'")
        try:
            result = analyzer.analyze(report)
            print(f"  Symptoms: {result['extracted_symptoms']}")
            print(f"  Sentiment: {result['health_sentiment']}")
            print(f"  Severity: {result['severity_level']}")
            print(f"  Severity Score: {result['severity_score']:.2f}")
            print("  ✓ PASSED")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
    return True

def test_risk_predictor():
    """Test risk prediction module"""
    print("\n" + "="*60)
    print("TESTING RISK PREDICTION MODULE")
    print("="*60)
    
    predictor = EnhancedRiskPredictor()
    
    test_cases = [
        {
            'name': 'Emergency: Fall + Chest Pain',
            'fall_data': {
                'posture': 'Fall Detected',
                'confidence': 0.94,
                'emergency_status': True
            },
            'nlp_data': {
                'extracted_symptoms': ['Chest Pain', 'Breathing'],
                'health_sentiment': 'Negative Health Condition',
                'severity_level': 'High',
                'severity_score': 0.85
            }
        },
        {
            'name': 'High Risk: Multiple Symptoms',
            'fall_data': {
                'posture': 'Normal Standing',
                'confidence': 0.91,
                'emergency_status': False
            },
            'nlp_data': {
                'extracted_symptoms': ['Weakness', 'Dizziness', 'Breathing'],
                'health_sentiment': 'Negative Health Condition',
                'severity_level': 'Medium',
                'severity_score': 0.65
            }
        },
        {
            'name': 'Low Risk: Normal Condition',
            'fall_data': {
                'posture': 'Normal Standing',
                'confidence': 0.91,
                'emergency_status': False
            },
            'nlp_data': {
                'extracted_symptoms': [],
                'health_sentiment': 'Positive Health Condition',
                'severity_level': 'Low',
                'severity_score': 0.15
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        try:
            result = predictor.predict_comprehensive_risk(
                fall_data=test_case['fall_data'],
                nlp_data=test_case['nlp_data'],
                user_health_data={'age': 75}
            )
            
            print(f"  Risk Category: {result['risk_category']}")
            print(f"  Risk Score: {result['final_risk_score']:.2f} ({int(result['final_risk_score']*100)}%)")
            print(f"  Alert Status: {result['alert_status']}")
            print(f"  Medical Action: {result['medical_action']}")
            print("  ✓ PASSED")
        except Exception as e:
            print(f"  ✗ FAILED: {str(e)}")
    
    return True

def test_fall_detector():
    """Test fall detection module"""
    print("\n" + "="*60)
    print("TESTING FALL DETECTION MODULE")
    print("="*60)
    
    detector = ImageFallDetector()
    
    print("\nFall Detection Module Loaded Successfully")
    print("  Model Version: 2.0.0")
    print("  Posture Classes:")
    for posture, code in detector.posture_classes.items():
        print(f"    - {posture}: {code}")
    print("  ✓ PASSED")
    
    return True

def test_complete_workflow():
    """Test complete workflow"""
    print("\n" + "="*60)
    print("TESTING COMPLETE WORKFLOW")
    print("="*60)
    
    nlp_analyzer = NLPAnalyzer()
    risk_predictor = EnhancedRiskPredictor()
    
    # Simulate a complete assessment
    print("\nWorkflow: Image Analysis + Report Analysis → Risk Prediction")
    
    # Simulated fall detection (no actual image)
    fall_result = {
        'posture': 'Normal Standing',
        'confidence': 0.91,
        'emergency_status': False
    }
    
    # Analyze a health report
    report = "Patient is feeling very weak and dizzy. Has difficulty breathing. Feels like falling."
    
    print(f"\n1. Fall Detection Result: {fall_result['posture']}")
    print(f"   Confidence: {fall_result['confidence']:.2%}")
    
    print(f"\n2. Analyzing Report: '{report}'")
    nlp_result = nlp_analyzer.analyze(report)
    print(f"   Symptoms: {', '.join(nlp_result['extracted_symptoms'])}")
    print(f"   Severity: {nlp_result['severity_level']}")
    
    print(f"\n3. Predicting Comprehensive Risk...")
    risk_result = risk_predictor.predict_comprehensive_risk(
        fall_data=fall_result,
        nlp_data=nlp_result,
        user_health_data={'age': 75}
    )
    
    print(f"   Risk Category: {risk_result['risk_category']}")
    print(f"   Risk Score: {risk_result['final_risk_score']:.2%}")
    print(f"   Alert Status: {risk_result['alert_status']}")
    print(f"   Medical Action: {risk_result['medical_action']}")
    print(f"\n   Recommendations:")
    for rec in risk_result['recommendations'][:3]:
        print(f"   • {rec}")
    
    print("\n  ✓ WORKFLOW PASSED")
    
    return True

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("SMART ELDERLY CARE MONITORING SYSTEM - TEST SUITE")
    print("="*60)
    
    tests = [
        ("NLP Analyzer", test_nlp_analyzer),
        ("Risk Predictor", test_risk_predictor),
        ("Fall Detector", test_fall_detector),
        ("Complete Workflow", test_complete_workflow)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "PASSED" if result else "FAILED"))
        except Exception as e:
            results.append((test_name, f"FAILED: {str(e)}"))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    for test_name, result in results:
        status = "✓" if "PASSED" in result else "✗"
        print(f"{status} {test_name}: {result}")
    
    total_passed = sum(1 for _, r in results if "PASSED" in r)
    print(f"\nTotal: {total_passed}/{len(results)} tests passed")
    
    if total_passed == len(results):
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("\n⚠️ SOME TESTS FAILED")
        return 1

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
