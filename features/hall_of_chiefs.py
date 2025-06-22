"""
Hall of Chiefs Points Efficiency Tab for Whiteout Survival Calculator
Allows users to input and compare points gained from Construction, Research, and Training activities.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Tuple
from calculations import calculate_efficiency_metrics
from utils.session_manager import get_training_params

# --- Session State Keys ---
CONSTRUCTION_ENTRIES_KEY = "hall_of_chiefs_construction_entries"
RESEARCH_ENTRIES_KEY = "hall_of_chiefs_research_entries"

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

def calculate_research_points(description: str, speedup_minutes: float, points_per_power: int) -> float:
    """
    Calculate points for research activity.
    
    Args:
        description (str): Research description
        speedup_minutes (float): Speed-up minutes used
        points_per_power (int): Points per power (30 or 45)
    
    Returns:
        float: Total points earned (estimated based on time)
    """
    # Estimate power based on speedup minutes (rough approximation)
    estimated_power = speedup_minutes / 10  # Rough estimate: 10 minutes per power
    return estimated_power * points_per_power

def calculate_training_points(params: Dict[str, Any]) -> Tuple[float, float]:
    """
    Calculate training points and speedup minutes from training parameters.
    
    Args:
        params (Dict[str, Any]): Training parameters
    
    Returns:
        Tuple[float, float]: Total points and total speedup minutes
    """
    from calculations import calculate_batches_and_points
    
    total_speedups = params['general_speedups'] + params['training_speedups']
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
                    
                    if st.button("Remove", key=f"remove_construction_{i}"):
                        entries.pop(i)
                        st.session_state[CONSTRUCTION_ENTRIES_KEY] = entries
                        st.experimental_rerun()
                
                # Update entry
                entry.update({
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
                    
                    if st.button("Remove", key=f"remove_research_{i}"):
                        entries.pop(i)
                        st.session_state[RESEARCH_ENTRIES_KEY] = entries
                        st.experimental_rerun()
                
                # Update entry
                entry.update({
                    'description': description,
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
            'Description': f"Power: {entry['power']:.0f}",
            'Total Points': points,
            'Speed-up Minutes': entry['speedup_minutes'],
            'Efficiency (Points/Min)': efficiency
        })
    
    # Add research entries
    for i, entry in enumerate(research_entries):
        points = calculate_research_points(entry['description'], entry['speedup_minutes'], entry['points_per_power'])
        efficiency = points / entry['speedup_minutes'] if entry['speedup_minutes'] > 0 else 0.0
        
        data.append({
            'Activity Type': 'Research',
            'Description': entry['description'] or f"Research {i + 1}",
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
            'Total Points': training_points,
            'Speed-up Minutes': training_speedups,
            'Efficiency (Points/Min)': efficiency
        })
    
    return pd.DataFrame(data)

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
    
    # Display summary metrics
    if not df.empty:
        st.subheader("Summary Metrics")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Research Avg Efficiency",
                f"{summary['research_avg_efficiency']:.2f} pts/min",
                help="Average efficiency for all research entries"
            )
        with col2:
            st.metric(
                "Overall Total Points",
                f"{summary['overall_total_points']:,.0f}",
                help="Total points across all activities"
            )
        with col3:
            st.metric(
                "Overall Total Speed-ups",
                f"{summary['overall_total_speedups']:,.0f} min",
                help="Total speed-up minutes across all activities"
            )
        
        # Activity type breakdown
        st.subheader("Activity Breakdown")
        for activity_type in ['Construction', 'Research', 'Training']:
            if activity_type in summary['total_points_by_type']:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(
                        f"{activity_type} Total Points",
                        f"{summary['total_points_by_type'][activity_type]:,.0f}"
                    )
                with col2:
                    st.metric(
                        f"{activity_type} Total Speed-ups",
                        f"{summary['total_speedups_by_type'][activity_type]:,.0f} min"
                    )
                with col3:
                    efficiency = (summary['total_points_by_type'][activity_type] / 
                                summary['total_speedups_by_type'][activity_type] 
                                if summary['total_speedups_by_type'][activity_type] > 0 else 0.0)
                    st.metric(
                        f"{activity_type} Efficiency",
                        f"{efficiency:.2f} pts/min"
                    )
    
    # Display efficiency table
    st.subheader("Efficiency Comparison Table")
    
    if not df.empty:
        # Sort options
        col1, col2 = st.columns(2)
        with col1:
            sort_column = st.selectbox(
                "Sort by",
                options=df.columns,
                index=4,  # Default to Efficiency
                key="efficiency_sort_col"
            )
        with col2:
            sort_ascending = st.radio(
                "Sort Order",
                ["Descending", "Ascending"],
                index=0,
                horizontal=True,
                key="efficiency_sort_order"
            )
        
        # Sort DataFrame
        df_sorted = df.sort_values(
            by=sort_column,
            ascending=(sort_ascending == "Ascending"),
            ignore_index=True
        )
        
        # Display table
        st.dataframe(
            df_sorted,
            use_container_width=True,
            hide_index=True
        )
        
        # Export functionality
        csv = df_sorted.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export Efficiency Data (CSV)",
            data=csv,
            file_name="hall_of_chiefs_efficiency.csv",
            mime="text/csv",
            key="export_efficiency_csv"
        )
    else:
        st.info("No data available. Add entries in the sidebar to see efficiency comparisons.") 