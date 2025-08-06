"""
Utility functions for generating HTML test pages for CTC Health voice assistants.
Updated with CTC Health branding and improved workflow.
"""

import os
import time
import base64
import glob
from typing import Optional, Tuple

def generate_vapi_test_page(
    assistant_id: str, 
    public_key: str, 
    persona_name: str = "Generated Persona",
    output_dir: str = "generated_tests"
) -> Tuple[str, str]:
    """
    Generates a complete HTML test page for a CTC Health voice assistant.
    
    Args:
        assistant_id: The voice assistant ID
        public_key: The public API key
        persona_name: Name of the persona for display
        output_dir: Directory to save the HTML file
    
    Returns:
        tuple: (html_content, file_path)
    """
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get the HTML template
    html_content = get_html_template()
    
    # Replace placeholders
    html_content = html_content.replace("{{ASSISTANT_ID}}", assistant_id)
    html_content = html_content.replace("{{PUBLIC_KEY}}", public_key)
    html_content = html_content.replace("{{PERSONA_NAME}}", persona_name)
    html_content = html_content.replace("{{CREATION_TIME}}", time.strftime('%d/%m/%Y %H:%M'))
    
    # Generate filename with CTC Health naming convention
    timestamp = int(time.time())
    filename = f"ctc_health_assistant_{assistant_id[:8]}_{timestamp}.html"
    file_path = os.path.join(output_dir, filename)
    
    # Save to file
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"✅ CTC Health test page generated: {file_path}")
    except Exception as e:
        print(f"❌ Error saving HTML file: {e}")
        raise
    
    return html_content, file_path


def create_quick_test_link(assistant_id: str, public_key: str, persona_name: str = "Test Persona") -> str:
    """
    Creates a data URL for quick testing without saving files.
    
    Args:
        assistant_id: The voice assistant ID
        public_key: The public API key
        persona_name: Name of the persona for display
    
    Returns:
        str: Data URL that can be used in browser
    """
    # Get the same template as the file generation
    html_content = get_html_template()
    
    # Add cache-busting timestamp to ensure fresh content
    timestamp = int(time.time())
    creation_time = time.strftime('%d/%m/%Y %H:%M:%S')
    
    # Replace placeholders
    html_content = html_content.replace("{{ASSISTANT_ID}}", assistant_id)
    html_content = html_content.replace("{{PUBLIC_KEY}}", public_key)
    html_content = html_content.replace("{{PERSONA_NAME}}", persona_name)
    html_content = html_content.replace("{{CREATION_TIME}}", f"{creation_time} (Quick Link)")
    
    # Add debug comment to verify content freshness
    debug_comment = f"<!-- CTC Health Quick Link Generated: {timestamp} -->\n"
    html_content = html_content.replace("<body>", f"<body>\n{debug_comment}")
    
    # Create data URL
    try:
        html_b64 = base64.b64encode(html_content.encode('utf-8')).decode('utf-8')
        data_url = f"data:text/html;base64,{html_b64}"
        
        # Log what we're actually including
        has_mic_button = 'request-mic' in html_content
        has_mic_function = 'requestMicrophoneAccess' in html_content
        
        print(f"✅ CTC Health quick test link created:")
        print(f"   - Content length: {len(html_content)} characters")
        print(f"   - Microphone button: {'✅' if has_mic_button else '❌'}")
        print(f"   - Microphone function: {'✅' if has_mic_function else '❌'}")
        print(f"   - Timestamp: {timestamp}")
        
        return data_url
    except Exception as e:
        print(f"❌ Error creating data URL: {e}")
        return ""


def validate_vapi_credentials(public_key: str, private_key: str) -> dict:
    """
    Validates voice system credentials and returns status information.
    
    Args:
        public_key: Public API key
        private_key: Private API key
    
    Returns:
        dict: Validation results
    """
    results = {
        "valid": False,
        "public_key_valid": False,
        "private_key_valid": False,
        "errors": []
    }
    
    # Basic format validation
    if not public_key or len(public_key) < 20:
        results["errors"].append("Public key appears to be invalid or missing")
    else:
        results["public_key_valid"] = True
    
    if not private_key or len(private_key) < 20:
        results["errors"].append("Private key appears to be invalid or missing")
    else:
        results["private_key_valid"] = True
    
    # Check for placeholder values
    placeholder_indicators = ["YOUR_VAPI", "your-vapi", "replace", "insert", "add_your"]
    
    for indicator in placeholder_indicators:
        if indicator.lower() in public_key.lower():
            results["errors"].append("Public key contains placeholder text")
            results["public_key_valid"] = False
            break
    
    for indicator in placeholder_indicators:
        if indicator.lower() in private_key.lower():
            results["errors"].append("Private key contains placeholder text")
            results["private_key_valid"] = False
            break
    
    results["valid"] = results["public_key_valid"] and results["private_key_valid"]
    
    return results


