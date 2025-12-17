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
    # Configure the API
    genai.configure(api_key=api_key)
    
    # --- USE THE CLASSIC MODEL (Stable) ---
    # We use 'gemini-pro' because it works on all software versions
    model = genai.GenerativeModel("gemini-pro")

    # --- USER INTERFACE ---
    with st.form("msg_form"):
        st.write("✅ System Ready (Classic Mode)")
        user_notes = st.text_area("Paste notes here:", height=100)
        msg_type = st.radio("Type:", ["Template A (Parent)", "Template B (Exec)", "Template C (Post)"])
        submitted = st.form_submit_button("Generate")

    if submitted and user_notes:
        try:
            # Classic model needs the prompt combined manually
            full_prompt = f"{sys_instruction}\n\nTASK: Use {msg_type} for: {user_notes}"
            response = model.generate_content(full_prompt)
            
            st.success("Draft:")
            st.text_area("Copy:", value=response.text, height=250)
            
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("If this fails, your API Key might be invalid or from Google Cloud instead of AI Studio.")

else:
    st.warning("Enter API Key to start.")
