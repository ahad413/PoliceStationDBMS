import streamlit as st
import base64
st.set_page_config(
    page_title="About",
    layout="wide"
)

# ════════════════════════════════════════════════
# CSS
# ════════════════════════════════════════════════
st.markdown("""
<style>

.stApp {
    background-color: #0f1117;
}

/* Hero */
.hero-title {
    text-align: center;
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-sub {
    text-align: center;
    font-size: 16px;
    color: #9aa0b8;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #1e2130, #252a3d);
    border: 1px solid #2f344d;
    border-radius: 16px;
    padding: 28px;
    transition: 0.3s;
}

.card:hover {
    border-color: #4CAF50;
    transform: translateY(-3px);
}

.card-title {
    font-size: 18px;
    font-weight: bold;
    color: #4CAF50;
    margin-bottom: 10px;
}

.card-text {
    font-size: 14px;
    color: #9aa0b8;
    line-height: 1.7;
}

/* Team card */
.team-card {
    background: linear-gradient(135deg, #1e2130, #252a3d);
    border: 1px solid #2f344d;
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: 0.3s;
}

.team-card:hover {
    border-color: #4CAF50;
    transform: translateY(-3px);
}

.team-name {
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    margin-top: 10px;
    margin-bottom: 5px;
}

.team-role {
    font-size: 14px;
    color: #9aa0b8;
    line-height: 1.5;
    margin-top: 8px;
}

.divider {
    height: 1px;
    background: linear-gradient(to right, transparent, #2f344d, transparent);
    margin: 40px 0;
}

.team-avatar {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
    margin-bottom: 15px;
    border: 3px solid #4CAF50;
}

.footer {
    text-align: center;
    color: #555e7a;
    font-size: 13px;
    padding: 30px 0 10px 0;
}

</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# HERO
# ════════════════════════════════════════════════

st.markdown("""
<div style='padding:40px 0; text-align:center;'>
    <div style='font-size:55px;'></div>
    <div class='hero-title'>Police Station Management System</div>
    <div class='hero-sub'>
        A modern platform designed to streamline police operations
        with efficiency, accuracy and digital control.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# ABOUT SYSTEM
# ════════════════════════════════════════════════

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>Overview</div>
        <div class='card-text'>
            The Police Station Management System is a centralized
            digital solution that simplifies day‑to‑day law enforcement
            operations. It enables structured management of records,
            reporting, monitoring and administrative workflows
            through a unified interface.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>Core Capabilities</div>
        <div class='card-text'>
            • Duty & Attendance Management<br>
            • FIR & Crime Tracking<br>
            • Property & Asset Monitoring<br>
            • Beat & Patrol Logging<br>
            • Operational Reporting<br>
            • Administrative Control
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# TEAM
# ════════════════════════════════════════════════


def get_base64(image_path):
    with open(image_path, "rb") as img:
        return base64.b64encode(img.read()).decode()


img1 = get_base64("assets/system.png")
img2 = get_base64("assets/backend.png")
img3 = get_base64("assets/front.png")
st.markdown("### 👥 Our Team")
st.markdown(" ")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class='team-card'>
        <img src="data:image/png;base64,{img1}" class='team-avatar'>
        <div class='team-name'>Ahad Ata</div>
        <div class='team-role'>System Architecture & Development</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='team-card'>
        <img src="data:image/png;base64,{img2}" class='team-avatar'>
        <div class='team-name'>Ahmer Ijaz</div>
        <div class='team-role'>Backend & Database Design</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='team-card'>
        <img src="data:image/png;base64,{img3}" class='team-avatar'>
        <div class='team-name'>Sulman Tariq</div>
        <div class='team-role'>UI UX & Frontend Design</div>
    </div>
    """, unsafe_allow_html=True)
# ════════════════════════════════════════════════
# FOOTER
# ════════════════════════════════════════════════

st.markdown("""
<div class='footer'>
    © 2026 Police Station Management System · All Rights Reserved
</div>
""", unsafe_allow_html=True)