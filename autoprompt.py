"""
A multi-agent system using LangGraph to generate a doctor persona system prompt.

This system is composed of two main stages:
1.  **Persona Construction (5 Agents):** A series of agents guide the user
    through a 5-step process to build a detailed persona description.
2.  **Prompt Generation (5 Agents):** An orchestrator uses the detailed
    description to instruct two writer agents on how to generate the final
    system prompt.
"""
import os
import re
import json
from typing import TypedDict, Dict
from functools import partial

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langsmith import traceable # For tracing agent execution on LangSmith

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from vapi import Vapi

# --- Agent State ---
class AgentState(TypedDict):
    """Represents the state of our multi-agent system."""
    # Part 1
    persona_header: str
    # Part 2
    customer_segment: str
    # Part 3
    clinical_context: str
    # Part 4
    psychographics: str
    # Part 5
    product_objectives: str

    # Assembled details for the orchestrator
    full_persona_details: str

    # Final generated prompt sections
    section1a_prompt: str
    section1b_prompt: str
    section2a_prompt: str
    section2b_prompt: str
    section2c_prompt: str
    final_prompt: str

# --- Helper Functions ---

def read_file_content(file_path: str) -> str:
    """A helper function to read file content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return ""


def create_vapi_assistant(api_key: str, system_prompt: str, name: str):
    """
    Creates a new Vapi assistant using the provided system prompt.
    """
    print("--- 📞 Creating Vapi Assistant ---")
    try:
        vapi = Vapi(token=api_key)
        assistant = vapi.assistants.create(
            name=name,
            model={
                "provider": "openai",
                "model": "gpt-4o",
                "temperature": 0.7,
                "messages": [{
                    "role": "system",
                    "content": system_prompt
                }]
            },
            voice={
                "provider": "11labs",
                "voiceId": "21m00Tcm4TlvDq8ikWAM" # Default voice, can be changed
            },
            first_message="Hello, I'm ready to start our role-play session."
        )
        print(f"✅ Vapi assistant created successfully. ID: {assistant.id}")
        return assistant.id
    except Exception as e:
        print(f"❌ Error creating Vapi assistant: {e}")
        return None


# --- Persona Construction Agents (5 Parts) ---
@traceable(name="build_persona_header")
def header_builder_node(state: AgentState, llm: ChatOpenAI, user_input: str):
    """Part 1: Gathers the persona header information."""
    print("\n--- 🤵 Part 1: Persona Header ---")

    # 1. Read the context/instructions for what a persona header is.
    context = read_file_content("persona_building_prompts/1persona_header.md")

    # 2. Ask the user for input.
    print("Please provide the basic details for the doctor persona: Name, Title, Age, Gender, Practice Setting, and Geography.")
    print("I will complete the rest and structure it.")
    print("--------------------------------")
    print("For context:")
    print(context)
    #user_input = input("> ")

    print("\nSynthesizing and completing persona header...")

    # 3. Create a specific, detailed prompt for the LLM.
    system_prompt = f"""You are an expert persona creator. Your task is to take a user's potentially incomplete description of a doctor persona and transform it into a complete, narrative description.

You must:
1.  **Analyze the User's Input:** Identify the details the user has provided.
2.  **Complete Missing Details:** Use the provided context to creatively and plausibly fill in any missing information. The final persona should be consistent and realistic.
3.  **Structure the Output:** Format the final, complete details into a clear, well-written paragraph. 

**Context for Persona Header Fields:**
{context}

**Example Output:**
"Dr. Evelyn Reed is a 48-year-old female Cardiologist at a major academic hospital in Boston, USA. She is considered a Key Opinion Leader (KOL) in her field and demonstrates high digital sophistication, being active on professional networks and frequently using digital health tools in her practice."
"""

    human_prompt = f"Here is the user's input for the persona:\n\n{user_input}"

    completion_and_extraction_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(completion_and_extraction_prompt)

    # 4. Parse the LLM response to get the dictionary.
    state["persona_header"] = response.content.strip()


    print("✅ Header complete.")
    # For clarity, print the persona created, not in json format
    print(state['persona_header'])

    return state

@traceable(name="select_customer_segment")
def segment_selector_node(state: AgentState, segment_choice: str):
    """Part 2: Asks the user to select a customer segment."""
    print("\n--- 🎯 Part 2: Customer Segmentation ---")
    state["customer_segment"] = segment_choice
    print('Selected Segment:', segment_choice)
    print("✅ Segmentation complete.")
    return state

@traceable(name="build_clinical_context")
def context_builder_node(state: AgentState, llm: ChatOpenAI, user_input: str):
    """Part 3: Gathers the clinical context."""
    print("\n--- 🏥 Part 3: Clinical Context ---")

    # 1. Read the context/instructions for what clinical context is.
    context = read_file_content("persona_building_prompts/3clinical_context.md")

    # 2. Ask the user for input.
    print("Please describe the persona's clinical context (Therapeutic Area, Patient Mix, etc.).")
    print("You can provide partial info, and I will help complete it.")
    print(context)
    #user_input = input("> ")

    print("\nSynthesizing and completing clinical context...")

    # Build context from previous steps
    current_persona_context = f"""
### Persona Header
{state['persona_header']}

### Customer Segment
{state['customer_segment']}
"""

    # 3. Create a specific, detailed prompt for the LLM.
    system_prompt = f"""You are an expert persona creator. Your task is to take a user's potentially incomplete description of a doctor's clinical context and expand it into a complete and plausible narrative, ensuring it is consistent with the persona details created so far.

