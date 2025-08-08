
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



# # app.py
# import streamlit as st
# import autoprompt
# from langchain_openai import ChatOpenAI
# import time
# import streamlit.components.v1 as components
# import os
# from dotenv import load_dotenv
# import base64

# load_dotenv()

# st.set_page_config(layout="wide", page_title="Persona Prompt Generator")

# def get_segment_options():
#     """Helper to read segment options from the markdown file."""
#     content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
#     return [seg.strip() for seg in content.split('---') if seg.strip()]

# def embed_vapi_widget(vapi_public_key, assistant_id, show_widget=True):
#     """
#     Embeds the Vapi Web Widget in the Streamlit app.
    
#     Args:
#         vapi_public_key: Your Vapi public API key
#         assistant_id: The ID of the created assistant
#         show_widget: Whether to show the widget immediately
#     """
    
#     # Personalizzazione del widget
#     widget_config = {
#         "position": "bottom-right",  # Posizione: bottom-right, bottom-left, top-right, top-left
#         "offset": "40px",  # Distanza dal bordo
#         "width": "50px",  # Larghezza del pulsante
#         "height": "50px",  # Altezza del pulsante
#         "buttonColor": "#0084ff",  # Colore del pulsante
#         "buttonTextColor": "#ffffff",  # Colore del testo/icona
#     }
    
#     vapi_html = f"""
#     <div id="vapi-widget-container">
#         <!-- Carica il Web Widget di Vapi -->
#         <script src="https://cdn.vapi.ai/widget.js"></script>
        
#         <script>
#         (function() {{
#             // Configurazione del widget
#             const config = {{
#                 apiKey: '{vapi_public_key}',
#                 assistantId: '{assistant_id}',
                
#                 // Configurazione UI
#                 position: '{widget_config["position"]}',
#                 offset: '{widget_config["offset"]}',
#                 width: '{widget_config["width"]}',
#                 height: '{widget_config["height"]}',
                
#                 // Stile personalizzato
#                 buttonColor: '{widget_config["buttonColor"]}',
#                 buttonTextColor: '{widget_config["buttonTextColor"]}',
                
#                 // Mostra automaticamente il widget
#                 show: {str(show_widget).lower()},
                
#                 // Modalità: 'voice' per solo voce, 'chat' per chat+voce
#                 mode: 'voice',
                
#                 // Callbacks per eventi
#                 onCallStart: function() {{
#                     console.log('Vapi: Chiamata iniziata');
#                     // Puoi aggiungere logica personalizzata qui
#                 }},
                
#                 onCallEnd: function() {{
#                     console.log('Vapi: Chiamata terminata');
#                     // Puoi aggiungere logica personalizzata qui
#                 }},
                
#                 onError: function(error) {{
#                     console.error('Vapi Error:', error);
#                     // Gestione errori
#                 }},
                
#                 onTranscript: function(transcript) {{
#                     console.log('Transcript:', transcript);
#                     // Puoi catturare il transcript se necessario
#                 }},
                
#                 // Messaggi personalizzati
#                 strings: {{
#                     title: "AI Assistant",
#                     subtitle: "Click to start voice conversation",
#                     endCallButton: "End Call",
#                     startCallButton: "Start Call"
#                 }}
#             }};
            
#             // Inizializza il widget
#             try {{
#                 window.vapiWidget = new Vapi.Widget(config);
#                 console.log('Vapi Widget initialized successfully');
                
#                 // Opzionale: Aggiungi un pulsante personalizzato per mostrare/nascondere il widget
#                 window.toggleVapiWidget = function() {{
#                     if (window.vapiWidget) {{
#                         window.vapiWidget.toggle();
#                     }}
#                 }};
                
#             }} catch (error) {{
#                 console.error('Failed to initialize Vapi Widget:', error);
#             }}
#         }})();
#         </script>
        
#         <!-- Container per eventuali elementi custom -->
#         <div style="position: fixed; top: 10px; right: 10px; z-index: 9998;">
#             <button 
#                 onclick="toggleVapiWidget()" 
#                 style="
#                     display: none; /* Nascosto di default, mostra se necessario */
#                     padding: 8px 16px;
#                     background: #0084ff;
#                     color: white;
#                     border: none;
#                     border-radius: 20px;
#                     cursor: pointer;
#                     font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#                     font-size: 14px;
#                     box-shadow: 0 2px 8px rgba(0,0,0,0.15);
#                 ">
#                 Toggle Assistant
#             </button>
#         </div>
#     </div>
    
#     <style>
#         /* Stili aggiuntivi per il widget se necessario */
#         #vapi-widget-container {{
#             position: relative;
#             z-index: 9999;
#         }}
#     </style>
#     """
    
#     # Renderizza il widget
#     components.html(vapi_html, height=0, scrolling=False)

# st.title("👨‍⚕️ Persona Prompt Generator")
# st.markdown("""
# Welcome to the Persona Prompt Generator! This tool uses a multi-agent system 
# to help you create a detailed doctor persona for role-playing scenarios.

# Follow the steps below to build your persona, then click "Generate System Prompt" at the bottom.
# """)

