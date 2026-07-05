import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.duty import get_all_staff
from backend.transcripts import get_officer_profile, get_criminal_profile
from backend.db import fetch_all

st.set_page_config(page_title="Transcripts", page_icon=None, layout="wide")

# ==========================================================
# CUSTOM CSS FOR PRINT-LIKE VIEW
# ==========================================================
st.markdown("""
<style>
    .report-card {
        background: #1e2130;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #3a3f5c;
        margin-bottom: 20px;
    }
    .section-header {
        color: #4CAF50;
        font-size: 20px;
        font-weight: bold;
        border-bottom: 2px solid #4CAF50;
        margin-bottom: 15px;
        padding-bottom: 5px;
    }
    .label { color: #9aa0b8; font-size: 14px; }
    .value { color: #ffffff; font-size: 16px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("Official Transcripts & Dossiers")
st.markdown("---")

choice = st.radio(
    "Select Transcript Type",
    ["Officer Dossier", "Criminal Record"],
    horizontal=True
)

# ==========================================================
# OFFICER DOSSIER
# ==========================================================
if choice == "Officer Dossier":
    staff_list = get_all_staff()
    staff_opts = {
        f"{s['BeltNo']} - {s['Name']}": s['StaffID']
        for s in staff_list
    }

    selected_staff = st.selectbox("Select Officer", list(staff_opts.keys()))

    if st.button("Generate Transcript"):
        data = get_officer_profile(staff_opts[selected_staff])
        p = data['profile']

        # Header
        st.markdown(f"""
        <div class='report-card'>
            <div style='text-align:center;'>
                <h2>OFFICIAL POLICE TRANSCRIPT</h2>
                <p style='color:#4CAF50;'>Confidential Personnel Record</p>
            </div>
            <div style='display: flex; justify-content: space-around; flex-wrap: wrap; margin-top:20px;'>
                <div><p class='label'>Name</p><p class='value'>{p['Name']}</p></div>
                <div><p class='label'>Belt Number</p><p class='value'>{p['BeltNo']}</p></div>
                <div><p class='label'>Rank</p><p class='value'>{p['RankOfficer']}</p></div>
                <div><p class='label'>CNIC</p><p class='value'>{p['CNIC']}</p></div>
                <div><p class='label'>Status</p><p class='value'>{p['Status']}</p></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(
                "<div class='section-header'>Recent Duty History</div>",
                unsafe_allow_html=True
            )
            if data['duties']:
                st.table(pd.DataFrame(data['duties']))
            else:
                st.info("No duty records found.")

            st.markdown(
                "<div class='section-header'>Assigned Beat</div>",
                unsafe_allow_html=True
            )
            if data['beat']:
                st.table(pd.DataFrame(data['beat']))
            else:
                st.info("No beat assigned.")

        with col2:
            st.markdown(
                "<div class='section-header'>Case Investigations (Assigned)</div>",
                unsafe_allow_html=True
            )
            if data['investigating_firs']:
                st.table(pd.DataFrame(data['investigating_firs']))
            else:
                st.info("No active investigations.")

            st.markdown(
                "<div class='section-header'>Operations Conducted</div>",
                unsafe_allow_html=True
            )
            if data['ops']:
                st.table(pd.DataFrame(data['ops']))
            else:
                st.info("No operations recorded.")

# ==========================================================
# CRIMINAL RECORD
# ==========================================================
else:
    cnics = fetch_all("""
        SELECT DISTINCT CNIC FROM WantedCriminals
        UNION
        SELECT DISTINCT CNIC FROM ArrestRegister
    """)
    cnic_list = [c['CNIC'] for c in cnics if c['CNIC']]

    search_cnic = st.selectbox("Search Subject by CNIC", cnic_list)

    if st.button("Generate Dossier"):
        data = get_criminal_profile(search_cnic)

        st.markdown(f"""
        <div class='report-card'>
            <div style='text-align:center; color: #ff4b4b;'>
                <h2>CRIMINAL DOSSIER</h2>
                <p>Subject History & Crime Records</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if data['wanted_info']:
            w = data['wanted_info']
            st.warning(f"Current Status: {w['Status']}")
            col1, col2 = st.columns(2)
            col1.metric("Name", w['Name'])
            col2.metric("CNIC", w['CNIC'])
            st.markdown(f"**Crime Details:** {w['CrimeDetails']}")

        st.markdown(
            "<div class='section-header'>Arrest History</div>",
            unsafe_allow_html=True
        )
        if data['arrests']:
            st.dataframe(
                pd.DataFrame(data['arrests']),
                use_container_width=True
            )
        else:
            st.success("No arrest history found in this station.")

        st.markdown(
            "<div class='section-header'>Linked FIRs / Cases</div>",
            unsafe_allow_html=True
        )
        if data['firs']:
            st.dataframe(
                pd.DataFrame(data['firs']),
                use_container_width=True
            )
        else:
            st.info("No FIRs linked to this subject.")

# ==========================================================
# PRINT TIP
# ==========================================================
st.info("Tip: Use Ctrl + P to save this transcript as a PDF.")