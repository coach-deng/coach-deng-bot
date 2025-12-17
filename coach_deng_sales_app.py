import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Coach Deng | Outreach Agent",
    page_icon="🏀",
    layout="centered"
)

# --- HEADER & STYLE ---
st.title("🏀 Corporate Athlete Sales Bot")
st.markdown("*Your AI assistant for high-stakes outreach.*")

# --- SIDEBAR (API KEY) ---
# This checks if the key is in Streamlit Secrets (for the live app)
# or asks you to paste it if running locally.
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("AIzaSyDGY2NAIrd24n_i-yBp0wF9LU7_gVtprAA", type="password")

# --- THE AI BRAIN (MOVED TO PROMPT FOR STABILITY) ---
sys_instruction = """
You are the elite Sales Assistant for Coach Deng Awak.
Coach Deng is pivoting to "Executive Mental Performance".

Your Goal: Write short, punchy, high-status messages.

TEMPLATE A (Parents of Elite Kids):
"Hey [Name], hope the family is well! I’m launching a new Elite Mental Performance program in January focused on 'Clutch Mentality'. I think [Kid's Name] has the talent for it. I’m opening 3 spots for a 'Founding Member' rate. Open to a 5-min chat?"

TEMPLATE B (Executives/CEOs):
"Hey [Name], hope you're doing well. I’m making a shift in 2026 to bring my pro athlete protocols into the business world—helping leaders manage high-pressure decision-making. I’m looking for 2-3 experienced leaders to beta test the program. No sales pitch, just value. Let me know if you're open to a 10-min coffee."

TEMPLATE C (LinkedIn Post):
Write a LinkedIn post using the hook "Stop playing like an amateur." Focus on the connection between Sports Pressure and Business Pressure. Tone: Professional, Athletic, Confident.
"""

if api_key:
    # Configure the API
    genai.configure(api_key=api_key)
    
    # We use a simpler model initialization to avoid errors
    model = genai.GenerativeModel("gemini-1.5-flash")

    # --- THE USER INTERFACE ---
    with st.form("message_form"):
        st.write("### 🎯 Who are we messaging?")
        
        # Input Note
        user_notes = st.text_area(
            "Paste rough notes here:", 
            placeholder="e.g. Peter, CEO of Maersk, met at gala. Wants to improve focus.",
            height=100
        )
        
        # Buttons to select type
        msg_type = st.radio(
            "Select Output Type:",
            ["Template A (Parent)", "Template B (Executive)", "Template C (LinkedIn Post)"],
            horizontal=True
        )
        
        submitted = st.form_submit_button("🚀 Generate Message")

    # --- OUTPUT ---
    if submitted and user_notes:
        with st.spinner("Drafting the perfect message..."):
            # Combine the brain instructions with the user request (Fail-safe method)
            full_prompt = f"{sys_instruction}\n\nTASK: Using {msg_type}, write a message based on these notes: {user_notes}"
            
            try:
                response = model.generate_content(full_prompt)
                st.success("Draft Ready:")
                st.text_area("Copy this:", value=response.text, height=250)
            except Exception as e:
                st.error(f"Error: {e}")
            
    elif submitted and not user_notes:
        st.warning("Please enter some notes first.")

else:
    st.warning("⚠️ Please enter your API Key in the sidebar to start.")
