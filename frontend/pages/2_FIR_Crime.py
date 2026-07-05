import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from datetime import datetime
from backend.fir import (
    add_fir, get_all_firs, update_fir_status, delete_fir,
    add_arrest, get_all_arrests, delete_arrest,
    add_challan, get_all_challans, delete_challan,
    add_criminal, get_all_criminals,
    update_criminal_status, delete_criminal
)
from backend.duty import get_all_staff
from backend.beat import get_all_beats

st.title("FIR & Crime Management")

tab1, tab2, tab3, tab4 = st.tabs([
    "FIR Register",
    "Arrest Register",
    "Challan Register",
    "Wanted Criminals"
])

def staff_options():
    staff = get_all_staff()
    return {f"{s['Name']} ({s['RankOfficer']})": s['StaffID'] for s in staff}

def beat_options():
    beats = get_all_beats()
    return {b['BeatName']: b['BeatID'] for b in beats}

def fir_options():
    firs = get_all_firs()
    return {f['FIRNumber']: f['FIRID'] for f in firs}

# ==========================================================
# TAB 1: FIR
# ==========================================================
with tab1:
    st.subheader("File New FIR")
    staff_opts = staff_options()
    beat_opts = beat_options()

    with st.form("fir_form"):

        st.markdown("#### Victim Information")
        col1, col2 = st.columns(2)
        with col1:
            fir_number = st.text_input("FIR Number *")
            dt_str = st.text_input(
                "Date & Time (YYYY-MM-DD HH:MM:SS) *",
                value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            victim_name = st.text_input("Victim Name *")
        with col2:
            victim_cnic = st.text_input("Victim CNIC")
            victim_address = st.text_input("Victim Address")

        st.markdown("#### Accused Information")
        col3, col4 = st.columns(2)
        with col3:
            accused_name = st.text_input("Accused Name *")
            accused_cnic = st.text_input("Accused CNIC")
        with col4:
            accused_address = st.text_input("Accused Address")

        st.markdown("#### Crime Information")
        crime_type = st.selectbox(
            "Crime Type *",
            [
                "-- Select Crime Type --",
                "Murder",
                "Attempted Murder",
                "Robbery",
                "Burglary",
                "Theft",
                "Kidnapping",
                "Assault",
                "Rape",
                "Drug Trafficking",
                "Fraud",
                "Domestic Violence",
                "Cyber Crime",
                "Traffic Violation",
                "Illegal Weapons",
                "Rioting",
                "Extortion",
                "Terrorism",
                "Other"
            ]
        )

        st.markdown("#### Location & Officer Details")
        col5, col6 = st.columns(2)
        with col5:
            crime_location = st.text_input("Crime Location *")
            distance = st.number_input(
                "Distance from Station (km)",
                min_value=0.0, step=0.1)
            beat_label = st.selectbox(
                "Beat",
                ["-- None --"] + list(beat_opts.keys()))
        with col6:
            rep_officer = st.selectbox(
                "Reporting Officer",
                list(staff_opts.keys()) if staff_opts else ["No Staff"])
            rep_rank = st.text_input("Reporting Officer Rank")
            fit_status = st.text_input("Fit Status")
            asgn_officer = st.selectbox(
                "Assigned Officer",
                list(staff_opts.keys()) if staff_opts else ["No Staff"],
                key="asgn")
            case_status = st.selectbox(
                "Case Status", ["Open", "Ongoing", "Closed"])

        st.markdown("#### Incident Details")
        fir_details = st.text_area(
            "FIR Details *",
            placeholder="Describe the incident in detail...",
            max_chars=1500,
            height=150
        )

        submitted = st.form_submit_button("File FIR")

        if submitted:
            if not fir_number:
                st.error("FIR Number required.")
            elif not victim_name:
                st.error("Victim Name required.")
            elif not accused_name:
                st.error("Accused Name required.")
            elif crime_type == "-- Select Crime Type --":
                st.error("Please select Crime Type.")
            elif not crime_location:
                st.error("Crime Location required.")
            elif not fir_details or len(fir_details.strip()) < 10:
                st.error("FIR Details required (minimum 10 characters).")
            elif not staff_opts:
                st.error("Please add staff first.")
            else:
                beat_id = beat_opts.get(beat_label)

                ok = add_fir(
                    fir_number, dt_str,
                    victim_name, victim_cnic, victim_address,
                    accused_name, accused_cnic, accused_address,
                    crime_type,
                    crime_location, distance, beat_id,
                    staff_opts[rep_officer], rep_rank, fit_status,
                    staff_opts[asgn_officer], case_status,
                    fir_details
                )

                if ok:
                    st.success("FIR filed successfully.")
                    st.rerun()
                else:
                    st.error("Failed. FIR number may already exist.")

    st.markdown("---")
    st.subheader("FIR Records")
    records = get_all_firs()

    if records:
        df = pd.DataFrame(records)

        cols_order = [
            "FIRID", "FIRNumber", "DateTime",
            "VictimName", "VictimCNIC", "VictimAddress",
            "AccusedName", "AccusedCNIC", "AccusedAddress",
            "CrimeType",
            "CrimeLocation", "DistanceFromStation",
            "BeatName", "ReportingOfficer", "AssignedOfficer",
            "CaseStatus", "FIRDetails"
        ]

        cols_order = [c for c in cols_order if c in df.columns]
        st.dataframe(df[cols_order], use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            upd_id = st.number_input(
                "FIRID to update status", min_value=1, step=1)
            new_sta = st.selectbox(
                "New Status", ["Open", "Ongoing", "Closed"])
            if st.button("Update Status", key="fir_update"):
                ok = update_fir_status(upd_id, new_sta)
                if ok:
                    st.success("Status updated.")
                    st.rerun()
                else:
                    st.error("Failed to update.")
        with col2:
            del_id = st.number_input(
                "FIRID to delete", min_value=1, step=1, key="del_fir")
            if st.button("Delete FIR"):
                ok = delete_fir(del_id)
                if ok:
                    st.success("FIR deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete.")
    else:
        st.info("No FIR records found.")

# ==========================================================
# TAB 2: ARREST REGISTER
# ==========================================================
with tab2:
    st.subheader("Add Arrest Record")
    fir_opts = fir_options()

    with st.form("arrest_form"):
        col1, col2 = st.columns(2)
        with col1:
            fir_label = st.selectbox(
                "Related FIR *",
                list(fir_opts.keys()) if fir_opts else ["No FIRs"])
            accused_name = st.text_input("Accused Name *")
            cnic = st.text_input("CNIC")
            arrest_date = st.date_input("Arrest Date *")
        with col2:
            arrest_loc = st.text_input("Arrest Location")
            station = st.text_input("Sent to Police Station")
            remarks = st.text_area("Remarks")

        submitted = st.form_submit_button("Add Arrest")
        if submitted:
            if not accused_name or not fir_opts:
                st.error("Accused Name and a valid FIR are required.")
            else:
                ok = add_arrest(
                    fir_opts[fir_label], accused_name, cnic,
                    arrest_date, arrest_loc, station, remarks)
                if ok:
                    st.success("Arrest record added.")
                    st.rerun()
                else:
                    st.error("Failed to add arrest.")

    st.markdown("---")
    st.subheader("Arrest Records")
    records = get_all_arrests()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("ArrestID to delete", min_value=1, step=1)
        if st.button("Delete Arrest Record"):
            ok = delete_arrest(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed to delete.")
    else:
        st.info("No arrest records.")

# ==========================================================
# TAB 3: CHALLAN REGISTER
# ==========================================================
with tab3:
    st.subheader("Add Challan")
    fir_opts = fir_options()

    with st.form("challan_form"):
        col1, col2 = st.columns(2)
        with col1:
            fir_label = st.selectbox(
                "Related FIR *",
                list(fir_opts.keys()) if fir_opts else ["No FIRs"])
            court_name = st.text_input("Court Name *")
        with col2:
            challan_date = st.date_input("Challan Date *")
            fine_amount = st.number_input(
                "Fine Amount (Rs)", min_value=0.0, step=100.0)
            status = st.selectbox("Status", ["Pending", "Paid"])

        submitted = st.form_submit_button("Add Challan")
        if submitted:
            if not court_name or not fir_opts:
                st.error("Court Name and a valid FIR are required.")
            else:
                ok = add_challan(
                    fir_opts[fir_label], court_name,
                    challan_date, fine_amount, status)
                if ok:
                    st.success("Challan added.")
                    st.rerun()
                else:
                    st.error("Failed to add challan.")

    st.markdown("---")
    st.subheader("Challan Records")
    records = get_all_challans()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("ChallanID to delete", min_value=1, step=1)
        if st.button("Delete Challan"):
            ok = delete_challan(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed to delete.")
    else:
        st.info("No challan records.")

# ==========================================================
# TAB 4: WANTED CRIMINALS
# ==========================================================
with tab4:
    st.subheader("Add Wanted Criminal")

    with st.form("criminal_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name *")
            cnic = st.text_input("CNIC")
            fir_opts = fir_options()
            fir_label = st.selectbox(
                "Linked FIR (Optional)",
                ["-- None --"] + list(fir_opts.keys()))
        with col2:
            crime_details = st.text_area("Crime Details")
            last_seen = st.text_input("Last Seen Location")
            status = st.selectbox("Status", ["Wanted", "Arrested"])

        submitted = st.form_submit_button("Add Criminal")
        if submitted:
            if not name:
                st.error("Name is required.")
            else:
                fir_id = fir_opts.get(fir_label)
                ok = add_criminal(
                    name, cnic, crime_details,
                    last_seen, status, fir_id)
                if ok:
                    st.success("Criminal record added.")
                    st.rerun()
                else:
                    st.error("Failed to add.")

    st.markdown("---")
    st.subheader("Wanted Criminals List")
    records = get_all_criminals()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            upd_id = st.number_input(
                "CriminalID to update", min_value=1, step=1)
            new_sta = st.selectbox(
                "New Status", ["Wanted", "Arrested"])
            if st.button("Update Status", key="criminal_update"):
                ok = update_criminal_status(upd_id, new_sta)
                if ok:
                    st.success("Status updated.")
                    st.rerun()
                else:
                    st.error("Failed to update.")
        with col2:
            del_id = st.number_input(
                "CriminalID to delete", min_value=1, step=1, key="del_crim")
            if st.button("Delete Record"):
                ok = delete_criminal(del_id)
                if ok:
                    st.success("Deleted.")
                    st.rerun()
                else:
                    st.error("Failed to delete.")
    else:
        st.info("No wanted criminal records.")