# # --- Main UI ---
# st.header("Step 1: Persona Header")
# header_input = st.text_area(
#     "Provide basic details for the doctor persona: Name, Title, Age, Gender, Practice Setting, and Geography.",
#     "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
#     help="You can provide partial info, and the AI will complete it."
# )

# st.header("Step 2: Customer Segmentation")
# segment_options = get_segment_options()
# # Use format_func to display only the title of the segment
# segment_choice = st.radio(
#     "Please select a customer segment for this persona:",
#     options=segment_options,
#     format_func=lambda x: x.split('\n')[0].replace('###','').strip()
# )

# # Display the description of the selected segment
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

# # The labels and help text are derived from 4psychographics.md
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

# if 'persona_details' not in st.session_state:
#     st.session_state.persona_details = None
# if 'final_prompt' not in st.session_state:
#     st.session_state.final_prompt = ""
# if 'assistant_id' not in st.session_state:
#     st.session_state.assistant_id = None
# if 'widget_shown' not in st.session_state:
#     st.session_state.widget_shown = False

# if not st.session_state.persona_details:
#     if st.button("📝 Build Persona Details", type="primary"):
#         # Format the psychographics input string from the slider values
#         psychographics_input_str = f"""
#     - Risk Tolerance: {risk_tolerance} (0=Conservative, 1=Bold Experimenter)
#     - Brand Loyalty: {brand_loyalty} (0=Low, 1=High)
#     - Research Orientation: {research_orientation} (0=Anecdote-driven, 1=Data-heavy)
#     - Recognition Need: {recognition_need} (0=Seeks podium, 1=Low-profile)
#     - Patient Empathy: {patient_empathy} (0=Transactional, 1=Advocate)
#     """

#         with st.spinner("🤖 The agents are building the persona... This may take a moment."):
#             # This function will be created in the next step inside autoprompt.py
#             persona_state = autoprompt.build_persona_details(
#                 header_input=header_input,
#                 segment_input=segment_choice,
#                 context_input=context_input,
#                 psychographics_input=psychographics_input_str,
#                 objectives_input=objectives_input
#             )
#             st.session_state.persona_details = persona_state
        
#         st.success("🎉 Persona Details Built!")

# if st.session_state.persona_details:
#     st.markdown("---")
#     st.subheader("Confirm Assembled Persona Details")
#     st.markdown(st.session_state.persona_details['full_persona_details'])

#     if st.button("🚀 Confirm and Generate Final Prompt", type="primary"):
#         with st.spinner("🤖 The writer agents are crafting the final prompt..."):
#             final_prompt = autoprompt.generate_final_prompt(st.session_state.persona_details)
#             st.session_state.final_prompt = final_prompt
#         st.success("🎉 System Prompt Generated!")

# if st.session_state.final_prompt:
#     st.markdown("---")
#     st.success("✅ Final prompt completed and is ready for use.")
    
#     st.markdown("---")
#     st.header("Step 6: Test with Vapi")
    
#     # Load keys from .env file
#     vapi_private_key = os.getenv("VAPI_PRIVATE_KEY")
#     vapi_public_key = os.getenv("VAPI_PUBLIC_KEY")

#     if not vapi_private_key or not vapi_public_key or "YOUR_VAPI" in vapi_private_key:
#         st.warning("⚠️ Vapi keys not found in .env file. Please add them to enable Vapi integration.")
#         st.code("""
# # Add to your .env file:
# VAPI_PRIVATE_KEY=your_private_key_here
# VAPI_PUBLIC_KEY=your_public_key_here
#         """)
#     else:
#         col1, col2 = st.columns(2)
        
#         with col1:
#             if st.button("🎙️ Create Vapi Assistant", type="primary", disabled=st.session_state.assistant_id is not None):
#                 with st.spinner("Creating Vapi assistant..."):
#                     # Use a unique name for the assistant to avoid conflicts
#                     assistant_name = f"Persona-Role-Play-{int(time.time())}"
#                     assistant_id = autoprompt.create_vapi_assistant(
#                         api_key=vapi_private_key,
#                         system_prompt=st.session_state.final_prompt,
#                         name=assistant_name
#                     )
#                     if assistant_id:
#                         st.session_state.assistant_id = assistant_id
#                         st.success(f"✅ Assistant created! ID: {assistant_id}")
#                         st.info("The voice assistant widget will appear in the bottom-right corner.")
#                         # Mostra automaticamente il widget dopo la creazione
#                         st.session_state.widget_shown = True
#                         st.rerun()
#                     else:
#                         st.error("❌ Failed to create Vapi assistant. Please check your API keys.")
        
#         with col2:
#             if st.session_state.assistant_id:
#                 if st.button("🔄 Create New Assistant", help="Create a new assistant with the same prompt"):
#                     st.session_state.assistant_id = None
#                     st.session_state.widget_shown = False
#                     st.rerun()
        
#         # Se l'assistente è stato creato, mostra il widget
#         if st.session_state.assistant_id and st.session_state.widget_shown:
#             st.markdown("---")
#             st.subheader("🎤 Voice Assistant Ready!")
            