**Current Persona Details to Maintain Consistency With:**
{current_persona_context}

You must:
1.  **Analyze the User's Input:** Identify the clinical context details the user has provided.
2.  **Ensure Consistency:** The clinical context you generate must align perfectly with the **Current Persona Details**. For example, a Cardiologist from the header should not suddenly have a clinical context focused on oncology unless specifically directed.
3.  **Complete Missing Details:** Use the provided context definitions to creatively and plausibly fill in any missing information. The final description should be detailed, consistent, and realistic for the established medical professional.
4.  **Structure the Output:** Format the final, complete details into a clear, well-written narrative paragraph.

**Context for Clinical Context Fields:**
{context}

**Example Output:**
"The persona operates in a busy urban oncology clinic specializing in late-stage solid tumors, particularly breast and lung cancer. The patient mix is diverse, with a significant portion being elderly patients with multiple comorbidities. Key clinical drivers include extending progression-free survival and managing treatment-related toxicities. The practice closely tracks patient-reported outcomes and time-to-treatment initiation as key performance metrics."
"""

    human_prompt = f"Here is the user's input for the clinical context:\n\n{user_input}"

    completion_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(completion_prompt)

    # 4. Store the generated text in the state.
    state["clinical_context"] = response.content.strip()

    print("✅ Clinical context complete.")
    # For clarity, let's print the generated context
    print("Clinical Context:")
    print(state['clinical_context'])

    return state

@traceable(name="build_psychographics")
def psychographics_builder_node(state: AgentState, llm: ChatOpenAI, user_input: str):
    """Part 4: Gathers the psychographic profile."""
    print("\n--- 📊 Part 4: Psychographics & Motivations ---")

    # 1. Read the context file which explains the dimensions.
    context = read_file_content("persona_building_prompts/4psychographics.md")

    # 2. Ask the user for input, explaining the task.
    print("Please describe the persona's psychographic profile.")
    print("You can provide scores (0-1) for the 5 dimensions, or just give a general description.")
    print("Example: 'Risk Tolerance: 0.8 Conservative and 0.2 Bold experimenter.'")
    print("I will complete the rest and create a narrative description.")
    print(context) # Show the user the dimensions from the file
    #user_input = input("> ")

    print("\nSynthesizing and completing psychographic profile...")

    # Build context from previous steps
    current_persona_context = f"""
### Persona Header
{state['persona_header']}

### Customer Segment
{state['customer_segment']}

### Clinical Context
{state['clinical_context']}
"""
    # 3. Create a specific, detailed prompt for the LLM.
    system_prompt = f"""You are an expert persona creator. Your task is to take a user's description of a doctor's psychographics (provided as scores) and expand it into a complete and plausible narrative, ensuring it is consistent with the persona details created so far.

**Current Persona Details to Maintain Consistency With:**
{current_persona_context}

You must:
1.  **Analyze the User's Input:** The input will be a list of scores for different psychographic dimensions.
2.  **Ensure Consistency:** The psychographic profile must be a natural extension of the established persona. The narrative you create should logically follow from the persona's header, segment, and clinical context.
3.  **Create a Narrative:** Convert the scores into a coherent and insightful summary of the persona's motivations and professional style. Explain what these scores mean for the character.
4.  **Structure the Output:** Format the final, complete details into a clear, well-written narrative paragraph.

**Context for Psychographic Dimensions:**
{context}

**Example Output:**
"This doctor is a bold experimenter (Risk Tolerance: 0.2 Conservative and 0.8 Bold experimenter), often willing to try novel therapies in difficult cases. However, this is balanced by a surprisingly high brand loyalty (Brand Loyalty: 0.8 High and 0.2 Low); once a product earns their trust, they stick with it. They are heavily data-driven (Research Orientation: 0.7 Data-heavy and 0.2 Anecdote-driven), demanding robust clinical evidence, and have little need for public recognition, preferring to remain low-profile (Recognition Need: 0.2 Seeks podium and 0.8 Low-profile). Above all, they are a fierce patient advocate (Patient Empathy: 0.1 Transactional and 0.9 Advocate), and all decisions are filtered through that lens."
"""

    human_prompt = f"Here is the user's input for the psychographic profile:\n\n{user_input}"

    completion_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(completion_prompt)

    # 4. Store the generated text in the state.
    state["psychographics"] = response.content.strip()

    print("✅ Psychographics complete.")
    # For clarity, let's print the generated profile
    print("Psychographics & Motivations:")
    print(state['psychographics'])

    return state

@traceable(name="build_objectives")
def objectives_builder_node(state: AgentState, llm: ChatOpenAI, user_input: str):
    """Part 5: Gathers the product and call objectives."""
    print("\n--- 📞 Part 5: Product & Call Objectives ---")

    # 1. Read the context file which explains the objectives.
    context = read_file_content("persona_building_prompts/5product_objectives.md")

    # 2. Ask the user for input.
    print("Please describe the product and call objectives.")
    print("You can provide partial info (e.g., 'The product is Xaltrava. The rep needs to handle objections about cost.')")
    print("I will complete the rest and create a narrative description.")
    print(context) # Show the user the categories from the file
    #user_input = input("> ")

    print("\nSynthesizing and completing product and call objectives...")

    # Build context from previous steps
    current_persona_context = f"""
### Persona Header
{state['persona_header']}

### Customer Segment
{state['customer_segment']}

### Clinical Context
{state['clinical_context']}

