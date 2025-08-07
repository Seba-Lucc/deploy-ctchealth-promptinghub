
# # Dashboard that create the system prompt and create the assistant, it can be enteracted trought an html file created by html_generator.py
# # This codbase is also set to connet API Keys directy from streamlit 
# import streamlit as st
# import autoprompt
# from langchain_openai import ChatOpenAI
# import time
# import streamlit.components.v1 as components
# import os
# from dotenv import load_dotenv
# import base64
# import webbrowser
# from pathlib import Path

# # Import our new HTML generator utilities
# try:
#     from html_generator import generate_vapi_test_page, create_quick_test_link, cleanup_old_test_files
#     HTML_UTILS_AVAILABLE = True
# except ImportError:
#     HTML_UTILS_AVAILABLE = False

# load_dotenv()

# st.set_page_config(layout="wide", page_title="CTC Health Solution - Persona Prompt Generator")

# def get_segment_options():
#     """Helper to read segment options from the markdown file."""
#     content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
#     return [seg.strip() for seg in content.split('---') if seg.strip()]

# def create_test_page_html_fallback(assistant_id, public_key, persona_name="Generated Persona"):
#     """Fallback function to create HTML if utilities are not available."""
#     html_content = f"""<!DOCTYPE html>
# <html lang="it">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Test CTC Health Assistant - {persona_name}</title>
#     <style>
#         body {{
#             font-family: Arial, sans-serif;
#             max-width: 800px;
#             margin: 0 auto;
#             padding: 20px;
#             background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
#             min-height: 100vh;
#         }}
#         .container {{
#             background: white;
#             padding: 30px;
#             border-radius: 15px;
#             box-shadow: 0 10px 30px rgba(0,0,0,0.1);
#             text-align: center;
#         }}
#         .header {{
#             margin-bottom: 30px;
#         }}
#         .title {{
#             font-size: 2.5rem;
#             font-weight: 700;
#             color: #2d3748;
#             margin-bottom: 10px;
#         }}
#         .subtitle {{
#             font-size: 1.2rem;
#             color: #718096;
#             margin-bottom: 20px;
#         }}
#         .brand {{
#             background: linear-gradient(90deg, #2E86AB, #A23B72);
#             -webkit-background-clip: text;
#             -webkit-text-fill-color: transparent;
#             font-weight: bold;
#             font-size: 1.1rem;
#         }}
#         .status {{
#             padding: 15px;
#             margin: 20px 0;
#             border-radius: 8px;
#             font-weight: bold;
#         }}
#         .loading {{ background: #e3f2fd; color: #1976d2; }}
#         .ready {{ background: #e8f5e8; color: #2e7d32; }}
#         .error {{ background: #ffebee; color: #c62828; }}
#         .info-box {{
#             background: #f5f5f5;
#             padding: 20px;
#             border-radius: 8px;
#             margin: 20px 0;
#             text-align: left;
#         }}
#         .btn {{
#             background: #2E86AB;
#             color: white;
#             padding: 10px 20px;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#             margin: 5px;
#             transition: background 0.3s;
#         }}
#         .btn:hover {{ background: #1a5f7a; }}
#         .footer {{
#             margin-top: 40px;
#             padding-top: 20px;
#             border-top: 1px solid #e2e8f0;
#             color: #718096;
#             font-size: 0.9rem;
#         }}
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1 class="title">🎙️ CTC Health Assistant</h1>
#             <p class="subtitle">Test your personalized medical assistant</p>
#             <div class="brand">Powered by CTC Health Solution</div>
#         </div>
        
#         <div id="status-message" class="status loading">
#             🔄 Loading CTC Health assistant...
#         </div>
        
#         <div class="info-box">
#             <h3>💡 Instructions</h3>
#             <ul>
#                 <li>Wait for the assistant to be ready</li>
#                 <li>Look for the call button (usually bottom-right)</li>
#                 <li>Click to start the voice call</li>
#                 <li>Test various scenarios based on the created persona</li>
#                 <li>Verify consistency with the psychographic profile</li>
#             </ul>
#         </div>
        