#             # Informazioni per l'utente
#             with st.expander("ℹ️ How to use the voice assistant", expanded=True):
#                 st.markdown("""
#                 ### Instructions:
#                 1. **Look for the blue chat bubble** in the bottom-right corner of the page
#                 2. **Click on it** to start the voice conversation
#                 3. **Allow microphone access** when prompted by your browser
#                 4. **Start speaking** - the assistant will respond in real-time
#                 5. **Click the button again** to end the conversation
                
#                 ### Troubleshooting:
#                 - **Can't see the widget?** Try refreshing the page (F5)
#                 - **Microphone not working?** Check that you're on HTTPS and have granted permissions
#                 - **Widget not responding?** Check the browser console for errors (F12)
                
#                 ### Important:
#                 - The assistant is configured with your generated persona prompt
#                 - The conversation is completely private and secure
#                 - You can create a new assistant anytime with the button above
#                 """)
            
#             # Embed il widget Vapi
#             embed_vapi_widget(
#                 vapi_public_key=vapi_public_key,
#                 assistant_id=st.session_state.assistant_id,
#                 show_widget=True
#             )
            
#             # Mostra l'ID dell'assistente per riferimento
#             st.info(f"🤖 Assistant ID: `{st.session_state.assistant_id}`")
            
#             # Link alla dashboard Vapi
#             st.markdown(
#                 f"[View in Vapi Dashboard →](https://dashboard.vapi.ai/assistants/{st.session_state.assistant_id})",
#                 unsafe_allow_html=True
#             )


# # app.py - Versione semplificata SENZA backend

# import os
# import time
# import streamlit as st
# import streamlit.components.v1 as components
# from dotenv import load_dotenv
# import autoprompt
# from langchain_openai import ChatOpenAI
# import streamlit.components.v1 as components
# load_dotenv()

# st.set_page_config(layout="wide", page_title="Persona Prompt Generator")

# def get_segment_options():
#     """Helper to read segment options from the markdown file."""
#     content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
#     return [seg.strip() for seg in content.split('---') if seg.strip()]


# def embed_vapi_widget(vapi_public_key: str, assistant_id: str):
#     html = f"""
#     <script src="https://cdn.jsdelivr.net/npm/@vapi-ai/web@latest"></script>
#     <button id="vapi-btn" style="padding:10px 16px;border-radius:10px;border:0;cursor:pointer">
#       🎤 Avvia chiamata
#     </button>
#     <script>
#       const vapi = new window.Vapi("{vapi_public_key}");
#       let active = false;
#       const btn = document.getElementById('vapi-btn');

#       btn.addEventListener('click', async () => {{
#         try {{
#           if (!active) {{
#             await vapi.start("{assistant_id}");
#             active = true; btn.textContent = "⏹️ Ferma chiamata";
#           }} else {{
#             vapi.stop(); active = false; btn.textContent = "🎤 Avvia chiamata";
#           }}
#         }} catch (e) {{
#           console.error("Vapi error:", e);
#           alert(e?.message || "Errore Vapi");
#         }}
#       }});
#     </script>
#     """
#     components.html(html, height=80, scrolling=False)

# # TITOLO E INTRO
# st.title("👨‍⚕️ CTC Helath - Persona Prompt Generator")
# st.markdown("""
# Welcome to the Persona Prompt Generator! This tool uses a multi-agent system
# to help you create a detailed doctor persona for role-playing scenarios.
# """)

# # Aggiungi controllo chiavi all'inizio
# st.sidebar.header("🔑 API Keys Status")
# vapi_private_key = os.getenv("VAPI_PRIVATE_KEY", "")
# vapi_public_key = os.getenv("VAPI_PUBLIC_KEY", "")
# openai_key = os.getenv("OPENAI_API_KEY", "")

# if vapi_private_key:
#     st.sidebar.success("✅ VAPI_PRIVATE_KEY configured")
# else:
#     st.sidebar.error("❌ VAPI_PRIVATE_KEY missing")
    
# if vapi_public_key:
#     st.sidebar.success("✅ VAPI_PUBLIC_KEY configured")
# else:
#     st.sidebar.error("❌ VAPI_PUBLIC_KEY missing")
    
# if openai_key:
#     st.sidebar.success("✅ OPENAI_API_KEY configured")
# else:
#     st.sidebar.warning("⚠️ OPENAI_API_KEY missing")

# # Step 1: Persona Header
# st.header("Step 1: Persona Header")
# header_input = st.text_area(
#     "Provide basic details for the doctor persona:",
#     "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
#     help="You can provide partial info, and the AI will complete it."
# )

# # Step 2: Customer Segmentation
# st.header("Step 2: Customer Segmentation")
# segment_options = get_segment_options()
# segment_choice = st.radio(
#     "Please select a customer segment for this persona:",
#     options=segment_options,
#     format_func=lambda x: x.split('\n')[0].replace('###','').strip()
# )

