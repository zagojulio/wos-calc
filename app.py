"""
Whiteout Survival Investment/Return Calculator
Main Streamlit application for calculating and optimizing investment returns.
"""

import streamlit as st
from features.ui_manager import setup_page_config, apply_custom_styling, render_header
from features.training_manager import render_training_sidebar, render_training_analysis
from features.purchase_manager import render_purchase_tab
from utils.session_manager import init_session_state

def main():
    # Setup page configuration and styling
    setup_page_config()
    apply_custom_styling()
    render_header()

    # Initialize session state
    init_session_state()

    # Main tabs navigation
    tab1, tab2 = st.tabs(["Training Analysis", "Pack Purchases"])

    # Training Analysis Tab
    with tab1:
        # Render training parameters in sidebar
        params = render_training_sidebar()
        # Render training analysis results
        render_training_analysis(params)

    # Pack Purchases Tab
    with tab2:
        # Render purchase tab UI and handle interactions
        render_purchase_tab()

if __name__ == "__main__":
    main()