// Smart Elderly Care Monitoring Dashboard - JavaScript

// State management
let currentAssessmentData = {
    fall_detection: null,
    nlp_analysis: null,
    risk_prediction: null
};

let selectedImageFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateSystemTime();
    setInterval(updateSystemTime, 1000);
});

// Setup event listeners
function setupEventListeners() {
    // Navigation tabs
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const tabName = btn.dataset.tab;
            switchTab(tabName);
        });
    });

    // Image upload
    const uploadArea = document.getElementById('upload-area');
    const imageInput = document.getElementById('image-input');

    uploadArea.addEventListener('click', () => imageInput.click());
    uploadArea.addEventListener('dragover', e => {
        e.preventDefault();
        uploadArea.style.borderColor = '#1d4ed8';
        uploadArea.style.background = '#eff6ff';
    });

    uploadArea.addEventListener('dragleave', e => {
        e.preventDefault();
        uploadArea.style.borderColor = '#2563eb';
        uploadArea.style.background = '#f8fafc';
    });

    uploadArea.addEventListener('drop', e => {
        e.preventDefault();
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageSelect(files[0]);
        }
        uploadArea.style.borderColor = '#2563eb';
        uploadArea.style.background = '#f8fafc';
    });

    imageInput.addEventListener('change', e => {
        if (e.target.files.length > 0) {
            handleImageSelect(e.target.files[0]);
        }
    });
}

// Handle image selection
function handleImageSelect(file) {
    if (!file.type.startsWith('image/')) {
        showToast('Please select a valid image file', 'error');
        return;
    }

    if (file.size > 10 * 1024 * 1024) { // 10MB limit
        showToast('Image file is too large (max 10MB)', 'error');
        return;
    }

    selectedImageFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = e => {
        const preview = document.getElementById('image-preview');
        preview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
    };
    reader.readAsDataURL(file);

    showToast('Image selected successfully', 'success');
}

// Analyze image
async function analyzeImage() {
    if (!selectedImageFile) {
        showToast('Please select an image first', 'warning');
        return;
    }

    const formData = new FormData();
    formData.append('image', selectedImageFile);

    try {
        showToast('Analyzing image...', 'info');
        
        const response = await fetch('/monitoring/api/upload-image', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Failed to analyze image');

        const data = await response.json();
        currentAssessmentData.fall_detection = data.fall_detection;

        updateFallDetectionDisplay(data.fall_detection);
        showToast('Fall detection analysis complete', 'success');
        showResultsSection();

    } catch (error) {
        console.error('Error:', error);
        showToast('Error analyzing image: ' + error.message, 'error');
    }
}

// Analyze report
async function analyzeReport() {
    const reportText = document.getElementById('report-input').value.trim();

    if (!reportText) {
        showToast('Please enter a health report', 'warning');
        return;
    }

    try {
        showToast('Analyzing report...', 'info');

        const response = await fetch('/monitoring/api/analyze-report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ report: reportText })
        });

        if (!response.ok) throw new Error('Failed to analyze report');

        const data = await response.json();
        currentAssessmentData.nlp_analysis = data.nlp_analysis;

        updateNLPDisplay(data.nlp_analysis);
        showToast('Report analysis complete', 'success');
        showResultsSection();

    } catch (error) {
        console.error('Error:', error);
        showToast('Error analyzing report: ' + error.message, 'error');
    }
}

// Submit complete assessment
async function submitCompleteAssessment() {
    try {
        const reportText = document.getElementById('report-input').value.trim();

        if (!currentAssessmentData.fall_detection && !reportText) {
            showToast('Please provide either an image or a report', 'warning');
            return;
        }

        showToast('Generating complete assessment...', 'info');

        const response = await fetch('/monitoring/api/complete-assessment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                fall_detection: currentAssessmentData.fall_detection || {},
                report: reportText,
                user_health: {
                    age: parseInt(document.getElementById('setting-age')?.value || 75)
                }
            })
        });

        if (!response.ok) throw new Error('Failed to complete assessment');

        const data = await response.json();
        currentAssessmentData = data;

        updateDashboard(data);
        switchTab('dashboard');
        showToast('Assessment complete and dashboard updated', 'success');

    } catch (error) {
        console.error('Error:', error);
        showToast('Error completing assessment: ' + error.message, 'error');
    }
}

