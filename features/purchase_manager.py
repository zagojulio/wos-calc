"""
Module for managing purchase data persistence and calculations.
"""

import pandas as pd
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st
import plotly.express as px

# Constants for file paths
AUTO_PURCHASES_PATH = 'data/purchase_history.csv'
MANUAL_PURCHASES_PATH = 'data/manual_purchases.csv'

def load_purchases(auto_path: str = AUTO_PURCHASES_PATH, manual_path: str = MANUAL_PURCHASES_PATH) -> Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]:
    """
    Load both automatic and manual purchases.
    
    Args:
        auto_path (str): Path to automatic purchases CSV
        manual_path (str): Path to manual purchases CSV
    
    Returns:
        Tuple[Optional[pd.DataFrame], Optional[pd.DataFrame]]: Auto and manual purchases
    
    Raises:
        Exception: If file exists but cannot be read
    """
    auto_purchases = None
    manual_purchases = None
    
    try:
        if os.path.exists(auto_path):
            auto_purchases = pd.read_csv(auto_path, parse_dates=['Date'])
        else:
            raise Exception(f"Automatic purchases file not found: {auto_path}")
    except Exception as e:
        st.error(f"Error loading automatic purchases: {str(e)}")
        raise

    try:
        if os.path.exists(manual_path):
            manual_purchases = pd.read_csv(manual_path, parse_dates=['Date'])
        else:
            raise Exception(f"Manual purchases file not found: {manual_path}")
    except Exception as e:
        st.error(f"Error loading manual purchases: {str(e)}")
        raise
    
    return auto_purchases, manual_purchases