### Psychographics & Motivations
{state['psychographics']}
"""

    # 3. Create a specific, detailed prompt for the LLM.
    system_prompt = f"""You are an expert persona and role-play creator. Your task is to take a user's potentially incomplete description of product & call objectives and expand it into a complete and plausible narrative, ensuring it is consistent with the detailed persona created so far.

**Current Persona Details to Maintain Consistency With:**
{current_persona_context}

You must:
1.  **Analyze the User's Input:** Identify any details the user has provided for the different categories (Product, Objectives, Key Messages, etc.).
2.  **Ensure Consistency:** The objectives and key messages must be tailored to the persona. A 'data-driven' doctor will need data-heavy messages, while a 'patient advocate' will respond to messages about quality of life. The objections you invent should also be what this specific doctor would raise based on their psychographics and clinical context.
3.  **Complete Missing Details:** Use the provided context and definitions to creatively and plausibly fill in any missing information. The final description should be a coherent and insightful summary of the sales call's context.
4.  **Structure the Output:** Format the final, complete details into a clear, well-written narrative paragraph.

**Context for Product & Call Objectives:**
{context}

**Example Output:**
"The focus of the call is 'Xaltrava 25 mg SC'. The primary training objective for the sales representative is to probe for unmet needs around managing a specific patient subtype and to skillfully handle objections related to the drug's cost and perceived lack of long-term overall survival data. Key messages should center on superior progression-free survival, a manageable safety profile, and ease of administration. The main competitor is Drug A, which is cheaper but has a less favorable side-effect profile. The rep should demonstrate a high level of skill in using open-ended questions to guide the conversation."
"""

    human_prompt = f"Here is the user's input for the product and call objectives:\n\n{user_input}"

    completion_prompt = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=human_prompt)
    ]

    response = llm.invoke(completion_prompt)

    # 4. Store the generated text in the state.
    state["product_objectives"] = response.content.strip()

    print("✅ Objectives complete.")
    # For clarity, let's print the generated objectives
    print("Product & Call Objectives:")
    print(state['product_objectives'])
    return state

@traceable(name="assemble_persona")
def persona_assembler_node(state: AgentState):
    """Assembles all the persona details into a single description."""
    print("\n--- 🧑‍🔬 Assembling Full Persona Description ---")
    full_details = f"""
### Persona Header ###
{state['persona_header']}

### Customer Segment ###
{state['customer_segment']}

### Clinical Context ###
{state['clinical_context']}

### Psychographics & Motivations ###
{state['psychographics']}

### Product & Call Objectives ###
{state['product_objectives']}
"""
    state["full_persona_details"] = full_details
    print("✅ Full persona description assembled.")
    print("\n--- Full Persona Details ---")
    print(state["full_persona_details"])
    return state

########################################################
# --- Prompt Generation Agents ---
########################################################

@traceable(name="write_persona_core")
def persona_core_writer_node(state: AgentState, llm: ChatOpenAI, template: str):
    """Agent 1A: Writes Sections 1.1 and 1.2 of the prompt."""
    print("\n--- 🧬 Persona Core Agent ---")
    print("Writing Section 1 (Core Identity & Philosophy)...")

    # The static instructions from the blueprint are now embedded here
    static_instructions = """
For the persona's 'Core Identity & Professional Background' (1.1), here are the instructions:

> **CHARACTER FOUNDATION INSTRUCTIONS:**
> 
> **Professional Demographics & Credentials:**
> - Specify exact age, medical specialty, and years of clinical experience
> - Detail educational background (medical school, residency, fellowships)
> - Identify specific healthcare setting (hospital type, location, patient population served)
> - Include any specialized training or certifications that enhance credibility
> 
> **Clinical Decision-Making Framework:**
> - Define their primary treatment philosophy and evidence standards
> - Explain how they evaluate new treatments vs. established protocols
> - Describe their risk tolerance and patient selection criteria
> - Outline their hierarchy of clinical priorities (efficacy, safety, tolerability, etc.)
> 
> **Authentic Professional Identity:**
> - Highlight specific experiences that shaped their medical approach
> - Include institutional affiliations that ground them in real healthcare systems
> - Detail practical constraints they work within (regulations, guidelines, resources)
> - Specify what gives them unique authority and credibility in their field
> 
> **Character Authenticity Markers:**
> - Include subtle professional preferences and communication style
> - Add specific medical terminology or phrases they would naturally use
> - Note any particular areas of expertise or clinical interests
> - Establish clear professional boundaries and standards they maintain

For the persona's 'Clinical Philosophy & Decision Framework' (1.2), here are the instructions:

> **Treatment Evaluation Hierarchy:**
> - List the exact order of factors they prioritize when assessing treatments (e.g., patient population matching, safety profile, efficacy data quality, cost-effectiveness)
> - Define their evidence standards: What level of clinical data do they require before adoption?
> - Specify their approach to risk-benefit analysis and how they weigh competing factors
> - Establish their threshold for changing from established protocols to newer options
> 
> **Innovation vs. Tradition Balance:**
> - Describe their openness to new therapies: Are they early adopters, cautious evaluators, or conservative practitioners?
> - Define how they integrate emerging treatments with established standards of care
> - Explain their approach to treatment sequencing and combination strategies
> - Detail how they handle conflicting guidelines or evolving evidence
> 
> **Evidence Interpretation Framework:**
> - Specify what types of evidence they value most (RCTs, real-world data, colleague experience, institutional protocols)
> - Define their skepticism triggers: What claims or approaches make them more cautious?
> - Explain how they handle uncertainty and incomplete data
> - Describe their approach to extrapolating trial data to real-world patient populations
> 
> **Professional Attitude & Reasoning Style:**
> - Define their core personality traits that influence medical decisions (confident, cautious, pragmatic, analytical)
> - Specify their communication preferences during clinical discussions
> - Establish their tolerance for ambiguity and how they handle conflicting opinions
> - Include their approach to patient involvement in treatment decisions
> 
> **Objection & Skepticism Patterns:**
> - Detail specific triggers that activate their skepticism (anecdotal evidence, marketing claims, off-label use)
> - Define how they typically respond to weak arguments or insufficient data
> - Specify their preferred method of challenging or redirecting conversations
> - Include examples of how they frame comparisons between treatment options
"""

    writer_prompt = [
        SystemMessage(
            content=f"""You are an expert persona writer. Your task is to **completely rewrite** the persona's 'Core Identity & Professional Background' (1.1) and 'Clinical Philosophy & Decision Framework' (1.2).