# # Step 3: Clinical Context
# st.header("Step 3: Clinical Context")
# context_input = st.text_area(
#     "Describe the persona's clinical context:",
#     "Specializes in late-stage lung cancer. Sees a mix of newly diagnosed and treatment-experienced patients.",
#     help="You can provide partial info, and the AI will help complete it."
# )

# # Step 4: Psychographics
# st.header("Step 4: Psychographics & Motivations")

# def slider_row(label, low_label, high_label, key, default):
#     st.markdown(f"**{label}**")
#     col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
#     with col1: st.caption(low_label)
#     with col2:
#         val = st.slider(label, 0.0, 1.0, default, step=0.1, 
#                        label_visibility="collapsed", format="%.1f", key=key)
#     with col3: st.caption(high_label)
#     return val

# risk_tolerance = slider_row("Risk Tolerance", "Conservative", "Bold", "risk", 0.7)
# brand_loyalty = slider_row("Brand Loyalty", "Low", "High", "loyalty", 0.3)
# research_orientation = slider_row("Research Orientation", "Anecdote", "Data", "research", 0.8)
# recognition_need = slider_row("Recognition Need", "Seeks podium", "Low-profile", "recognition", 0.2)
# patient_empathy = slider_row("Patient Empathy", "Transactional", "Advocate", "empathy", 0.9)

# # Step 5: Product & Call Objectives
# st.header("Step 5: Product & Call Objectives")
# objectives_input = st.text_area(
#     "Describe the product and call objectives:",
#     "The product is a new immunotherapy, Xaltorvima. The rep needs to handle objections about its novel mechanism of action.",
#     help="You can provide partial info, and the AI will help complete it."
# )

# # Initialize session state
# if "persona_details" not in st.session_state:
#     st.session_state.persona_details = None
# if "final_prompt" not in st.session_state:
#     st.session_state.final_prompt = ""
# if "assistant_id" not in st.session_state:
#     st.session_state.assistant_id = ""

# # Build Persona Details
# if not st.session_state.persona_details:
#     if st.button("📝 Build Persona Details", type="primary"):
#         psychographics_input_str = f"""
# - Risk Tolerance: {risk_tolerance}
# - Brand Loyalty: {brand_loyalty}
# - Research Orientation: {research_orientation}
# - Recognition Need: {recognition_need}
# - Patient Empathy: {patient_empathy}
# """
#         with st.spinner("🤖 Building persona..."):
#             st.session_state.persona_details = autoprompt.build_persona_details(
#                 header_input, segment_choice, context_input, 
#                 psychographics_input_str, objectives_input
#             )
#         st.success("🎉 Persona Details Built!")

# # Generate Final Prompt
# if st.session_state.persona_details:
#     st.markdown("---")
#     st.subheader("Confirm Assembled Persona Details")
#     st.markdown(st.session_state.persona_details['full_persona_details'])
    
#     if st.button("🚀 Generate Final Prompt", type="primary"):
#         with st.spinner("🤖 Generating final system prompt..."):
#             st.session_state.final_prompt = autoprompt.generate_final_prompt(
#                 st.session_state.persona_details
#             )
#         st.success("✅ System Prompt Generated!")

# # Step 6: Create Assistant and Test
# if st.session_state.final_prompt:
#     st.markdown("---")
#     st.header("Step 6: Create Vapi Assistant & Test Voice")
    
#     if not (vapi_private_key and vapi_public_key):
#         st.error("""
#         ⚠️ Missing API Keys! Please add to your .env file:
#         - VAPI_PRIVATE_KEY
#         - VAPI_PUBLIC_KEY
#         """)
#     else:
#         col1, col2 = st.columns(2)
        
#         with col1:
#             # Create Assistant button
#             if not st.session_state.assistant_id:
#                 if st.button("🎙️ Create Vapi Assistant", type="primary"):
#                     with st.spinner("Creating Vapi assistant..."):
#                         assistant_name = f"Persona-{int(time.time())}"
                        
#                         # CHIAMATA DIRETTA senza backend
#                         st.session_state.assistant_id = autoprompt.create_vapi_assistant(
#                             api_key=vapi_private_key,
#                             system_prompt=st.session_state.final_prompt,
#                             name=assistant_name
#                         )
                        
#                         if st.session_state.assistant_id:
#                             st.success(f"✅ Assistant created! ID: {st.session_state.assistant_id}")
#                             st.balloons()
#                             st.rerun()
#                         else:
#                             st.error("❌ Failed to create assistant. Check console for errors.")
#             else:
#                 st.info(f"✅ Assistant ready: `{st.session_state.assistant_id}`")
        
#         with col2:
#             # Reset button
#             if st.session_state.assistant_id:
#                 if st.button("🔄 Create New Assistant"):
#                     st.session_state.assistant_id = ""
#                     st.rerun()
        
#         # Show Widget if assistant exists
#         if st.session_state.assistant_id:
#             st.markdown("---")
#             st.subheader("🎤 Voice Widget Active!")
            
#             # Dashboard link
#             st.markdown(
#                 f"[📊 View in Vapi Dashboard](https://dashboard.vapi.ai/assistants/{st.session_state.assistant_id})",
#                 unsafe_allow_html=True
#             )
            