#         <div class="footer">
#             <p><strong>CTC Health Solution</strong> • Advanced Medical Training Platform</p>
#             <p>Generated: {time.strftime('%d/%m/%Y %H:%M')}</p>
#         </div>
#     </div>

#     <script>
#         const ASSISTANT_ID = "{assistant_id}";
#         const PUBLIC_KEY = "{public_key}";
        
#         function updateStatus(message, isError = false) {{
#             const statusEl = document.getElementById('status-message');
#             statusEl.className = `status ${{isError ? 'error' : 'ready'}}`;
#             statusEl.innerHTML = message;
#         }}
        
#         // Load CTC Health Voice SDK (powered by advanced voice technology)
#         (function(d, t) {{
#             var g = d.createElement(t), s = d.getElementsByTagName(t)[0];
#             g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
#             g.defer = g.async = true;
#             s.parentNode.insertBefore(g, s);
            
#             g.onload = function() {{
#                 try {{
#                     window.vapiSDK.run({{
#                         apiKey: PUBLIC_KEY,
#                         assistant: ASSISTANT_ID,
#                         config: {{
#                             position: "bottom-right",
#                             offset: "40px",
#                             width: "60px",
#                             height: "60px"
#                         }}
#                     }});
#                     updateStatus('🎉 CTC Health assistant ready! Look for the call button in the bottom-right.');
#                 }} catch(e) {{
#                     updateStatus('❌ Initialization error: ' + e.message, true);
#                 }}
#             }};
            
#             g.onerror = () => updateStatus('❌ Unable to load voice system', true);
            
#             setTimeout(() => {{
#                 if (document.getElementById('status-message').classList.contains('loading')) {{
#                     updateStatus('⏱️ Slow loading, try reload', true);
#                 }}
#             }}, 15000);
#         }})(document, "script");
        
#         console.log('CTC Health Assistant Test Page - ID:', ASSISTANT_ID);
#     </script>
# </body>
# </html>"""
#     return html_content

# def create_download_with_auto_open(html_content, file_name, persona_name):
#     """Creates download button with auto-open functionality"""
    
#     # Create columns for better layout
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         st.success("🎉 Your CTC Health Assistant is ready for testing!")
        
#         # Create the download button
#         st.download_button(
#             label="⬇️ Download & Test Assistant",
#             data=html_content,
#             file_name=file_name,
#             mime="text/html",
#             help="Download the test file and open it automatically",
#             use_container_width=True,
#             type="primary"
#         )
        
#         # Instructions
#         with st.expander("📋 Testing Instructions", expanded=True):
#             st.markdown(f"""
#             **🚀 Quick Start:**
#             1. **Click** the download button above
#             2. **Save** the file when prompted by your browser
#             3. The file will **automatically open** in a new tab
#             4. **Allow** microphone access when prompted
#             5. **Click** the call button (bottom-right corner)
#             6. **Start testing** your {persona_name} assistant!
            
#             **🔧 If auto-open doesn't work:**
#             - Find the downloaded file in your Downloads folder
#             - Double-click to open in your browser
#             - Or drag & drop into a browser tab
            
#             **💡 Best browsers:** Chrome, Firefox, Safari, Edge
#             """)
    
#     # Auto-open JavaScript (this will attempt to open after download)
#     st.components.v1.html("""
#     <script>
#     // Listen for download events and try to help with opening
#     document.addEventListener('DOMContentLoaded', function() {
#         // Add click handler to download buttons
#         const downloadBtns = document.querySelectorAll('[data-testid="stDownloadButton"] button');
#         downloadBtns.forEach(btn => {
#             btn.addEventListener('click', function() {
#                 setTimeout(() => {
#                     // Show helpful message
#                     console.log('CTC Health: File downloaded, check Downloads folder');
                    
#                     // Try to provide helpful instructions
#                     if (navigator.userAgent.includes('Chrome')) {
#                         console.log('Chrome detected - file should auto-open or check downloads bar');
#                     }
#                 }, 1000);
#             });
#         });
#     });
#     </script>
#     """, height=0)

# st.title("🏥 CTC Health Solution - Medical Training Platform")
# st.markdown("""
# Welcome to the **CTC Health Solution** Persona Prompt Generator! This advanced platform uses a 
# multi-agent AI system to help you create detailed medical professional personas for training scenarios.