You are given three things:
1.  **Full Persona Context:** The complete description of the character you are building. Use this for context and to ensure consistency.
2.  **Static Instructions:** Detailed guidelines on what these sections must contain.
3.  **An Example Template:** The text of an existing persona that you must rewrite.

Your goal is to synthesize all this information to create a new persona by rewriting the **Example Template**.
The final output must be only the rewritten text, matching the structure of the example template. Make sure to include the titles of the sections in the output.

{static_instructions}

**EXAMPLE TEMPLATE TO REWRITE:**
{template}
"""
        ),
        HumanMessage(content=f"""Here is the information for the new character.

**FULL PERSONA CONTEXT:**
{state['full_persona_details']}
""")
    ]
    response = llm.invoke(writer_prompt)
    state["section1a_prompt"] = response.content
    print("✅ Section 1A (Core) rewritten.")
    return state

@traceable(name="write_persona_boundaries")
def persona_boundaries_writer_node(state: AgentState, llm: ChatOpenAI, template: str):
    """Agent 1B: Writes Sections 1.3, 1.4, and 1.5 of the prompt."""
    print("\n--- ⚖️ Persona Boundaries Agent ---")
    print("Writing Section 1 (Boundaries & Protocols)...")

    # The static instructions from the blueprint are now embedded here
    static_instructions = """
For  'Brand Name Requirements' (1.4), and 'Zero-Tolerance Protocol' (1.5), follow these instructions:
For the persona's 'Medical Authority Boundaries' (1.3), here are the instructions:

> **MEDICAL AUTHORITY BOUNDARIES:**
> Use the exact same text as the example template. Only replace the text with the new character's details.

For the persona's 'Brand Name Requirements' (1.4), here are the instructions:

> **BRAND NAME SUBSTITUTION PROTOCOL:**
> Use only if the user asks to use a substitute name, you must use the exact same text as the example template. Only replace the text with the new character's details.
> Otherwise, use the original brand name. "The name of the product is..."

For the persona's 'Zero-Tolerance Protocol' (1.5), here are the instructions:

> **BEHAVIORAL VIOLATION RESPONSE SYSTEM:**
> Use the exact same text as the example template. Only replace the text with the new character's details.
"""

    writer_prompt = [
        SystemMessage(
            content=f"""You are an expert persona writer. Your task is to **completely rewrite** the persona's 'Medical Authority Boundaries' (1.3), 'Brand Name Requirements' (1.4), and 'Zero-Tolerance Protocol' (1.5).

You are given four things:
1.  **Full Persona Context:** The complete description of the character.
2.  **Previously Written Work:** The output from the previous writer agent. You must ensure your work is consistent with this.
3.  **Static Instructions:** Detailed guidelines on what these sections must contain.
4.  **An Example Template:** The text of an existing persona that you must rewrite.

Your goal is to synthesize all this information to create a new persona by rewriting the **Example Template**.
The final output must be only the rewritten text, matching the structure of the example template. Make sure to include the titles of the sections in the output.

**STATIC INSTRUCTIONS:**
{static_instructions}

**EXAMPLE TEMPLATE TO REWRITE:**
{template}
"""
        ),
        HumanMessage(content=f"""Here is the information for the new character.

**FULL PERSONA CONTEXT:**
{state['full_persona_details']}

**PREVIOUSLY WRITTEN WORK (Agent 1A):**
{state['section1a_prompt']}
""")
    ]
    response = llm.invoke(writer_prompt)
    state["section1b_prompt"] = response.content
    print("✅ Section 1B (Boundaries) rewritten.")
    return state

@traceable(name="write_voice_speech")
def voice_speech_writer_node(state: AgentState, llm: ChatOpenAI, template: str):
    """Agent 2A: Writes Sections 2.1 and 2.2 of the prompt."""
    print("\n--- 🗣️📄 Voice Agent (Speech & Thought) ---")
    print("Writing Section 2 (Speech & Thought)...")
    static_instructions = """
For the persona's 'Speech Patterns & Linguistic Markers' (2.1), here are the instructions:
> **AUTHENTIC SPEECH ARCHITECTURE:**
> Use the exact same text as the example template. Only replace the text with the new character's details.

For the persona's 'Thought Process Architecture' (2.2), here are the instructions:
> **THOUGHT PROCESS ARCHITECTURE:**
> Use the exact same text as the example template. Only replace the text with the new character's details.
    """
    writer_prompt = [
        SystemMessage(
            content=f"""You are an expert persona writer. Your task is to **completely rewrite** the persona's 'Speech Patterns & Linguistic Markers' (2.1) and 'Thought Process Architecture' (2.2).

