import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
import pandas as pd
from backend.property import (
    add_asset, get_all_assets, delete_asset,
    add_recovered, get_all_recovered, delete_recovered
)
from backend.fir import get_all_firs

st.title("Property Management")

tab1, tab2 = st.tabs(["Government Assets", "Recovered Property"])

def fir_options():
    firs = get_all_firs()
    return {f['FIRNumber']: f['FIRID'] for f in firs}

# ==========================================================
# TAB 1: GOVERNMENT ASSETS
# ==========================================================

with tab1:
    st.subheader("Add Asset")

    with st.form("asset_form"):
        col1, col2 = st.columns(2)
        with col1:
            prop_type   = st.selectbox(
                "Property Type *",
                ["Weapon", "Vehicle", "Furniture", "Facility"]
            )
            description = st.text_input("Description")
        with col2:
            quantity   = st.number_input("Quantity *", min_value=1, step=1)
            issue_date = st.date_input("Issue Date")
            condition  = st.selectbox("Condition", ["Good", "Bad"])

        submitted = st.form_submit_button("Add Asset")
        if submitted:
            ok = add_asset(prop_type, description, quantity, issue_date, condition)
            if ok:
                st.success("Asset added successfully.")
                st.rerun()
            else:
                st.error("Failed to add asset.")

    st.markdown("---")
    st.subheader("Asset Records")
    records = get_all_assets()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("PropertyID to delete", min_value=1, step=1)
        if st.button("Delete Asset"):
            ok = delete_asset(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed to delete.")
    else:
        st.info("No assets found.")

# ==========================================================
# TAB 2: RECOVERED PROPERTY
# ==========================================================

with tab2:
    st.subheader("Add Recovered Item")
    fir_opts = fir_options()

    with st.form("recovery_form"):
        col1, col2 = st.columns(2)
        with col1:
            fir_label = st.selectbox(
                "Related FIR *",
                list(fir_opts.keys()) if fir_opts else ["No FIRs"]
            )
            item_name = st.text_input("Item Name *")
            quantity  = st.number_input("Quantity *", min_value=1, step=1)
        with col2:
            recovery_date  = st.date_input("Recovery Date *")
            recovered_from = st.text_input("Recovered From")
            status         = st.selectbox("Status", ["Kept", "Returned"])

        submitted = st.form_submit_button("Add Recovery")
        if submitted:
            if not item_name or not fir_opts:
                st.error("Item Name and a valid FIR are required.")
            else:
                ok = add_recovered(
                    fir_opts[fir_label],
                    item_name,
                    quantity,
                    recovery_date,
                    recovered_from,
                    status
                )
                if ok:
                    st.success("Recovery record added.")
                    st.rerun()
                else:
                    st.error("Failed to add recovery.")

    st.markdown("---")
    st.subheader("Recovered Property Records")
    records = get_all_recovered()
    if records:
        st.dataframe(pd.DataFrame(records), use_container_width=True)
        del_id = st.number_input("RecoveryID to delete", min_value=1, step=1)
        if st.button("Delete Record"):
            ok = delete_recovered(del_id)
            if ok:
                st.success("Deleted.")
                st.rerun()
            else:
                st.error("Failed to delete.")
    else:
        st.info("No recovery records.")