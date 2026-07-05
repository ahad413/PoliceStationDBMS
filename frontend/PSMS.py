
from pathlib import Path

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import urllib.request
import mysql.connector
from backend.db import DB_CONFIG

st.set_page_config(
    page_title="Police Station Management System",
    page_icon="",
    layout="wide"
)

# ══════════════════════════════════════════════════════════
# INTERNET CHECK
# ══════════════════════════════════════════════════════════

def check_internet():
    try:
        urllib.request.urlopen("https://www.google.com", timeout=3)
        return True
    except:
        return False

internet_status = check_internet()

if internet_status:
    status_badge = "<span class='badge-online'> System Online</span>"
else:
    status_badge = "<span class='badge-offline'> System Offline</span>"

# ══════════════════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════════════════

st.markdown("""
<style>
.stApp { background-color: #0f1117; }
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1e2130, #2a2f45);
    border: 1px solid #3a3f5c;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.module-card {
    background: linear-gradient(135deg, #1e2130, #252a3d);
    border: 1px solid #3a3f5c;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 16px;
    transition: 0.3s;
}
.module-card:hover { border-color: #4CAF50; transform: translateY(-2px); }
.module-title { font-size: 17px; font-weight: bold; color: #ffffff; margin-bottom: 6px; }
.module-desc  { font-size: 13px; color: #9aa0b8; }
.hero-title   { text-align: center; font-size: 42px; font-weight: 800; color: #ffffff; margin-bottom: 6px; letter-spacing: 1px; }
.hero-sub     { text-align: center; font-size: 16px; color: #9aa0b8; margin-bottom: 0px; }
.badge-online  { display:inline-block; background:#4CAF50; color:white; padding:4px 16px; border-radius:20px; font-size:13px; font-weight:bold; }
.badge-offline { display:inline-block; background:#e53935; color:white; padding:4px 16px; border-radius:20px; font-size:13px; font-weight:bold; animation:blink 1s infinite; }
@keyframes blink { 0%{opacity:1;} 50%{opacity:0.3;} 100%{opacity:1;} }
.custom-divider { border:none; height:1px; background:linear-gradient(to right,transparent,#3a3f5c,transparent); margin:24px 0; }
.footer { text-align:center; font-size:18px; padding:20px 0 15px 0; }
[data-testid="stSidebar"] { background-color:#13151f; border-right:1px solid #2a2f45; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# HERO SECTION
# ══════════════════════════════════════════════════════════

st.markdown(f"""
<div style='text-align:center; padding: 30px 0 10px 0;'>
    <div style='font-size:52px; margin-bottom:10px;'></div>
    <div class='hero-title'>Police Station Management System</div>
    <div class='hero-sub'>Digital solution for modern law enforcement operations</div>
    <br>
    {status_badge}
</div>
""", unsafe_allow_html=True)

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# LIVE STATS — via sp_dashboard_summary stored procedure
# ══════════════════════════════════════════════════════════

def get_dashboard_stats():
    """Call sp_dashboard_summary and return the single row as a dict."""
    conn = mysql.connector.connect(use_pure=True, **DB_CONFIG)
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_dashboard_summary')
        for rs in cursor.stored_results():
            row = rs.fetchone()
            if row:
                return row
    except Exception as e:
        print(f"Dashboard stats error: {e}")
    finally:
        cursor.close()
        conn.close()
    return {}

try:
    stats = get_dashboard_stats()
    active_staff    = stats.get('ActiveStaff',      0)
    open_firs       = stats.get('OpenFIRs',         0)
    wanted          = stats.get('WantedCriminals',  0)
    total_balance   = float(stats.get('TotalFundBalance', 0))
    present_today   = stats.get('PresentToday',     0)
    arrests_month   = stats.get('ArrestsThisMonth', 0)
except:
    active_staff = open_firs = wanted = present_today = arrests_month = 0
    total_balance = 0.0

st.markdown("### Live Dashboard")

col1, col2, col3, col4, col5, col6 = st.columns(6)

col1.metric(label=" Active Staff",      value=active_staff,               delta="Officers")
col2.metric(label=" Open FIRs",         value=open_firs,                  delta="Cases")
col3.metric(label=" Wanted",            value=wanted,                     delta="Criminals")
col4.metric(label=" Fund Balance",      value=f"Rs {total_balance:,.0f}", delta="Available")
col5.metric(label=" Present Today",     value=present_today,              delta="On Duty")
col6.metric(label=" Arrests (30 days)", value=arrests_month,              delta="This Month")

st.markdown("<hr class='custom-divider'>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════

st.markdown(" ")
st.markdown("""
<div class='footer'>
     Police Station Management System &nbsp;|&nbsp;
    Built with Python &amp; Streamlit &nbsp;|&nbsp;
    Database: MySQL
</div>
""", unsafe_allow_html=True)
