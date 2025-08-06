
# Dashboard that create the system prompt and create the assistant, it can be enteracted trought an html file created by html_generator.py
# This codbase is also set to connet API Keys directy from streamlit 
import streamlit as st
import autoprompt
from langchain_openai import ChatOpenAI
import time
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
import base64
import webbrowser
from pathlib import Path

# Import our new HTML generator utilities
try:
    from html_generator import generate_vapi_test_page, create_quick_test_link, cleanup_old_test_files
    HTML_UTILS_AVAILABLE = True
except ImportError:
    HTML_UTILS_AVAILABLE = False

load_dotenv()

st.set_page_config(layout="wide", page_title="CTC Health Solution - Persona Prompt Generator")

def get_segment_options():
    """Helper to read segment options from the markdown file."""
    content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
    return [seg.strip() for seg in content.split('---') if seg.strip()]

def create_test_page_html_fallback(assistant_id, public_key, persona_name="Generated Persona"):
    """Fallback function to create HTML if utilities are not available."""
    html_content = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test CTC Health Assistant - {persona_name}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
            min-height: 100vh;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .header {{
            margin-bottom: 30px;
        }}
        .title {{
            font-size: 2.5rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        .subtitle {{
            font-size: 1.2rem;
            color: #718096;
            margin-bottom: 20px;
        }}
        .brand {{
            background: linear-gradient(90deg, #2E86AB, #A23B72);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
            font-size: 1.1rem;
        }}
        .status {{
            padding: 15px;
            margin: 20px 0;
            border-radius: 8px;
            font-weight: bold;
        }}
        .loading {{ background: #e3f2fd; color: #1976d2; }}
        .ready {{ background: #e8f5e8; color: #2e7d32; }}
        .error {{ background: #ffebee; color: #c62828; }}
        .info-box {{
            background: #f5f5f5;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: left;
        }}
        .btn {{
            background: #2E86AB;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
            transition: background 0.3s;
        }}
        .btn:hover {{ background: #1a5f7a; }}
        .footer {{
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 0.9rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1 class="title">🎙️ CTC Health Assistant</h1>
            <p class="subtitle">Test your personalized medical assistant</p>
            <div class="brand">Powered by CTC Health Solution</div>
        </div>
        
        <div id="status-message" class="status loading">
            🔄 Loading CTC Health assistant...
        </div>
        
        <div class="info-box">
            <h3>💡 Instructions</h3>
            <ul>
                <li>Wait for the assistant to be ready</li>
                <li>Look for the call button (usually bottom-right)</li>
                <li>Click to start the voice call</li>
                <li>Test various scenarios based on the created persona</li>
                <li>Verify consistency with the psychographic profile</li>
            </ul>
        </div>
        
        <div class="footer">
            <p><strong>CTC Health Solution</strong> • Advanced Medical Training Platform</p>
            <p>Generated: {time.strftime('%d/%m/%Y %H:%M')}</p>
        </div>
    </div>

    <script>
        const ASSISTANT_ID = "{assistant_id}";
        const PUBLIC_KEY = "{public_key}";
        
        function updateStatus(message, isError = false) {{
            const statusEl = document.getElementById('status-message');
            statusEl.className = `status ${{isError ? 'error' : 'ready'}}`;
            statusEl.innerHTML = message;
        }}
        
        // Load CTC Health Voice SDK (powered by advanced voice technology)
        (function(d, t) {{
            var g = d.createElement(t), s = d.getElementsByTagName(t)[0];
            g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
            g.defer = g.async = true;
            s.parentNode.insertBefore(g, s);
            
            g.onload = function() {{
                try {{
                    window.vapiSDK.run({{
                        apiKey: PUBLIC_KEY,
                        assistant: ASSISTANT_ID,
                        config: {{
                            position: "bottom-right",
                            offset: "40px",
                            width: "60px",
                            height: "60px"
                        }}
                    }});
                    updateStatus('🎉 CTC Health assistant ready! Look for the call button in the bottom-right.');
                }} catch(e) {{
                    updateStatus('❌ Initialization error: ' + e.message, true);
                }}
            }};
            
            g.onerror = () => updateStatus('❌ Unable to load voice system', true);
            
            setTimeout(() => {{
                if (document.getElementById('status-message').classList.contains('loading')) {{
                    updateStatus('⏱️ Slow loading, try reload', true);
                }}
            }}, 15000);
        }})(document, "script");
        
        console.log('CTC Health Assistant Test Page - ID:', ASSISTANT_ID);
    </script>
</body>
</html>"""
    return html_content

def create_download_with_auto_open(html_content, file_name, persona_name):
    """Creates download button with auto-open functionality"""
    
    # Create columns for better layout
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.success("🎉 Your CTC Health Assistant is ready for testing!")
        
        # Create the download button
        st.download_button(
            label="⬇️ Download & Test Assistant",
            data=html_content,
            file_name=file_name,
            mime="text/html",
            help="Download the test file and open it automatically",
            use_container_width=True,
            type="primary"
        )
        
        # Instructions
        with st.expander("📋 Testing Instructions", expanded=True):
            st.markdown(f"""
            **🚀 Quick Start:**
            1. **Click** the download button above
            2. **Save** the file when prompted by your browser
            3. The file will **automatically open** in a new tab
            4. **Allow** microphone access when prompted
            5. **Click** the call button (bottom-right corner)
            6. **Start testing** your {persona_name} assistant!
            
            **🔧 If auto-open doesn't work:**
            - Find the downloaded file in your Downloads folder
            - Double-click to open in your browser
            - Or drag & drop into a browser tab
            
            **💡 Best browsers:** Chrome, Firefox, Safari, Edge
            """)
    
    # Auto-open JavaScript (this will attempt to open after download)
    st.components.v1.html("""
    <script>
    // Listen for download events and try to help with opening
    document.addEventListener('DOMContentLoaded', function() {
        // Add click handler to download buttons
        const downloadBtns = document.querySelectorAll('[data-testid="stDownloadButton"] button');
        downloadBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                setTimeout(() => {
                    // Show helpful message
                    console.log('CTC Health: File downloaded, check Downloads folder');
                    
                    // Try to provide helpful instructions
                    if (navigator.userAgent.includes('Chrome')) {
                        console.log('Chrome detected - file should auto-open or check downloads bar');
                    }
                }, 1000);
            });
        });
    });
    </script>
    """, height=0)

st.title("🏥 CTC Health Solution - Medical Training Platform")
st.markdown("""
Welcome to the **CTC Health Solution** Persona Prompt Generator! This advanced platform uses a 
multi-agent AI system to help you create detailed medical professional personas for training scenarios.

Follow the steps below to build your persona, then test it with our interactive voice assistant.
""")

# --- Main UI ---
st.header("Step 1: Persona Header")
header_input = st.text_area(
    "Provide basic details for the medical professional persona: Name, Title, Age, Gender, Practice Setting, and Geography.",
    "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
    help="You can provide partial info, and the AI will complete it."
)

st.header("Step 2: Customer Segmentation")
segment_options = get_segment_options()
segment_choice = st.radio(
    "Please select a customer segment for this persona:",
    options=segment_options,
    format_func=lambda x: x.split('\n')[0].replace('###','').strip()
)

if segment_choice:
    with st.expander("View Selected Segment Description", expanded=True):
        st.markdown(segment_choice)

st.header("Step 3: Clinical Context")
st.markdown("Provide details about the persona's clinical practice. Use the points below for guidance:")
st.info("""
**Key areas to describe:**
- Therapeutic Area / Sub-specialty – e.g., "Hematology-Oncology and Multiple Myeloma".
- Typical Patient Mix – percentage of newly diagnosed patients, lines of therapy, comorbidities.
- Key Clinical Drivers – survival, progression-free, side-effect profile, dosing convenience.
- Practice Metrics – infusion chair capacity, average pts/day, clinical trial participation.
""")

context_input = st.text_area(
    "Describe the persona's clinical context (Therapeutic Area, Patient Mix, etc.).",
    "Specializes in late-stage lung cancer. Sees a mix of newly diagnosed and treatment-experienced patients.",
    help="You can provide partial info, and the AI will help complete it."
)

st.header("Step 4: Psychographics & Motivations")
st.markdown("Use the sliders to define the persona's psychographic profile (0.0 to 1.0).")


# Risk Tolerance
st.markdown("**Risk Tolerance**")
col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
with col1:
    st.caption("Conservative")
with col2:
    risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.7, step=0.1, label_visibility="collapsed", format="%.1f")
with col3:
    st.caption("Bold Experimenter")

# Brand Loyalty
st.markdown("**Brand Loyalty**")
col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
with col1:
    st.caption("Low")
with col2:
    brand_loyalty = st.slider("Brand Loyalty", 0.0, 1.0, 0.3, step=0.1, label_visibility="collapsed", format="%.1f")
with col3:
    st.caption("High")

# Research Orientation
st.markdown("**Research Orientation**")
col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
with col1:
    st.caption("Anecdote-driven")
with col2:
    research_orientation = st.slider("Research Orientation", 0.0, 1.0, 0.8, step=0.1, label_visibility="collapsed", format="%.1f")
with col3:
    st.caption("Data-heavy")

# Recognition Need
st.markdown("**Recognition Need**")
col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
with col1:
    st.caption("Seeks podium")
with col2:
    recognition_need = st.slider("Recognition Need", 0.0, 1.0, 0.2, step=0.1, label_visibility="collapsed", format="%.1f")
with col3:
    st.caption("Low-profile")

# Patient Empathy
st.markdown("**Patient Empathy**")
col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
with col1:
    st.caption("Transactional")
with col2:
    patient_empathy = st.slider("Patient Empathy", 0.0, 1.0, 0.9, step=0.1, label_visibility="collapsed", format="%.1f")
with col3:
    st.caption("Advocate")
    
st.header("Step 5: Product & Call Objectives")
st.markdown("Describe the product, call objectives, and the context for the role-play.")
st.info("""
**Key areas to describe:**
- **Product in Focus:** e.g., "Xaltrava 25 mg SC"
- **Training Objective(s):** e.g., "Probe for unmet needs, handle safety concerns"
- **Key Messages:** e.g., "<3 crisp value props>"
- **Anticipated Objections:** e.g., "Too new, budget impact, no OS data yet"
- **Competitor Snapshot:** e.g., "Drug A: oral, cheaper; Drug B: same MoA"
- **Desired Rep Skill:** e.g., "Open-ended questioning, objection-reframe, close"
""")

objectives_input = st.text_area(
    "Describe the product and call objectives.",
    "The product is a new immunotherapy, Xaltorvima. The rep needs to handle objections about its novel mechanism of action.",
    help="You can provide partial info, and the AI will help complete it."
)

# Initialize session state variables
if 'persona_details' not in st.session_state:
    st.session_state.persona_details = None
if 'final_prompt' not in st.session_state:
    st.session_state.final_prompt = ""
if 'assistant_id' not in st.session_state:
    st.session_state.assistant_id = None
if 'persona_name' not in st.session_state:
    st.session_state.persona_name = ""

# Step 1: Build Persona Details
if not st.session_state.persona_details:
    if st.button("📝 Build Persona Details", type="primary"):
   
        psychographics_input_str = f"""
    - Risk Tolerance: {risk_tolerance} (0=Conservative, 1=Bold Experimenter)
    - Brand Loyalty: {brand_loyalty} (0=Low, 1=High)
    - Research Orientation: {research_orientation} (0=Anecdote-driven, 1=Data-heavy)
    - Recognition Need: {recognition_need} (0=Seeks podium, 1=Low-profile)  
    - Patient Empathy: {patient_empathy} (0=Transactional, 1=Advocate)
    """

        with st.spinner("🤖 CTC Health AI agents are building the persona... This may take a moment."):
            persona_state = autoprompt.build_persona_details(
                header_input=header_input,
                segment_input=segment_choice,
                context_input=context_input,
                psychographics_input=psychographics_input_str,
                objectives_input=objectives_input
            )
            st.session_state.persona_details = persona_state
            
            # Extract persona name from header
            if persona_state and 'persona_header' in persona_state:
                header_text = persona_state['persona_header']
                if 'Dr.' in header_text:
                    name_part = header_text.split('Dr.')[1].split(',')[0].split(' is a')[0].strip()
                    st.session_state.persona_name = f"Dr. {name_part}"
                else:
                    st.session_state.persona_name = "Generated Persona"
        
        st.success("🎉 Persona Details Built Successfully!")

# Step 2: Show persona details and generate final prompt
if st.session_state.persona_details:
    st.markdown("---")
    st.subheader("✅ Assembled Persona Details")
    st.markdown(st.session_state.persona_details['full_persona_details'])

    if st.button("🚀 Confirm and Generate System Prompt", type="primary"):
        with st.spinner("🤖 CTC Health AI writers are crafting the final prompt..."):
            final_prompt = autoprompt.generate_final_prompt(st.session_state.persona_details)
            st.session_state.final_prompt = final_prompt
        st.success("🎉 System Prompt Generated Successfully!")

# Step 3: Create assistant and provide testing
if st.session_state.final_prompt:
    st.markdown("---")
    st.success("✅ Final prompt completed and ready for deployment.")
    
    st.markdown("---")
    st.header("Step 6: Create & Test Your CTC Health Assistant")
    
    # Load CTC Health voice system keys
    vapi_private_key = os.getenv("VAPI_PRIVATE_KEY")
    vapi_public_key = os.getenv("VAPI_PUBLIC_KEY")

    if not vapi_private_key or not vapi_public_key or "YOUR_VAPI" in vapi_private_key:
        st.warning("⚠️ CTC Health voice system keys not found in .env file. Please add them to enable voice integration.")
        st.code("""
        VAPI_PRIVATE_KEY=your_private_key_here
        VAPI_PUBLIC_KEY=your_public_key_here
        """)
    else:
        # Create assistant if not already created
        if not st.session_state.assistant_id:
            if st.button("🎙️ Create CTC Health Assistant", type="primary"):
                with st.spinner("🔧 Creating your personalized CTC Health assistant..."):
                    assistant_name = f"CTC-Health-Assistant-{int(time.time())}"
                    assistant_id = autoprompt.create_vapi_assistant(
                        api_key=vapi_private_key,
                        system_prompt=st.session_state.final_prompt,
                        name=assistant_name
                    )
                    if assistant_id:
                        st.session_state.assistant_id = assistant_id
                        st.success(f"✅ CTC Health Assistant created successfully!")
                        # Auto-rerun to show testing interface
                        st.rerun()
                    else:
                        st.error("❌ Failed to create CTC Health assistant. Please check your API keys.")
        
        # Show testing interface if assistant is created
        if st.session_state.assistant_id:
            st.markdown("---")
            st.subheader("🎯 Test Your CTC Health Assistant")
            
            # Generate filename with timestamp for uniqueness
            timestamp = int(time.time())
            file_name = f"ctc_health_assistant_{st.session_state.assistant_id[:8]}_{timestamp}.html"
            
            # Generate HTML content
            if HTML_UTILS_AVAILABLE:
                try:
                    html_content, file_path = generate_vapi_test_page(
                        assistant_id=st.session_state.assistant_id,
                        public_key=vapi_public_key,
                        persona_name=st.session_state.persona_name
                    )
                    cleanup_old_test_files()  # Clean up old files
                except Exception as e:
                    html_content = create_test_page_html_fallback(
                        assistant_id=st.session_state.assistant_id,
                        public_key=vapi_public_key,
                        persona_name=st.session_state.persona_name
                    )
            else:
                html_content = create_test_page_html_fallback(
                    assistant_id=st.session_state.assistant_id,
                    public_key=vapi_public_key,
                    persona_name=st.session_state.persona_name
                )
            
            # Create the download with auto-open functionality
            create_download_with_auto_open(html_content, file_name, st.session_state.persona_name)