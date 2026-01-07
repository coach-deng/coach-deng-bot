import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Coach Deng OS", page_icon="🏀", layout="wide")

st.sidebar.title("COACH DENG")
app_mode = st.sidebar.radio("S Y S T E M", ["📈 Finance Hub", "📝 Morten/Club Comms"])

# ==========================================
# TOOL: FINANCE HUB
# ==========================================
if app_mode == "📈 Finance Hub":
    st.title("📈 Revenue & Contract Tracker")
    
    # Static Data
    club_base = 7500
    private_target = 15000
    
    # Active Revenue
    st.subheader("Monthly Projections")
    col1, col2, col3 = st.columns(3)
    
    # Current Private Clients
    privates = 6600 # Ole, Emmanuel, Sigurd
    
    # New Potential Contracts (Morten/Espergærde)
    st.sidebar.subheader("Contract Estimator")
    camp_days = st.sidebar.number_input("Camp Days (Feb)", value=2)
    academy_visits = st.sidebar.number_input("Academy Visits/Mo", value=2)
    
    espergaerde_rev = (camp_days * 4000) + (academy_visits * 2000)
    
    total_rev = club_base + privates + espergaerde_rev
    
    col1.metric("TOTAL PROJECTED", f"{total_rev:,} DKK")
    col2.metric("PRIVATE/CONTRACT", f"{privates + espergaerde_rev:,} DKK")
    col3.metric("GAP TO 15K", f"{max(private_target - (privates + espergaerde_rev), 0):,} DKK")

    if (privates + espergaerde_rev) >= private_target:
        st.balloons()
        st.success("🔥 15K SAFETY GOAL EXCEEDED.")

# ==========================================
# TOOL: COMMS
# ==========================================
elif app_mode == "📝 Morten/Club Comms":
    st.title("📝 Club Proposal Builder")
    st.write("Use this to draft the official fee structure for Morten.")
    
    with st.form("proposal"):
        st.write("### Espergærde Academy & Camp Proposal")
        daily_rate = st.number_input("Camp Daily Rate (DKK)", value=4000)
        visit_rate = st.number_input("Academy Visit Rate (DKK)", value=2000)
        
        if st.form_submit_button("Generate Proposal Text"):
            proposal = f"""
            **Proposal for Espergærde Basketball**
            **Coach:** Deng Awak (Ex-Pro / Performance Consultant)
            
            1. **High-Performance Camp (Feb 21-22):** {daily_rate} DKK / day.
               *Focus: Technical Audits, Elite Standard Protocols.*
               
            2. **Academy Consultant (Bi-monthly):** {visit_rate} DKK / visit.
               *Focus: On-court development + 20 min Mental Performance session.*
            
            Total Monthly (Est): {(daily_rate*2) + (visit_rate*2)} DKK
            """
            st.code(proposal)
