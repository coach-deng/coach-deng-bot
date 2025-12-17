import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Coach Deng Bot", page_icon="🏀")
st.title("🏀 Corporate Athlete Sales Bot")

# --- API KEY SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# --- THE SYSTEM INSTRUCTIONS ---
sys_instruction = """
You are the elite Sales Assistant for Coach Deng Awak.
Goal: Write short, punchy, high-status messages.
Templates:
A (Parents): "Hey [Name], launching Elite Mental Performance program... think [Kid] has talent... 3 spots left... 5-min chat?"
B (Execs): "Hey [Name], bringing pro athlete protocols to business... avoid burnout... beta testing... 10-min coffee?"
C (Post): Hook "Stop playing like an amateur." Sports vs Business pressure.
"""

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- THE UNIVERSAL ADAPTER (Fixes 404 Errors) ---
        # 1. Ask Google what models are actually available for this Key
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        # 2. Smart Selection Logic
        if not available_models:
            st.error("❌ No models found. Your API Key might be valid but has no access to Generative AI.")
            st.info("Please create a new key at: https://aistudio.google.com/")
            st.stop()
            
        # Priority list: Try Flash first (fastest), then Pro, then whatever is first in the list
        if "models/gemini-1.5-flash" in available_models:
            model_name = "models/gemini-1.5-flash"
        elif "models/gemini-pro" in available_models:
            model_name = "models/gemini-pro"
        elif "models/gemini-1.0-pro" in available_models:
             model_name = "models/gemini-1.0-pro"
        else:
            model_name = available_models[0] # Fallback: Just take the first one that works

        # 3. Load the winner
        model = genai.GenerativeModel(model_name)

        # --- USER INTERFACE ---
        with st.form("msg_form"):
            st.caption(f"✅ Connected to: {model_name}")
            user_notes = st.text_area("Paste notes here:", height=100)
            msg_type = st.radio("Type:", ["Template A (Parent)", "Template B (Exec)", "Template C (Post)"])
            submitted = st.form_submit_button("Generate")

        if submitted and user_notes:
            # Combine Prompt
            full_prompt = f"{sys_instruction}\n\nTASK: Use {msg_type} for: {user_notes}"
            response = model.generate_content(full_prompt)
            st.success("Draft:")
            st.text_area("Copy:", value=response.text, height=250)

    except Exception as e:
        st.error(f"Error: {e}")
        st.info("If this persists, verify your Key is from Google AI Studio (aistudio.google.com).")
else:
    st.warning("Enter API Key to start.")