// Update fall detection display
function updateFallDetectionDisplay(fallData) {
    document.getElementById('fall-posture').textContent = fallData.posture || 'Unknown';
    const confidence = Math.round(fallData.confidence * 100);
    document.getElementById('fall-confidence').textContent = confidence + '%';
    document.getElementById('fall-confidence-bar').style.width = confidence + '%';
    document.getElementById('fall-emergency').textContent = fallData.emergency_status ? 'Emergency' : 'Safe';
    document.getElementById('fall-emergency').className = fallData.emergency_status ? 'badge-critical' : 'badge-safe';
}

// Update NLP display
function updateNLPDisplay(nlpData) {
    const symptoms = nlpData.extracted_symptoms || [];
    const symptomsList = document.getElementById('symptoms-list');

    if (symptoms.length > 0) {
        symptomsList.innerHTML = symptoms.map(s => `<span class="badge-info">${s}</span>`).join('');
    } else {
        symptomsList.innerHTML = '<span class="badge-info">No symptoms detected</span>';
    }

    document.getElementById('health-sentiment').textContent = nlpData.health_sentiment || 'Unknown';
    document.getElementById('severity-level').textContent = nlpData.severity_level || 'Low';
    
    // Color code severity
    const severityBadge = document.getElementById('severity-level');
    severityBadge.className = 'badge-' + nlpData.severity_level.toLowerCase();
}

// Update dashboard with complete assessment
function updateDashboard(assessmentData) {
    // Update fall detection
    if (assessmentData.fall_detection) {
        updateFallDetectionDisplay(assessmentData.fall_detection);
    }

    // Update NLP
    if (assessmentData.nlp_analysis) {
        updateNLPDisplay(assessmentData.nlp_analysis);
    }

    // Update risk prediction
    if (assessmentData.risk_prediction) {
        updateRiskDisplay(assessmentData.risk_prediction);
    }

    // Update last assessment time
    document.getElementById('last-assessment').textContent = new Date().toLocaleString();
}

// Update risk display
function updateRiskDisplay(riskData) {
    const riskScore = Math.round(riskData.final_risk_score * 100);
    document.getElementById('risk-score').textContent = riskScore + '%';

    const riskMeter = document.getElementById('risk-meter');
    riskMeter.className = 'risk-meter ' + getRiskColor(riskData.risk_category);

    document.getElementById('risk-category').textContent = riskData.risk_category;
    document.getElementById('risk-category').className = 'badge-' + getRiskBadgeClass(riskData.risk_category);

    document.getElementById('alert-status').textContent = riskData.alert_status;
    document.getElementById('alert-status').className = 'badge-' + getAlertBadgeClass(riskData.alert_status);

    // Update alert panel
    const alertPanel = document.getElementById('alert-panel');
    alertPanel.className = 'alert-panel ' + getAlertPanelClass(riskData.alert_status);
    document.getElementById('alert-message').textContent = riskData.medical_action;

    // Update recommendations
    const recList = document.getElementById('recommendations-list');
    if (riskData.recommendations && riskData.recommendations.length > 0) {
        recList.innerHTML = riskData.recommendations.map(rec => `<li>${rec}</li>`).join('');
    }
}

// Helper functions
function getRiskColor(category) {
    switch(category) {
        case 'Low Risk': return 'green';
        case 'Medium Risk': return 'yellow';
        case 'High Risk': return 'orange';
        case 'Emergency Critical': return 'red';
        default: return 'green';
    }
}

function getRiskBadgeClass(category) {
    switch(category) {
        case 'Low Risk': return 'low';
        case 'Medium Risk': return 'medium';
        case 'High Risk': return 'high';
        case 'Emergency Critical': return 'critical';
        default: return 'low';
    }
}

function getAlertBadgeClass(status) {
    switch(status) {
        case 'GREEN_SAFE': return 'safe';
        case 'YELLOW_ALERT': return 'medium';
        case 'ORANGE_ALERT': return 'high';
        case 'RED_ALERT': return 'critical';
        default: return 'safe';
    }
}