# Follow the steps below to build your persona, then test it with our interactive voice assistant.
# """)

# # --- Main UI ---
# st.header("Step 1: Persona Header")
# header_input = st.text_area(
#     "Provide basic details for the medical professional persona: Name, Title, Age, Gender, Practice Setting, and Geography.",
#     "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
#     help="You can provide partial info, and the AI will complete it."
# )

# st.header("Step 2: Customer Segmentation")
# segment_options = get_segment_options()
# segment_choice = st.radio(
#     "Please select a customer segment for this persona:",
#     options=segment_options,
#     format_func=lambda x: x.split('\n')[0].replace('###','').strip()
# )

# if segment_choice:
#     with st.expander("View Selected Segment Description", expanded=True):
#         st.markdown(segment_choice)

# st.header("Step 3: Clinical Context")
# st.markdown("Provide details about the persona's clinical practice. Use the points below for guidance:")
# st.info("""
# **Key areas to describe:**
# - Therapeutic Area / Sub-specialty – e.g., "Hematology-Oncology and Multiple Myeloma".
# - Typical Patient Mix – percentage of newly diagnosed patients, lines of therapy, comorbidities.
# - Key Clinical Drivers – survival, progression-free, side-effect profile, dosing convenience.
# - Practice Metrics – infusion chair capacity, average pts/day, clinical trial participation.
# """)

# context_input = st.text_area(
#     "Describe the persona's clinical context (Therapeutic Area, Patient Mix, etc.).",
#     "Specializes in late-stage lung cancer. Sees a mix of newly diagnosed and treatment-experienced patients.",
#     help="You can provide partial info, and the AI will help complete it."
# )

# st.header("Step 4: Psychographics & Motivations")
# st.markdown("Use the sliders to define the persona's psychographic profile (0.0 to 1.0).")


# # Risk Tolerance
# st.markdown("**Risk Tolerance**")
# col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
# with col1:
#     st.caption("Conservative")
# with col2:
#     risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.7, step=0.1, label_visibility="collapsed", format="%.1f")
# with col3:
#     st.caption("Bold Experimenter")

# # Brand Loyalty
# st.markdown("**Brand Loyalty**")
# col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
# with col1:
#     st.caption("Low")
# with col2:
#     brand_loyalty = st.slider("Brand Loyalty", 0.0, 1.0, 0.3, step=0.1, label_visibility="collapsed", format="%.1f")
# with col3:
#     st.caption("High")

# # Research Orientation
# st.markdown("**Research Orientation**")
# col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
# with col1:
#     st.caption("Anecdote-driven")
# with col2:
#     research_orientation = st.slider("Research Orientation", 0.0, 1.0, 0.8, step=0.1, label_visibility="collapsed", format="%.1f")
# with col3:
#     st.caption("Data-heavy")

# # Recognition Need
# st.markdown("**Recognition Need**")
# col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
# with col1:
#     st.caption("Seeks podium")
# with col2:
#     recognition_need = st.slider("Recognition Need", 0.0, 1.0, 0.2, step=0.1, label_visibility="collapsed", format="%.1f")
# with col3:
#     st.caption("Low-profile")

# # Patient Empathy
# st.markdown("**Patient Empathy**")
# col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
# with col1:
#     st.caption("Transactional")
# with col2:
#     patient_empathy = st.slider("Patient Empathy", 0.0, 1.0, 0.9, step=0.1, label_visibility="collapsed", format="%.1f")
# with col3:
#     st.caption("Advocate")
    
# st.header("Step 5: Product & Call Objectives")
# st.markdown("Describe the product, call objectives, and the context for the role-play.")
# st.info("""
# **Key areas to describe:**
# - **Product in Focus:** e.g., "Xaltrava 25 mg SC"
# - **Training Objective(s):** e.g., "Probe for unmet needs, handle safety concerns"
# - **Key Messages:** e.g., "<3 crisp value props>"
# - **Anticipated Objections:** e.g., "Too new, budget impact, no OS data yet"
# - **Competitor Snapshot:** e.g., "Drug A: oral, cheaper; Drug B: same MoA"
# - **Desired Rep Skill:** e.g., "Open-ended questioning, objection-reframe, close"
# """)

