import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Coach Deng Command Center", page_icon="🏀", layout="wide")

# --- API KEY SETUP ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# --- MODEL SETUP (Universal Adapter v2) ---
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # 1. Get list of ALL models your key can see
        try:
            all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        except:
            all_models = []

        # 2. Smart Selection (Prioritize Flash, then Pro, then Anything)
        if "models/gemini-1.5-flash" in all_models:
            model_name = "models/gemini-1.5-flash"
        elif "models/gemini-1.5-pro" in all_models:
            model_name = "models/gemini-1.5-pro"
        elif "models/gemini-1.0-pro" in all_models:
            model_name = "models/gemini-1.0-pro"
        elif all_models:
            model_name = all_models[0] # Just take the first one that works
        else:
            model_name = "gemini-1.5-flash" # Blind fallback

        model = genai.GenerativeModel(model_name)
        
        # Show connection status in sidebar (for debugging)
        st.sidebar.success(f"Connected: {model_name}")
        
    except Exception as e:
        st.sidebar.error(f"API Connection Error: {e}")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏀 Command Center")
app_mode = st.sidebar.radio("Select Tool:", ["📝 Sales Agent", "🧠 Curriculum Builder", "💰 Revenue Calc"])

# ==========================================
# TOOL 1: SALES AGENT (The Outreach Bot)
# ==========================================
if app_mode == "📝 Sales Agent":
    st.title("📝 Outreach Specialist")
    st.caption("Draft high-status messages in seconds.")
    
    sys_instruction = """
    Role: Elite Sales Assistant for Coach Deng.
    Tone: Professional, Athletic, Confident.
    Templates:
    A (Parents): "Hey [Name], launching Elite Mental Performance program... 3 spots left... 5-min chat?"
    B (Execs): "Hey [Name], bringing pro athlete protocols to business... avoid burnout... 10-min coffee?"
    C (Post): Hook "Stop playing like an amateur." Sports vs Business pressure.
    """
    
    with st.form("msg_form"):
        user_notes = st.text_area("Prospect Notes:", height=100)
        msg_type = st.radio("Type:", ["Template A (Parent)", "Template B (Exec)", "Template C (Post)"])
        submitted = st.form_submit_button("Generate Draft")
    
    if submitted and user_notes:
        if model:
            try:
                with st.spinner("Drafting..."):
                    prompt = f"{sys_instruction}\n\nTASK: Use {msg_type} for: {user_notes}"
                    response = model.generate_content(prompt)
                    st.success("Ready to Send:")
                    st.text_area("Copy:", value=response.text, height=200)
            except Exception as e:
                st.error(f"Error generating message: {e}")
        else:
            st.warning("Please check API Key.")

# ==========================================
# TOOL 2: CURRICULUM BUILDER (The Organizer)
# ==========================================
elif app_mode == "🧠 Curriculum Builder":
    st.title("🧠 Curriculum Architect")
    st.caption("Plan your sessions so you never show up unprepared.")
    
    col1, col2 = st.columns(2)
    with col1:
        client_type = st.selectbox("Client Type", ["Executive (Burnout/Focus)", "Elite Athlete (Clutch/Confidence)", "Youth (Discipline)"])
    with col2:
        session_week = st.selectbox("Session Week", ["Week 1 (Foundation)", "Week 2 (Pressure)", "Week 3 (Recovery)", "Week 4 (Execution)"])
        
    if st.button("Design Session Plan"):
        if model:
            try:
                with st.spinner("Designing High-Performance Plan..."):
                    prompt = f"""
                    Act as a World-Class Performance Coach.
                    Create a 60-minute session plan for: {client_type}, {session_week}.
                    
                    Format:
                    1. The Big Idea (The "Why")
                    2. The Warm-up (Mental or Physical)
                    3. The Core Concept (What are we teaching?)
                    4. The Drill/Exercise (Practical application)
                    5. The Homework (One actionable takeaway)
                    """
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
            except Exception as e:
                st.error(f"Error generating plan: {e}")
        else:
            st.warning("Please check API Key.")

# ==========================================
# TOOL 3: REVENUE CALCULATOR (The Math)
# ==========================================
elif app_mode == "💰 Revenue Calc":
    st.title("💰 2026 Goal Tracker")
    st.caption("Live math on your startup capital.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        youth_clients = st.number_input("Youth Clients", value=0)
        youth_rate = st.number_input("Youth Rate", value=2200)
    with col2:
        elite_clients = st.number_input("Elite Clients", value=0)
        elite_rate = st.number_input("Elite Rate", value=3400)
    with col3:
        exec_clients = st.number_input("Exec Clients", value=0)
        exec_rate = st.number_input("Exec Rate", value=6500)
        
    monthly_rev = (youth_clients * youth_rate) + (elite_clients * elite_rate) + (exec_clients * exec_rate)
    
    st.divider()
    st.metric(label="Total Monthly Revenue", value=f"{monthly_rev:,} DKK")
    
    if monthly_rev > 0:
        months_to_startup = 25000 / monthly_rev
        months_to_100k = 100000 / monthly_rev
        
        c1, c2 = st.columns(2)
        c1.info(f"**Time to Startup (25k):** {months_to_startup:.1f} Months")
        c2.success(f"**Time to 100k:** {months_to_100k:.1f} Months")
    else:
        st.warning("Enter clients to see timeline.")