#             # Embed the widget
#             embed_vapi_widget(vapi_public_key, st.session_state.assistant_id)
            
#             # Instructions
#             st.markdown("""
#             ### 📱 How to use:
#             1. **Look for the blue button** in the bottom-right corner
#             2. **Click it** to start the conversation
#             3. **Allow microphone access** when prompted
#             4. **Speak naturally** with your AI doctor persona
#             5. **Click again** to end the call
            
#             ### 🐛 Troubleshooting:
#             - Don't see the button? Check browser console (F12)
#             - Button not working? Verify microphone permissions
#             - No response? Check Vapi Dashboard for errors
#             """)

# # Footer debug info
# st.markdown("---")
# with st.expander("🔧 Debug Information"):
#     st.json({
#         "persona_built": bool(st.session_state.persona_details),
#         "prompt_generated": bool(st.session_state.final_prompt),
#         "assistant_id": st.session_state.assistant_id,
#         "vapi_keys_present": bool(vapi_private_key and vapi_public_key),
#     })
    
    
    
    


# # app.py - Versione semplificata SENZA backend
# import os
# import time
# import streamlit as st
# import streamlit.components.v1 as components
# from dotenv import load_dotenv
# import autoprompt
# from langchain_openai import ChatOpenAI

# # ──────────────────────────────────────────────────────────────────────────────
# # Setup base
# # ──────────────────────────────────────────────────────────────────────────────
# load_dotenv()
# st.set_page_config(layout="wide", page_title="Persona Prompt Generator")

# # ──────────────────────────────────────────────────────────────────────────────
# # Helpers
# # ──────────────────────────────────────────────────────────────────────────────
# def get_segment_options():
#     """
#     Legge le opzioni di segmento dal markdown (fallback a lista base se non esiste).
#     """
#     try:
#         content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
#         if not content:
#             raise FileNotFoundError()
#         # Estrai bullet points tipo "- Cardiologist" ecc.
#         opts = []
#         for line in content.splitlines():
#             line = line.strip()
#             if line.startswith("- "):
#                 opts.append(line[2:].strip())
#         return opts or ["Cardiologist", "Oncologist", "General Practitioner", "Dermatologist"]
#     except Exception:
#         return ["Cardiologist", "Oncologist", "General Practitioner", "Dermatologist"]


# def embed_vapi_button(vapi_public_key: str, assistant_id: str):
#     """
#     Mostra SOLO il bottone Vapi (voice) e lo inietta nel DOM del parent
#     per evitare i limiti dell'iframe di Streamlit (about:srcdoc).
#     Questo elimina i 404 su /embed e l'errore Daily 'The string did not match...'.
#     """
#     components.html(f"""
#     <script>
#       (function() {{
#         const P = window.parent || window;

#         function loadSDK(cb) {{
#           if (P.document.getElementById('vapi-sdk-script')) return cb();
#           const s = P.document.createElement('script');
#           s.id = 'vapi-sdk-script';
#           s.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
#           s.defer = true; s.async = true;
#           s.onload = cb;
#           P.document.head.appendChild(s);
#         }}

#         function run() {{
#           try {{ P.vapiInstance?.destroy?.(); }} catch (e) {{}}
#           const buttonConfig = {{
#             position: "bottom-right",
#             width: "56px",
#             height: "56px"
#           }};
#           P.vapiInstance = P.vapiSDK.run({{
#             apiKey: "{vapi_public_key}",
#             assistant: "{assistant_id}",
#             config: buttonConfig
#           }});
#           P.vapiInstance.on('error',      (e) => console.error('Vapi error:', e));
#           P.vapiInstance.on('call-start', () => console.log('Vapi call started'));
#           P.vapiInstance.on('call-end',   () => console.log('Vapi call ended'));
#         }}

#         loadSDK(run);
#       }})();
#     </script>
#     """, height=0, scrolling=False)


# def show_section_header(step: int, title: str, subtitle: str = ""):
#     st.markdown(f"## Step {step}: {title}")
#     if subtitle:
#         st.caption(subtitle)


# # ──────────────────────────────────────────────────────────────────────────────
# # Sidebar: chiavi & stato
# # ──────────────────────────────────────────────────────────────────────────────
# st.sidebar.header("🔑 API Keys Status")
# vapi_private_key = os.getenv("VAPI_PRIVATE_KEY", "")
# vapi_public_key = os.getenv("VAPI_PUBLIC_KEY", "")
# openai_key = os.getenv("OPENAI_API_KEY", "")

# st.sidebar.write("VAPI_PRIVATE_KEY: " + ("✅ set" if vapi_private_key else "❌ missing"))
# st.sidebar.write("VAPI_PUBLIC_KEY: " + ("✅ set" if vapi_public_key else "❌ missing"))
# st.sidebar.write("OPENAI_API_KEY: " + ("✅ set" if openai_key else "❌ missing"))

# # Init session state
# for k, v in {
#     "persona_state": None,
#     "persona_details": "",
#     "final_prompt": "",
#     "assistant_id": "",
# }.items():
#     if k not in st.session_state:
#         st.session_state[k] = v