# objectives_input = st.text_area(
#     "Describe the product and call objectives.",
#     "The product is a new immunotherapy, Xaltorvima. The rep needs to handle objections about its novel mechanism of action.",
#     help="You can provide partial info, and the AI will help complete it."
# )

# # Initialize session state variables
# if 'persona_details' not in st.session_state:
#     st.session_state.persona_details = None
# if 'final_prompt' not in st.session_state:
#     st.session_state.final_prompt = ""
# if 'assistant_id' not in st.session_state:
#     st.session_state.assistant_id = None
# if 'persona_name' not in st.session_state:
#     st.session_state.persona_name = ""

# # Step 1: Build Persona Details
# if not st.session_state.persona_details:
#     if st.button("📝 Build Persona Details", type="primary"):
   
#         psychographics_input_str = f"""
#     - Risk Tolerance: {risk_tolerance} (0=Conservative, 1=Bold Experimenter)
#     - Brand Loyalty: {brand_loyalty} (0=Low, 1=High)
#     - Research Orientation: {research_orientation} (0=Anecdote-driven, 1=Data-heavy)
#     - Recognition Need: {recognition_need} (0=Seeks podium, 1=Low-profile)  
#     - Patient Empathy: {patient_empathy} (0=Transactional, 1=Advocate)
#     """

#         with st.spinner("🤖 CTC Health AI agents are building the persona... This may take a moment."):
#             persona_state = autoprompt.build_persona_details(
#                 header_input=header_input,
#                 segment_input=segment_choice,
#                 context_input=context_input,
#                 psychographics_input=psychographics_input_str,
#                 objectives_input=objectives_input
#             )
#             st.session_state.persona_details = persona_state
            
#             # Extract persona name from header
#             if persona_state and 'persona_header' in persona_state:
#                 header_text = persona_state['persona_header']
#                 if 'Dr.' in header_text:
#                     name_part = header_text.split('Dr.')[1].split(',')[0].split(' is a')[0].strip()
#                     st.session_state.persona_name = f"Dr. {name_part}"
#                 else:
#                     st.session_state.persona_name = "Generated Persona"
        
#         st.success("🎉 Persona Details Built Successfully!")

# # Step 2: Show persona details and generate final prompt
# if st.session_state.persona_details:
#     st.markdown("---")
#     st.subheader("✅ Assembled Persona Details")
#     st.markdown(st.session_state.persona_details['full_persona_details'])

#     if st.button("🚀 Confirm and Generate System Prompt", type="primary"):
#         with st.spinner("🤖 CTC Health AI writers are crafting the final prompt..."):
#             final_prompt = autoprompt.generate_final_prompt(st.session_state.persona_details)
#             st.session_state.final_prompt = final_prompt
#         st.success("🎉 System Prompt Generated Successfully!")

# # Step 3: Create assistant and provide testing
# if st.session_state.final_prompt:
#     st.markdown("---")
#     st.success("✅ Final prompt completed and ready for deployment.")
    
#     st.markdown("---")
#     st.header("Step 6: Create & Test Your CTC Health Assistant")
    
#     # Load CTC Health voice system keys
#     vapi_private_key = os.getenv("VAPI_PRIVATE_KEY")
#     vapi_public_key = os.getenv("VAPI_PUBLIC_KEY")

#     if not vapi_private_key or not vapi_public_key or "YOUR_VAPI" in vapi_private_key:
#         st.warning("⚠️ CTC Health voice system keys not found in .env file. Please add them to enable voice integration.")
#         st.code("""
#         VAPI_PRIVATE_KEY=your_private_key_here
#         VAPI_PUBLIC_KEY=your_public_key_here
#         """)
#     else:
#         # Create assistant if not already created
#         if not st.session_state.assistant_id:
#             if st.button("🎙️ Create CTC Health Assistant", type="primary"):
#                 with st.spinner("🔧 Creating your personalized CTC Health assistant..."):
#                     assistant_name = f"CTC-Health-Assistant-{int(time.time())}"
#                     assistant_id = autoprompt.create_vapi_assistant(
#                         api_key=vapi_private_key,
#                         system_prompt=st.session_state.final_prompt,
#                         name=assistant_name
#                     )
#                     if assistant_id:
#                         st.session_state.assistant_id = assistant_id
#                         st.success(f"✅ CTC Health Assistant created successfully!")
#                         # Auto-rerun to show testing interface
#                         st.rerun()
#                     else:
#                         st.error("❌ Failed to create CTC Health assistant. Please check your API keys.")
        
