"""
Hall of Chiefs Points Efficiency Module
Handles comparison of points gained from different activities.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple
from utils.session_manager import get_training_params

# Session state keys
CONSTRUCTION_ENTRIES_KEY = 'hall_of_chiefs_construction_entries'
RESEARCH_ENTRIES_KEY = 'hall_of_chiefs_research_entries'

def init_hall_of_chiefs_session_state():
    """Initialize session state for Hall of Chiefs tab."""
    if CONSTRUCTION_ENTRIES_KEY not in st.session_state:
        st.session_state[CONSTRUCTION_ENTRIES_KEY] = []
    if RESEARCH_ENTRIES_KEY not in st.session_state:
        st.session_state[RESEARCH_ENTRIES_KEY] = []

def calculate_construction_points(power: float, points_per_power: int) -> float:
    """
    Calculate points for construction activity.
    
    Args:
        power (float): Power value
        points_per_power (int): Points per power (30 or 45)
    
    Returns:
        float: Total points earned
    """
    return power * points_per_power

def calculate_research_points(power: float, points_per_power: int) -> float:
    """
    Calculate points for research activity.
    
    Args:
        power (float): Power value
        points_per_power (int): Points per power (30 or 45)
    
    Returns:
        float: Total points earned
    """
    return power * points_per_power

def calculate_training_points(params: Dict[str, Any]) -> Tuple[float, float]:
    """
    Calculate training points and speedup minutes from training parameters.
    
    Args:
        params (Dict[str, Any]): Training parameters
    
    Returns:
        Tuple[float, float]: Total points and total speedup minutes
    """
    from calculations import calculate_batches_and_points
    from features.speedup_inventory import get_speedup_inventory, get_total_speedups_for_category
    
    # Get speed-up inventory and calculate total training speed-ups
    inventory = get_speedup_inventory()
    total_speedups = get_total_speedups_for_category('training', inventory)
    
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    
    # Calculate base training time from individual components
    base_training_time = (params['days'] * 24 * 60) + (params['hours'] * 60) + params['minutes'] + (params['seconds'] / 60)
    
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        base_training_time,
        points_per_batch,
        0.0  # Current points
    )
    
    speedup_minutes_used = batches * base_training_time
    return total_points, speedup_minutes_used

def render_construction_sidebar() -> List[Dict[str, Any]]:
    """Render construction parameters in sidebar."""
    with st.sidebar.expander("Construction Parameters", expanded=False):
        st.subheader("Construction Entries")
        
        entries = st.session_state.get(CONSTRUCTION_ENTRIES_KEY, [])
        
        # Add new entry button
        if st.button("Add Construction Entry", key="add_construction"):
            entries.append({
                'description': '',
                'power': 0.0,
                'speedup_minutes': 0.0,
                'points_per_power': 30
            })
            st.session_state[CONSTRUCTION_ENTRIES_KEY] = entries
            st.experimental_rerun()
        
        # Render existing entries
        for i, entry in enumerate(entries):
            with st.container():
                st.write(f"**Entry {i + 1}**")
                
                # Description field
                description = st.text_input(
                    "Description",
                    value=entry.get('description', ''),
                    key=f"construction_description_{i}",
                    help="Optional description for this construction entry"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    power = st.number_input(
                        "Power",
                        min_value=0.0,
                        value=entry['power'],
                        step=1.0,
                        key=f"construction_power_{i}"
                    )
                    speedup_minutes = st.number_input(
                        "Speed-up Minutes",
                        min_value=0.0,
                        value=entry['speedup_minutes'],
                        step=1.0,
                        key=f"construction_speedup_{i}"
                    )
                
                with col2:
                    points_per_power = st.selectbox(
                        "Points per Power",
                        options=[30, 45],
                        index=0 if entry['points_per_power'] == 30 else 1,
                        key=f"construction_points_per_power_{i}"
                    )
                    
                    # Red Remove button
                    if st.button(
                        "Remove", 
                        key=f"remove_construction_{i}",
                        help="Remove this construction entry"
                    ):
                        entries.pop(i)
                        st.session_state[CONSTRUCTION_ENTRIES_KEY] = entries
                        st.experimental_rerun()
                
                # Update entry
                entry.update({
                    'description': description,
                    'power': power,
                    'speedup_minutes': speedup_minutes,
                    'points_per_power': points_per_power
                })
        
        return entries

def render_research_sidebar() -> List[Dict[str, Any]]:
    """Render research parameters in sidebar."""
    with st.sidebar.expander("Research Parameters", expanded=False):
        st.subheader("Research Entries")
        
        entries = st.session_state.get(RESEARCH_ENTRIES_KEY, [])
        
        # Add new entry button
        if st.button("Add Research Entry", key="add_research"):
            entries.append({
                'description': '',
                'power': 0.0,
                'speedup_minutes': 0.0,
                'points_per_power': 30
            })
            st.session_state[RESEARCH_ENTRIES_KEY] = entries
            st.experimental_rerun()
        
        # Render existing entries
        for i, entry in enumerate(entries):
            with st.container():
                st.write(f"**Entry {i + 1}**")
                
                description = st.text_input(
                    "Description",
                    value=entry['description'],
                    key=f"research_description_{i}"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    power = st.number_input(
                        "Power",
                        min_value=0.0,
                        value=entry.get('power', 0.0),
                        step=1.0,
                        key=f"research_power_{i}"
                    )
                    speedup_minutes = st.number_input(
                        "Speed-up Minutes",
                        min_value=0.0,
                        value=entry['speedup_minutes'],
                        step=1.0,
                        key=f"research_speedup_{i}"
                    )
                
                with col2:
                    points_per_power = st.selectbox(
                        "Points per Power",
                        options=[30, 45],
                        index=0 if entry['points_per_power'] == 30 else 1,
                        key=f"research_points_per_power_{i}"
                    )
                    
                    # Red Remove button
                    if st.button(
                        "Remove", 
                        key=f"remove_research_{i}",
                        help="Remove this research entry"
                    ):
                        entries.pop(i)
                        st.session_state[RESEARCH_ENTRIES_KEY] = entries
                        st.experimental_rerun()
                
                # Update entry
                entry.update({
                    'description': description,
                    'power': power,
                    'speedup_minutes': speedup_minutes,
                    'points_per_power': points_per_power
                })
        
        return entries

def create_efficiency_dataframe(
    construction_entries: List[Dict[str, Any]],
    research_entries: List[Dict[str, Any]],
    training_params: Dict[str, Any]
) -> pd.DataFrame:
    """
    Create a DataFrame with all activities and their efficiency metrics.
    
    Args:
        construction_entries (List[Dict[str, Any]]): Construction entries
        research_entries (List[Dict[str, Any]]): Research entries
        training_params (Dict[str, Any]): Training parameters
    
    Returns:
        pd.DataFrame: DataFrame with all activities and efficiency data
    """
    data = []
    
    # Add construction entries
    for i, entry in enumerate(construction_entries):
        points = calculate_construction_points(entry['power'], entry['points_per_power'])
        efficiency = points / entry['speedup_minutes'] if entry['speedup_minutes'] > 0 else 0.0
        
        data.append({
            'Activity Type': 'Construction',
            'Description': entry.get('description', f"Power: {entry['power']:.0f}"),
            'Power': entry['power'],
            'Total Points': points,
            'Speed-up Minutes': entry['speedup_minutes'],
            'Efficiency (Points/Min)': efficiency
        })
    
    # Add research entries
    for i, entry in enumerate(research_entries):
        points = calculate_research_points(entry.get('power', 0.0), entry['points_per_power'])
        efficiency = points / entry['speedup_minutes'] if entry['speedup_minutes'] > 0 else 0.0
        
        data.append({
            'Activity Type': 'Research',
            'Description': entry['description'] or f"Research {i + 1}",
            'Power': entry.get('power', 0.0),
            'Total Points': points,
            'Speed-up Minutes': entry['speedup_minutes'],
            'Efficiency (Points/Min)': efficiency
        })
    
    # Add training entry
    if training_params:
        training_points, training_speedups = calculate_training_points(training_params)
        efficiency = training_points / training_speedups if training_speedups > 0 else 0.0
        
        data.append({
            'Activity Type': 'Training',
            'Description': f"Troops: {training_params['troops_per_batch']} per batch",
            'Power': 0.0,  # Training doesn't use power
            'Total Points': training_points,
            'Speed-up Minutes': training_speedups,
            'Efficiency (Points/Min)': efficiency
        })
    
    return pd.DataFrame(data)

def create_category_dataframes(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Split the main DataFrame into category-specific DataFrames.
    
    Args:
        df (pd.DataFrame): Main efficiency DataFrame
    
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of category-specific DataFrames
    """
    if df.empty:
        return {
            'Construction': pd.DataFrame(),
            'Research': pd.DataFrame(),
            'Training': pd.DataFrame()
        }
    
    return {
        'Construction': df[df['Activity Type'] == 'Construction'].copy(),
        'Research': df[df['Activity Type'] == 'Research'].copy(),
        'Training': df[df['Activity Type'] == 'Training'].copy()
    }