# # ──────────────────────────────────────────────────────────────────────────────
# # STEP 1: Input base per costruzione persona
# # ──────────────────────────────────────────────────────────────────────────────
# show_section_header(1, "Costruisci la Persona", "Compila i campi e genera la bozza della persona (fase 1/2).")

# col1, col2 = st.columns(2)
# with col1:
#     header_input = st.text_area(
#         "1) Persona Header (nome, ruolo, età, genere, setting, geografia ecc.)",
#         placeholder="Es: Dr. Jane Doe, Cardiologa 45 anni, Milano, ospedale universitario...",
#         height=160,
#     )
#     segment_options = get_segment_options()
#     segment_input = st.selectbox("2) Segmento (specializzazione)", options=segment_options, index=0)

# with col2:
#     context_input = st.text_area(
#         "3) Clinical Context (linee guida, tecnologie, workflow clinici rilevanti)",
#         placeholder="Es: gestione pazienti cronici, uso di sistemi EHR, linee guida ESC 2023...",
#         height=160,
#     )
#     psychographics_input = st.text_area(
#         "4) Psychographics (atteggiamenti, stile cognitivo, valori)",
#         placeholder="Es: evidence-based, avversa al rischio, orientata al paziente...",
#         height=100,
#     )
#     objectives_input = st.text_area(
#         "5) Product/Use-case Objectives (cosa deve saper fare l'assistente)",
#         placeholder="Es: triage sintomi, gestione follow-up, educazione paziente...",
#         height=100,
#     )

# colA, colB = st.columns([1, 2])
# with colA:
#     if st.button("🚀 Genera Persona (fase 1)", type="primary"):
#         with st.spinner("Creo la descrizione dettagliata della persona..."):
#             try:
#                 # Usa il tuo workflow per la prima metà (build persona)
#                 state = autoprompt.build_persona_details(
#                     header_input, segment_input, context_input, psychographics_input, objectives_input
#                 )
#                 st.session_state.persona_state = state
#                 # Provo a leggere un campo testuale comodo da mostrare
#                 persona_txt = ""
#                 if isinstance(state, dict):
#                     persona_txt = state.get("persona_details") or state.get("persona_header") or ""
#                 st.session_state.persona_details = persona_txt
#                 st.success("Persona creata! Rivedi e conferma sotto.")
#             except Exception as e:
#                 st.error(f"Errore durante la creazione della persona: {e}")

# with colB:
#     st.text_area("📄 Anteprima Persona (fase 1)", value=st.session_state.persona_details, height=220)

# # ──────────────────────────────────────────────────────────────────────────────
# # STEP 2: Conferma e generazione System Prompt finale (fase 2/2)
# # ──────────────────────────────────────────────────────────────────────────────
# show_section_header(2, "Genera System Prompt Finale", "Conferma la persona e lascia lavorare gli agent per il prompt finale.")

# colC, colD = st.columns([1, 2])
# with colC:
#     can_generate = st.session_state.persona_state is not None
#     if st.button("✍️ Genera System Prompt", disabled=not can_generate):
#         with st.spinner("Gli agent stanno componendo il system prompt definitivo..."):
#             try:
#                 final_state = autoprompt.generate_final_prompt(st.session_state.persona_state)
#                 # Estraggo il testo finale se presente
#                 final_txt = ""
#                 if isinstance(final_state, dict):
#                     final_txt = final_state.get("final_prompt", "") or final_state.get("compiled_prompt", "")
#                 # Fallback: se il tuo modulo ha un compilatore esplicito
#                 if not final_txt and hasattr(autoprompt, "compile_and_save_prompt"):
#                     try:
#                         final_txt = autoprompt.compile_and_save_prompt(final_state)
#                     except Exception:
#                         pass
#                 if not final_txt:
#                     final_txt = "⚠️ Non ho ricevuto il testo del prompt dal workflow. Controlla il modulo 'autoprompt'."
#                 st.session_state.final_prompt = final_txt
#                 st.success("System prompt generato!")
#             except Exception as e:
#                 st.error(f"Errore durante la generazione del system prompt: {e}")

# with colD:
#     st.text_area("🧠 System Prompt Finale", value=st.session_state.final_prompt, height=260)

# # ──────────────────────────────────────────────────────────────────────────────
# # STEP 3: Crea Assistant Vapi
# # ──────────────────────────────────────────────────────────────────────────────
# show_section_header(3, "Crea Assistente Vapi", "Usa il system prompt per creare l'assistente vocale su Vapi.")

# colE, colF = st.columns([1, 2])
# with colE:
#     assistant_name = st.text_input("Nome Assistant", value="ctcHealth Voice Assistant")
#     can_create = bool(vapi_private_key and st.session_state.final_prompt.strip())
#     if st.button("📞 Crea Assistente su Vapi", disabled=not can_create):
#         with st.spinner("Creo l'assistente su Vapi..."):
#             try:
#                 assistant_id = autoprompt.create_vapi_assistant(
#                     api_key=vapi_private_key,
#                     system_prompt=st.session_state.final_prompt,
#                     name=assistant_name,
#                 )
#                 if assistant_id:
#                     st.session_state.assistant_id = assistant_id
#                     st.success(f"Assistente creato! ID: {assistant_id}")
#                 else:
#                     st.error("Creazione assistant fallita. Controlla le chiavi e la configurazione Vapi.")
#             except Exception as e:
#                 st.error(f"Errore durante la creazione dell'assistente: {e}")