def cleanup_old_test_files(output_dir: str = "generated_tests", max_age_hours: int = 24) -> int:
    """
    Cleans up old test files to prevent directory bloat.
    
    Args:
        output_dir: Directory containing test files
        max_age_hours: Maximum age of files to keep (in hours)
    
    Returns:
        int: Number of files deleted
    """
    if not os.path.exists(output_dir):
        return 0
    
    current_time = time.time()
    max_age_seconds = max_age_hours * 3600
    
    # Find all HTML files in the directory
    html_files = glob.glob(os.path.join(output_dir, "ctc_health_assistant_*.html"))
    
    deleted_count = 0
    for file_path in html_files:
        try:
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age_seconds:
                os.remove(file_path)
                deleted_count += 1
                print(f"🗑️ Deleted old CTC Health test file: {os.path.basename(file_path)}")
        except OSError as e:
            print(f"⚠️ Could not delete {file_path}: {e}")
    
    if deleted_count > 0:
        print(f"✅ Cleaned up {deleted_count} old test files")
    
    return deleted_count


def get_html_template() -> str:
    """
    Returns the HTML template for CTC Health voice assistant testing.
    """
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CTC Health Assistant - {{PERSONA_NAME}}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
            padding: 40px;
            max-width: 900px;
            width: 100%;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #2E86AB, #A23B72);
        }
        
        .header {
            margin-bottom: 30px;
        }
        
        .title {
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }
        
        .subtitle {
            font-size: 1.3rem;
            color: #718096;
            margin-bottom: 15px;
        }
        
        .brand {
            background: linear-gradient(90deg, #2E86AB, #A23B72);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            font-size: 1.2rem;
            margin-bottom: 20px;
        }
        
        .assistant-info {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 5px solid #2E86AB;
            text-align: left;
        }
        
        .assistant-info h3 {
            color: #2E86AB;
            margin-bottom: 15px;
            font-size: 1.3rem;
            text-align: center;
        }
        
        .assistant-id {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 0.9rem;
            color: #4a5568;
            word-break: break-all;
            background: #ffffff;
            padding: 10px;
            border-radius: 8px;
            margin-top: 8px;
            border: 1px solid #e2e8f0;
        }
        
        .status-container {
            margin: 30px 0;
        }
        
        .status-message {
            display: inline-block;
            padding: 18px 30px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.1rem;
            transition: all 0.3s ease;
            min-width: 280px;
        }
        
        .status-loading {
            background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
            color: #1976d2;
            border: 2px solid #90caf9;
        }
        
        .status-ready {
            background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%);
            color: #2e7d32;
            border: 2px solid #81c784;
        }
        
        .status-error {
            background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
            color: #c62828;
            border: 2px solid #ef5350;
        }
        
        .instructions {
            background: linear-gradient(135deg, #fffbf0 0%, #fff8e1 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            border: 1px solid #ffcc02;
            text-align: left;
        }
        
        .instructions h3 {
            color: #f57c00;
            margin-bottom: 20px;
            font-size: 1.4rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        
        .instruction-list {
            list-style: none;
            padding: 0;
        }
        
        .instruction-list li {
            margin: 15px 0;
            padding-left: 35px;
            position: relative;
            color: #e65100;
            line-height: 1.6;
            font-weight: 500;
        }
        
        .instruction-list li::before {
            content: "🎯";
            position: absolute;
            left: 0;
            font-size: 1.2rem;
        }
        
        .action-buttons {
            margin: 30px 0;
            display: flex;
            gap: 15px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .action-btn {
            padding: 12px 25px;
            border-radius: 10px;
            border: none;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: inline-block;
            min-width: 140px;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #2E86AB 0%, #1565c0 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(46, 134, 171, 0.3);
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46, 134, 171, 0.4);
        }
        
        .btn-secondary {
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            color: #4a5568;
            border: 1px solid #cbd5e0;
        }
        
        .btn-secondary:hover {
            background: linear-gradient(135deg, #e0e0e0 0%, #d0d0d0 100%);
            transform: translateY(-1px);
        }
        
        .footer {
            margin-top: 40px;
            padding-top: 25px;
            border-top: 2px solid #e2e8f0;
            color: #718096;
            font-size: 0.95rem;
        }
        
        .footer-brand {
            font-weight: bold;
            background: linear-gradient(90deg, #2E86AB, #A23B72);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .feature-highlight {
            background: linear-gradient(135deg, #e8f4fd 0%, #f0f9ff 100%);
            border: 1px solid #2E86AB;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .container {
                padding: 25px 20px;
                margin: 10px;
            }
            
            .title {
                font-size: 2rem;
            }
            
            .subtitle {
                font-size: 1.1rem;
            }
            
            .action-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .action-btn {
                width: 100%;
                max-width: 280px;
            }
        }
    </style>
</head>
<body>
    <div class="container fade-in">
        <div class="header">
            <h1 class="title">🏥 CTC Health Assistant</h1>
            <p class="subtitle">Advanced Medical Training Platform</p>
            <div class="brand">Powered by CTC Health Solution</div>
        </div>
        
        <div class="feature-highlight">
            <p><strong>🎓 Professional Medical Training:</strong> Experience realistic physician interactions powered by advanced AI technology</p>
        </div>
        
        <div class="assistant-info">
            <h3>📋 Assistant Information</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div>
                    <p><strong>Persona:</strong> {{PERSONA_NAME}}</p>
                    <p><strong>Platform:</strong> CTC Health Solution</p>
                </div>
                <div>
                    <p><strong>Status:</strong> <span id="connection-status">Initializing...</span></p>
                    <p><strong>Type:</strong> Voice Interaction</p>
                </div>
            </div>
            <p><strong>Assistant ID:</strong></p>
            <div class="assistant-id">{{ASSISTANT_ID}}</div>
        </div>
        
        <div class="status-container">
            <div id="status-message" class="status-message status-loading pulse">
                🔄 Loading CTC Health voice system...
            </div>
        </div>
        
        <div class="action-buttons">
            <button id="request-mic" class="action-btn btn-primary" onclick="requestMicrophoneAccess()" style="display: none;">
                🎙️ Enable Microphone
            </button>
            <button id="test-connection" class="action-btn btn-secondary" onclick="testConnection()">
                🔧 Test Connection
            </button>
            <button id="refresh-page" class="action-btn btn-secondary" onclick="location.reload()">
                🔄 Refresh Page
            </button>
        </div>
        
        <div class="instructions">
            <h3>💡 How to Use Your CTC Health Assistant</h3>
            <ul class="instruction-list">
                <li><strong>STEP 1:</strong> Wait for the "Assistant Ready" message above</li>
                <li><strong>STEP 2:</strong> Look for the voice call button (usually in bottom-right corner)</li>
                <li><strong>STEP 3:</strong> Click the button to start your medical training session</li>
                <li><strong>STEP 4:</strong> Grant microphone access when prompted by your browser</li>
                <li><strong>STEP 5:</strong> Engage in realistic physician role-play scenarios</li>
                <li><strong>STEP 6:</strong> Test various medical situations and objection handling</li>
            </ul>
            
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 8px; margin-top: 20px;">
                <p style="margin: 0; color: #856404; font-weight: 600;">
                    🎙️ <strong>Important:</strong> Microphone access is required for voice interactions. 
                    Make sure to allow access when prompted by your browser.
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><span class="footer-brand">CTC Health Solution</span> • Advanced Medical AI Training Platform</p>
            <p>Session Created: {{CREATION_TIME}} • Secure Healthcare Training Environment</p>
            <p><small>Optimized for Chrome, Firefox, Safari, and Edge browsers</small></p>
        </div>
    </div>

    <script>
        // Configuration
        const ASSISTANT_ID = "{{ASSISTANT_ID}}";
        const PUBLIC_KEY = "{{PUBLIC_KEY}}";
        
        console.log('🏥 CTC Health Assistant Test Platform Loaded');
        console.log('Assistant ID:', ASSISTANT_ID);
        console.log('API Key Available:', PUBLIC_KEY ? 'Yes' : 'No');
        
        // Voice system configuration
        const buttonConfig = {
            position: "bottom-right",
            offset: "40px",
            width: "65px",
            height: "65px",
            idle: {
                color: "#2E86AB",
                type: "pill",
                title: "Start Medical Training",
                subtitle: "Click to begin voice interaction"
            },
            loading: {
                color: "#f59e0b",
                type: "pill", 
                title: "Connecting...",
                subtitle: "Preparing voice system"
            },
            active: {
                color: "#ef4444",
                type: "pill",
                title: "Training Active",
                subtitle: "Click to end session"
            }
        };

        // Global variables for microphone management
        let microphonePermissionGranted = false;
        let microphoneStream = null;

        // Utility functions
        function updateStatus(status, message, isError = false) {
            const statusEl = document.getElementById('status-message');
            const connectionEl = document.getElementById('connection-status');
            
            if (statusEl) {
                statusEl.className = `status-message ${isError ? 'status-error' : 'status-ready'}`;
                statusEl.innerHTML = message;
                statusEl.classList.remove('pulse');
                if (!isError) {
                    statusEl.classList.add('fade-in');
                }
            }
            
            if (connectionEl) {
                connectionEl.textContent = status;
                connectionEl.style.color = isError ? '#c62828' : '#2e7d32';
                connectionEl.style.fontWeight = 'bold';
            }
            
            console.log(`CTC Health Status: ${status} - ${message}`);
        }
        
        // Microphone access request
        async function requestMicrophoneAccess() {
            console.log('🎙️ CTC Health: Requesting microphone access...');
            updateStatus('🎙️ Microphone Setup...', '🎙️ Requesting microphone access for voice training...');
            
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ 
                    audio: {
                        echoCancellation: true,
                        noiseSuppression: true,
                        sampleRate: 44100
                    } 
                });
                
                console.log('✅ CTC Health: Microphone access granted');
                microphonePermissionGranted = true;
                microphoneStream = stream;
                
                document.getElementById('request-mic').style.display = 'none';
                updateStatus('✅ Microphone Ready', '🎙️ Microphone enabled! Voice training system is ready.');
                
                // Initialize voice system now that we have permissions
                initializeVoiceSystem();
                
            } catch (error) {
                console.error('❌ CTC Health: Microphone access error:', error);
                let errorMessage = '❌ Microphone access denied. ';
                
                if (error.name === 'NotAllowedError') {
                    errorMessage += 'Please click the microphone icon in your browser address bar to allow access.';
                } else if (error.name === 'NotFoundError') {
                    errorMessage += 'No microphone detected. Please check your audio settings.';
                } else if (error.name === 'NotSupportedError') {
                    errorMessage += 'Browser not supported or connection not secure (HTTPS required).';
                } else {
                    errorMessage += error.message;
                }
                
                updateStatus('❌ Microphone Error', errorMessage, true);
            }
        }
        
        // Check microphone permissions
        async function checkMicrophonePermissions() {
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                console.warn('⚠️ CTC Health: getUserMedia not supported');
                updateStatus('❌ Not Supported', '❌ Voice features not supported in this browser', true);
                return false;
            }
            
            try {
                const result = await navigator.permissions.query({ name: 'microphone' });
                console.log('🔍 CTC Health: Microphone permission state:', result.state);
                
                if (result.state === 'granted') {
                    microphonePermissionGranted = true;
                    return true;
                } else if (result.state === 'prompt') {
                    document.getElementById('request-mic').style.display = 'inline-block';
                    updateStatus('🎙️ Permissions Needed', '🎙️ Click "Enable Microphone" to start voice training.');
                    return false;
                } else {
                    updateStatus('❌ Access Blocked', '❌ Microphone access blocked in browser settings.', true);
                    return false;
                }
            } catch (error) {
                console.warn('⚠️ CTC Health: Could not check permissions:', error);
                document.getElementById('request-mic').style.display = 'inline-block';
                updateStatus('🎙️ Setup Required', '🎙️ Microphone setup required for voice features.');
                return false;
            }
        }
        
        function testConnection() {
            updateStatus('🔍 Testing...', '🔍 Testing CTC Health platform connectivity...');
            
            fetch('https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js')
                .then(response => {
                    if (response.ok) {
                        updateStatus('✅ Connected', '✅ CTC Health voice platform is reachable');
                    } else {
                        updateStatus('❌ Platform Error', '❌ Could not reach voice platform services', true);
                    }
                })
                .catch(error => {
                    updateStatus('❌ Network Error', '❌ Network connectivity issue. Check internet connection.', true);
                });
        }
        
        // Initialize voice system
        function initializeVoiceSystem() {
            if (!window.vapiSDK) {
                console.log('⚠️ CTC Health: Voice SDK not loaded yet, waiting...');
                return;
            }
            
            try {
                console.log('📦 CTC Health: Initializing voice system with microphone permissions...');
                
                const voiceConfig = {
                    apiKey: PUBLIC_KEY,
                    assistant: ASSISTANT_ID,
                    config: {
                        ...buttonConfig,
                        transcriber: {
                            provider: "deepgram",
                            model: "nova-2",
                            language: "en"
                        }
                    }
                };
                
                window.vapiSDK.run(voiceConfig);
                
                updateStatus('✅ System Ready!', '🎉 CTC Health Assistant ready! Look for the voice call button in the bottom-right corner.');
                
                console.log('✅ CTC Health: Voice system initialized successfully');
                
            } catch (error) {
                console.error('❌ CTC Health: Voice system initialization error:', error);
                updateStatus('❌ System Error', '❌ Voice system initialization failed: ' + error.message, true);
            }
        }

        // Main voice system loading
        (function (d, t) {
            var g = document.createElement(t),
                s = d.getElementsByTagName(t)[0];
            g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
            g.defer = true;
            g.async = true;
            s.parentNode.insertBefore(g, s);
            
            g.onload = function () {
                console.log('📦 CTC Health: Voice SDK loaded successfully');
                
                if (microphonePermissionGranted) {
                    initializeVoiceSystem();
                } else {
                    updateStatus('⚠️ Setup Required', '⚠️ Microphone access required for voice training features.');
                }
            };
            
            g.onerror = function() {
                console.error('❌ CTC Health: Voice SDK loading failed');
                updateStatus('❌ System Error', '❌ Could not load voice system. Check internet connection.', true);
            };
            
            // Safety timeout
            setTimeout(() => {
                const statusEl = document.getElementById('status-message');
                if (statusEl && statusEl.classList.contains('status-loading')) {
                    updateStatus('⏱️ Timeout', '⚠️ Loading timeout. Try the test connection or refresh the page.', true);
                }
            }, 15000);
            
        })(document, "script");
        
        // Initialize on page load
        document.addEventListener('DOMContentLoaded', async function() {
            console.log('🎯 CTC Health Assistant Training Platform Ready');
            console.log('🔧 Configuration:', {
                assistantId: ASSISTANT_ID,
                hasApiKey: !!PUBLIC_KEY,
                userAgent: navigator.userAgent,
                timestamp: new Date().toISOString()
            });
            
            // Check microphone permissions immediately
            await checkMicrophonePermissions();
        });
        
        // Add some visual feedback for user interactions
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('action-btn')) {
                e.target.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    e.target.style.transform = '';
                }, 150);
            }
        });
    </script>
</body>
</html>"""


# Test function
def test_html_generator():
    """
    Test function to verify CTC Health HTML generator works correctly.
    """
    print("🧪 Testing CTC Health HTML Generator...")
    
    try:
        # Test basic generation
        html, path = generate_vapi_test_page(
            assistant_id="ctc-test-12345",
            public_key="test-public-key",
            persona_name="Dr. Test Persona"
        )
        
        print(f"✅ HTML generated successfully: {len(html)} characters")
        print(f"✅ File saved at: {path}")
        
        # Test data URL creation
        data_url = create_quick_test_link(
            assistant_id="ctc-test-12345",
            public_key="test-public-key", 
            persona_name="Dr. Test Persona"
        )
        
        print(f"✅ Data URL created: {len(data_url)} characters")
        
        # Test credential validation
        validation = validate_vapi_credentials("valid-key-12345", "valid-private-key-12345")
        print(f"✅ Credential validation: {validation['valid']}")
        
        # Test cleanup
        deleted = cleanup_old_test_files()
        print(f"✅ Cleanup completed: {deleted} files removed")
        
        print("🎉 All CTC Health tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    test_html_generator()