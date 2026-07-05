import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.beat import (add_beat, get_all_beats, delete_beat,
                           add_beat_record, get_all_beat_records, delete_beat_record)
from backend.duty import get_all_staff

st.title("Beat & Patrol Management")

tab1, tab2 = st.tabs(["Beats", "Beat Book (Patrol Log)"])

def staff_options():
    staff = get_all_staff()
    return {f"{s['Name']} ({s['RankOfficer']})": s['StaffID'] for s in staff}

def beat_options():
    beats = get_all_beats()
    return {b['BeatName']: b['BeatID'] for b in beats}

# TAB 1: BEATS
with tab1:
    st.subheader("Add Beat")
    staff_opts = staff_options()

    with st.form("beat_form"):
        col1, col2 = st.columns(2)
        with col1:
            beat_name = st.text_input("Beat Name *")
            area      = st.text_input("Area")
        with col2:
            officer_label = st.selectbox("Assigned Officer", ["-- None --"] + list(staff_opts.keys()))

        submitted = st.form_submit_button("Add Beat")
        if submitted:
            if not beat_name:
                st.error("Beat Name is required.")
            else:
                assigned = staff_opts.get(officer_label)
                ok = add_beat(beat_name, area, assigned)
                if ok:
                    st.success("Beat added successfully!")
                    st.rerun()
                else:
                    st.error("Failed to add beat.")

    st.markdown("---")
    st.subheader("Beat Records")
    records = get_all_beats()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("BeatID to delete", min_value=1, step=1)
        if st.button("Delete Beat"):
            ok = delete_beat(del_id)
            if ok:
                st.success("Deleted!")
                st.rerun()
            else:
                st.error("Failed - beat may be in use.")
    else:
        st.info("No beats found.")

# TAB 2: BEAT BOOK
with tab2:
    st.subheader("Add Patrol Entry")
    staff_opts = staff_options()
    beat_opts  = beat_options()

    with st.form("beatbook_form"):
        col1, col2 = st.columns(2)
        with col1:
            beat_label    = st.selectbox("Beat *", list(beat_opts.keys()) if beat_opts else ["No Beats"])
            officer_label = st.selectbox("Officer *", list(staff_opts.keys()) if staff_opts else ["No Staff"])
            date          = st.date_input("Date *")
        with col2:
            activity = st.text_area("Activity Details *")
            remarks  = st.text_area("Remarks")

        submitted = st.form_submit_button("Add Record")
        if submitted:
            if not activity or not beat_opts or not staff_opts:
                st.error("Activity Details, valid Beat and Staff are required.")
            else:
                ok = add_beat_record(beat_opts[beat_label], staff_opts[officer_label],
                                     date, activity, remarks)
                if ok:
                    st.success("Patrol record added!")
                    st.rerun()
                else:
                    st.error("Failed to add record.")

    st.markdown("---")
    st.subheader("Patrol Log")
    records = get_all_beat_records()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("BeatRecordID to delete", min_value=1, step=1)
        if st.button("Delete Record"):
            ok = delete_beat_record(del_id)
            if ok:
                st.success("Deleted!")
                st.rerun()
            else:
                st.error("Failed to delete.")
    else:
        st.info("No patrol records.")