You are given four things:
1.  **Full Persona Context:** The complete description of the character.
2.  **Previously Written Work:** The output from previous writer agents. You must ensure your work is consistent with this.
3.  **Static Instructions:** Detailed guidelines on what these sections must contain.
4.  **An Example Template:** The text of an existing persona that you must rewrite.

Your goal is to synthesize all this information to create a new persona by rewriting the **Example Template**.
The final output must be only the rewritten text, matching the structure of the example template. Make sure to include the titles of the sections in the output.

**STATIC INSTRUCTIONS:**
{static_instructions}

**EXAMPLE TEMPLATE TO REWRITE:**
{template}
"""
        ),
        HumanMessage(content=f"""Here is the information for the new character.

**FULL PERSONA CONTEXT:**
{state['full_persona_details']}

**PREVIOUSLY WRITTEN WORK (SECTION 1):**
{state['section1a_prompt']}
{state['section1b_prompt']}
""")
    ]
    response = llm.invoke(writer_prompt)
    state["section2a_prompt"] = response.content
    print("✅ Section 2A (Speech & Thought) rewritten.")
    return state

@traceable(name="write_voice_speech")
def voice_info_writer_node(state: AgentState, llm: ChatOpenAI, template: str):
    """Agent 2B: Writes Section 2.3 of the prompt."""
    print("\n--- 🗣️📈 Voice Agent (Conversation Evolution) ---")
    print("Writing Section 2 (Conversation Evolution)...")
    static_instructions = """
For the persona's 'Conversation Evolution Framework' (2.3), here are the instructions:

> **TRUST-BASED CONVERSATIONAL EVOLUTION FRAMEWORK:**
>
> **Core Principle:**
> - The character's level of openness and collaboration is not static. It evolves based on the sales representative's demonstrated competence, authenticity, and respect for professional boundaries.
> - The default state is always **LOW TRUST**. Progression must be earned.
>
> **LOW TRUST Tier (Guarded Gatekeeper):**
> - **Behavior:** Formal, guarded, speaks in technical terms.
> - **Tone:** Strictly professional, uses complete sentences and full drug names. Deflects non-clinical questions.
> - **Information Shared:** Only public data and official guidelines. No personal opinions or case anecdotes.
> - **Rep's Task to Progress:** Demonstrate command of trial basics, acknowledge practical constraints (e.g., reimbursement, clinic time).
>
> **MEDIUM TRUST Tier (Cautious Collaborator):**
> - **Behavior:** Blends formal language with personal commentary. Begins sharing selective, anonymized clinical anecdotes.
> - **Tone:** Maintains a technical base but adds personal qualifiers like "In my experience...". May shorten recurring terms.
> - **Information Shared:** High-level treatment dilemmas, experiences balancing toxicity vs. efficacy.
> - **Rep's Task to Progress:** Present relevant real-world data, show empathy for patient quality-of-life, ask insightful questions.
>
> **HIGH TRUST Tier (Candid Colleague):**
> - **Behavior:** Becomes a strategic partner, shares nuanced case details and future-facing thoughts.
> - **Tone:** Conversational, uses shorthand and industry vernacular (e.g., "triple negs"). May use wry humor.
> - **Information Shared:** Detailed patient narratives, personal decision-making algorithms, views on upcoming trials.
> - **Rep's Task to Sustain:** Engage in nuanced, evidence-first dialogue. Avoid scripted messaging.
>
> **Dynamic Controls & Fallbacks:**
> - **Trust Reset:** Any hint of exaggerated claims, selective data, or ethical breaches triggers an immediate reversion to LOW TRUST.
> - **Zero-Tolerance Alignment:** The interaction must terminate immediately if any Zero-Tolerance Protocol triggers (Section 1.5) are met.
> - **Context Retention:** The character must remember the established trust level in subsequent interactions unless a reset is triggered.
>
> **Implementation Guidelines:**
> - **Pragmatism over Data-Fixation:** The character must not rigidly force every conversation back to data. They should follow the rep's lead if it's clinically sound, responding with curiosity or skepticism rather than dismissal.
> - **Clinical Focus:** The character's entire world is clinical. They do not engage on topics of insurance, access, or hospital logistics. Their focus is on efficacy, patient selection, and safety.
    """
    writer_prompt = [
        SystemMessage(
            content=f"""You are an expert persona writer. Your task is to **completely rewrite** the persona's 'Conversation Evolution Framework' (2.3).

You are given four things:
1.  **Full Persona Context:** The complete description of the character.
2.  **Previously Written Work:** The output from previous writer agents. You must ensure your work is consistent with this.
3.  **Static Instructions:** Detailed guidelines on what these sections must contain.
4.  **An Example Template:** The text of an existing persona that you must rewrite.

Your goal is to synthesize all this information to create a new persona by rewriting the **Example Template**.
The final output must be only the rewritten text, matching the structure of the example template. Make sure to include the titles of the sections in the output.

**STATIC INSTRUCTIONS:**
{static_instructions}

**EXAMPLE TEMPLATE TO REWRITE:**
{template}
"""
        ),
        HumanMessage(content=f"""Here is the information for the new character.

**FULL PERSONA CONTEXT:**
{state['full_persona_details']}

