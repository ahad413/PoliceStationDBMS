import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.admin import (
    add_correspondence, get_all_correspondence, delete_correspondence,
    add_inspection, get_all_inspections, delete_inspection,
    add_fund, get_all_funds, delete_fund,
    use_fund, get_fund_usage
)

st.title("Administration & Finance")

tab1, tab2, tab3 = st.tabs([
    "Correspondence",
    "Inspections",
    "Government Funds"
])

# ═══════════════════════════════════════════════════════════
# TAB 1: CORRESPONDENCE
# ═══════════════════════════════════════════════════════════

with tab1:

    st.subheader("Add Correspondence")

    with st.form("corr_form"):

        col1, col2 = st.columns(2)

        with col1:
            letter_num = st.text_input("Letter Number *")
            date = st.date_input("Date *")
            from_dept = st.text_input("From Department")

        with col2:
            to_dept = st.text_input("To Department")
            subject = st.text_input("Subject *")
            description = st.text_area("Description")

        submitted = st.form_submit_button("Add Letter")

        if submitted:

            if not letter_num or not subject:
                st.error("Letter Number and Subject are required.")

            else:

                ok = add_correspondence(
                    letter_num,
                    date,
                    from_dept,
                    to_dept,
                    subject,
                    description
                )

                if ok:
                    st.success("Letter added successfully.")
                    st.rerun()

                else:
                    st.error("Failed. Letter number may already exist.")

    st.markdown("---")

    st.subheader("Correspondence Records")

    records = get_all_correspondence()

    if records:

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

        del_id = st.number_input(
            "LetterID to delete",
            min_value=1,
            step=1,
            key="del_letter"
        )

        if st.button("Delete Letter", key="btn_del_letter"):

            ok = delete_correspondence(del_id)

            if ok:
                st.success("Deleted successfully.")
                st.rerun()

            else:
                st.error("Failed to delete.")

    else:
        st.info("No correspondence records.")


# ═══════════════════════════════════════════════════════════
# TAB 2: INSPECTIONS
# ═══════════════════════════════════════════════════════════

with tab2:

    st.subheader("Add Inspection")

    with st.form("insp_form"):

        col1, col2 = st.columns(2)

        with col1:
            inspector_name = st.text_input("Inspector Name *")
            designation = st.text_input("Designation")

        with col2:
            visit_date = st.date_input("Visit Date *")
            remarks = st.text_area("Remarks")

        submitted = st.form_submit_button("Add Inspection")

        if submitted:

            if not inspector_name:
                st.error("Inspector Name is required.")

            else:

                ok = add_inspection(
                    inspector_name,
                    designation,
                    visit_date,
                    remarks
                )

                if ok:
                    st.success("Inspection record added successfully.")
                    st.rerun()

                else:
                    st.error("Failed to add inspection.")

    st.markdown("---")

    st.subheader("Inspection Records")

    records = get_all_inspections()

    if records:

        st.dataframe(
            pd.DataFrame(records),
            use_container_width=True
        )

        del_id = st.number_input(
            "InspectionID to delete",
            min_value=1,
            step=1,
            key="del_insp"
        )

        if st.button("Delete Inspection", key="btn_del_insp"):

            ok = delete_inspection(del_id)

            if ok:
                st.success("Deleted successfully.")
                st.rerun()

            else:
                st.error("Failed to delete.")

    else:
        st.info("No inspection records.")


# ═══════════════════════════════════════════════════════════
# TAB 3: GOVERNMENT FUNDS
# ═══════════════════════════════════════════════════════════

with tab3:

    # ── Add Fund ───────────────────────────────────────────

    st.subheader("Add Fund")

    with st.form("fund_form"):

        col1, col2 = st.columns(2)

        with col1:
            source = st.text_input("Source *")

            amount_received = st.number_input(
                "Amount Received (Rs) *",
                min_value=0.0,
                step=1000.0
            )

            date_received = st.date_input("Date Received *")

        with col2:

            init_used = st.number_input(
                "Initial Used Amount (Rs)",
                min_value=0.0,
                step=500.0
            )

            purpose = st.text_input("Purpose")

        submitted = st.form_submit_button("Add Fund")

        if submitted:

            if not source:
                st.error("Source is required.")

            elif init_used > amount_received:
                st.error("Used amount cannot exceed received amount.")

            else:

                ok = add_fund(
                    source,
                    amount_received,
                    date_received,
                    init_used,
                    purpose
                )

                if ok:
                    st.success("Fund added successfully.")
                    st.rerun()

                else:
                    st.error("Failed to add fund.")

    st.markdown("---")

    # ── Use Fund ───────────────────────────────────────────

    st.subheader("Use Fund")

    funds = get_all_funds()

    if funds:

        fund_options = {
            f"{f['Source']} (Balance: Rs {f['Balance']})": f['FundID']
            for f in funds
        }

        with st.form("use_fund_form"):

            fund_label = st.selectbox(
                "Select Fund *",
                list(fund_options.keys())
            )

            spend_amount = st.number_input(
                "Amount to Use (Rs) *",
                min_value=0.0,
                step=500.0
            )

            used_date = st.date_input("Used Date *")

            description = st.text_input(
                "Purpose / Description *"
            )

            submitted = st.form_submit_button("Use Fund")

            if submitted:

                success, message = use_fund(
                    fund_options[fund_label],
                    spend_amount,
                    used_date,
                    description
                )

                if success:
                    st.success(message)
                    st.rerun()

                else:
                    st.error(message)

    else:
        st.info("No funds available. Add a fund first.")

    st.markdown("---")

    # ── Fund Records ───────────────────────────────────────

    st.subheader("Fund Records")

    records = get_all_funds()

    if records:

        df = pd.DataFrame(records)

        st.dataframe(
            df,
            use_container_width=True
        )

        total_received = df['AmountReceived'].sum()
        total_used = df['AmountUsed'].sum()
        total_balance = df['Balance'].sum()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Received",
            f"Rs {total_received:,.0f}"
        )

        col2.metric(
            "Total Used",
            f"Rs {total_used:,.0f}"
        )

        col3.metric(
            "Total Balance",
            f"Rs {total_balance:,.0f}"
        )

        st.markdown("---")

        del_id = st.number_input(
            "FundID to delete",
            min_value=1,
            step=1,
            key="del_fund"
        )

        if st.button("Delete Fund", key="btn_del_fund"):

            ok = delete_fund(del_id)

            if ok:
                st.success("Deleted successfully.")
                st.rerun()

            else:
                st.error("Failed to delete.")

    else:
        st.info("No fund records.")

    st.markdown("---")

    # ── Fund Usage History ─────────────────────────────────

    st.subheader("Fund Usage History")

    usage = get_fund_usage()

    if usage:

        st.dataframe(
            pd.DataFrame(usage),
            use_container_width=True
        )

    else:
        st.info("No usage history found.")