/**
 * Main JavaScript file for Smart Elderly Care Monitoring System
 */

// Check API health on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('Smart Elderly Care System loaded');
    checkApiHealth();
});

/**
 * Check the health of the API
 */
async function checkApiHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API Health:', data);
    } catch (error) {
        console.error('Error checking API health:', error);
    }
}

/**
 * Send fall detection request
 */
async function detectFall(sensorData) {
    try {
        const response = await fetch('/api/fall-detection/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(sensorData)
        });
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error in fall detection:', error);
        throw error;
    }
}

/**
 * Send NLP analysis request
 */
async function analyzeText(text, userId) {
    try {
        const response = await fetch('/api/nlp/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: text,
                user_id: userId
            })
        });
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error in NLP analysis:', error);
        throw error;
    }
}

/**
 * Send risk prediction request
 */
async function predictRisk(userData) {
    try {
        const response = await fetch('/api/risk-prediction/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error in risk prediction:', error);
        throw error;
    }
}