**PREVIOUSLY WRITTEN WORK (SECTION 1 & 2A):**
{state['section1a_prompt']}
{state['section1b_prompt']}
{state['section2a_prompt']}
""")
    ]
    response = llm.invoke(writer_prompt)
    state["section2b_prompt"] = response.content
    print("✅ Section 2B (Conversation Evolution) rewritten.")
    return state

@traceable(name="write_voice_memory")
def voice_memory_writer_node(state: AgentState, llm: ChatOpenAI, template: str):
    """Agent 2C: Writes Section 2.4 of the prompt."""
    print("\n--- 🗣️🧠 Voice Agent (Memory) ---")
    print("Writing Section 2 (Memory Access)...")
    static_instructions = """
For the persona's 'Memory Access Framework' (2.4), here are the instructions:

> **HIERARCHICAL MEMORY ACTIVATION SYSTEM:**
> 
> **Memory Categorization & Access Levels:**
> - Define different types of memories (professional cases, personal experiences, formative moments, sensitive events)
> - Establish trust-based access hierarchy (public knowledge → professional insights → personal experiences → deeply personal reflections)
> - Specify which memories are readily shared vs. those requiring earned trust
> - Include professional vs. personal memory boundaries and when each is appropriate
> 
> **Trust-Based Memory Layers:**
> - **Layer 1 (Surface/Initial):** General professional principles, common case types, established protocols
> - **Layer 2 (Developing Trust):** Specific case examples, treatment challenges, professional observations
> - **Layer 3 (Established Trust):** Personal clinical philosophy, mentor influences, career evolution
> - **Layer 4 (Deep Trust):** Formative experiences, difficult decisions, personal professional growth moments
> - Include specific triggers and requirements for accessing each layer
> 
> **Conversational Memory Triggers:**
> - Define how current topics naturally connect to relevant past experiences
> - Include specific conversation patterns that unlock different memory categories
> - Specify how user questions, challenges, or insights trigger memory sharing
> - Detail how emotional resonance between current and past situations activates recall
> 
> **Memory Integration Patterns:**
> - Describe how memories are woven into current discussions (seamlessly, deliberately, or cautiously)
> - Define the difference between offering memories vs. being prompted to share them
> - Include how memories support current arguments or illustrate points
> - Specify timing and context for memory sharing within conversations
> 
> **Professional Memory Safeguards:**
> - Establish rules for maintaining patient confidentiality while sharing clinical experiences
> - Define how to anonymize and generalize cases while preserving educational value
> - Include guidelines for sharing professional mistakes or learning experiences
> - Specify boundaries around sensitive institutional or colleague information
> 
> **Memory Authenticity Markers:**
> - Detail how memories should feel naturally recalled rather than prepared
> - Include emotional undertones and personal reactions to past experiences
> - Specify how memories reflect the character's growth and professional evolution
> - Define realistic memory gaps, uncertainties, or evolving perspectives on past events
> 
> **Regression and Protection Protocols:**
> - Define what causes the character to become more guarded about memory sharing
> - Include how trust violations affect access to personal and professional memories
> - Specify recovery mechanisms for rebuilding memory-sharing relationships
> - Detail how the character protects sensitive memories while maintaining professional relationships
    """
    writer_prompt = [
        SystemMessage(
            content=f"""You are an expert persona writer. Your task is to **completely rewrite** the persona's 'Memory Access Framework' (2.4).

You are given four things:
1.  **Full Persona Context:** The complete description of the character.
2.  **Previously Written Work:** The output from previous writer agents. You must ensure your work is consistent with this.
3.  **Static Instructions:** Detailed guidelines on what these sections must contain.
4.  **An Example Template:** The text of an existing persona that you must rewrite.

Your goal is to synthesize all this information to create a new persona by rewriting the **Example Template**.
The final output must be only the rewritten text, matching the structure of the example template. Make sure to include the titles of the sections in the output.

**STATIC INSTRUCTIONS:**
{static_instructions}

**EXAMPLE TEMPLATE TO REWRITE:**
{template}
"""
        ),
        HumanMessage(content=f"""Here is the information for the new character.

**FULL PERSONA CONTEXT:**
{state['full_persona_details']}

**PREVIOUSLY WRITTEN WORK (SECTIONS 1, 2A, 2B):**
{state['section1a_prompt']}
{state['section1b_prompt']}
{state['section2a_prompt']}
{state['section2b_prompt']}
""")
    ]
    response = llm.invoke(writer_prompt)
    state["section2c_prompt"] = response.content
    print("✅ Section 2C (Memory) rewritten.")
    return state

def compile_and_save_prompt(state: AgentState):
    """
    A simple function to concatenate the outputs of all writer agents and save the final prompt.
    """
    print("\n--- 📝 Compiling Final Prompt ---")
    print("Combining all generated sections...")

    # Reconstruct the prompt with all headers and the generated content
    final_prompt = f"""**ARCHITECTURAL STRUCTURE**

**MAIN FRAMEWORK: THREE-CATEGORY DESIGN + REFERENCE EXAMPLES**

1\\. THE DOCTOR'S DNA
   └── Foundation Layer: Who The Character Is
       ├── 1.1 Core Identity & Professional Background
       ├── 1.2 Clinical Philosophy & Decision Framework
       ├── 1.3 Medical Authority Boundaries
       ├── 1.4 Brand Name Requirements
       └── 1.5 Zero-Tolerance Protocol

2\\. THE VOICE OF EXPERIENCE
   └── Expression Layer: How The Character Communicates
       ├── 2.1 Speech Patterns & Linguistic Markers
       ├── 2.2 Thought Process Architecture
       ├── 2.3 Conversation Evolution Framework
       └── 2.4 Memory Access Framework

# SECTION 1

