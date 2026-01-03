import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Deng Performance OS", page_icon="🏀", layout="wide")

# --- 🔐 API KEY SETUP (SECURE) ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")

# --- MODEL SETUP ---
model = None
if api_key:
    try:
        genai.configure(api_key=api_key)
        all_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in all_models else all_models[0]
        model = genai.GenerativeModel(model_name)
        st.sidebar.success(f"Connected: {model_name}")
    except Exception as e:
        st.sidebar.error(f"API Error: {e}")

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🏀 Deng Performance OS")
st.sidebar.caption("v4.0 - Finance & Strategy Edition")
app_mode = st.sidebar.radio("Navigate:", [
    "📈 Finance & Strategy Hub",
    "📝 Sales & Content Agent", 
    "🧠 Curriculum Builder"
])

# ==========================================
# TOOL 1: FINANCE & STRATEGY HUB
# ==========================================
if app_mode == "📈 Finance & Strategy Hub":
    st.title("📈 2026 Finance & Strategy Hub")
    st.write("Target: $100k CAD (~510,000 DKK) Annual Profit")

    # --- CORE BUSINESS DATA ---
    club_income = 7500
    private_target_goal = 15000 # Your specific 15k coaching goal
    total_safety_target = club_income + private_target_goal

    # --- CLIENT DATABASE (Ole, Emmanuel, Sigurd) ---
    clients = [
        {"Month": "January", "Name": "Ole", "Tier": "Amateur", "DKK": 2200, "Status": "Pending"},
        {"Month": "January", "Name": "Emmanuel", "Tier": "Amateur", "DKK": 2200, "Status": "Paid"},
        {"Month": "January", "Name": "Sigurd", "Tier": "Amateur", "DKK": 2200, "Status": "Pending"},
    ]
    df_clients = pd.DataFrame(clients)

    # --- CALCULATIONS ---
    current_private_total = df_clients["DKK"].sum()
    current_monthly_total = club_income + current_private_total
    remaining_gap = max(private_target_goal - current_private_total, 0)
    
    # --- TOP METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Current Total (Club + Private)", f"{current_monthly_total:,} DKK")
    m2.metric("Current Private Rev", f"{current_private_total:,} DKK")
    m3.metric("Gap to 15k Private Goal", f"{remaining_gap:,} DKK", delta_color="inverse")

    # --- EXPORT TO GOOGLE SHEETS ---
    st.divider()
    col_table, col_export = st.columns([2, 1])
    
    with col_table:
        st.subheader("📋 Active Client List")
        st.dataframe(df_clients, use_container_width=True)
        
    with col_export:
        st.subheader("📥 Export Data")
        st.write("Download this CSV and upload it to Google Sheets.")
        
        # Convert DF to CSV
        csv_buffer = StringIO()
        df_clients.to_csv(csv_buffer, index=False)
        csv_string = csv_buffer.getvalue()
        
        st.download_button(
            label="Download for Google Sheets",
            data=csv_string,
            file_name="Deng_Performance_2026_Tracker.csv",
            mime="text/csv"
        )

    # --- STRATEGY & TIPS SECTION ---
    st.divider()
    st.header("🧠 Coaching Strategy & Formulas")
    
    tip1, tip2 = st.columns(2)
    
    with tip1:
        st.info("**Current Sales Strategy**")
        if remaining_gap > 0:
            st.write(f"You are **{remaining_gap:,} DKK** away from your safety goal.")
            st.write(f"- Need **1 Executive** (6,500) and **1 Amateur** (2,200).")
            st.write("- OR need **4 Amateurs** (2,200).")
        else:
            st.write("✅ Safety Goal Met. Shift focus to Executive Upselling.")

    with tip2:
        st.info("**The Alberta Advantage**")
        alberta_tax = current_private_total * 0.11
        denmark_tax = current_private_total * 0.22
        savings = denmark_tax - alberta_tax
        st.write(f"Estimated Monthly Tax Savings: **{savings:,.0f} DKK**")
        st.write("Keep this revenue in the Alberta Corp to maximize your $100k CAD goal.")

    # --- GOOGLE SHEETS FORMULA CHEAT SHEET ---
    with st.expander("📝 View Google Sheets Formulas"):
        st.write("Paste these into your cells for auto-tracking:")
        st.code("=SUM(E2:E10) # Total Revenue column")
        st.code("=15000 - [Cell] # Remaining Gap")
        st.code("=([Cell] * 0.19) / 100000 # % of $100k CAD Goal")

# ==========================================
# TOOL 2: SALES & CONTENT AGENT
# ==========================================
elif app_mode == "📝 Sales & Content Agent":
    st.title("📝 Sales & Content Agent")
    tab1, tab2 = st.tabs(["Sales Outreach", "Social Hooks"])
    
    with tab1:
        st.subheader("Write a Sales Message")
        notes = st.text_area("Prospect Details:", placeholder="e.g. Peter, 45, Tech Exec, back pain but wants to stay sharp...")
        tier = st.radio("Tier:", ["Amateur (Parent)", "Elite (Athlete)", "Executive (CEO)"])
        
        if st.button("Generate Message") and model:
            prompt = f"As Coach Deng, write a high-status, athletic, and professional sales message for a {tier} client based on these notes: {notes}. Use Deng Performance branding."
            with st.spinner("Drafting..."):
                response = model.generate_content(prompt)
                st.success("Draft Ready:")
                st.write(response.text)

    with tab2:
        st.subheader("Viral Content Hooks")
        topic = st.text_input("Topic:", value="Interview with Malthe (Orangeville Prep)")
        if st.button("Generate Viral Hooks") and model:
            prompt = f"Generate 3 viral hooks for Instagram/TikTok about {topic}. Focus on 'The Elite Standard' and 'Mental Toughness'."
            response = model.generate_content(prompt)
            st.write(response.text)

# ==========================================
# TOOL 3: CURRICULUM BUILDER
# ==========================================
elif app_mode == "🧠 Curriculum Builder":
    st.title("🧠 Curriculum Architect")
    st.caption("Design 60-minute high-performance sessions.")
    
    c1, c2 = st.columns(2)
    client_type = c1.selectbox("Client Type", ["Youth Amateur", "Elite Athlete", "Corporate Executive"])
    focus_week = c2.selectbox("Focus Area", ["Foundation/Core", "Pressure/Clutch", "Recovery/Mobility", "Execution/IQ"])
    
    if st.button("Build Plan") and model:
        prompt = f"Design a professional 60-minute Deng Performance session for a {client_type} focusing on {focus_week}. Include 'The Big Idea' and a 'Homework Takeaway'."
        with st.spinner("Designing..."):
            response = model.generate_content(prompt)
            st.markdown(response.text)