# with colF:
#     st.text_input("Assistant ID", value=st.session_state.assistant_id, disabled=True)

# # ──────────────────────────────────────────────────────────────────────────────
# # STEP 4: Test in pagina — SOLO BOTTONE (niente /embed)
# # ──────────────────────────────────────────────────────────────────────────────
# show_section_header(4, "Testa l'Assistente (Voice)", "Comparirà un bottone fluttuante in basso a destra.")

# if st.session_state.assistant_id and vapi_public_key:
#     st.info("Premi il bottone fluttuante per avviare/fermare la chiamata.")
#     embed_vapi_button(vapi_public_key, st.session_state.assistant_id)
# else:
#     st.warning("Serve **Assistant ID** e **VAPI_PUBLIC_KEY** per mostrare il bottone.")

# with st.expander("🐛 Troubleshooting"):
#     st.markdown("""
#     - Se **non vedi alcun bottone**, verifica i log console (F12).
#     - In **produzione** usa **HTTPS**: altrimenti il browser non concede il microfono.
#     - Disattiva ad-blocker/VPN che possano bloccare `c.daily.co`.
#     - Verifica che **Public Key** e **Assistant ID** provengano dallo **stesso workspace** Vapi.
#     """)

# # ──────────────────────────────────────────────────────────────────────────────
# # Footer debug
# # ──────────────────────────────────────────────────────────────────────────────
# st.markdown("---")
# with st.expander("🔧 Debug Information"):
#     st.json({
#         "persona_built": bool(st.session_state.persona_state),
#         "prompt_generated": bool(st.session_state.final_prompt),
#         "assistant_id": st.session_state.assistant_id,
#         "vapi_keys_present": bool(vapi_private_key and vapi_public_key),
#     })





import os
import time
import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv
import autoprompt
from langchain_openai import ChatOpenAI
import streamlit.components.v1 as components
load_dotenv()

st.set_page_config(layout="wide", page_title="Persona Prompt Generator")

def get_segment_options():
    """Helper to read segment options from the markdown file."""
    content = autoprompt.read_file_content("persona_building_prompts/2customer_segmentation.md")
    return [seg.strip() for seg in content.split('---') if seg.strip()]


def embed_vapi_widget(vapi_public_key: str, assistant_id: str):
    # 🔧 Modifica ESSENZIALE: niente @vapi-ai/web (che rompe in <script>),
    # niente iframe; iniettiamo lo snippet ufficiale nel parent DOM
    components.html(f"""
    <script>
      (function() {{
        const P = window.parent || window;

        function loadSDK(cb) {{
          if (P.document.getElementById('vapi-sdk-script')) return cb();
          const s = P.document.createElement('script');
          s.id = 'vapi-sdk-script';
          s.src = "https://cdn.jsdelivr.net/gh/VapiAI/html-script-tag@latest/dist/assets/index.js";
          s.defer = true; s.async = true;
          s.onload = cb;
          P.document.head.appendChild(s);
        }}

        function run() {{
          try {{ P.vapiInstance?.destroy?.(); }} catch (e) {{}}
          const buttonConfig = {{
            position: "bottom",
            width: "56px",
            height: "64px"
          }};
          P.vapiInstance = P.vapiSDK.run({{
            apiKey: "{vapi_public_key}",
            assistant: "{assistant_id}",
            config: buttonConfig
          }});
          P.vapiInstance.on('error',      (e) => console.error('Vapi error:', e));
          P.vapiInstance.on('call-start', () => console.log('Vapi call started'));
          P.vapiInstance.on('call-end',   () => console.log('Vapi call ended'));
        }}

        loadSDK(run);
      }})();
    </script>
    """, height=0, scrolling=False)

# TITOLO E INTRO
st.title("👨‍⚕️ CTC Helath - Persona Prompt Generator")
st.markdown("""
Welcome to the Persona Prompt Generator! This tool uses a multi-agent system
to help you create a detailed doctor persona for role-playing scenarios.
""")

# Step 1: Persona Header
st.header("Step 1: Persona Header")
header_input = st.text_area(
    "Provide basic details for the doctor persona:",
    "Dr. Anya Sharma, Oncologist, 45, female, private practice, New York",
    help="You can provide partial info, and the AI will complete it."
)

# Step 2: Customer Segmentation
st.header("Step 2: Customer Segmentation")
segment_options = get_segment_options()
segment_choice = st.radio(
    "Please select a customer segment for this persona:",
    options=segment_options,
    format_func=lambda x: x.split('\n')[0].replace('###','').strip()
)

