"""
Whiteout Survival Investment/Return Calculator
Main Streamlit application for calculating and optimizing investment returns.
"""

import streamlit as st
from features.ui_manager import setup_page_config, apply_custom_styling, render_header
from features.purchase_manager import render_purchase_tab
from features.speedup_inventory import render_speedup_inventory_sidebar
from utils.session_manager import init_session_state

def main():
    # Setup page configuration and styling
    setup_page_config()
    apply_custom_styling()
    render_header()

    # Initialize session state
    init_session_state()

    # Render speed-up inventory sidebar (available on all tabs)
    render_speedup_inventory_sidebar()

    # Main tabs navigation
    tab1, tab2, tab3 = st.tabs(["Pack Purchases", "Pack Value Comparison", "Hall of Chiefs"])

    # Pack Purchases Tab
    with tab1:
        # Render purchase tab UI and handle interactions
        render_purchase_tab()

    # Pack Value Comparison Tab
    with tab2:
        # Render the new pack value comparison tab
        from features.pack_value_comparison import render_pack_value_comparison_tab
        render_pack_value_comparison_tab()

    # Hall of Chiefs Tab
    with tab3:
        # Render the Hall of Chiefs points efficiency tab
        from features.hall_of_chiefs import render_hall_of_chiefs_tab
        render_hall_of_chiefs_tab()

if __name__ == "__main__":
    main()