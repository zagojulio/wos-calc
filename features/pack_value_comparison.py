"""
Pack Value Comparison Tab for Whiteout Survival Calculator
Allows users to add, compare, and export pack value data.
"""

import streamlit as st
import pandas as pd
import json
import os
from typing import List, Dict
from utils.formatters import format_currency

PACKS_JSON_PATH = "data/pack_value_comparison.json"

# --- Persistence Helpers ---
def load_pack_history() -> List[Dict]:
    if os.path.exists(PACKS_JSON_PATH):
        try:
            with open(PACKS_JSON_PATH, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_pack_history(history: List[Dict]):
    os.makedirs(os.path.dirname(PACKS_JSON_PATH), exist_ok=True)
    with open(PACKS_JSON_PATH, "w") as f:
        json.dump(history, f, indent=2)

# --- Calculation Helpers ---
def calculate_total_minutes(hour_speedups: int, five_min_speedups: int) -> int:
    """
    Calculate total speed-up minutes from 60min and 5min speedups.
    
    Args:
        hour_speedups (int): Number of 60-minute speedups
        five_min_speedups (int): Number of 5-minute speedups
    
    Returns:
        int: Total speed-up minutes
    """
    return (hour_speedups * 60) + (five_min_speedups * 5)

def calculate_cost_per_minute(price: float, total_minutes: int) -> float:
    """
    Calculate cost per minute with validation for division by zero.
    
    Args:
        price (float): Pack price
        total_minutes (int): Total speed-up minutes
    
    Returns:
        float: Cost per minute, or 0.0 if total_minutes is 0
    """
    if total_minutes <= 0:
        return 0.0
    return round(price / total_minutes, 4)

# --- Main Tab Renderer ---
def render_pack_value_comparison_tab():
    st.header("Pack Value Comparison")
    st.caption("Compare the value of different packs by cost per speed-up minute. Data is saved locally and persists across reloads.")

    # --- Session State ---
    if "pack_value_history" not in st.session_state:
        st.session_state.pack_value_history = load_pack_history()
    history = st.session_state.pack_value_history

    # --- Input Form ---
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([3, 2, 1.5, 1.5, 2])
        with col1:
            pack_name = st.text_input("Pack Name", key="pack_name_input")
        with col2:
            price = st.number_input("Price ($)", min_value=0.0, step=0.01, format="%.2f", key="pack_price_input")
        with col3:
            hour_speedups = st.number_input("60min Speedups", min_value=0, step=1, key="pack_60min_input")
        with col4:
            five_min_speedups = st.number_input("5min Speedups", min_value=0, step=1, key="pack_5min_input")
        with col5:
            # Calculate total minutes dynamically
            total_minutes = calculate_total_minutes(hour_speedups, five_min_speedups)
            st.metric("Total Minutes", total_minutes)
            
            add_disabled = not (pack_name.strip() and price > 0 and total_minutes > 0)
            add_btn = st.button("Add Pack", disabled=add_disabled, key="add_pack_btn")

        # --- Inline Validation ---
        validation_msg = ""
        if pack_name and not pack_name.strip():
            validation_msg = "Pack name cannot be empty."
        elif price <= 0:
            validation_msg = "Price must be greater than 0."
        elif total_minutes <= 0:
            validation_msg = "At least one speedup must be greater than 0."
        if validation_msg and st.session_state.get("add_pack_btn"):
            st.error(validation_msg)

        # --- Add Pack Logic ---
        if add_btn and not add_disabled:
            cost_per_min = calculate_cost_per_minute(price, total_minutes)
            new_entry = {
                "Pack Name": pack_name.strip(),
                "Price": float(price),
                "60min Speedups": int(hour_speedups),
                "5min Speedups": int(five_min_speedups),
                "Total Speedup Minutes": int(total_minutes),
                "Cost per Minute": cost_per_min
            }
            history.append(new_entry)
            st.session_state.pack_value_history = history
            save_pack_history(history)
            st.success(f"Pack '{pack_name.strip()}' added.")
            st.experimental_rerun()

    st.markdown("---")

    # --- Table Display ---
    if history:
        df = pd.DataFrame(history)
        sort_col = st.selectbox("Sort by", options=df.columns, index=5, key="sort_col")
        ascending = st.radio("Order", ["Ascending", "Descending"], index=0, horizontal=True, key="sort_order")
        df = df.sort_values(by=sort_col, ascending=(ascending=="Ascending"), ignore_index=True)

        # --- Action Buttons ---
        col1, col2, col3 = st.columns([2,2,2])
        with col1:
            remove_idx = st.selectbox(
                "Remove Pack",
                options=["-"] + [f"{row['Pack Name']} (${row['Price']}, {row['Total Speedup Minutes']}m)" for i, row in df.iterrows()],
                key="remove_pack_select"
            )
            if remove_idx != "-":
                if st.button("Remove Selected", key="remove_btn"):
                    st.session_state.remove_confirm = remove_idx
            if st.session_state.get("remove_confirm") == remove_idx:
                if st.button(f"Confirm Remove '{remove_idx.split(' ($')[0]}'", key="remove_confirm_btn"):
                    idx = df.index[df["Pack Name"] == remove_idx.split(" ($")[0]].tolist()
                    if idx:
                        history.pop(idx[0])
                        st.session_state.pack_value_history = history
                        save_pack_history(history)
                        st.success("Removed successfully.")
                        st.session_state.remove_confirm = None
                        st.experimental_rerun()
                if st.button("Cancel", key="remove_cancel_btn"):
                    st.session_state.remove_confirm = None
        with col2:
            if st.button("Clear All", key="clear_all_btn"):
                st.session_state.clear_all_confirm = True
            if st.session_state.get("clear_all_confirm"):
                if st.button("Confirm Clear All", key="clear_all_confirm_btn"):
                    st.session_state.pack_value_history = []
                    save_pack_history([])
                    st.success("All history cleared.")
                    st.session_state.clear_all_confirm = False
                    st.experimental_rerun()
                if st.button("Cancel", key="clear_all_cancel_btn"):
                    st.session_state.clear_all_confirm = False
        with col3:
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Export CSV",
                data=csv,
                file_name="pack_value_comparison.csv",
                mime="text/csv",
                key="export_csv_btn"
            )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No pack history yet. Add a pack above to get started.") 