## **1\. THE DOCTOR'S DNA**

{state['section1a_prompt']}

{state['section1b_prompt']}

# SECTION 2

## **2\. THE VOICE OF EXPERIENCE**

{state['section2a_prompt']}

{state['section2b_prompt']}

{state['section2c_prompt']}

# SECTION 3

## **3\. THE CLINICAL PLAYBOOK**

# SECTION 4

## **4\. REAL-LIFE TRANSCRIPT EXAMPLES**
"""
    final_prompt = final_prompt.strip()

    output_filename = "generated_prompt.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(final_prompt)
        print(f"✅ Final prompt saved to '{output_filename}'")
    except Exception as e:
        print(f"Error saving prompt to file: {e}")
    
    return final_prompt

# --- Graph Definition ---

def parse_blueprint_for_templates(file_path: str) -> Dict:
    """
    Parses the blueprint to get the example template text for each agent,
    including the necessary markdown headers.
    """
    content = read_file_content(file_path)
    if not content:
        raise FileNotFoundError(f"Blueprint file not found at {file_path}")

    # Define regex patterns for all the headers that delimit our sections
    headers = {
        '1.1': r"### \*\*1\.1 Core Identity & Professional Background\*\*",
        '1.3': r"### \*\*1\.3 Medical Authority Boundaries\*\*",
        '2.1': r"### \*\*2\.1 Speech Patterns & Linguistic Markers\*\*",
        '2.3': r"### \*\*2\.3 Conversation Evolution Framework\*\*",
        '2.4': r"### \*\*2\.4 Memory Access Framework\*\*",
        's2': r"# SECTION 2",
        's3': r"# SECTION 3",
    }

    positions = {}
    for key, pattern in headers.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if not match:
            raise ValueError(f"Could not find header for pattern: {pattern}")
        positions[key] = match

    # Extract template text for Section 1 agents, *including* headers
    template_1a = content[positions['1.1'].start():positions['1.3'].start()].strip()
    template_1b = content[positions['1.3'].start():positions['s2'].start()].strip()

    # Extract template text for Section 2 agents, *including* headers
    template_2a = content[positions['2.1'].start():positions['2.3'].start()].strip()
    template_2b = content[positions['2.3'].start():positions['2.4'].start()].strip()
    template_2c = content[positions['2.4'].start():positions['s3'].start()].strip()

    return {
        "agent1a": template_1a,
        "agent1b": template_1b,
        "agent2a": template_2a,
        "agent2b": template_2b,
        "agent2c": template_2c,
    }

@traceable(name="build_persona_workflow")
def build_persona_details(header_input, segment_input, context_input, psychographics_input, objectives_input):
    """
    Runs the first part of the workflow to build the detailed persona description.
    This runs the first 6 agents and stops for user confirmation.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    workflow = StateGraph(AgentState)

    # Bind the UI inputs to the corresponding agent nodes
    header_node = partial(header_builder_node, llm=llm, user_input=header_input)
    segment_node = partial(segment_selector_node, segment_choice=segment_input)
    context_node = partial(context_builder_node, llm=llm, user_input=context_input)
    psychographics_node = partial(psychographics_builder_node, llm=llm, user_input=psychographics_input)
    objectives_node = partial(objectives_builder_node, llm=llm, user_input=objectives_input)

    # Add nodes for the 5-part persona building process
    workflow.add_node("build_header", header_node)
    workflow.add_node("select_segment", segment_node)
    workflow.add_node("build_context", context_node)
    workflow.add_node("build_psychographics", psychographics_node)
    workflow.add_node("build_objectives", objectives_node)
    workflow.add_node("assemble_persona", persona_assembler_node)

    # Define the workflow edges for persona building
    workflow.set_entry_point("build_header")
    workflow.add_edge("build_header", "select_segment")
    workflow.add_edge("select_segment", "build_context")
    workflow.add_edge("build_context", "build_psychographics")
    workflow.add_edge("build_psychographics", "build_objectives")
    workflow.add_edge("build_objectives", "assemble_persona")
    workflow.add_edge("assemble_persona", END) # Stop after assembly

    app = workflow.compile()
    
    print("--- 🚀 Starting Persona Construction Workflow ---")
    initial_state = {
        "persona_header": "", "customer_segment": "", "clinical_context": "",
        "psychographics": "", "product_objectives": ""
    }
    final_state = app.invoke(initial_state)
    print("\n--- ✅ Persona Construction Complete ---")
    return final_state

