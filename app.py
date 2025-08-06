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


# Solution with embedded interactionability
import streamlit as st
import autoprompt
from langchain_openai import ChatOpenAI
import time
import streamlit.components.v1 as components
import os
from dotenv import load_dotenv
import base64
import json

# Import HTML generator for fallback
try:
    from html_generator import generate_vapi_test_page, validate_vapi_credentials, cleanup_old_test_files
    HTML_UTILS_AVAILABLE = True
except ImportError:
    HTML_UTILS_AVAILABLE = False

load_dotenv()

# Page config with CTC Health branding
st.set_page_config(
    layout="wide", 
    page_title="CTC Health Solution - Medical Training Platform",
    page_icon="🏥",
    initial_sidebar_state="collapsed"
)

def get_segment_options():
    """Helper to read segment options from the markdown file."""
    content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
    return [seg.strip() for seg in content.split('---') if seg.strip()]

def create_vapi_widget_component_fixed(assistant_id: str, public_key: str, persona_name: str = "CTC Health Assistant"):
    """
    Creates the FIXED integrated VAPI voice widget component.
    Addresses layout visibility and error handling issues.
    """
    
    component_id = f"ctc_health_widget_{int(time.time())}"
    
    # Enhanced HTML with better button positioning and error handling
    vapi_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CTC Health Voice Assistant</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                padding: 20px;
                min-height: 500px;
                position: relative;
                overflow: visible;
            }}
            
            .ctc-container {{
                background: white;
                border-radius: 15px;
                padding: 30px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                text-align: center;
                position: relative;
                min-height: 450px;
                border: 2px solid transparent;
                background: linear-gradient(white, white) padding-box,
                           linear-gradient(135deg, #2E86AB, #A23B72) border-box;
                overflow: visible;
            }}
            
            .ctc-header {{
                margin-bottom: 25px;
            }}
            
            .ctc-title {{
                font-size: 1.8rem;
                font-weight: 700;
                background: linear-gradient(135deg, #2E86AB, #A23B72);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 10px;
            }}
            
            .ctc-subtitle {{
                color: #64748b;
                font-size: 1rem;
                margin-bottom: 15px;
            }}
            
            .ctc-persona-info {{
                background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #2E86AB;
            }}
            
            .ctc-status {{
                display: inline-block;
                padding: 15px 30px;
                border-radius: 25px;
                font-weight: 600;
                margin: 20px 0;
                transition: all 0.3s ease;
                min-width: 300px;
                font-size: 1rem;
            }}
            
            .status-loading {{
                background: linear-gradient(135deg, #dbeafe, #bfdbfe);
                color: #1e40af;
                border: 2px solid #93c5fd;
            }}
            
            .status-ready {{
                background: linear-gradient(135deg, #dcfce7, #bbf7d0);
                color: #166534;
                border: 2px solid #86efac;
            }}
            
            .status-error {{
                background: linear-gradient(135deg, #fee2e2, #fecaca);
                color: #dc2626;
                border: 2px solid #f87171;
            }}
            
            .status-active {{
                background: linear-gradient(135deg, #fef3c7, #fde68a);
                color: #92400e;
                border: 2px solid #fbbf24;
            }}
            
            /* FIXED: Manual call button for better visibility */
            .manual-call-button {{
                position: relative;
                margin: 20px auto;
                width: 120px;
                height: 120px;
                border-radius: 50%;
                background: linear-gradient(135deg, #2E86AB, #A23B72);
                border: none;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                color: white;
                font-weight: bold;
                font-size: 0.9rem;
                box-shadow: 0 8px 25px rgba(46, 134, 171, 0.3);
                z-index: 1000;
            }}
            
            .manual-call-button:hover {{
                transform: scale(1.05);
                box-shadow: 0 12px 35px rgba(46, 134, 171, 0.4);
            }}
            
            .manual-call-button:disabled {{
                background: #94a3b8;
                cursor: not-allowed;
                transform: none;
            }}
            
            .call-icon {{
                font-size: 2rem;
                margin-bottom: 5px;
            }}
            
            .call-text {{
                font-size: 0.8rem;
                text-align: center;
                line-height: 1.2;
            }}
            
            /* Enhanced instructions */
            .ctc-instructions {{
                text-align: left;
                background: #f8fafc;
                padding: 25px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            
            .ctc-instructions h4 {{
                color: #2E86AB;
                margin-bottom: 15px;
                font-size: 1.2rem;
                text-align: center;
            }}
            
            .ctc-instructions ul {{
                list-style: none;
                padding: 0;
            }}
            
            .ctc-instructions li {{
                margin: 12px 0;
                padding-left: 30px;
                position: relative;
                color: #475569;
                line-height: 1.5;
            }}
            
            .ctc-instructions li::before {{
                content: "🎯";
                position: absolute;
                left: 0;
                font-size: 1.2rem;
            }}
            
            .ctc-controls {{
                margin: 25px 0;
                display: flex;
                gap: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }}
            
            .ctc-btn {{
                padding: 12px 24px;
                border-radius: 8px;
                border: none;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-decoration: none;
                display: inline-block;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, #2E86AB, #1e40af);
                color: white;
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(46, 134, 171, 0.3);
            }}
            
            .btn-secondary {{
                background: #f1f5f9;
                color: #475569;
                border: 1px solid #cbd5e0;
            }}
            
            .btn-secondary:hover {{
                background: #e2e8f0;
            }}
            
            .ctc-footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #64748b;
                font-size: 0.9rem;
            }}
            
            .pulse {{
                animation: pulse 2s infinite;
            }}
            
            @keyframes pulse {{
                0% {{ transform: scale(1); }}
                50% {{ transform: scale(1.05); }}
                100% {{ transform: scale(1); }}
            }}
            
            /* Debug info */
            .debug-info {{
                background: #f1f5f9;
                border: 1px solid #cbd5e0;
                border-radius: 8px;
                padding: 15px;
                margin: 20px 0;
                font-family: monospace;
                font-size: 0.8rem;
                text-align: left;
            }}
            
            /* Mobile responsive */
            @media (max-width: 768px) {{
                .ctc-container {{
                    padding: 20px;
                }}
                
                .ctc-title {{
                    font-size: 1.5rem;
                }}
                
                .manual-call-button {{
                    width: 100px;
                    height: 100px;
                }}
                
                .call-icon {{
                    font-size: 1.5rem;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="ctc-container">
            <div class="ctc-header">
                <h2 class="ctc-title">🏥 CTC Health Voice Assistant</h2>
                <p class="ctc-subtitle">Advanced Medical Training Platform</p>
            </div>
            
            <div class="ctc-persona-info">
                <h4>📋 Training Assistant Details</h4>
                <p><strong>Persona:</strong> {persona_name}</p>
                <p><strong>Platform:</strong> CTC Health Solution</p>
                <p><strong>Type:</strong> Interactive Voice Training</p>
                <p><strong>Assistant ID:</strong> <code>{assistant_id[:12]}...</code></p>
            </div>
            
            <div id="ctc-status" class="ctc-status status-loading pulse">
                🔄 Initializing CTC Health voice system...
            </div>
            
            <!-- FIXED: Manual call button with better visibility -->
            <button id="manual-call-btn" class="manual-call-button" onclick="startVoiceCall()" disabled>
                <div class="call-icon">📞</div>
                <div class="call-text">Start<br>Training</div>
            </button>
            
            <div class="ctc-controls">
                <button id="mic-request" class="ctc-btn btn-primary" onclick="requestMicAccess()" style="display: none;">
                    🎙️ Enable Microphone
                </button>
                <button id="test-connection" class="ctc-btn btn-secondary" onclick="testConnection()">
                    🔧 Test Connection
                </button>
                <button id="refresh-component" class="ctc-btn btn-secondary" onclick="refreshComponent()">
                    🔄 Refresh
                </button>
            </div>
            
            <div class="ctc-instructions">
                <h4>💡 How to Use Your Training Assistant</h4>
                <ul>
                    <li><strong>Wait</strong> for the green "Ready" status above</li>
                    <li><strong>Click</strong> the large "Start Training" button when enabled</li>
                    <li><strong>Grant</strong> microphone access when prompted by browser</li>
                    <li><strong>Speak clearly</strong> during your training conversation</li>
                    <li><strong>Practice</strong> realistic medical scenarios with your AI persona</li>
                </ul>
            </div>
            
            <!-- Debug information -->
            <div class="debug-info" id="debug-info" style="display: none;">
                <strong>Debug Info:</strong><br>
                <span id="debug-content">Initializing...</span>
            </div>
            
            <div class="ctc-footer">
                <p><strong>CTC Health Solution</strong> • Professional Medical Training Platform</p>
                <p>Session ID: <code>{component_id}</code></p>
            </div>
        </div>

        <script>
            // Configuration with validation
            const ASSISTANT_ID = "{assistant_id}";
            const PUBLIC_KEY = "{public_key}";
            const COMPONENT_ID = "{component_id}";
            
            console.log('🏥 CTC Health: Voice component initialized');
            console.log('Assistant ID:', ASSISTANT_ID);
            console.log('Public Key length:', PUBLIC_KEY ? PUBLIC_KEY.length : 0);
            console.log('Component ID:', COMPONENT_ID);
            
            // State management
            let isVapiLoaded = false;
            let isMicrophoneReady = false;
            let vapiInstance = null;
            let isCallActive = false;
            let debugMode = false;
            
            // Enhanced VAPI button configuration - DISABLED for manual control
            const buttonConfig = null; // We'll use manual button instead
            
            // Utility functions
            function updateStatus(message, type = 'loading') {{
                const statusEl = document.getElementById('ctc-status');
                const callBtn = document.getElementById('manual-call-btn');
                
                if (statusEl) {{
                    statusEl.className = `ctc-status status-${{type}}`;
                    statusEl.innerHTML = message;
                    
                    if (type === 'ready') {{
                        statusEl.classList.remove('pulse');
                        if (callBtn) callBtn.disabled = false;
                    }} else if (type === 'loading') {{
                        statusEl.classList.add('pulse');
                        if (callBtn) callBtn.disabled = true;
                    }} else if (type === 'error') {{
                        statusEl.classList.remove('pulse');
                        if (callBtn) callBtn.disabled = true;
                    }}
                }}
                
                updateDebugInfo(`Status: ${{type}} - ${{message}}`);
                console.log(`CTC Health Status: ${{type}} - ${{message}}`);
            }}
            
            function updateDebugInfo(info) {{
                const debugEl = document.getElementById('debug-content');
                if (debugEl && debugMode) {{
                    const timestamp = new Date().toLocaleTimeString();
                    debugEl.innerHTML += `<br>[${{timestamp}}] ${{info}}`;
                }}
            }}
            
            // Enable debug mode on triple click
            document.addEventListener('click', function(e) {{
                if (e.detail === 3) {{
                    debugMode = !debugMode;
                    document.getElementById('debug-info').style.display = debugMode ? 'block' : 'none';
                    console.log('Debug mode:', debugMode ? 'enabled' : 'disabled');
                }}
            }});
            
            // FIXED: Manual call function with better error handling
            async function startVoiceCall() {{
                const callBtn = document.getElementById('manual-call-btn');
                
                if (!vapiInstance) {{
                    updateStatus('❌ Voice system not ready. Try refreshing.', 'error');
                    return;
                }}
                
                try {{
                    if (!isCallActive) {{
                        updateStatus('📞 Starting training call...', 'loading');
                        updateDebugInfo('Attempting to start call manually');
                        
                        // Start call with the assistant
                        await vapiInstance.start({{
                            assistantId: ASSISTANT_ID
                        }});
                        
                        isCallActive = true;
                        callBtn.innerHTML = '<div class="call-icon">📱</div><div class="call-text">End<br>Training</div>';
                        callBtn.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                        updateStatus('🎙️ Training call active - speak clearly', 'active');
                        
                    }} else {{
                        updateStatus('📞 Ending training call...', 'loading');
                        updateDebugInfo('Ending call manually');
                        
                        await vapiInstance.stop();
                        
                        isCallActive = false;
                        callBtn.innerHTML = '<div class="call-icon">📞</div><div class="call-text">Start<br>Training</div>';
                        callBtn.style.background = 'linear-gradient(135deg, #2E86AB, #A23B72)';
                        updateStatus('✅ Training call ended - ready for new session', 'ready');
                    }}
                    
                }} catch (error) {{
                    console.error('❌ CTC Health: Call error:', error);
                    updateStatus('❌ Call failed: ' + error.message, 'error');
                    updateDebugInfo('Call error: ' + error.toString());
                    
                    // Reset button state
                    isCallActive = false;
                    callBtn.innerHTML = '<div class="call-icon">📞</div><div class="call-text">Start<br>Training</div>';
                    callBtn.style.background = 'linear-gradient(135deg, #2E86AB, #A23B72)';
                }}
            }}
            
            // Enhanced microphone access request
            async function requestMicAccess() {{
                updateStatus('🎙️ Requesting microphone access...', 'loading');
                updateDebugInfo('Requesting microphone access');
                
                try {{
                    const stream = await navigator.mediaDevices.getUserMedia({{
                        audio: {{
                            echoCancellation: true,
                            noiseSuppression: true,
                            sampleRate: 44100
                        }}
                    }});
                    
                    console.log('✅ CTC Health: Microphone access granted');
                    isMicrophoneReady = true;
                    
                    // Hide mic button
                    document.getElementById('mic-request').style.display = 'none';
                    
                    updateStatus('✅ Microphone ready! Voice system operational.', 'ready');
                    updateDebugInfo('Microphone access granted');
                    
                    // Initialize VAPI now
                    if (isVapiLoaded) {{
                        initializeVapiFixed();
                    }}
                    
                }} catch (error) {{
                    console.error('❌ CTC Health: Microphone error:', error);
                    updateDebugInfo('Microphone error: ' + error.toString());
                    
                    let errorMsg = '❌ Microphone access denied. ';
                    
                    if (error.name === 'NotAllowedError') {{
                        errorMsg += 'Please allow microphone access in your browser settings.';
                    }} else if (error.name === 'NotFoundError') {{
                        errorMsg += 'No microphone found. Check your audio settings.';
                    }} else if (error.name === 'NotSupportedError') {{
                        errorMsg += 'Browser not supported or insecure context (need HTTPS).';
                    }} else {{
                        errorMsg += 'Check browser microphone permissions.';
                    }}
                    
                    updateStatus(errorMsg, 'error');
                }}
            }}
            
            // Check microphone permissions with better error handling
            async function checkMicPermissions() {{
                updateDebugInfo('Checking microphone permissions');
                
                if (!navigator.mediaDevices?.getUserMedia) {{
                    updateStatus('❌ Voice features not supported in this browser', 'error');
                    updateDebugInfo('getUserMedia not supported');
                    return false;
                }}
                
                // Check if we're in a secure context
                if (!window.isSecureContext) {{
                    updateStatus('❌ Voice features require HTTPS connection', 'error');
                    updateDebugInfo('Insecure context - HTTPS required');
                    return false;
                }}
                
                try {{
                    const result = await navigator.permissions.query({{ name: 'microphone' }});
                    console.log('🔍 CTC Health: Microphone permission:', result.state);
                    updateDebugInfo('Permission state: ' + result.state);
                    
                    if (result.state === 'granted') {{
                        isMicrophoneReady = true;
                        return true;
                    }} else if (result.state === 'prompt') {{
                        document.getElementById('mic-request').style.display = 'inline-block';
                        updateStatus('🎙️ Microphone access required for voice training', 'loading');
                        return false;
                    }} else {{
                        updateStatus('❌ Microphone blocked in browser settings', 'error');
                        return false;
                    }}
                }} catch (error) {{
                    console.warn('⚠️ CTC Health: Could not check permissions:', error);
                    updateDebugInfo('Permission check failed: ' + error.toString());
                    document.getElementById('mic-request').style.display = 'inline-block';
                    updateStatus('🎙️ Click to enable microphone for voice training', 'loading');
                    return false;
                }}
            }}
            
            // Test connection with better validation
            function testConnection() {{
                updateStatus('🔍 Testing CTC Health platform connectivity...', 'loading');
                updateDebugInfo('Testing connection');
                
                // Test 1: Check if we have valid configuration
                if (!ASSISTANT_ID || !PUBLIC_KEY) {{
                    updateStatus('❌ Invalid configuration - missing API credentials', 'error');
                    updateDebugInfo('Missing credentials - Assistant ID: ' + !!ASSISTANT_ID + ', Public Key: ' + !!PUBLIC_KEY);
                    return;
                }}
                
                // Test 2: Check network connectivity
                fetch('https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js', {{
                    method: 'HEAD',
                    cache: 'no-cache'
                }})
                .then(response => {{
                    updateDebugInfo('CDN response: ' + response.status);
                    if (response.ok) {{
                        updateStatus('✅ CTC Health platform connectivity confirmed', 'ready');
                        
                        // Test 3: Try to validate API key format
                        if (PUBLIC_KEY.length < 20 || PUBLIC_KEY.includes('YOUR_')) {{
                            updateStatus('⚠️ API key appears invalid - check configuration', 'error');
                            updateDebugInfo('Suspicious API key format');
                        }}
                    }} else {{
                        updateStatus('❌ Platform connectivity issues detected', 'error');
                    }}
                }})
                .catch(error => {{
                    updateDebugInfo('Network error: ' + error.toString());
                    updateStatus('❌ Network connectivity issues. Check internet connection.', 'error');
                }});
            }}
            
            // Refresh component
            function refreshComponent() {{
                updateStatus('🔄 Refreshing CTC Health voice system...', 'loading');
                updateDebugInfo('Manual refresh requested');
                setTimeout(() => {{
                    location.reload();
                }}, 1000);
            }}
            
            // FIXED: Initialize VAPI with manual control instead of auto-button
            function initializeVapiFixed() {{
                if (!window.vapiSDK) {{
                    console.log('⚠️ CTC Health: VAPI SDK not loaded yet');
                    updateDebugInfo('VAPI SDK not loaded');
                    return;
                }}
                
                try {{
                    console.log('📦 CTC Health: Initializing voice system (manual mode)...');
                    updateDebugInfo('Initializing VAPI in manual mode');
                    
                    // Create VAPI instance WITHOUT auto-button
                    vapiInstance = new window.vapiSDK.Vapi({{
                        apiKey: PUBLIC_KEY
                    }});
                    
                    // Add enhanced event listeners
                    vapiInstance.on('call-start', () => {{
                        console.log('🎙️ CTC Health: Training session started');
                        updateStatus('🎙️ Training session active - conversation in progress', 'active');
                        updateDebugInfo('Call started');
                        isCallActive = true;
                    }});
                    
                    vapiInstance.on('call-end', () => {{
                        console.log('✅ CTC Health: Training session ended');
                        updateStatus('✅ Training session completed - ready for new session', 'ready');
                        updateDebugInfo('Call ended');
                        isCallActive = false;
                        
                        // Reset button
                        const callBtn = document.getElementById('manual-call-btn');
                        if (callBtn) {{
                            callBtn.innerHTML = '<div class="call-icon">📞</div><div class="call-text">Start<br>Training</div>';
                            callBtn.style.background = 'linear-gradient(135deg, #2E86AB, #A23B72)';
                        }}
                    }});
                    
                    vapiInstance.on('speech-start', () => {{
                        console.log('🗣️ CTC Health: AI assistant speaking');
                        updateDebugInfo('AI speech started');
                    }});
                    
                    vapiInstance.on('speech-end', () => {{
                        console.log('🎤 CTC Health: AI assistant finished speaking');
                        updateDebugInfo('AI speech ended');
                    }});
                    
                    vapiInstance.on('error', (error) => {{
                        console.error('❌ CTC Health: Voice system error:', error);
                        updateStatus('❌ Voice system error: ' + error.message, 'error');
                        updateDebugInfo('VAPI error: ' + error.toString());
                        isCallActive = false;
                    }});
                    
                    vapiInstance.on('volume-level', (volume) => {{
                        // Visual feedback for volume levels (optional)
                        if (volume > 0.3) {{
                            // User is speaking
                            updateDebugInfo('User speaking (volume: ' + volume.toFixed(2) + ')');
                        }}
                    }});
                    
                    updateStatus('🎉 CTC Health assistant ready! Click "Start Training" to begin.', 'ready');
                    updateDebugInfo('VAPI initialized successfully');
                    console.log('✅ CTC Health: Voice system initialized successfully (manual mode)');
                    
                }} catch (error) {{
                    console.error('❌ CTC Health: Initialization error:', error);
                    updateStatus('❌ Voice system initialization failed: ' + error.message, 'error');
                    updateDebugInfo('Initialization error: ' + error.toString());
                }}
            }}
            
            // FIXED: Load VAPI SDK with better error handling
            (function loadVapiSDK() {{
                updateDebugInfo('Loading VAPI SDK');
                
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js';
                script.defer = true;
                script.async = true;
                
                script.onload = function() {{
                    console.log('📦 CTC Health: VAPI SDK loaded successfully');
                    updateDebugInfo('VAPI SDK loaded');
                    isVapiLoaded = true;
                    
                    if (isMicrophoneReady) {{
                        initializeVapiFixed();
                    }} else {{
                        updateStatus('⚠️ Microphone access required for voice training', 'loading');
                    }}
                }};
                
                script.onerror = function() {{
                    console.error('❌ CTC Health: Failed to load voice SDK');
                    updateStatus('❌ Failed to load voice system. Check internet connection.', 'error');
                    updateDebugInfo('SDK loading failed');
                }};
                
                document.head.appendChild(script);
                
                // Safety timeout with more specific error
                setTimeout(() => {{
                    if (!isVapiLoaded) {{
                        updateStatus('⏱️ Loading timeout. Network or firewall blocking SDK.', 'error');
                        updateDebugInfo('SDK loading timeout');
                    }}
                }}, 15000);
            }})();
            
            // Initialize on load
            document.addEventListener('DOMContentLoaded', async function() {{
                console.log('🎯 CTC Health: Voice component ready');
                updateDebugInfo('DOM loaded');
                
                const config = {{
                    assistantId: ASSISTANT_ID,
                    publicKeyLength: PUBLIC_KEY ? PUBLIC_KEY.length : 0,
                    componentId: COMPONENT_ID,
                    secureContext: window.isSecureContext,
                    timestamp: new Date().toISOString()
                }};
                
                console.log('🔧 Configuration:', config);
                updateDebugInfo('Config: ' + JSON.stringify(config));
                
                // Check microphone permissions immediately
                await checkMicPermissions();
            }});
            
            // Enhanced communication with Streamlit parent
            window.addEventListener('message', function(event) {{
                if (event.data.type === 'ctc-refresh') {{
                    refreshComponent();
                }} else if (event.data.type === 'ctc-debug') {{
                    debugMode = event.data.enabled;
                    document.getElementById('debug-info').style.display = debugMode ? 'block' : 'none';
                }}
            }});
            
            // Send enhanced status updates to Streamlit
            function sendStatusToStreamlit(status, type, extra = {{}}) {{
                if (window.parent) {{
                    window.parent.postMessage({{
                        type: 'ctc-status-update',
                        status: status,
                        statusType: type,
                        assistantId: ASSISTANT_ID,
                        componentId: COMPONENT_ID,
                        isCallActive: isCallActive,
                        isMicrophoneReady: isMicrophoneReady,
                        isVapiLoaded: isVapiLoaded,
                        timestamp: Date.now(),
                        ...extra
                    }}, '*');
                }}
            }}
            
            // Override updateStatus to also send to Streamlit with more data
            const originalUpdateStatus = updateStatus;
            updateStatus = function(message, type = 'loading') {{
                originalUpdateStatus(message, type);
                sendStatusToStreamlit(message, type, {{
                    debugMode: debugMode,
                    secureContext: window.isSecureContext
                }});
            }};
        </script>
    </body>
    </html>
    """
    
    return vapi_html

def create_assistant_testing_page():
    """
    Creates the FIXED integrated testing page with better error handling.
    """
    
    st.subheader("🎯 Test Your CTC Health Assistant")
    
    # Load and validate API keys
    vapi_private_key = os.getenv("VAPI_PRIVATE_KEY") 
    vapi_public_key = os.getenv("VAPI_PUBLIC_KEY")
    
    if not vapi_private_key or not vapi_public_key:
        st.error("⚠️ CTC Health voice system keys not found in .env file.")
        with st.expander("🔧 Configuration Help"):
            st.code("""
            # Add to your .env file:
            VAPI_PRIVATE_KEY=your_private_key_here
            VAPI_PUBLIC_KEY=your_public_key_here
            """)
            st.markdown("""
            **To get your VAPI keys:**
            1. Go to [VAPI Dashboard](https://dashboard.vapi.ai)
            2. Create an account or log in
            3. Copy your Private Key and Public Key
            4. Add them to your `.env` file
            """)
        return
    
    # Validate API keys
    key_issues = []
    if "YOUR_VAPI" in str(vapi_private_key) or len(str(vapi_private_key)) < 20:
        key_issues.append("Private key appears to be invalid or placeholder")
    if "YOUR_VAPI" in str(vapi_public_key) or len(str(vapi_public_key)) < 20:
        key_issues.append("Public key appears to be invalid or placeholder")
    
    if key_issues:
        st.error("❌ API Key Issues:")
        for issue in key_issues:
            st.write(f"• {issue}")
        return
    
    # Create layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.success("🎉 Your CTC Health Assistant is ready for integrated testing!")
        
        # Add connection status indicator
        status_placeholder = st.empty()
        
        # FIXED: Use improved widget component
        widget_html = create_vapi_widget_component_fixed(
            assistant_id=st.session_state.assistant_id,
            public_key=vapi_public_key,
            persona_name=st.session_state.persona_name
        )
        
        # Render with increased height for better button visibility
        components.html(widget_html, height=750, scrolling=False)
        
        # Real-time status monitoring
        with st.container():
            st.markdown("### 📊 System Status & Troubleshooting")
            
            # JavaScript to communicate with the embedded component
            status_js = """
            <script>
            let lastStatusUpdate = null;
            
            // Listen for status updates from the embedded component
            window.addEventListener('message', function(event) {
                if (event.data.type === 'ctc-status-update') {
                    lastStatusUpdate = event.data;
                    console.log('Status update received:', event.data);
                    
                    // You can add real-time status display here
                    if (event.data.statusType === 'error') {
                        console.warn('Error detected in voice component:', event.data.status);
                    }
                }
            });
            
            // Debug function accessible from console
            window.ctcDebug = function() {
                console.log('Last status:', lastStatusUpdate);
                
                // Send debug enable to iframe
                const iframe = document.querySelector('iframe[title*="stHTML"]');
                if (iframe) {
                    iframe.contentWindow.postMessage({type: 'ctc-debug', enabled: true}, '*');
                }
            };
            
            console.log('CTC Health Debug: Run ctcDebug() in console for detailed info');
            </script>
            """
            components.html(status_js, height=0)
            
            # Troubleshooting tips
            with st.expander("🛠️ Troubleshooting Tips", expanded=False):
                st.markdown("""
                **If you see "Voice system error":**
                1. **Check API Keys**: Make sure your VAPI keys are valid and not placeholders
                2. **HTTPS Required**: Voice features require HTTPS - deploy to secure environment
                3. **Browser Compatibility**: Use Chrome, Firefox, or Edge (latest versions)
                4. **Microphone Access**: Click "Enable Microphone" button when it appears
                5. **Network/Firewall**: Ensure CDN access to `cdn.jsdelivr.net` is allowed
                
                **If the call button is not visible:**
                1. Look for the large blue "Start Training" button in the widget
                2. The button is disabled until system is ready (green status)
                3. Scroll down in the widget if needed
                
                **Debug Mode:**
                - Triple-click anywhere in the widget to enable debug mode
                - Check browser console (F12) for detailed logs
                - Run `ctcDebug()` in browser console for status info
                """)
    
    with col2:
        st.markdown("### 🛠️ Controls & Info")
        
        # Assistant information with validation
        with st.expander("ℹ️ Assistant Details", expanded=True):
            st.code(f"ID: {st.session_state.assistant_id}")
            st.markdown(f"**Persona:** {st.session_state.persona_name}")
            st.markdown(f"**Platform:** CTC Health Solution")
            st.markdown(f"**Type:** Integrated Voice Training")
            st.markdown(f"**Created:** {time.strftime('%d/%m/%Y %H:%M')}")
            
            # API key validation status
            if HTML_UTILS_AVAILABLE:
                try:
                    validation = validate_vapi_credentials(vapi_public_key, vapi_private_key)
                    if validation["valid"]:
                        st.success("✅ API credentials validated")
                    else:
                        st.warning("⚠️ API credential issues:")
                        for error in validation["errors"]:
                            st.write(f"• {error}")
                except Exception as e:
                    st.info(f"Note: Could not validate credentials")
        
        # Advanced controls
        with st.expander("🔧 Advanced Options"):
            if st.button("🔄 Create New Assistant", help="Generate a new assistant with the same persona", use_container_width=True):
                with st.spinner("Creating new assistant..."):
                    assistant_name = f"CTC-Health-Assistant-{int(time.time())}"
                    new_assistant_id = autoprompt.create_vapi_assistant(
                        api_key=vapi_private_key,
                        system_prompt=st.session_state.final_prompt,
                        name=assistant_name
                    )
                    if new_assistant_id:
                        st.session_state.assistant_id = new_assistant_id
                        st.success(f"✅ New assistant created!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to create new assistant.")
            
            if st.button("♻️ Refresh Voice Widget", help="Refresh the integrated voice component", use_container_width=True):
                # Send refresh message to embedded component
                refresh_js = """
                <script>
                const iframe = document.querySelector('iframe[title*="stHTML"]');
                if (iframe) {
                    iframe.contentWindow.postMessage({type: 'ctc-refresh'}, '*');
                }
                </script>
                """
                components.html(refresh_js, height=0)
                st.success("🔄 Voice widget refreshed!")
            
            # Toggle debug mode
            if st.button("🐛 Enable Debug Mode", help="Enable detailed logging in widget", use_container_width=True):
                debug_js = """
                <script>
                const iframe = document.querySelector('iframe[title*="stHTML"]');
                if (iframe) {
                    iframe.contentWindow.postMessage({type: 'ctc-debug', enabled: true}, '*');
                }
                console.log('Debug mode enabled in voice widget');
                </script>
                """
                components.html(debug_js, height=0)
                st.info("🐛 Debug mode enabled - check widget for debug info")
            
            st.download_button(
                label="⬇️ Download System Prompt",
                data=st.session_state.final_prompt,
                file_name=f"ctc_health_prompt_{int(time.time())}.md",
                mime="text/markdown",
                help="Download the generated system prompt as markdown file",
                use_container_width=True
            )
        
        # Enhanced fallback option
        with st.expander("📁 Fallback Options"):
            st.markdown("**If integrated testing has issues:**")
            
            if HTML_UTILS_AVAILABLE:
                if st.button("⬇️ Generate Standalone HTML", help="Create downloadable HTML file as backup", use_container_width=True):
                    try:
                        html_content, file_path = generate_vapi_test_page(
                            assistant_id=st.session_state.assistant_id,
                            public_key=vapi_public_key,
                            persona_name=st.session_state.persona_name
                        )
                        
                        st.download_button(
                            label="💾 Download Standalone File",
                            data=html_content,
                            file_name=f"ctc_health_standalone_{int(time.time())}.html",
                            mime="text/html",
                            use_container_width=True,
                            help="Download and open this file directly in your browser"
                        )
                        st.success("✅ Standalone file generated!")
                        st.info("💡 The standalone file will work even if the integrated version has issues.")
                        
                    except Exception as e:
                        st.error(f"❌ Standalone generation failed: {e}")
            else:
                st.info("Install html_generator.py for standalone file generation")
        
        # Usage instructions
        st.markdown("### 💡 Usage Instructions")
        st.markdown("""
        **🚀 Quick Start (Fixed Version):**
        1. **Wait** for green "Ready" status in the widget
        2. **Click** the large blue "Start Training" button
        3. **Allow** microphone access when browser prompts
        4. **Speak clearly** during training conversation
        5. **Click** button again to end session
        
        **🔧 If you encounter issues:**
        - Enable debug mode for detailed error info
        - Use "Test Connection" button to verify connectivity  
        - Try the standalone HTML file as fallback
        - Check browser console (F12) for detailed logs
        
        **✨ Fixed in this version:**
        - Manual call button always visible
        - Better error messages and debugging
        - Enhanced microphone permission handling
        - HTTPS/security context validation
        - Improved mobile responsiveness
        """)

# Main App Layout (same as before but with fixed widget)
st.title("🏥 CTC Health Solution - Medical Training Platform")
st.markdown("""
Welcome to **CTC Health Solution's** advanced medical training platform! This integrated system uses 
multi-agent AI to create realistic medical professional personas and provides **seamless voice testing** 
directly within the application.

**🔧 New: Fixed Integration** - Improved error handling and manual call button for better reliability!
""")

# Custom CSS (same as before)
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #2E86AB 0%, #A23B72 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .step-header {
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    
    .success-banner {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        border: 1px solid #86efac;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #2E86AB, #1e40af);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(46, 134, 171, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# --- Same UI flow as before with session state management ---

# Step 1: Persona Header
st.markdown('<h2 class="step-header">Step 1: Medical Professional Header</h2>', unsafe_allow_html=True)
header_input = st.text_area(
    "Provide basic details for the medical professional persona:",
    "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
    help="Name, Title, Age, Gender, Practice Setting, Geography - AI will complete missing details",
    height=100
)

# Step 2: Customer Segmentation
st.markdown('<h2 class="step-header">Step 2: Customer Segmentation</h2>', unsafe_allow_html=True)
segment_options = get_segment_options()
segment_choice = st.radio(
    "Select a customer segment for this persona:",
    options=segment_options,
    format_func=lambda x: x.split('\n')[0].replace('###','').strip()
)

if segment_choice:
    with st.expander("📋 View Selected Segment Description", expanded=False):
        st.markdown(segment_choice)

# Step 3: Clinical Context
st.markdown('<h2 class="step-header">Step 3: Clinical Context</h2>', unsafe_allow_html=True)
st.info("""
**Key areas to describe:**
• Therapeutic Area/Sub-specialty • Patient Mix & Demographics • Clinical Drivers & Priorities • Practice Metrics & KPIs
""")

context_input = st.text_area(
    "Describe the clinical practice context:",
    "Specializes in late-stage lung cancer. Sees a mix of newly diagnosed and treatment-experienced patients.",
    help="Therapeutic area, patient mix, clinical drivers, practice metrics",
    height=100
)

# Step 4: Psychographics (Streamlined UI)
st.markdown('<h2 class="step-header">Step 4: Psychographics & Motivations</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    risk_tolerance = st.slider("Risk Tolerance", 0.0, 1.0, 0.7, step=0.1, 
                              format="%.1f", help="0=Conservative, 1=Bold Experimenter")
    research_orientation = st.slider("Research Orientation", 0.0, 1.0, 0.8, step=0.1, 
                                   format="%.1f", help="0=Anecdote-driven, 1=Data-heavy")
    patient_empathy = st.slider("Patient Empathy", 0.0, 1.0, 0.9, step=0.1, 
                               format="%.1f", help="0=Transactional, 1=Advocate")

with col2:
    brand_loyalty = st.slider("Brand Loyalty", 0.0, 1.0, 0.3, step=0.1, 
                             format="%.1f", help="0=Low, 1=High")
    recognition_need = st.slider("Recognition Need", 0.0, 1.0, 0.2, step=0.1, 
                                format="%.1f", help="0=Seeks podium, 1=Low-profile")

# Step 5: Product & Objectives
st.markdown('<h2 class="step-header">Step 5: Product & Training Objectives</h2>', unsafe_allow_html=True)
st.info("""
**Key areas to describe:**
• Product Focus • Training Objectives • Key Messages • Anticipated Objections • Competitor Landscape • Desired Skills
""")

objectives_input = st.text_area(
    "Describe the product and training objectives:",
    "The product is a new immunotherapy, Xaltorvima. The rep needs to handle objections about its novel mechanism of action.",
    help="Product details, training goals, key messages, objections, competitors",
    height=100
)

# Initialize session state
if 'persona_details' not in st.session_state:
    st.session_state.persona_details = None
if 'final_prompt' not in st.session_state:
    st.session_state.final_prompt = ""
if 'assistant_id' not in st.session_state:
    st.session_state.assistant_id = None
if 'persona_name' not in st.session_state:
    st.session_state.persona_name = ""

# Processing workflow
st.markdown("---")

# Step 1: Build Persona Details
if not st.session_state.persona_details:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🧠 Build Medical Persona Details", type="primary"):
            psychographics_input_str = f"""
        - Risk Tolerance: {risk_tolerance} (0=Conservative, 1=Bold Experimenter)
        - Brand Loyalty: {brand_loyalty} (0=Low, 1=High)
        - Research Orientation: {research_orientation} (0=Anecdote-driven, 1=Data-heavy)
        - Recognition Need: {recognition_need} (0=Seeks podium, 1=Low-profile)  
        - Patient Empathy: {patient_empathy} (0=Transactional, 1=Advocate)
        """

            with st.spinner("🤖 CTC Health AI agents are analyzing and building your medical persona..."):
                persona_state = autoprompt.build_persona_details(
                    header_input=header_input,
                    segment_input=segment_choice,
                    context_input=context_input,
                    psychographics_input=psychographics_input_str,
                    objectives_input=objectives_input
                )
                st.session_state.persona_details = persona_state
                
                # Extract persona name
                if persona_state and 'persona_header' in persona_state:
                    header_text = persona_state['persona_header']
                    if 'Dr.' in header_text:
                        name_part = header_text.split('Dr.')[1].split(',')[0].split(' is a')[0].strip()
                        st.session_state.persona_name = f"Dr. {name_part}"
                    else:
                        st.session_state.persona_name = "Generated Medical Persona"
            
            st.balloons()
            st.success("🎉 Medical persona details created successfully!")
            st.rerun()

# Step 2: Show persona and generate prompt
if st.session_state.persona_details:
    st.markdown('<div class="success-banner">', unsafe_allow_html=True)
    st.markdown("### ✅ Medical Persona Details Completed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.expander("📋 Review Generated Persona Details", expanded=False):
        st.markdown(st.session_state.persona_details['full_persona_details'])

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Generate Final Training Prompt", type="primary"):
            with st.spinner("🤖 CTC Health AI writers are crafting the comprehensive training prompt..."):
                final_prompt = autoprompt.generate_final_prompt(st.session_state.persona_details)
                st.session_state.final_prompt = final_prompt
            
            st.balloons()
            st.success("🎉 Training prompt generated successfully!")
            st.rerun()

# Step 3: Create assistant and FIXED integrated testing
if st.session_state.final_prompt:
    st.markdown('<div class="success-banner">', unsafe_allow_html=True)
    st.markdown("### ✅ Training Prompt Ready for Deployment")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<h2 class="step-header">Step 6: Create & Test Your Assistant (Fixed Integration)</h2>', unsafe_allow_html=True)
    
    vapi_private_key = os.getenv("VAPI_PRIVATE_KEY")
    vapi_public_key = os.getenv("VAPI_PUBLIC_KEY")

    if not vapi_private_key or not vapi_public_key or "YOUR_VAPI" in str(vapi_private_key):
        st.error("⚠️ CTC Health voice system credentials not configured.")
        with st.expander("🔧 Configuration Instructions"):
            st.code("""
            # Add to your .env file:
            VAPI_PRIVATE_KEY=your_private_key_here
            VAPI_PUBLIC_KEY=your_public_key_here
            """)
    else:
        # Create assistant if not exists
        if not st.session_state.assistant_id:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("🎙️ Create CTC Health Voice Assistant", type="primary"):
                    with st.spinner("🔧 Creating your personalized medical training assistant..."):
                        assistant_name = f"CTC-Health-Medical-{int(time.time())}"
                        assistant_id = autoprompt.create_vapi_assistant(
                            api_key=vapi_private_key,
                            system_prompt=st.session_state.final_prompt,
                            name=assistant_name
                        )
                        if assistant_id:
                            st.session_state.assistant_id = assistant_id
                            st.balloons()
                            st.success(f"✅ Medical training assistant created successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to create assistant. Check your API keys.")
        
        # FIXED integrated testing interface
        if st.session_state.assistant_id:
            st.markdown("---")
            # This uses the FIXED widget with manual button and better error handling
            create_assistant_testing_page()
            
            # Cleanup in background
            if HTML_UTILS_AVAILABLE:
                try:
                    cleanup_old_test_files()
                except:
                    pass  # Silent cleanup