#         # Show testing interface if assistant is created
#         if st.session_state.assistant_id:
#             st.markdown("---")
#             st.subheader("🎯 Test Your CTC Health Assistant")
            
#             # Generate filename with timestamp for uniqueness
#             timestamp = int(time.time())
#             file_name = f"ctc_health_assistant_{st.session_state.assistant_id[:8]}_{timestamp}.html"
            
#             # Generate HTML content
#             if HTML_UTILS_AVAILABLE:
#                 try:
#                     html_content, file_path = generate_vapi_test_page(
#                         assistant_id=st.session_state.assistant_id,
#                         public_key=vapi_public_key,
#                         persona_name=st.session_state.persona_name
#                     )
#                     cleanup_old_test_files()  # Clean up old files
#                 except Exception as e:
#                     html_content = create_test_page_html_fallback(
#                         assistant_id=st.session_state.assistant_id,
#                         public_key=vapi_public_key,
#                         persona_name=st.session_state.persona_name
#                     )
#             else:
#                 html_content = create_test_page_html_fallback(
#                     assistant_id=st.session_state.assistant_id,
#                     public_key=vapi_public_key,
#                     persona_name=st.session_state.persona_name
#                 )
            
#             # Create the download with auto-open functionality
#             create_download_with_auto_open(html_content, file_name, st.session_state.persona_name)


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
import tempfile

load_dotenv()

st.set_page_config(layout="wide", page_title="CTC Health Solution - Persona Prompt Generator")

def get_segment_options():
    """Helper to read segment options from the markdown file."""
    content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
    return [seg.strip() for seg in content.split('---') if seg.strip()]