def calculate_category_summary(df: pd.DataFrame, category: str) -> Dict[str, Any]:
    """
    Calculate summary metrics for a specific category.
    
    Args:
        df (pd.DataFrame): Category-specific DataFrame
        category (str): Category name
    
    Returns:
        Dict[str, Any]: Summary metrics for the category
    """
    if df.empty:
        return {
            'avg_efficiency': 0.0,
            'total_points': 0.0,
            'total_speedups': 0.0,
            'entry_count': 0
        }
    
    return {
        'avg_efficiency': df['Efficiency (Points/Min)'].mean(),
        'total_points': df['Total Points'].sum(),
        'total_speedups': df['Speed-up Minutes'].sum(),
        'entry_count': len(df)
    }

def calculate_summary_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate summary metrics for the efficiency data.
    
    Args:
        df (pd.DataFrame): Efficiency DataFrame
    
    Returns:
        Dict[str, Any]: Summary metrics
    """
    if df.empty:
        return {
            'research_avg_efficiency': 0.0,
            'total_points_by_type': {},
            'total_speedups_by_type': {},
            'overall_total_points': 0.0,
            'overall_total_speedups': 0.0
        }
    
    # Research average efficiency
    research_df = df[df['Activity Type'] == 'Research']
    research_avg_efficiency = research_df['Efficiency (Points/Min)'].mean() if not research_df.empty else 0.0
    
    # Totals by activity type
    total_points_by_type = df.groupby('Activity Type')['Total Points'].sum().to_dict()
    total_speedups_by_type = df.groupby('Activity Type')['Speed-up Minutes'].sum().to_dict()
    
    # Overall totals
    overall_total_points = df['Total Points'].sum()
    overall_total_speedups = df['Speed-up Minutes'].sum()
    
    return {
        'research_avg_efficiency': research_avg_efficiency,
        'total_points_by_type': total_points_by_type,
        'total_speedups_by_type': total_speedups_by_type,
        'overall_total_points': overall_total_points,
        'overall_total_speedups': overall_total_speedups
    }

def clear_all_entries():
    """Clear all entries from all categories."""
    st.session_state[CONSTRUCTION_ENTRIES_KEY] = []
    st.session_state[RESEARCH_ENTRIES_KEY] = []

def render_hall_of_chiefs_tab():
    """Render the Hall of Chiefs Points Efficiency tab."""
    st.header("Hall of Chiefs Points Efficiency")
    st.caption("Compare points gained from Construction, Research, and Training activities relative to speed-up minutes spent.")
    
    # Initialize session state
    init_hall_of_chiefs_session_state()
    
    # Get training parameters (reuse existing UI)
    training_params = get_training_params()
    
    # Render sidebar sections
    construction_entries = render_construction_sidebar()
    research_entries = render_research_sidebar()
    
    # Create efficiency DataFrame
    df = create_efficiency_dataframe(construction_entries, research_entries, training_params)
    
    # Calculate summary metrics
    summary = calculate_summary_metrics(df)
    
    # Remove All Entries button
    if not df.empty:
        st.subheader("Manage Entries")
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button(
                "🗑️ Remove All Entries",
                type="primary",
                help="Clear all entries from all categories"
            ):
                # Show confirmation dialog
                st.warning("Are you sure you want to remove all entries?")
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("Yes, Remove All"):
                        clear_all_entries()
                        st.success("All entries have been removed.")
                        st.experimental_rerun()
                with col_confirm2:
                    if st.button("Cancel"):
                        st.info("Operation cancelled.")
        with col2:
            st.write("⚠️ This action cannot be undone.")
    
    # Display overall summary table
    if not df.empty:
        st.subheader("Overall Summary")
        
        # Create summary table
        summary_data = []
        for activity_type in ['Construction', 'Research', 'Training']:
            if activity_type in summary['total_points_by_type']:
                efficiency = (summary['total_points_by_type'][activity_type] / 
                            summary['total_speedups_by_type'][activity_type] 
                            if summary['total_speedups_by_type'][activity_type] > 0 else 0.0)
                summary_data.append({
                    'Category': activity_type,
                    'Total Points': summary['total_points_by_type'][activity_type],
                    'Total Speed-ups': summary['total_speedups_by_type'][activity_type],
                    'Avg Efficiency (pts/min)': efficiency
                })
        
        summary_df = pd.DataFrame(summary_data)
        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )
    
    # Split into category-specific tables
    category_dfs = create_category_dataframes(df)
    
    # Display category-specific tables
    for category in ['Construction', 'Research', 'Training']:
        category_df = category_dfs[category]
        if not category_df.empty:
            st.subheader(f"{category} Entries")
            
            # Calculate category summary
            category_summary = calculate_category_summary(category_df, category)
            
            # Display category summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(
                    f"{category} Entries",
                    category_summary['entry_count']
                )
            with col2:
                st.metric(
                    f"{category} Total Points",
                    f"{category_summary['total_points']:,.0f}"
                )
            with col3:
                st.metric(
                    f"{category} Total Speed-ups",
                    f"{category_summary['total_speedups']:,.0f} min"
                )
            with col4:
                st.metric(
                    f"{category} Avg Efficiency",
                    f"{category_summary['avg_efficiency']:.2f} pts/min"
                )
            
            # Display category table
            display_df = category_df.drop('Activity Type', axis=1)  # Remove redundant column
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.subheader(f"{category} Entries")
            st.info(f"No {category.lower()} entries available. Add entries in the sidebar.")
    
    # Export functionality
    if not df.empty:
        st.subheader("Export Data")
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export All Efficiency Data (CSV)",
            data=csv,
            file_name="hall_of_chiefs_efficiency.csv",
            mime="text/csv",
            key="export_efficiency_csv"
        ) 