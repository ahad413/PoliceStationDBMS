import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.duty import (
    add_staff, get_all_staff, update_staff_status,
    update_staff, delete_staff,
    add_duty, get_all_duties, delete_duty,
    add_roznamcha, get_all_roznamcha, delete_roznamcha
)

st.title("Duty & Attendance")

tab1, tab2, tab3 = st.tabs([
    "Staff Register",
    "Duty Roster",
    "Roznamcha"
])

# ==========================================================
# TAB 1: STAFF REGISTER
# ==========================================================

with tab1:

    # ADD STAFF
    st.subheader("Add Staff Member")

    with st.form("staff_form"):
        col1, col2 = st.columns(2)
        with col1:
            belt_no      = st.text_input("Belt No *")
            name         = st.text_input("Full Name *")
            rank_officer = st.text_input("Rank *")
            cnic         = st.text_input("CNIC *")
        with col2:
            phone   = st.text_input("Phone")
            address = st.text_input("Address")
            status  = st.selectbox("Status", ["Active", "Suspended"])

        submitted = st.form_submit_button("Add Staff")
        if submitted:
            if not belt_no or not name or not rank_officer or not cnic:
                st.error("Belt No, Name, Rank and CNIC are required.")
            else:
                ok = add_staff(
                    belt_no, name, rank_officer, cnic, phone, address, status
                )
                if ok:
                    st.success("Staff member added.")
                    st.rerun()
                else:
                    st.error("Failed. Belt No or CNIC may already exist.")

    st.markdown("---")

    # STAFF RECORDS
    st.subheader("Staff Records")
    records = get_all_staff()

    if records:
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)

        st.markdown("---")

        # EDIT STAFF
        st.subheader("Edit Staff Member")

        staff_options = {
            f"{s['BeltNo']} — {s['Name']}": s['StaffID']
            for s in records
        }

        selected_label = st.selectbox(
            "Select Staff to Edit",
            list(staff_options.keys()),
            key="edit_select"
        )

        selected_id = staff_options[selected_label]

        current = next(
            (s for s in records if s['StaffID'] == selected_id), None
        )

        if current:
            with st.form("edit_staff_form"):
                st.markdown(f"Editing: {current['Name']} (ID: {selected_id})")
                st.markdown(" ")

                col1, col2 = st.columns(2)
                with col1:
                    e_belt_no = st.text_input(
                        "Belt No *",
                        value=current['BeltNo']
                    )
                    e_name = st.text_input(
                        "Full Name *",
                        value=current['Name']
                    )
                    e_rank = st.text_input(
                        "Rank *",
                        value=current['RankOfficer']
                    )
                    e_cnic = st.text_input(
                        "CNIC *",
                        value=current['CNIC']
                    )
                with col2:
                    e_phone = st.text_input(
                        "Phone",
                        value=current['Phone'] or ""
                    )
                    e_address = st.text_input(
                        "Address",
                        value=current['Address'] or ""
                    )
                    e_status = st.selectbox(
                        "Status",
                        ["Active", "Suspended"],
                        index=0 if current['Status'] == "Active" else 1
                    )

                submitted = st.form_submit_button("Save Changes")
                if submitted:
                    if not e_belt_no or not e_name or not e_rank or not e_cnic:
                        st.error("Belt No, Name, Rank and CNIC are required.")
                    else:
                        ok = update_staff(
                            selected_id,
                            e_belt_no,
                            e_name,
                            e_rank,
                            e_cnic,
                            e_phone,
                            e_address,
                            e_status
                        )
                        if ok:
                            st.success("Staff updated successfully.")
                            st.rerun()
                        else:
                            st.error("Failed. Belt No or CNIC may already exist.")

        st.markdown("---")

        # DELETE STAFF
        st.subheader("Delete Staff")

        del_id = st.number_input(
            "StaffID to delete",
            min_value=1,
            step=1,
            key="del_staff"
        )
        if st.button("Delete Staff", key="btn_del_staff"):
            ok = delete_staff(del_id)
            if ok:
                st.success("Staff deleted.")
                st.rerun()
            else:
                st.error("Failed — staff may be referenced in other records.")

    else:
        st.info("No staff records found. Add staff above.")

# ==========================================================
# TAB 2: DUTY ROSTER
# ==========================================================

with tab2:
    st.subheader("Add Duty Entry")

    staff_list    = get_all_staff()
    staff_options = {
        f"{s['BeltNo']} — {s['Name']} ({s['RankOfficer']})": s['StaffID']
        for s in staff_list
    }

    with st.form("duty_form"):
        col1, col2 = st.columns(2)
        with col1:
            staff_label = st.selectbox(
                "Staff Member *",
                list(staff_options.keys()) if staff_options else ["No Staff"]
            )
            duty_date = st.date_input("Duty Date *")
            division  = st.selectbox(
                "Division *", ["Investigation", "Operation"]
            )
        with col2:
            shift  = st.text_input("Shift (e.g. 8am-4pm) *")
            status = st.selectbox("Attendance", ["Present", "Absent"])

        submitted = st.form_submit_button("Add Duty")
        if submitted:
            if not shift or not staff_options:
                st.error("Shift and valid staff required.")
            else:
                ok = add_duty(
                    staff_options[staff_label],
                    duty_date, division, shift, status
                )
                if ok:
                    st.success("Duty entry added.")
                    st.rerun()
                else:
                    st.error("Failed.")

    st.markdown("---")
    st.subheader("Duty Roster Records")
    records = get_all_duties()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input(
            "DutyID to delete", min_value=1, step=1, key="del_duty"
        )
        if st.button("Delete Duty", key="btn_del_duty"):
            ok = delete_duty(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed.")
    else:
        st.info("No duty records.")

# ==========================================================
# TAB 3: ROZNAMCHA
# ==========================================================

with tab3:
    st.subheader("Add Roznamcha Entry")

    staff_list    = get_all_staff()
    staff_options = {
        f"{s['BeltNo']} — {s['Name']} ({s['RankOfficer']})": s['StaffID']
        for s in staff_list
    }

    with st.form("roznamcha_form"):
        col1, col2 = st.columns(2)
        with col1:
            staff_label = st.selectbox(
                "Staff Member *",
                list(staff_options.keys()) if staff_options else ["No Staff"],
                key="roz_staff"
            )
            date     = st.date_input("Date *")
            time_out = st.time_input("Time Out *")
            time_in  = st.time_input("Time In")
        with col2:
            purpose  = st.text_input("Purpose *")
            location = st.text_input("Location *")
            remarks  = st.text_area("Remarks")

        submitted = st.form_submit_button("Add Entry")
        if submitted:
            if not purpose or not location or not staff_options:
                st.error("Purpose, Location and valid staff required.")
            else:
                ok = add_roznamcha(
                    staff_options[staff_label], date,
                    str(time_out), purpose, location,
                    str(time_in), remarks
                )
                if ok:
                    st.success("Roznamcha entry added.")
                    st.rerun()
                else:
                    st.error("Failed.")

    st.markdown("---")
    st.subheader("Roznamcha Records")
    records = get_all_roznamcha()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input(
            "DiaryID to delete", min_value=1, step=1, key="del_roz"
        )
        if st.button("Delete Entry", key="btn_del_roz"):
            ok = delete_roznamcha(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed.")
    else:
        st.info("No roznamcha records.")