# Step 3: Clinical Context
st.header("Step 3: Clinical Context")
context_input = st.text_area(
    "Describe the persona's clinical context:",
    "Specializes in late-stage lung cancer. Sees a mix of newly diagnosed and treatment-experienced patients.",
    help="You can provide partial info, and the AI will help complete it."
)

# Step 4: Psychographics
st.header("Step 4: Psychographics & Motivations")

def slider_row(label, low_label, high_label, key, default):
    st.markdown(f"**{label}**")
    col1, col2, col3 = st.columns([0.5, 4, 1], gap=None)
    with col1: st.caption(low_label)
    with col2:
        val = st.slider(label, 0.0, 1.0, default, step=0.1, 
                       label_visibility="collapsed", format="%.1f", key=key)
    with col3: st.caption(high_label)
    return val

risk_tolerance = slider_row("Risk Tolerance", "Conservative", "Bold", "risk", 0.7)
brand_loyalty = slider_row("Brand Loyalty", "Low", "High", "loyalty", 0.3)
research_orientation = slider_row("Research Orientation", "Anecdote", "Data", "research", 0.8)
recognition_need = slider_row("Recognition Need", "Seeks podium", "Low-profile", "recognition", 0.2)
patient_empathy = slider_row("Patient Empathy", "Transactional", "Advocate", "empathy", 0.9)

# Step 5: Product & Call Objectives
st.header("Step 5: Product & Call Objectives")
objectives_input = st.text_area(
    "Describe the product and call objectives:",
    "The product is a new immunotherapy, Xaltorvima. The rep needs to handle objections about its novel mechanism of action.",
    help="You can provide partial info, and the AI will help complete it."
)

# Initialize session state
if "persona_details" not in st.session_state:
    st.session_state.persona_details = None
if "final_prompt" not in st.session_state:
    st.session_state.final_prompt = ""
if "assistant_id" not in st.session_state:
    st.session_state.assistant_id = ""

# Build Persona Details
if not st.session_state.persona_details:
    if st.button("📝 Build Persona Details", type="primary"):
        psychographics_input_str = f"""
- Risk Tolerance: {risk_tolerance}
- Brand Loyalty: {brand_loyalty}
- Research Orientation: {research_orientation}
- Recognition Need: {recognition_need}
- Patient Empathy: {patient_empathy}
"""
        with st.spinner("🤖 Building persona..."):
            st.session_state.persona_details = autoprompt.build_persona_details(
                header_input, segment_choice, context_input, 
                psychographics_input_str, objectives_input
            )
        st.success("🎉 Persona Details Built!")

# Generate Final Prompt
if st.session_state.persona_details:
    st.markdown("---")
    st.subheader("Confirm Assembled Persona Details")
    st.markdown(st.session_state.persona_details['full_persona_details'])
    
    if st.button("🚀 Generate Final Prompt", type="primary"):
        with st.spinner("🤖 Generating final system prompt..."):
            st.session_state.final_prompt = autoprompt.generate_final_prompt(
                st.session_state.persona_details
            )
        st.success("✅ System Prompt Generated!")

# Step 6: Create Assistant and Test
if st.session_state.final_prompt:
    st.markdown("---")
    st.header("Step 6: Create CTC Health Assistant & Test Voice")
    
    if not (vapi_private_key and vapi_public_key):
        st.error("""
        ⚠️ Missing API Keys! Please add to your .env file:
        - VAPI_PRIVATE_KEY
        - VAPI_PUBLIC_KEY
        """)
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            # Create Assistant button
            if not st.session_state.assistant_id:
                if st.button("🎙️ Create CTC Healht Assistant", type="primary"):
                    with st.spinner("Creating CTC Healht assistant..."):
                        assistant_name = f"Persona-{int(time.time())}"
                        
                        # CHIAMATA DIRETTA senza backend
                        st.session_state.assistant_id = autoprompt.create_vapi_assistant(
                            api_key=vapi_private_key,
                            system_prompt=st.session_state.final_prompt,
                            name=assistant_name
                        )
                        
                        if st.session_state.assistant_id:
                            st.success(f"✅ Assistant created! ID: {st.session_state.assistant_id}")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("❌ Failed to create assistant. Check console for errors.")
            else:
                st.info(f"✅ Assistant ready: `{st.session_state.assistant_id}`")
        
        with col2:
            # Reset button
            if st.session_state.assistant_id:
                if st.button("🔄 Create New Assistant"):
                    st.session_state.assistant_id = ""
                    st.rerun()
        
        # Show Widget if assistant exists
        if st.session_state.assistant_id:
            st.markdown("---")
            st.subheader("🎤 Voice Widget Active!")
            
            # Embed the widget (🔧 ora inietta solo il bottone funzionante nel parent)
            embed_vapi_widget(vapi_public_key, st.session_state.assistant_id)
            

# Footer debug info
# st.markdown("---")
# with st.expander("🔧 Debug Information"):
#     st.json({
#         "persona_built": bool(st.session_state.persona_details),
#         "prompt_generated": bool(st.session_state.final_prompt),
#         "assistant_id": st.session_state.assistant_id,
#         "vapi_keys_present": bool(vapi_private_key and vapi_public_key),
#     })