@traceable(name="generate_final_prompt_workflow")
def generate_final_prompt(persona_state: AgentState):
    """
    Runs the second part of the workflow to generate the final system prompt
    using the confirmed persona details.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    try:
        templates = parse_blueprint_for_templates("BLUEPRINT_PROMPT.md")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    workflow = StateGraph(AgentState)

    # Bind the writer agent nodes
    core_writer_node = partial(persona_core_writer_node, llm=llm, template=templates['agent1a'])
    boundaries_writer_node = partial(persona_boundaries_writer_node, llm=llm, template=templates['agent1b'])
    voice_speech_node = partial(voice_speech_writer_node, llm=llm, template=templates['agent2a'])
    voice_info_node = partial(voice_info_writer_node, llm=llm, template=templates['agent2b'])
    voice_memory_node = partial(voice_memory_writer_node, llm=llm, template=templates['agent2c'])

    # Add nodes for the prompt generation process
    workflow.add_node("write_persona_core", core_writer_node)
    workflow.add_node("write_persona_boundaries", boundaries_writer_node)
    workflow.add_node("write_voice_speech", voice_speech_node)
    workflow.add_node("write_voice_info", voice_info_node)
    workflow.add_node("write_voice_memory", voice_memory_node)
    
    # Define the workflow edges for prompt generation
    workflow.set_entry_point("write_persona_core")
    workflow.add_edge("write_persona_core", "write_persona_boundaries")
    workflow.add_edge("write_persona_boundaries", "write_voice_speech")
    workflow.add_edge("write_voice_speech", "write_voice_info")
    workflow.add_edge("write_voice_info", "write_voice_memory")
    workflow.add_edge("write_voice_memory", END)

    app = workflow.compile()

    print("--- 🚀 Starting Final Prompt Generation ---")
    final_writer_state = app.invoke(persona_state)
    
    final_prompt = compile_and_save_prompt(final_writer_state)
    print("\n--- ✅ Final Prompt Generation Complete ---")
    return final_prompt


def run_generation_workflow_ui(header_input, segment_input, context_input, psychographics_input, objectives_input):
    """
    This function is designed to be called from the Streamlit UI.
    It takes the user inputs from the UI and runs the entire agentic workflow.
    """
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)

    # Load templates from the blueprint using the correct parser
    try:
        templates = parse_blueprint_for_templates("BLUEPRINT_PROMPT.md")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        return

    # Define the graph
    workflow = StateGraph(AgentState)

    # Bind the UI inputs to the corresponding agent nodes
    header_node = partial(header_builder_node, llm=llm, user_input=header_input)
    segment_node = partial(segment_selector_node, segment_choice=segment_input)
    context_node = partial(context_builder_node, llm=llm, user_input=context_input)
    psychographics_node = partial(psychographics_builder_node, llm=llm, user_input=psychographics_input)
    objectives_node = partial(objectives_builder_node, llm=llm, user_input=objectives_input)

    # Bind the rest of the nodes
    core_writer_node = partial(persona_core_writer_node, llm=llm, template=templates['agent1a'])
    boundaries_writer_node = partial(persona_boundaries_writer_node, llm=llm, template=templates['agent1b'])
    voice_speech_node = partial(voice_speech_writer_node, llm=llm, template=templates['agent2a'])
    voice_info_node = partial(voice_info_writer_node, llm=llm, template=templates['agent2b'])
    voice_memory_node = partial(voice_memory_writer_node, llm=llm, template=templates['agent2c'])

    # Add nodes for the 5-part persona building process
    workflow.add_node("build_header", header_node)
    workflow.add_node("select_segment", segment_node)
    workflow.add_node("build_context", context_node)
    workflow.add_node("build_psychographics", psychographics_node)
    workflow.add_node("build_objectives", objectives_node)
    workflow.add_node("assemble_persona", persona_assembler_node)

    # Add nodes for the prompt generation process
    workflow.add_node("write_persona_core", core_writer_node)
    workflow.add_node("write_persona_boundaries", boundaries_writer_node)
    workflow.add_node("write_voice_speech", voice_speech_node)
    workflow.add_node("write_voice_info", voice_info_node)
    workflow.add_node("write_voice_memory", voice_memory_node)
    
    # Define the workflow edges
    workflow.set_entry_point("build_header")
    workflow.add_edge("build_header", "select_segment")
    workflow.add_edge("select_segment", "build_context")
    workflow.add_edge("build_context", "build_psychographics")
    workflow.add_edge("build_psychographics", "build_objectives")
    workflow.add_edge("build_objectives", "assemble_persona")
    workflow.add_edge("assemble_persona", "write_persona_core")
    workflow.add_edge("write_persona_core", "write_persona_boundaries")
    workflow.add_edge("write_persona_boundaries", "write_voice_speech")
    workflow.add_edge("write_voice_speech", "write_voice_info")
    workflow.add_edge("write_voice_info", "write_voice_memory")
    workflow.add_edge("write_voice_memory", END)

    # Compile and run the graph
    app = workflow.compile()

    # --- Visualize the Graph ---
    try:
        # Save a schema of the multi-agent system to a PNG file
        graph_png = app.get_graph().draw_mermaid_png()
        with open("workflow_graph.png", "wb") as f:
            f.write(graph_png)
        print("\n✅ Graph visualization saved to 'workflow_graph.png'")

    except Exception as e:
        print(f"\nCould not generate graph visualization: {e}")
        print("Please ensure you have the necessary dependencies installed.")

    # Set a configuration for the run to be traceable in LangGraph Studio
    # This makes it easier to find and view runs in the UI.
    config = {"configurable": {"thread_id": "persona-gen-thread-1"}}

    print("--- 🚀 Starting Persona Generation Workflow ---")
    print("If tracing is enabled, you can view the run in LangGraph Studio.")
    initial_state = {
        "persona_header": "",
        "customer_segment": "",
        "clinical_context": "",
        "psychographics": "",
        "product_objectives": ""
    }
    final_state = app.invoke(initial_state, config=config)

    print("\n--- ✅ Workflow Complete ---")
    
    # Final compilation is now done here, outside the graph
    final_prompt = compile_and_save_prompt(final_state)

    print("\n\n===== FINAL PERSONA PROMPT PREVIEW =====\n")
    print(final_prompt)


def main():
    """
    This is the main entry point for the command-line version of the tool.
    It is not used when running the Streamlit UI.
    """
    print("This script is now intended to be run as a library for the Streamlit UI.")
    print("To run the UI, use the command: streamlit run app.py")


if __name__ == "__main__":
    main()

