import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.search import (
    search_staff,
    search_duty,
    search_fir,
    search_criminals,
    search_arrests,
    search_beats,
    search_operations
)

st.set_page_config(
    page_title="Search",
    page_icon=None,
    layout="wide"
)

# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

.stApp {
    background-color: #0f1117;
}

.search-header {
    text-align: center;
    font-size: 36px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 6px;
}

.search-sub {
    text-align: center;
    font-size: 14px;
    color: #9aa0b8;
    margin-bottom: 20px;
}

.result-count {
    font-size: 13px;
    color: #4CAF50;
    font-weight: bold;
    margin-bottom: 8px;
}

.no-result {
    text-align: center;
    font-size: 14px;
    color: #9aa0b8;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown("""
<div style='padding: 20px 0 10px 0; text-align:center;'>
    <div class='search-header'>Search Records</div>
    <div class='search-sub'>
        Search across all modules instantly
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Staff",
    "Duty",
    "FIR",
    "Criminals",
    "Arrests",
    "Beats",
    "Operations"
])

# ==========================================================
# TAB 1: STAFF SEARCH
# ==========================================================

with tab1:
    st.subheader("Search Staff")

    keyword = st.text_input(
        "Search by Name, Belt No, CNIC, Rank or Status",
        placeholder="e.g. Ali Raza or B_001 or Inspector",
        key="search_staff"
    )

    if keyword:
        results = search_staff(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No staff found matching your search.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search staff records.")

# ==========================================================
# TAB 2: DUTY SEARCH
# ==========================================================

with tab2:
    st.subheader("Search Duty Records")

    keyword = st.text_input(
        "Search by Name, Belt No, Division, Attendance or Date",
        placeholder="e.g. Investigation or Present or 2026-05-01",
        key="search_duty"
    )

    if keyword:
        results = search_duty(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No duty records found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search duty records.")

# ==========================================================
# TAB 3: FIR SEARCH
# ==========================================================

with tab3:
    st.subheader("Search FIR Records")

    keyword = st.text_input(
        "Search by FIR Number, Victim, CNIC, Location or Status",
        placeholder="e.g. FIR-001 or Hassan Ali or Open",
        key="search_fir"
    )

    if keyword:
        results = search_fir(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No FIR records found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search FIR records.")

# ==========================================================
# TAB 4: CRIMINALS SEARCH
# ==========================================================

with tab4:
    st.subheader("Search Criminals")

    keyword = st.text_input(
        "Search by Name, CNIC, Crime Details, Location or Status",
        placeholder="e.g. Zubair or Robbery or Wanted",
        key="search_criminal"
    )

    if keyword:
        results = search_criminals(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            df = pd.DataFrame(results)

            def highlight_status(row):
                if row['Status'] == 'Wanted':
                    return ['background-color: #3d1a1a'] * len(row)
                else:
                    return ['background-color: #1a3d1a'] * len(row)

            st.dataframe(
                df.style.apply(highlight_status, axis=1),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No criminals found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search criminal records.")

# ==========================================================
# TAB 5: ARREST SEARCH
# ==========================================================

with tab5:
    st.subheader("Search Arrest Records")

    keyword = st.text_input(
        "Search by Name, CNIC, FIR Number or Location",
        placeholder="e.g. Bilal Ahmed or 35201 or Model Town",
        key="search_arrest"
    )

    if keyword:
        results = search_arrests(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No arrest records found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search arrest records.")

# ==========================================================
# TAB 6: BEAT SEARCH
# ==========================================================

with tab6:
    st.subheader("Search Beat Records")

    keyword = st.text_input(
        "Search by Beat Name, Area, Officer or Activity",
        placeholder="e.g. Beat A or Gulberg or Patrol",
        key="search_beat"
    )

    if keyword:
        results = search_beats(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No beat records found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search beat records.")

# ==========================================================
# TAB 7: OPERATIONS SEARCH
# ==========================================================

with tab7:
    st.subheader("Search Operations")

    keyword = st.text_input(
        "Search by Location, Reason, Result or Officer",
        placeholder="e.g. DHA or Drug or Detained",
        key="search_op"
    )

    if keyword:
        results = search_operations(keyword)
        if results:
            st.markdown(
                f"<div class='result-count'>{len(results)} record(s) found</div>",
                unsafe_allow_html=True
            )
            st.dataframe(
                pd.DataFrame(results),
                use_container_width=True
            )
        else:
            st.markdown(
                "<div class='no-result'>No operations found.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("Type something to search operations.")