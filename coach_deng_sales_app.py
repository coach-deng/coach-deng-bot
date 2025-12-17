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

# --- THE "AUTO-DETECT" ENGINE ---
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. Try to find the best available model automatically
        model_name = "gemini-1.5-flash" # Default target
        
        try:
            # Ask Google what models this key can see
            available_models = [m.name for m in genai.list_models()]
            
            # Logic to pick the best working model
            if "models/gemini-1.5-flash" in available_models:
                model_name = "gemini-1.5-flash"
            elif "models/gemini-pro" in available_models:
                model_name = "gemini-pro"
            elif "models/gemini-1.0-pro" in available_models:
                model_name = "gemini-1.0-pro"
                
        except Exception:
            # If listing fails, just force the standard one
            model_name = "gemini-pro"

        # 2. Load the model
        model = genai.GenerativeModel(model_name)

        # --- USER INTERFACE ---
        with st.form("msg_form"):
            st.write(f"✅ Connected using model: `{model_name}`")
            user_notes = st.text_area("Paste notes here:", height=100)
            msg_type = st.radio("Type:", ["Template A (Parent)", "Template B (Exec)", "Template C (Post)"])
            submitted = st.form_submit_button("Generate")

        if submitted and user_notes:
            prompt = f"{sys_instruction}\n\nREQ: Use {msg_type} for: {user_notes}"
            response = model.generate_content(prompt)
            st.success("Draft:")
            st.text_area("Copy:", value=response.text, height=250)

    except Exception as e:
        st.error(f"Connection Error: {e}")
        st.info("💡 Tip: Ensure your API Key is from 'aistudio.google.com' and not Google Cloud Console.")
else:
    st.warning("Enter API Key to start.")
