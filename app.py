"""
Whiteout Survival Investment/Return Calculator
Main Streamlit application for calculating and optimizing investment returns.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import plotly.express as px
from calculations import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)
from features.purchase_manager import (
    load_purchases,
    save_purchase,
    calculate_purchase_stats,
    export_combined_purchases
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

# Initialize session state for purchases if not exists
if 'auto_purchases' not in st.session_state:
    st.session_state.auto_purchases = None

if 'manual_purchases' not in st.session_state:
    st.session_state.manual_purchases = None

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
            value=18000.0,
            step=100.0,
            help="General purpose speed-up minutes available"
        )
        
        training_speedups = st.number_input(
            "Troop Training Speed-ups",
            min_value=0.0,
            value=1515.0,
            step=100.0,
            help="Speed-up minutes specifically for troop training"
        )
        
        total_speedups = general_speedups + training_speedups
        
        # Training parameters
        st.subheader("Base Training Time")
        col1, col2 = st.columns(2)
        with col1:
            days = st.number_input("Days", min_value=0, value=0, step=1)
            minutes = st.number_input("Minutes", min_value=0, max_value=59, value=50, step=1)
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
    
    # Load purchase data on tab entry or refresh
    if st.session_state.auto_purchases is None:
        try:
            st.session_state.auto_purchases = load_purchases('data/purchase_history.csv')
        except Exception as e:
            st.error(f"Error loading automatic purchases: {str(e)}")
    
    if st.session_state.manual_purchases is None:
        try:
            st.session_state.manual_purchases = load_purchases('data/manual_purchases.csv')
        except Exception as e:
            st.error(f"Error loading manual purchases: {str(e)}")
    
    # Date range filter
    col1, col2 = st.columns([3, 1])
    with col1:
        date_range = st.date_input(
            "Date Range",
            value=(
                datetime.now() - timedelta(days=30),
                datetime.now()
            ),
            help="Filter purchases by date range"
        )
    
    with col2:
        if st.button("🔄 Reload Data"):
            try:
                st.session_state.auto_purchases = load_purchases('data/purchase_history.csv')
                st.session_state.manual_purchases = load_purchases('data/manual_purchases.csv')
                st.success("Data reloaded successfully!")
            except Exception as e:
                st.error(f"Error reloading data: {str(e)}")
    
    # Calculate combined statistics
    stats = calculate_purchase_stats(
        st.session_state.auto_purchases,
        st.session_state.manual_purchases
    )
    
    # Combined Summary Section
    st.subheader("Combined Purchase Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_spent = stats["total_spent_auto"] + stats["total_spent_manual"]
        st.metric("Total Spent", f"R${total_spent:,.2f}")
    
    with col2:
        st.metric("Average Daily Spending", f"R${stats['avg_spending_per_day']:,.2f}")
    
    with col3:
        st.metric("Total Speed-ups", f"{stats['total_speedups']:,} min")
    
    # Spending by day chart
    if not stats["spending_by_day"].empty:
        fig = px.bar(
            stats["spending_by_day"],
            x='Date',
            y='Amount',
            title='Daily Spending',
            labels={'Amount': 'Amount (R$)', 'Date': 'Date'},
            template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Export button
    if st.button("📥 Export Combined History"):
        try:
            export_path = 'data/combined_purchases.csv'
            if export_combined_purchases(
                st.session_state.auto_purchases,
                st.session_state.manual_purchases,
                export_path
            ):
                st.success(f"Combined history exported to {export_path}")
            else:
                st.warning("No purchases to export")
        except Exception as e:
            st.error(f"Error exporting combined history: {str(e)}")
    
    st.markdown("---")
    
    # Automatic Purchases Section
    st.subheader("Automatic Purchase History")
    if st.session_state.auto_purchases is not None and not st.session_state.auto_purchases.empty:
        df_auto = st.session_state.auto_purchases.copy()
        df_auto['Date'] = pd.to_datetime(df_auto['Date'])
        df_auto = df_auto[
            (df_auto['Date'].dt.date >= date_range[0]) &
            (df_auto['Date'].dt.date <= date_range[1])
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent (Auto)", f"R${stats['total_spent_auto']:,.2f}")
        with col2:
            st.metric("Total Purchases (Auto)", f"{len(df_auto):,}")
        
        st.dataframe(
            df_auto,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No automatic purchase history available.")
    
    st.markdown("---")
    
    # Manual Purchase Form Section
    st.subheader("Manual Purchase Entry")
    with st.form("pack_purchase_form"):
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
                "Total Spending (R$)",
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
                try:
                    new_purchase = {
                        "Date": purchase_date,
                        "Pack Name": pack_name,
                        "Spending ($)": total_spending,
                        "Speed-ups (min)": speedups_included
                    }
                    
                    # Save to CSV
                    if save_purchase('data/manual_purchases.csv', new_purchase):
                        # Update session state
                        if st.session_state.manual_purchases is None:
                            st.session_state.manual_purchases = pd.DataFrame([new_purchase])
                        else:
                            st.session_state.manual_purchases = pd.concat([
                                st.session_state.manual_purchases,
                                pd.DataFrame([new_purchase])
                            ])
                        st.success("Purchase added successfully!")
                    else:
                        st.error("Failed to save purchase")
                except Exception as e:
                    st.error(f"Error saving purchase: {str(e)}")
            else:
                st.error("Please fill in all required fields.")
    
    # Display manual purchase history
    st.subheader("Manual Purchase History")
    if st.session_state.manual_purchases is not None and not st.session_state.manual_purchases.empty:
        df_manual = st.session_state.manual_purchases.copy()
        df_manual['Date'] = pd.to_datetime(df_manual['Date'])
        df_manual = df_manual[
            (df_manual['Date'].dt.date >= date_range[0]) &
            (df_manual['Date'].dt.date <= date_range[1])
        ]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Spent (Manual)", f"R${stats['total_spent_manual']:,.2f}")
        with col2:
            st.metric("Total Speed-ups (Manual)", f"{stats['total_speedups']:,} min")
        
        st.dataframe(
            df_manual,
            use_container_width=True,
            hide_index=True
        )
        
        # Add clear button
        if st.button("Clear Manual Purchase History"):
            try:
                if os.path.exists('data/manual_purchases.csv'):
                    os.remove('data/manual_purchases.csv')
                st.session_state.manual_purchases = None
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error clearing manual purchases: {str(e)}")
    else:
        st.info("No manual purchase history available. Add your first purchase using the form above.") 