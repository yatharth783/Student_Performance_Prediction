import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime

# --- SET PAGE CONFIG ---
st.set_page_config(page_title="EduAI Premium", page_icon="💎", layout="wide")

# --- THE ULTIMATE CSS OVERHAUL ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    /* Global Base */
    .stApp {
        background-color: #050505;
        background-image: 
            radial-gradient(at 0% 0%, rgba(37, 99, 235, 0.1) 0, transparent 50%), 
            radial-gradient(at 50% 0%, rgba(124, 58, 237, 0.1) 0, transparent 50%);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #ffffff;
    }

    /* Hide Streamlit Header & Elements */
    header {visibility: hidden;}
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Bento Card System */
    .bento-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 24px;
        padding: 24px;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
    }
    .bento-card:hover {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transform: translateY(-5px);
    }

    /* Typography */
    h1, h2, h3 { color: #ffffff; font-weight: 700; letter-spacing: -0.02em; }
    .metric-label { color: #94a3b8; font-size: 0.85rem; font-weight: 500; margin-bottom: 8px; }
    .metric-value { font-size: 2rem; font-weight: 800; color: #ffffff; }

    /* Prediction Glow Box */
    .prediction-box {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        border-radius: 32px;
        padding: 48px;
        text-align: center;
        box-shadow: 0 0 60px rgba(37, 99, 235, 0.3);
        margin-top: 20px;
    }

    /* Buttons */
    .stButton>button {
        background: #ffffff !important;
        color: #000000 !important;
        border-radius: 14px !important;
        padding: 16px 28px !important;
        font-weight: 700 !important;
        border: none !important;
        width: 100%;
        font-size: 1rem !important;
        transition: 0.3s !important;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px rgba(255,255,255,0.4);
    }

    /* Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #2563eb;
    }

    /* Sidebar Sliders & Inputs */
    .stSlider label, .stTextInput label { color: #cbd5e1 !important; font-weight: 600; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (CONFIG PANEL) ---
with st.sidebar:
    st.markdown("<h2 style='font-size: 1.5rem;'>Edu<span style='color:#3b82f6;'>AI</span> Pro</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("### 🧬 Data Profile")
    name = st.text_input("Candidate Name", "Anish Sharma")
    std_id = st.text_input("Reference ID", "STU-992-01")
    
    st.markdown("### 📊 Variables")
    attendance = st.slider("Attendance rate", 0, 100, 85)
    study_hours = st.slider("Weekly focus", 0, 60, 20)
    prev_score = st.slider("Benchmark score", 0, 100, 75)
    
    with st.expander("Advanced Overrides"):
        backlogs = st.number_input("Backlogs", 0, 5, 0)
        participation = st.slider("Participation", 0, 100, 60)

# --- MAIN CONTENT ---

# 1. Floating Header
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <div>
            <p style="color: #64748b; font-weight: 600; margin-bottom: 4px;">SYSTEM STATUS: ACTIVE</p>
            <h1 style="margin: 0; font-size: 2.5rem;">Academic Intelligence <span style="color:#3b82f6;">.</span></h1>
        </div>
        <div style="text-align: right; background: rgba(255,255,255,0.05); padding: 12px 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1);">
            <p style="color: #94a3b8; font-size: 0.8rem; margin: 0;">LOGGED IN AS</p>
            <p style="color: #ffffff; font-weight: 700; margin: 0;">{name}</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 2. Bento Grid Layout
col_main = st.columns([1, 1, 1], gap="medium")

# Card 1: Attendance
with col_main[0]:
    st.markdown(f"""
        <div class="bento-card">
            <p class="metric-label">ATTENDANCE LEVEL</p>
            <div class="metric-value">{attendance}%</div>
            <div style="height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 15px;">
                <div style="height: 4px; background: #3b82f6; width: {attendance}%; border-radius: 2px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Card 2: Study Time
with col_main[1]:
    st.markdown(f"""
        <div class="bento-card">
            <p class="metric-label">WEEKLY FOCUS</p>
            <div class="metric-value">{study_hours} hrs</div>
            <p style="color: #22c55e; font-size: 0.8rem; margin-top: 10px;">+12% vs. peer average</p>
        </div>
    """, unsafe_allow_html=True)

# Card 3: Risks
with col_main[2]:
    risk_color = "#ef4444" if backlogs > 0 else "#22c55e"
    risk_text = "HIGH RISK" if backlogs > 0 else "STABLE"
    st.markdown(f"""
        <div class="bento-card">
            <p class="metric-label">ACADEMIC STABILITY</p>
            <div class="metric-value" style="color: {risk_color};">{risk_text}</div>
            <p style="color: #94a3b8; font-size: 0.8rem; margin-top: 10px;">Based on {backlogs} active backlogs</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Prediction Section
col_left, col_right = st.columns([1.2, 1], gap="large")

with col_left:
    st.markdown("### 🤖 Neural Engine")
    st.markdown("<p style='color:#94a3b8;'>Running cross-validation on candidate metrics. Click below to execute the prediction model.</p>", unsafe_allow_html=True)
    
    if st.button("EXECUTE PREDICTION ENGINE"):
        with st.status("Initializing engine...", expanded=False) as status:
            time.sleep(0.6)
            st.write("Loading trained weights...")
            time.sleep(0.8)
            st.write("Normalizing input vectors...")
            time.sleep(0.6)
            status.update(label="Analysis Complete", state="complete")
        
        # Simulating Model Prediction
        res = (prev_score * 0.45) + (attendance * 0.25) + (study_hours * 0.2) + (participation * 0.1)
        if backlogs > 0: res -= (backlogs * 5)
        st.session_state['result'] = round(min(max(res, 0), 100), 1)

    # Feature Importance Chart
    if 'result' in st.session_state:
        st.markdown("<br><h4>Factor Contribution</h4>", unsafe_allow_html=True)
        factors = ['Score History', 'Attendance', 'Focus Time', 'Backlogs']
        impacts = [45, 25, 20, 10]
        
        fig = go.Figure(go.Bar(
            x=impacts, y=factors, orientation='h',
            marker=dict(color='rgba(37, 99, 235, 0.6)', line=dict(color='#3b82f6', width=1)),
            width=0.4
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'), margin=dict(l=0, r=0, t=0, b=0),
            height=200, xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

with col_right:
    if 'result' in st.session_state:
        score = st.session_state['result']
        if score >= 85: cat, glow = "EXCEPTIONAL", "rgba(34, 197, 94, 0.4)"
        elif score >= 70: cat, glow = "STRONG", "rgba(59, 130, 246, 0.4)"
        else: cat, glow = "AT RISK", "rgba(239, 68, 68, 0.4)"

        st.markdown(f"""
            <div class="prediction-box" style="box-shadow: 0 0 50px {glow};">
                <p style="text-transform: uppercase; letter-spacing: 3px; font-size: 0.75rem; opacity: 0.8; font-weight: 700;">Forecasted Score</p>
                <h1 style="font-size: 6rem; margin: 0; font-weight: 900;">{score}%</h1>
                <div style="background: rgba(255,255,255,1); color: #000; padding: 8px 32px; border-radius: 100px; display: inline-block; font-weight: 800; font-size: 1rem; margin-top: 1rem;">
                    {cat}
                </div>
            </div>
        """, unsafe_allow_html=True)

# 4. Insights Footer
if 'result' in st.session_state:
    st.markdown("<br>### 💡 AI Strategic Insights")
    i1, i2, i3 = st.columns(3)
    with i1:
        st.markdown("<div class='bento-card'><h4 style='color:#3b82f6;'>Momentum</h4><p style='color:#94a3b8; font-size:0.9rem;'>Increase weekly focus by 4 hours to hit the 90th percentile.</p></div>", unsafe_allow_html=True)
    with i2:
        st.markdown("<div class='bento-card'><h4 style='color:#3b82f6;'>Focus Area</h4><p style='color:#94a3b8; font-size:0.9rem;'>Historical data suggests your quiz performance is the key driver.</p></div>", unsafe_allow_html=True)
    with i3:
        st.markdown("<div class='bento-card'><h4 style='color:#3b82f6;'>Risk Factor</h4><p style='color:#94a3b8; font-size:0.9rem;'>No critical threats detected. Maintain current engagement levels.</p></div>", unsafe_allow_html=True)

# Footer
st.markdown("<br><p style='text-align:center; color:#475569; font-size:0.7rem;'>PROPRIETARY SYSTEM • EDUAI QUANTUM V4.2</p>", unsafe_allow_html=True)