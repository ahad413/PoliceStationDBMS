import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.operations import (
    add_operation,
    get_all_operations,
    delete_operation,
    add_surveillance,
    get_all_surveillance,
    delete_surveillance
)
from backend.duty import get_all_staff

st.title("Operations & Surveillance")

tab1, tab2 = st.tabs(["Search Operations", "Surveillance"])


def staff_options():
    staff = get_all_staff()
    return {
        f"{s['Name']} ({s['RankOfficer']})": s['StaffID']
        for s in staff
    }


# ═══════════════════════════════════════════════════════════════════════════
# TAB 1: SEARCH OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════

with tab1:

    st.subheader("Add Search Operation")

    staff_opts = staff_options()

    with st.form("op_form"):

        col1, col2 = st.columns(2)

        with col1:
            date = st.date_input("Date *")
            location = st.text_input("Location *")

            officer = st.selectbox(
                "Conducted By",
                ["-- None --"] + list(staff_opts.keys())
            )

        with col2:
            reason = st.text_area("Reason")
            result = st.text_area("Result")

        submitted = st.form_submit_button("Add Operation")

        if submitted:

            if not location:
                st.error("Location is required.")

            else:
                conducted = staff_opts.get(officer)

                ok = add_operation(
                    date,
                    location,
                    conducted,
                    reason,
                    result
                )

                if ok:
                    st.success("Operation added successfully.")
                    st.rerun()

                else:
                    st.error("Failed to add operation.")

    st.markdown("---")

    st.subheader("Operations Records")

    records = get_all_operations()

    if records:

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

        del_id = st.number_input(
            "OperationID to delete",
            min_value=1,
            step=1
        )

        if st.button("Delete Operation"):

            ok = delete_operation(del_id)

            if ok:
                st.success("Operation deleted successfully.")
                st.rerun()

            else:
                st.error("Failed to delete operation.")

    else:
        st.info("No operations recorded.")


# ═══════════════════════════════════════════════════════════════════════════
# TAB 2: SURVEILLANCE
# ═══════════════════════════════════════════════════════════════════════════

with tab2:

    st.subheader("Add Surveillance Entry")

    with st.form("surv_form"):

        col1, col2 = st.columns(2)

        with col1:
            person_name = st.text_input("Person Name *")
            cnic = st.text_input("CNIC")
            crime_hist = st.text_area("Crime History")

        with col2:
            interval = st.text_input(
                "Reporting Interval (e.g. Weekly)"
            )

            last_date = st.date_input("Last Reported Date")
            next_date = st.date_input("Next Reporting Date")

        submitted = st.form_submit_button("Add Entry")

        if submitted:

            if not person_name:
                st.error("Person Name is required.")

            else:

                ok = add_surveillance(
                    person_name,
                    cnic,
                    crime_hist,
                    interval,
                    last_date,
                    next_date
                )

                if ok:
                    st.success("Surveillance entry added successfully.")
                    st.rerun()

                else:
                    st.error("Failed to add surveillance entry.")

    st.markdown("---")

    st.subheader("Surveillance Records")

    records = get_all_surveillance()

    if records:

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

        del_id = st.number_input(
            "SurveillanceID to delete",
            min_value=1,
            step=1
        )

        if st.button("Delete Entry"):

            ok = delete_surveillance(del_id)

            if ok:
                st.success("Entry deleted successfully.")
                st.rerun()

            else:
                st.error("Failed to delete entry.")

    else:
        st.info("No surveillance records.")