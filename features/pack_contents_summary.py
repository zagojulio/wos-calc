"""
Module for aggregating and summarizing pack contents from purchase history.
"""

import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
import streamlit as st
from datetime import datetime

# Speed-up conversion constants
SPEEDUP_CONVERSIONS = {
    '1h_speedups': 60,  # 1 hour = 60 minutes
    '1h_speedups_training': 60,  # 1 hour = 60 minutes
    '5m_speedups': 5,  # 5 minutes = 5 minutes
    '5m_speedups_training': 5,  # 5 minutes = 5 minutes
}

def load_pack_data(file_path: str = 'data/pack_items.json') -> List[Dict]:
    """
    Load pack data from JSON file.
    
    Args:
        file_path (str): Path to pack items JSON file
    
    Returns:
        List[Dict]: List of pack data with rewards
    
    Raises:
        Exception: If file cannot be read or parsed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except FileNotFoundError:
        st.warning(f"Pack data file not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Error parsing pack data file: {str(e)}")
        return []
    except Exception as e:
        st.error(f"Error loading pack data: {str(e)}")
        return []

def aggregate_pack_rewards(pack_data: List[Dict]) -> Tuple[Dict, int]:
    """
    Aggregate all rewards from pack purchases.
    
    Args:
        pack_data (List[Dict]): List of pack data with rewards
    
    Returns:
        Tuple[Dict, int]: Aggregated rewards and total speed-up minutes
    """
    aggregated_rewards = {}
    total_speedup_minutes = 0
    
    for pack in pack_data:
        if 'rewards' not in pack:
            continue
            
        rewards = pack['rewards']
        for item_name, quantity in rewards.items():
            # Handle speed-up conversions
            if item_name in SPEEDUP_CONVERSIONS:
                minutes = quantity * SPEEDUP_CONVERSIONS[item_name]
                total_speedup_minutes += minutes
                # Add to aggregated rewards as speed-up minutes
                if 'speedup_minutes' not in aggregated_rewards:
                    aggregated_rewards['speedup_minutes'] = 0
                aggregated_rewards['speedup_minutes'] += minutes
            else:
                # Regular item aggregation
                if item_name not in aggregated_rewards:
                    aggregated_rewards[item_name] = 0
                aggregated_rewards[item_name] += quantity
    
    return aggregated_rewards, total_speedup_minutes

def format_item_name(item_name: str) -> str:
    """
    Format item name for display.
    
    Args:
        item_name (str): Raw item name
    
    Returns:
        str: Formatted display name
    """
    # Handle special cases
    if item_name == 'speedup_minutes':
        return 'Speed-up Minutes'
    
    # Replace underscores with spaces and capitalize
    formatted = item_name.replace('_', ' ').title()
    
    # Handle specific item types with parentheses
    if '10k' in formatted.lower():
        formatted = formatted.replace('10K', '(10K)').replace('10k', '(10K)')
    elif '100k' in formatted.lower():
        formatted = formatted.replace('100K', '(100K)').replace('100k', '(100K)')
    elif '1k' in formatted.lower():
        formatted = formatted.replace('1K', '(1K)').replace('1k', '(1K)')
    elif '5k' in formatted.lower():
        formatted = formatted.replace('5K', '(5K)').replace('5k', '(5K)')
    
    return formatted

def create_pack_summary_dataframe(aggregated_rewards: Dict) -> pd.DataFrame:
    """
    Create a DataFrame for displaying pack contents summary.
    
    Args:
        aggregated_rewards (Dict): Aggregated rewards data
    
    Returns:
        pd.DataFrame: Formatted DataFrame for display
    """
    if not aggregated_rewards:
        return pd.DataFrame()
    
    # Convert to DataFrame
    items = []
    quantities = []
    
    for item_name, quantity in aggregated_rewards.items():
        items.append(format_item_name(item_name))
        quantities.append(quantity)
    
    df = pd.DataFrame({
        'Item': items,
        'Total Quantity': quantities
    })
    
    # Sort by quantity (descending) with speed-up minutes at top
    df['sort_key'] = df['Item'].apply(lambda x: 0 if x == 'Speed-up Minutes' else 1)
    df = df.sort_values(['sort_key', 'Total Quantity'], ascending=[True, False])
    df = df.drop('sort_key', axis=1)
    
    return df

def render_pack_contents_summary():
    """
    Render the pack contents summary UI component.
    """
    st.subheader("📦 Pack Contents Summary")
    
    # Load pack data
    pack_data = load_pack_data()
    
    if not pack_data:
        st.info("No pack data available. Please ensure pack_items.json contains valid data.")
        return
    
    # Aggregate rewards
    aggregated_rewards, total_speedup_minutes = aggregate_pack_rewards(pack_data)
    
    if not aggregated_rewards:
        st.info("No rewards found in pack data.")
        return
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Items", len(aggregated_rewards))
    with col2:
        st.metric("Total Speed-up Minutes", f"{total_speedup_minutes:,}")
    with col3:
        total_packs = len(pack_data)
        st.metric("Total Packs", total_packs)
    
    # Create and display summary table
    summary_df = create_pack_summary_dataframe(aggregated_rewards)
    
    if not summary_df.empty:
        st.markdown("### Item Breakdown")
        
        # Add search/filter functionality
        search_term = st.text_input(
            "🔍 Search items",
            placeholder="Type to filter items...",
            help="Filter items by name"
        )
        
        if search_term:
            summary_df = summary_df[
                summary_df['Item'].str.contains(search_term, case=False, na=False)
            ]
        
        # Display the table with custom styling
        if not summary_df.empty:
            st.dataframe(
                summary_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Item": st.column_config.TextColumn(
                        "Item",
                        width="medium"
                    ),
                    "Total Quantity": st.column_config.NumberColumn(
                        "Total Quantity",
                        format="%d",
                        width="small"
                    )
                }
            )
            
            # Export functionality
            if st.button("📥 Export Summary"):
                try:
                    csv_data = summary_df.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name=f"pack_contents_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                except Exception as e:
                    st.error(f"Error exporting summary: {str(e)}")
        else:
            st.info("No items match your search criteria.")
    else:
        st.info("No items to display.") 