def create_vapi_test_html(assistant_id, public_key, persona_name="Generated Persona"):
    """Crea una pagina HTML completa per VAPI che verrà servita da Streamlit"""
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CTC Health Assistant - {persona_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 20px;
            padding: 60px 40px;
            text-align: center;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 30px 60px rgba(0,0,0,0.12);
        }}
        
        .header {{
            margin-bottom: 40px;
        }}
        
        .logo {{
            font-size: 3rem;
            margin-bottom: 10px;
        }}
        
        .title {{
            font-size: 2.2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 10px;
        }}
        
        .subtitle {{
            font-size: 1.1rem;
            color: #718096;
            margin-bottom: 20px;
        }}
        
        .persona-info {{
            background: #f7fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin: 30px 0;
        }}
        
        .persona-name {{
            font-size: 1.3rem;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 8px;
        }}
        
        .persona-subtitle {{
            color: #718096;
            font-size: 0.95rem;
        }}
        
        .instructions {{
            background: #ebf8ff;
            border-left: 4px solid #3182ce;
            padding: 20px;
            margin: 30px 0;
            text-align: left;
            border-radius: 0 8px 8px 0;
        }}
        
        .instructions h3 {{
            color: #2c5282;
            margin-bottom: 15px;
            font-size: 1.1rem;
        }}
        
        .instructions ul {{
            color: #2d3748;
            line-height: 1.6;
        }}
        
        .instructions li {{
            margin-bottom: 8px;
        }}
        
        .status {{
            padding: 15px 25px;
            border-radius: 10px;
            font-weight: 600;
            margin: 20px 0;
            transition: all 0.3s ease;
        }}
        
        .loading {{
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }}
        
        .ready {{
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
        }}
        
        .error {{
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }}
        
        .footer {{
            margin-top: 40px;
            padding-top: 30px;
            border-top: 1px solid #e2e8f0;
            color: #718096;
            font-size: 0.9rem;
        }}
        
        .brand {{
            font-weight: 600;
            color: #667eea;
        }}
        
        .debug-info {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            text-align: left;
            font-family: monospace;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🏥</div>
            <h1 class="title">CTC Health Assistant</h1>
            <p class="subtitle">Advanced Medical Training Platform</p>
        </div>
        
        <div class="persona-info">
            <div class="persona-name">{persona_name}</div>
            <div class="persona-subtitle">Your Personalized Medical Assistant</div>
        </div>
        
        <div id="status" class="status loading">
            🔄 Initializing voice system...
        </div>
        
        <div class="instructions">
            <h3>📋 How to Use</h3>
            <ul>
                <li><strong>Wait for initialization</strong> - The system will load automatically</li>
                <li><strong>Look for the voice button</strong> - It will appear in the bottom-right corner</li>
                <li><strong>Click to start talking</strong> - Have a conversation with {persona_name}</li>
                <li><strong>Allow microphone access</strong> - Your browser will ask for permission</li>
                <li><strong>Speak naturally</strong> - The assistant will respond based on the persona profile</li>
            </ul>
        </div>
        
        <div class="debug-info">
            <strong>🔧 Technical Info:</strong><br>
            Assistant ID: {assistant_id}<br>
            Public Key: {public_key[:12]}...<br>
            Page served via: Streamlit Static Files<br>
            Status: <span id="debug-status">Initializing...</span>
        </div>
        
        <div class="footer">
            <div class="brand">CTC Health Solution</div>
            <div>Advanced Voice AI • Medical Training Platform</div>
            <div>Generated: {time.strftime('%B %d, %Y at %H:%M')}</div>
        </div>
    </div>

    <!-- VAPI Integration Script -->
    <script>
        // Configuration
        var vapiInstance = null;
        const assistant = "{assistant_id}"; // Your assistant ID
        const apiKey = "{public_key}"; // Your Public API key
        
        const statusEl = document.getElementById('status');
        const debugStatusEl = document.getElementById('debug-status');
        
        function updateStatus(message, className) {{
            statusEl.innerHTML = message;
            statusEl.className = `status ${{className}}`;
        }}
        
        function updateDebugStatus(message) {{
            if (debugStatusEl) debugStatusEl.textContent = message;
        }}
        
        // Enhanced debug logging
        console.log('🏥 CTC Health Assistant Test Page');
        console.log('👨‍⚕️ Persona: {persona_name}');
        console.log('🆔 Assistant ID:', assistant);
        console.log('🔑 Public Key:', apiKey.substring(0, 8) + '...');
        console.log('🌍 Page URL:', window.location.href);
        console.log('📡 User Agent:', navigator.userAgent);
        
        // Validation checks
        if (!assistant || assistant === 'undefined' || assistant.includes('{{')) {{
            updateStatus('❌ Invalid Assistant ID configuration', 'error');
            updateDebugStatus('Invalid Assistant ID');
            console.error('❌ Invalid Assistant ID:', assistant);
        }} else if (!apiKey || apiKey === 'undefined' || apiKey.includes('{{')) {{
            updateStatus('❌ Invalid API Key configuration', 'error');
            updateDebugStatus('Invalid API Key');
            console.error('❌ Invalid API Key:', apiKey);
        }} else {{
            // Proceed with VAPI loading
            updateStatus('🔄 Loading VAPI SDK...', 'loading');
            updateDebugStatus('Loading SDK...');
            
            // VAPI Snippet (Official Documentation)
            (function (d, t) {{
                var g = document.createElement(t), s = d.getElementsByTagName(t)[0];
                g.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
                g.defer = true;
                g.async = true;
                s.parentNode.insertBefore(g, s);
                
                g.onload = function () {{
                    console.log('✅ VAPI SDK loaded successfully');
                    updateStatus('🚀 Initializing voice assistant...', 'loading');
                    updateDebugStatus('SDK loaded, initializing...');
                    
                    // Wait for SDK to be ready
                    setTimeout(() => {{
                        try {{
                            if (!window.vapiSDK) {{
                                throw new Error('VAPI SDK not available in window');
                            }}
                            
                            console.log('🔧 Creating VAPI instance...');
                            
                            vapiInstance = window.vapiSDK.run({{
                                apiKey: apiKey, // mandatory
                                assistant: assistant, // mandatory
                                config: {{
                                    position: "bottom-right",
                                    offset: "40px",
                                    width: "60px",
                                    height: "60px",
                                    idle: {{
                                        color: "#667eea",
                                        type: "pill",
                                        title: "🎙️ Talk to {persona_name}",
                                        subtitle: "CTC Health Assistant"
                                    }},
                                    loading: {{
                                        color: "#ed8936",
                                        title: "Connecting...",
                                        subtitle: "Please wait"
                                    }},
                                    active: {{
                                        color: "#e53e3e",
                                        title: "🔴 Live Call",
                                        subtitle: "Tap to end"
                                    }}
                                }}
                            }});
                            
                            if (vapiInstance) {{
                                console.log('✅ VAPI instance created successfully:', vapiInstance);
                                updateStatus('✅ Voice assistant ready! Look for the button in bottom-right corner.', 'ready');
                                updateDebugStatus('Ready and functional');
                                
                                // Event listeners
                                if (vapiInstance.on) {{
                                    vapiInstance.on('call-start', () => {{
                                        console.log('📞 Call started with {persona_name}');
                                        updateStatus('🔴 Call in progress with {persona_name}', 'ready');
                                        updateDebugStatus('Call active');
                                    }});
                                    
                                    vapiInstance.on('call-end', () => {{
                                        console.log('📞 Call ended');
                                        updateStatus('✅ Voice assistant ready! Click the button to start a new conversation.', 'ready');
                                        updateDebugStatus('Call ended - ready for new call');
                                    }});
                                    
                                    vapiInstance.on('error', (error) => {{
                                        console.error('❌ VAPI Runtime Error:', error);
                                        updateStatus('❌ Call error: ' + (error.message || 'Unknown error'), 'error');
                                        updateDebugStatus('Error: ' + (error.message || 'Unknown'));
                                    }});
                                    
                                    vapiInstance.on('speech-start', () => {{
                                        console.log('🎤 User started speaking');
                                    }});
                                    
                                    vapiInstance.on('speech-end', () => {{
                                        console.log('🎤 User stopped speaking');
                                    }});
                                    
                                    vapiInstance.on('message', (message) => {{
                                        console.log('📨 VAPI Message:', message);
                                    }});
                                }}
                                
                            }} else {{
                                throw new Error('VAPI instance creation returned null/undefined');
                            }}
                            
                        }} catch (error) {{
                            console.error('❌ VAPI Initialization Error:', error);
                            updateStatus('❌ Failed to initialize: ' + error.message, 'error');
                            updateDebugStatus('Initialization failed');
                        }}
                    }}, 1500); // Wait 1.5 seconds for SDK to be fully ready
                }};
                
                g.onerror = function(error) {{
                    console.error('❌ Failed to load VAPI SDK:', error);
                    updateStatus('❌ Failed to load voice system. Please check your internet connection.', 'error');
                    updateDebugStatus('SDK loading failed');
                }};
                
                // Timeout fallback
                setTimeout(() => {{
                    if (!window.vapiSDK) {{
                        console.error('⏱️ VAPI SDK loading timeout');
                        updateStatus('❌ Loading timeout. Please refresh the page and try again.', 'error');
                        updateDebugStatus('Timeout - please refresh');
                    }}
                }}, 15000); // 15 second timeout
                
            }})(document, "script");
        }}
    </script>
</body>
</html>"""
    
    return html_content

def save_vapi_html_to_static(assistant_id, public_key, persona_name):
    """Salva la pagina HTML nella cartella static per essere servita da Streamlit"""
    
    try:
        # Crea la directory static se non esiste
        static_dir = Path("./static")
        static_dir.mkdir(exist_ok=True)
        
        # Genera nome file unico
        timestamp = int(time.time())
        filename = f"ctc_health_test_{timestamp}.html"
        filepath = static_dir / filename
        
        # Genera contenuto HTML
        html_content = create_vapi_test_html(assistant_id, public_key, persona_name)
        
        # Salva il file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
        
    except Exception as e:
        st.error(f"Errore nel salvataggio della pagina di test: {str(e)}")
        return None

def get_static_file_url(filename):
    """Restituisce l'URL per accedere al file static"""
    # Per Streamlit locale: http://localhost:8501/app/static/filename
    # Per Streamlit Cloud: https://your-app.streamlit.app/app/static/filename
    
    # Prova a determinare l'URL base
    base_url = "http://localhost:8501"  # Default per sviluppo locale
    
    # Se in produzione, l'URL sarà diverso ma il path relativo rimane lo stesso
    return f"{base_url}/app/static/{filename}"

st.title("🏥 CTC Health Solution - Medical Training Platform")
st.markdown("""
Welcome to the **CTC Health Solution** Persona Prompt Generator! This advanced platform uses a 
multi-agent AI system to help you create detailed medical professional personas for training scenarios.

Follow the steps below to build your persona, then test it with our interactive voice assistant.
""")

# Verifica se static file serving è abilitato
st.sidebar.markdown("## ⚙️ Configuration Check")
if os.getenv("STREAMLIT_SERVER_ENABLE_STATIC_SERVING") == "true":
    st.sidebar.success("✅ Static file serving enabled")
else:
    st.sidebar.warning("""
    ⚠️ **Static file serving not enabled**
    
    Add to your config.toml:
    ```toml
    [server]
    enableStaticServing = true
    ```
    
    Or set environment variable:
    ```bash
    STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
    ```
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
if 'creation_date' not in st.session_state:
    st.session_state.creation_date = ""

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
    
    # Show the complete persona details
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
                        st.session_state.creation_date = time.strftime('%B %d, %Y at %H:%M')
                        st.success(f"✅ CTC Health Assistant created successfully!")
                        # Auto-rerun to show testing interface
                        st.rerun()
                    else:
                        st.error("❌ Failed to create CTC Health assistant. Please check your API keys.")
        
        # Show assistant info and test button if assistant is created
        if st.session_state.assistant_id:
            st.markdown("---")
            st.subheader("🎯 Your CTC Health Assistant")
            
            # Display assistant info in a nice card
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.success("🎉 Your CTC Health Assistant is ready!")
                
                # Assistant info card
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 25px;
                    border-radius: 15px;
                    color: white;
                    text-align: center;
                    margin: 20px 0;
                ">
                    <h3 style="margin: 0 0 10px 0; font-size: 1.4rem;">🎙️ {st.session_state.persona_name}</h3>
                    <p style="margin: 0 0 15px 0; opacity: 0.9;">CTC Health Voice Assistant</p>
                    <p style="margin: 0; font-size: 0.9rem; opacity: 0.8;">Created: {st.session_state.creation_date}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Test button
                if st.button("🎙️ Test Your CTC Health Assistant", type="primary", use_container_width=True):
                    with st.spinner("🔄 Creating test interface..."):
                        # Salva la pagina HTML nella cartella static
                        filename = save_vapi_html_to_static(
                            assistant_id=st.session_state.assistant_id,
                            public_key=vapi_public_key,
                            persona_name=st.session_state.persona_name
                        )
                        
                        if filename:
                            st.success("✅ Test page created successfully!")
                            
                            # URL per accedere al file
                            static_url = f"/app/static/{filename}"
                            
                            st.info(f"""
                            **🎯 Your test page is ready!**
                            
                            The HTML file has been saved to: `./static/{filename}`
                            
                            **Access URL:** `{static_url}`
                            """)
                            
                            # Mostra l'iframe con la pagina HTML servita da Streamlit
                            st.markdown("### 🎙️ Voice Assistant Interface")
                            
                            # Usa components.iframe per caricare la pagina HTML
                            components.iframe(static_url, height=700, scrolling=True)
                            
                            st.markdown("""
                            **📋 Instructions:**
                            
                            1. **Wait for initialization** - The voice system will load automatically
                            2. **Look for the voice button** in the bottom-right corner of the frame above
                            3. **Click to start talking** - Have a conversation with your assistant
                            4. **Allow microphone access** when your browser asks
                            
                            **🔧 Troubleshooting:**
                            - If you don't see the button, wait a few seconds for VAPI to load
                            - Check the debug information in the interface for any issues
                            - Make sure your browser allows microphone access
                            """)
                            
                        else:
                            st.error("❌ Failed to create test page")