"""
Whiteout Survival Investment/Return Calculator
Main Streamlit application for calculating and optimizing investment returns.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
from calculations import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)

# Page configuration
st.set_page_config(
    page_title="Whiteout Survival Calculator",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Main container */
    .stApp {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Cards and metrics */
    .stMetric {
        background-color: #2D2D2D;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stMetric label {
        color: #A0A0A0;
        font-size: 0.9rem;
    }
    
    .stMetric div[data-testid="stMetricValue"] {
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Input fields */
    .stNumberInput>div>div>input {
        background-color: #2D2D2D;
        color: white;
        border: 1px solid #404040;
        border-radius: 4px;
    }
    
    .stNumberInput>div>div>input:focus {
        border-color: #4CAF50;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        transition: background-color 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #45a049;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #252525;
    }
    
    /* Table styling */
    .stDataFrame {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Form styling */
    .stForm {
        background-color: #2D2D2D;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stMetric {
            margin-bottom: 0.5rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("❄️ Whiteout Survival Investment Calculator")
st.markdown("""
    Optimize your training strategy with precise calculations and visual insights.
    Input your parameters in the sidebar to analyze your training efficiency.
""")

# Initialize session state for pack purchases if not exists
if 'pack_purchases' not in st.session_state:
    st.session_state.pack_purchases = []

# Initialize session state for CSV data if not exists
if 'csv_purchases' not in st.session_state:
    st.session_state.csv_purchases = None

def load_csv_purchases():
    """Load purchases from CSV file."""
    try:
        csv_path = os.path.join('data', 'purchase_history.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path, parse_dates=['Date'])
            st.session_state.csv_purchases = df
            return True
        return False
    except Exception as e:
        st.error(f"Error loading CSV file: {str(e)}")
        return False

# Create tabs
tab1, tab2 = st.tabs(["Training Analysis", "Pack Purchases"])

with tab1:
    # Sidebar for input parameters
    with st.sidebar:
        st.header("Training Parameters")
        
        # Speed-up inputs
        st.subheader("Speed-up Minutes")
        general_speedups = st.number_input(
            "General Speed-ups",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            help="General purpose speed-up minutes available"
        )
        
        training_speedups = st.number_input(
            "Troop Training Speed-ups",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            help="Speed-up minutes specifically for troop training"
        )
        
        total_speedups = general_speedups + training_speedups
        
        # Training parameters
        st.subheader("Base Training Time")
        col1, col2 = st.columns(2)
        with col1:
            days = st.number_input("Days", min_value=0, value=0, step=1)
            minutes = st.number_input("Minutes", min_value=0, max_value=59, value=57, step=1)
        with col2:
            hours = st.number_input("Hours", min_value=0, max_value=23, value=4, step=1)
            seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1)
        
        base_training_time = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)
        
        # Troops and points
        st.subheader("Training Configuration")
        troops_per_batch = st.number_input(
            "Troops per Batch",
            min_value=1,
            value=426,
            step=1,
            help="Number of troops trained in each batch"
        )
        
        time_reduction_bonus = st.number_input(
            "Training Time Reduction (%)",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=1.0,
            help="Your training time reduction bonus"
        ) / 100
        
        points_per_troop = st.number_input(
            "Points per Troop",
            min_value=1.0,
            value=830.0,
            step=1.0,
            help="Base points earned per troop"
        )
        
        # Target points
        st.subheader("Goals")
        target_points = st.number_input(
            "Target Points",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
            help="Your target points goal"
        )

    # Main content area
    st.header("Training Analysis")

    # Calculate metrics
    effective_time = calculate_effective_training_time(
        base_training_time,
        time_reduction_bonus
    )

    num_batches, total_points = calculate_batches_and_points(
        total_speedups,
        effective_time,
        points_per_troop * troops_per_batch,
        0
    )

    efficiency = calculate_efficiency_metrics(total_speedups, total_points)

    # Display results in a grid
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Effective Training Time",
            f"{effective_time:.1f} min",
            help="Training time after reduction bonus"
        )

    with col2:
        st.metric(
            "Number of Batches",
            f"{num_batches:,}",
            help="Total batches that can be trained"
        )

    with col3:
        st.metric(
            "Total Points",
            f"{total_points:,.0f}",
            help="Total points earned from all batches"
        )

    with col4:
        st.metric(
            "Points per Minute",
            f"{efficiency['points_per_minute']:.2f}",
            help="Efficiency metric"
        )

    # Speed-up usage breakdown
    st.subheader("Speed-up Usage")
    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "General Speed-ups Used",
            f"{min(general_speedups, total_speedups):,.0f} min",
            help="General speed-ups that will be used"
        )

    with col2:
        st.metric(
            "Training Speed-ups Used",
            f"{min(training_speedups, total_speedups):,.0f} min",
            help="Training-specific speed-ups that will be used"
        )

    # Target points calculation
    if target_points > 0:
        speedups_needed = calculate_speedups_needed(
            target_points,
            points_per_troop * troops_per_batch,
            0,
            effective_time
        )
        st.metric(
            "Speed-ups Needed for Target",
            f"{speedups_needed:,.0f} min",
            help="Required speed-up minutes to reach target"
        )

with tab2:
    st.header("Pack Purchase History")
    
    # Load CSV data on tab entry or refresh
    if st.session_state.csv_purchases is None:
        load_csv_purchases()
    
    # CSV Data Section
    st.subheader("CSV Purchase History")
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Reload CSV"):
            if load_csv_purchases():
                st.success("CSV data reloaded successfully!")
    
    if st.session_state.csv_purchases is not None:
        df_csv = st.session_state.csv_purchases
        
        # Calculate CSV summary metrics
        total_spent_csv = df_csv["Value (R$)"].sum()
        total_purchases_csv = len(df_csv)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent (CSV)", f"R${total_spent_csv:,.2f}")
        with col2:
            st.metric("Total Purchases (CSV)", f"{total_purchases_csv:,}")
        
        # Display CSV data
        st.dataframe(
            df_csv,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No CSV purchase history available. Please ensure 'data/purchase_history.csv' exists.")
    
    st.markdown("---")
    
    # Manual Purchase Form Section
    st.subheader("Manual Purchase Entry")
    with st.form("pack_purchase_form"):
        st.subheader("Add New Purchase")
        
        col1, col2 = st.columns(2)
        with col1:
            purchase_date = st.date_input(
                "Date of Purchase",
                value=datetime.now(),
                help="When did you purchase this pack?"
            )
            pack_name = st.text_input(
                "Pack Name",
                help="Name or description of the pack"
            )
        
        with col2:
            total_spending = st.number_input(
                "Total Spending ($)",
                min_value=0.0,
                step=0.01,
                help="How much did you spend on this pack?"
            )
            speedups_included = st.number_input(
                "Speed-ups Included (min)",
                min_value=0,
                step=1,
                help="How many speed-up minutes were included?"
            )
        
        submitted = st.form_submit_button("Add Purchase")
        
        if submitted:
            if pack_name and total_spending > 0:
                new_purchase = {
                    "Date": purchase_date,
                    "Pack Name": pack_name,
                    "Spending ($)": total_spending,
                    "Speed-ups (min)": speedups_included
                }
                st.session_state.pack_purchases.append(new_purchase)
                st.success("Purchase added successfully!")
            else:
                st.error("Please fill in all required fields.")
    
    # Display manual purchase history
    if st.session_state.pack_purchases:
        st.subheader("Manual Purchase History")
        df_manual = pd.DataFrame(st.session_state.pack_purchases)
        
        # Calculate manual summary metrics
        total_spent_manual = df_manual["Spending ($)"].sum()
        total_speedups_manual = df_manual["Speed-ups (min)"].sum()
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent (Manual)", f"${total_spent_manual:,.2f}")
        with col2:
            st.metric("Total Speed-ups (Manual)", f"{total_speedups_manual:,} min")
        
        # Display manual purchases table
        st.dataframe(
            df_manual,
            use_container_width=True,
            hide_index=True
        )
        
        # Add clear button
        if st.button("Clear Manual Purchase History"):
            st.session_state.pack_purchases = []
            st.experimental_rerun()
    else:
        st.info("No manual purchase history available. Add your first purchase using the form above.") 