def save_purchase(csv_path: str, purchase: Dict) -> bool:
    """
    Append a new purchase to CSV file.
    
    Args:
        csv_path (str): Path to CSV file
        purchase (Dict): Purchase data to save
    
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Convert purchase to DataFrame
        df_new = pd.DataFrame([purchase])
        
        # Append to existing file or create new
        if os.path.exists(csv_path):
            df_new.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df_new.to_csv(csv_path, index=False)
        
        return True
    except Exception as e:
        raise Exception(f"Error saving purchase to {csv_path}: {str(e)}")

def calculate_purchase_stats(
    auto_purchases: Optional[pd.DataFrame],
    manual_purchases: Optional[pd.DataFrame]
) -> Dict:
    """
    Calculate combined purchase statistics.
    
    Args:
        auto_purchases (Optional[pd.DataFrame]): Automatic purchases
        manual_purchases (Optional[pd.DataFrame]): Manual purchases
    
    Returns:
        Dict: Statistics including totals and averages
    """
    stats = {
        "total_spent_auto": 0.0,
        "total_spent_manual": 0.0,
        "total_speedups": 0,
        "avg_spending_per_day": 0.0,
        "spending_by_day": pd.DataFrame()
    }
    
    # Process automatic purchases
    if auto_purchases is not None and not auto_purchases.empty:
        stats["total_spent_auto"] = auto_purchases["Value (R$)"].sum()
    
    # Process manual purchases
    if manual_purchases is not None and not manual_purchases.empty:
        stats["total_spent_manual"] = manual_purchases["Spending ($)"].sum()
        stats["total_speedups"] = manual_purchases["Speed-ups (min)"].sum()
    
    # Combine purchases for daily stats
    dfs = []
    if auto_purchases is not None and not auto_purchases.empty:
        auto_daily = auto_purchases.groupby('Date')["Value (R$)"].sum().reset_index()
        auto_daily.columns = ['Date', 'Amount']
        dfs.append(auto_daily)
    
    if manual_purchases is not None and not manual_purchases.empty:
        manual_daily = manual_purchases.groupby('Date')["Spending ($)"].sum().reset_index()
        manual_daily.columns = ['Date', 'Amount']
        dfs.append(manual_daily)
    
    if dfs:
        combined_daily = pd.concat(dfs).groupby('Date')['Amount'].sum().reset_index()
        stats["spending_by_day"] = combined_daily
        stats["avg_spending_per_day"] = combined_daily['Amount'].mean()
    
    return stats

def export_combined_purchases(
    auto_purchases: Optional[pd.DataFrame],
    manual_purchases: Optional[pd.DataFrame],
    output_path: str = 'data/combined_purchases.csv'
) -> bool:
    """
    Export combined purchase history to CSV.
    
    Args:
        auto_purchases (Optional[pd.DataFrame]): Automatic purchases
        manual_purchases (Optional[pd.DataFrame]): Manual purchases
        output_path (str): Path to save combined CSV
    
    Returns:
        bool: Success status
    Raises:
        Exception: If file writing fails
    """
    try:
        dfs = []
        if auto_purchases is not None and not auto_purchases.empty:
            auto_df = auto_purchases.copy()
            if 'Pack Name' not in auto_df.columns:
                if 'Purchase Name' in auto_df.columns:
                    auto_df['Pack Name'] = auto_df['Purchase Name']
                else:
                    auto_df['Pack Name'] = ''
            if 'Value (R$)' in auto_df.columns:
                auto_df['Amount'] = auto_df['Value (R$)']
            elif 'Spending ($)' in auto_df.columns:
                auto_df['Amount'] = auto_df['Spending ($)']
            else:
                auto_df['Amount'] = 0.0
            if 'Speed-ups (min)' not in auto_df.columns:
                auto_df['Speed-ups (min)'] = 0
            auto_df['Source'] = 'Automatic'
            dfs.append(auto_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])
        if manual_purchases is not None and not manual_purchases.empty:
            manual_df = manual_purchases.copy()
            if 'Amount' not in manual_df.columns:
                if 'Spending ($)' in manual_df.columns:
                    manual_df['Amount'] = manual_df['Spending ($)']
                else:
                    manual_df['Amount'] = 0.0
            if 'Speed-ups (min)' not in manual_df.columns:
                manual_df['Speed-ups (min)'] = 0
            manual_df['Source'] = 'Manual'
            if 'Pack Name' not in manual_df.columns:
                manual_df['Pack Name'] = ''
            dfs.append(manual_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])
        if dfs:
            combined_df = pd.concat(dfs).sort_values('Date')
            try:
                combined_df.to_csv(output_path, index=False)
            except Exception as e:
                raise Exception(f"Error exporting combined purchases: {str(e)}")
            return True
        return False
    except Exception as e:
        raise Exception(f"Error exporting combined purchases: {str(e)}")

def render_purchase_tab():
    """Render the purchase tab UI and handle interactions."""
    st.header("Pack Purchase History")
    
    # Load purchase data
    auto_purchases, manual_purchases = load_purchases()
    
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
            st.experimental_rerun()

    # Calculate and display summary metrics
    stats = calculate_purchase_stats(auto_purchases, manual_purchases)

    st.subheader("Combined Purchase Summary")
    col1, col2, col3 = st.columns(3)
    with col1:
        total_spent = stats["total_spent_auto"] + stats["total_spent_manual"]
        st.metric("Total Spent", f"R${total_spent:,.2f}")
    with col2:
        st.metric("Average Daily Spending", f"R${stats['avg_spending_per_day']:,.2f}")
    with col3:
        st.metric("Total Speed-ups", f"{stats['total_speedups']:,} min")

    # Display spending trend chart
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

    # Export combined history button
    if st.button("📥 Export Combined History"):
        try:
            if export_combined_purchases(auto_purchases, manual_purchases):
                st.success("Combined history exported successfully!")
            else:
                st.warning("No purchases to export")
        except Exception as e:
            st.error(f"Error exporting combined history: {str(e)}")

    st.markdown("---")

    # Manual Purchase Entry Form
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

                    if save_purchase('data/manual_purchases.csv', new_purchase):
                        st.success("Purchase added successfully!")
                        st.experimental_rerun()
                    else:
                        st.error("Failed to save purchase")
                except Exception as e:
                    st.error(f"Error saving purchase: {str(e)}")
            else:
                st.error("Please fill in all required fields.")

    st.markdown("---")

    # Display purchase history tables
    st.subheader("Purchase History")

    # Combine and filter purchases
    dfs = []
    if auto_purchases is not None and not auto_purchases.empty:
        auto_df = auto_purchases.copy()
        # Standardize column names
        auto_df = auto_df.rename(columns={
            'Purchase Name': 'Pack Name',
            'Value (R$)': 'Amount'
        })
        # Add missing columns with default values
        if 'Speed-ups (min)' not in auto_df.columns:
            auto_df['Speed-ups (min)'] = 0
        auto_df['Source'] = 'Automatic'
        dfs.append(auto_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])

    if manual_purchases is not None and not manual_purchases.empty:
        manual_df = manual_purchases.copy()
        # Standardize column names
        manual_df = manual_df.rename(columns={
            'Spending ($)': 'Amount'
        })
        manual_df['Source'] = 'Manual'
        dfs.append(manual_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])

    if dfs:
        combined_df = pd.concat(dfs)
        combined_df['Date'] = pd.to_datetime(combined_df['Date'])
        combined_df = combined_df[
            (combined_df['Date'].dt.date >= date_range[0]) &
            (combined_df['Date'].dt.date <= date_range[1])
        ].sort_values('Date', ascending=False)

        # Display the combined table
        st.dataframe(
            combined_df,
            use_container_width=True,
            hide_index=True
        )

        # Delete purchase functionality
        st.subheader("Delete Purchase")
        
        # Create formatted options for selectbox
        purchase_options = []
        for idx, row in combined_df.iterrows():
            formatted_date = row['Date'].strftime('%Y-%m-%d')
            formatted_amount = f"R${row['Amount']:,.2f}"
            option_text = f"{formatted_date} - {row['Pack Name']} - {formatted_amount}"
            purchase_options.append((idx, option_text))
        
        # Create selectbox with formatted options
        selected_option = st.selectbox(
            "Select purchase to delete",
            options=[opt[1] for opt in purchase_options],
            format_func=lambda x: x
        )
        
        # Get the selected index from the options list
        selected_idx = next(idx for idx, text in purchase_options if text == selected_option)

        if st.button("🗑️ Delete Selected Purchase"):
            if manual_purchases is not None and not manual_purchases.empty:
                # Remove from manual purchases if it's a manual entry
                if combined_df.loc[selected_idx, 'Source'] == 'Manual':
                    manual_purchases = manual_purchases[
                        ~(manual_purchases['Date'] == combined_df.loc[selected_idx, 'Date']) &
                        ~(manual_purchases['Pack Name'] == combined_df.loc[selected_idx, 'Pack Name'])
                    ]
                    # Update CSV file
                    manual_purchases.to_csv('data/manual_purchases.csv', index=False)
                    st.success("Purchase deleted successfully!")
                    st.experimental_rerun()
                else:
                    st.warning("Cannot delete automatic purchases")
            else:
                st.error("No manual purchases available to delete")
    else:
        st.info("No purchase history available. Add your first purchase using the form above.") 