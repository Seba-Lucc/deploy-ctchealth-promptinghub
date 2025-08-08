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

vapi_private_key = os.getenv("VAPI_PRIVATE_KEY", "")
vapi_public_key = os.getenv("VAPI_PUBLIC_KEY", "")
openai_key = os.getenv("OPENAI_API_KEY", "")

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
            # else:
            #     st.info(f"✅ Assistant ready: `{st.session_state.assistant_id}`")
        
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