function getAlertPanelClass(status) {
    switch(status) {
        case 'GREEN_SAFE': return 'green-safe';
        case 'YELLOW_ALERT': return 'yellow-alert';
        case 'ORANGE_ALERT': return 'orange-alert';
        case 'RED_ALERT': return 'red-alert';
        default: return 'green-safe';
    }
}

// Tab switching
function switchTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    // Remove active from all buttons
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    const tabElement = document.getElementById(tabName + '-tab');
    if (tabElement) {
        tabElement.classList.add('active');
    }

    // Activate button
    const navBtn = document.querySelector(`[data-tab="${tabName}"]`);
    if (navBtn) {
        navBtn.classList.add('active');
    }
}

// Show results section
function showResultsSection() {
    const resultsSection = document.getElementById('results-section');
    if (resultsSection) {
        resultsSection.style.display = 'block';
    }
}

// Update system time
function updateSystemTime() {
    const now = new Date();
    document.getElementById('system-time').textContent = now.toLocaleTimeString();
}

// Toast notifications
function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; cursor: pointer; color: inherit; font-size: 1.2rem;">×</button>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}

// Download report
function downloadReport() {
    if (!currentAssessmentData.risk_prediction) {
        showToast('No assessment data to download', 'warning');
        return;
    }

    const report = generateReport(currentAssessmentData);
    const element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(report));
    element.setAttribute('download', 'elderly_care_report_' + new Date().getTime() + '.txt');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);

    showToast('Report downloaded', 'success');
}

// Generate report
function generateReport(data) {
    const timestamp = new Date().toLocaleString();
    let report = `SMART ELDERLY CARE MONITORING REPORT\n`;
    report += `Generated: ${timestamp}\n`;
    report += `${'='.repeat(50)}\n\n`;

    if (data.fall_detection) {
        report += `📷 FALL DETECTION:\n`;
        report += `  Posture: ${data.fall_detection.posture}\n`;
        report += `  Confidence: ${Math.round(data.fall_detection.confidence * 100)}%\n`;
        report += `  Emergency Status: ${data.fall_detection.emergency_status ? 'Yes' : 'No'}\n\n`;
    }

    if (data.nlp_analysis) {
        report += `🧠 NLP ANALYSIS:\n`;
        report += `  Symptoms: ${data.nlp_analysis.extracted_symptoms.join(', ') || 'None'}\n`;
        report += `  Sentiment: ${data.nlp_analysis.health_sentiment}\n`;
        report += `  Severity: ${data.nlp_analysis.severity_level}\n\n`;
    }

    if (data.risk_prediction) {
        report += `⚠️ RISK PREDICTION:\n`;
        report += `  Risk Category: ${data.risk_prediction.risk_category}\n`;
        report += `  Risk Score: ${Math.round(data.risk_prediction.final_risk_score * 100)}%\n`;
        report += `  Alert Status: ${data.risk_prediction.alert_status}\n`;
        report += `  Medical Action: ${data.risk_prediction.medical_action}\n\n`;

        if (data.risk_prediction.recommendations) {
            report += `📋 RECOMMENDATIONS:\n`;
            data.risk_prediction.recommendations.forEach(rec => {
                report += `  • ${rec}\n`;
            });
        }
    }

    return report;
}

// Print dashboard
function printDashboard() {
    window.print();
}

// Contact emergency
function contactEmergency() {
    const phoneNumber = prompt('Enter emergency contact number:');
    if (phoneNumber) {
        showToast(`Emergency contact initiated to: ${phoneNumber}`, 'success');
    }
}

// Save settings
function saveSettings() {
    const age = document.getElementById('setting-age').value;
    const emergency = document.getElementById('setting-emergency').value;
    const threshold = document.getElementById('setting-threshold').value;

    localStorage.setItem('patient-age', age);
    localStorage.setItem('emergency-contact', emergency);
    localStorage.setItem('risk-threshold', threshold);

    showToast('Settings saved successfully', 'success');
}
