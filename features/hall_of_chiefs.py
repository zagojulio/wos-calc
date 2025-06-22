"""
Hall of Chiefs Points Efficiency Module
Handles comparison of points gained from different activities.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List, Any, Tuple
from features.hall_of_chiefs_session import get_session_manager
from features.hall_of_chiefs_data import CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY

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
    
    # Validate training time before calculation
    if base_training_time <= 0:
        # Return zero values for invalid training time instead of raising error
        return 0.0, 0.0
    
    try:
        batches, total_points = calculate_batches_and_points(
            total_speedups,
            base_training_time,
            points_per_batch,
            0.0  # Current points
        )
        
        speedup_minutes_used = batches * base_training_time
        return total_points, speedup_minutes_used
    except ValueError as e:
        # Handle any other validation errors from calculate_batches_and_points
        # Return zero values instead of crashing
        return 0.0, 0.0

def render_construction_sidebar() -> None:
    """Render construction input form in sidebar."""
    session_manager = get_session_manager()
    
    with st.sidebar.expander("Construction Parameters", expanded=False):
        st.subheader("Add Construction Entry")
        
        # Check if we need to clear inputs
        if session_manager.should_clear_inputs(CONSTRUCTION_CATEGORY):
            session_manager.reset_clear_inputs_flag(CONSTRUCTION_CATEGORY)
            # Clear input values
            st.session_state[f"new_{CONSTRUCTION_CATEGORY}_description"] = ""
            st.session_state[f"new_{CONSTRUCTION_CATEGORY}_power"] = 0.0
            st.session_state[f"new_{CONSTRUCTION_CATEGORY}_speedup"] = 0.0
            st.session_state[f"new_{CONSTRUCTION_CATEGORY}_points_per_power"] = 30
        
        # Input fields for new entry
        description = st.text_input(
            "Description",
            key=f"new_{CONSTRUCTION_CATEGORY}_description",
            help="Required description for this construction entry"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            power = st.number_input(
                "Power",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"new_{CONSTRUCTION_CATEGORY}_power",
                help="Required power value"
            )
            speedup_minutes = st.number_input(
                "Speed-up Minutes",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"new_{CONSTRUCTION_CATEGORY}_speedup",
                help="Speed-up minutes used"
            )
        
        with col2:
            points_per_power = st.selectbox(
                "Points per Power",
                options=[30, 45],
                index=0,
                key=f"new_{CONSTRUCTION_CATEGORY}_points_per_power"
            )
        
        # Add Entry button
        if st.button("Add Entry", key=f"add_{CONSTRUCTION_CATEGORY}_entry", type="primary"):
            # Validate inputs
            is_valid, error_message = session_manager.validate_construction_entry(
                description, power, speedup_minutes, points_per_power
            )
            
            if is_valid:
                # Create new entry
                new_entry = {
                    'description': description.strip(),
                    'power': power,
                    'speedup_minutes': speedup_minutes,
                    'points_per_power': points_per_power
                }
                
                # Add entry via session manager
                success, message = session_manager.add_entry(CONSTRUCTION_CATEGORY, new_entry)
                
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to add entry: {message}")
            else:
                st.error(f"Validation error: {error_message}")
        
        # Show current entries count
        entry_count = session_manager.get_entry_count(CONSTRUCTION_CATEGORY)
        if entry_count[CONSTRUCTION_CATEGORY] > 0:
            st.info(f"Current entries: {entry_count[CONSTRUCTION_CATEGORY]}")

def render_research_sidebar() -> None:
    """Render research input form in sidebar."""
    session_manager = get_session_manager()
    
    with st.sidebar.expander("Research Parameters", expanded=False):
        st.subheader("Add Research Entry")
        
        # Check if we need to clear inputs
        if session_manager.should_clear_inputs(RESEARCH_CATEGORY):
            session_manager.reset_clear_inputs_flag(RESEARCH_CATEGORY)
            # Clear input values
            st.session_state[f"new_{RESEARCH_CATEGORY}_description"] = ""
            st.session_state[f"new_{RESEARCH_CATEGORY}_power"] = 0.0
            st.session_state[f"new_{RESEARCH_CATEGORY}_speedup"] = 0.0
            st.session_state[f"new_{RESEARCH_CATEGORY}_points_per_power"] = 30
        
        # Input fields for new entry
        description = st.text_input(
            "Description",
            key=f"new_{RESEARCH_CATEGORY}_description",
            help="Required description for this research entry"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            power = st.number_input(
                "Power",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"new_{RESEARCH_CATEGORY}_power",
                help="Required power value"
            )
            speedup_minutes = st.number_input(
                "Speed-up Minutes",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key=f"new_{RESEARCH_CATEGORY}_speedup",
                help="Speed-up minutes used"
            )
        
        with col2:
            points_per_power = st.selectbox(
                "Points per Power",
                options=[30, 45],
                index=0,
                key=f"new_{RESEARCH_CATEGORY}_points_per_power"
            )
        
        # Add Entry button
        if st.button("Add Entry", key=f"add_{RESEARCH_CATEGORY}_entry", type="primary"):
            # Validate inputs
            is_valid, error_message = session_manager.validate_research_entry(
                description, power, speedup_minutes, points_per_power
            )
            
            if is_valid:
                # Create new entry
                new_entry = {
                    'description': description.strip(),
                    'power': power,
                    'speedup_minutes': speedup_minutes,
                    'points_per_power': points_per_power
                }
                
                # Add entry via session manager
                success, message = session_manager.add_entry(RESEARCH_CATEGORY, new_entry)
                
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to add entry: {message}")
            else:
                st.error(f"Validation error: {error_message}")
        
        # Show current entries count
        entry_count = session_manager.get_entry_count(RESEARCH_CATEGORY)
        if entry_count[RESEARCH_CATEGORY] > 0:
            st.info(f"Current entries: {entry_count[RESEARCH_CATEGORY]}")

def render_training_sidebar() -> None:
    """Render training input form in sidebar."""
    session_manager = get_session_manager()
    
    with st.sidebar.expander("Training Parameters", expanded=False):
        st.subheader("Add Training Entry")
        
        # Check if we need to clear inputs
        if session_manager.should_clear_inputs(TRAINING_CATEGORY):
            session_manager.reset_clear_inputs_flag(TRAINING_CATEGORY)
            # Clear input values
            st.session_state[f"new_{TRAINING_CATEGORY}_description"] = ""
            st.session_state[f"new_{TRAINING_CATEGORY}_days"] = 0
            st.session_state[f"new_{TRAINING_CATEGORY}_hours"] = 0
            st.session_state[f"new_{TRAINING_CATEGORY}_minutes"] = 0
            st.session_state[f"new_{TRAINING_CATEGORY}_seconds"] = 0
            st.session_state[f"new_{TRAINING_CATEGORY}_troops_per_batch"] = 426
            st.session_state[f"new_{TRAINING_CATEGORY}_points_per_troop"] = 830.0
        
        # Input fields for new entry
        description = st.text_input(
            "Description",
            key=f"new_{TRAINING_CATEGORY}_description",
            help="Required description for this training entry"
        )
        
        # Time inputs
        st.write("**Training Time:**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            days = st.number_input("Days", min_value=0, value=0, key=f"new_{TRAINING_CATEGORY}_days")
        with col2:
            hours = st.number_input("Hours", min_value=0, value=0, key=f"new_{TRAINING_CATEGORY}_hours")
        with col3:
            minutes = st.number_input("Minutes", min_value=0, value=0, key=f"new_{TRAINING_CATEGORY}_minutes")
        with col4:
            seconds = st.number_input("Seconds", min_value=0, value=0, key=f"new_{TRAINING_CATEGORY}_seconds")
        
        # Training parameters
        col1, col2 = st.columns(2)
        with col1:
            troops_per_batch = st.number_input(
                "Troops per Batch",
                min_value=1,
                value=426,
                key=f"new_{TRAINING_CATEGORY}_troops_per_batch"
            )
        with col2:
            points_per_troop = st.number_input(
                "Points per Troop",
                min_value=0.1,
                value=830.0,
                step=0.1,
                key=f"new_{TRAINING_CATEGORY}_points_per_troop"
            )
        
        # Add Entry button
        if st.button("Add Entry", key=f"add_{TRAINING_CATEGORY}_entry", type="primary"):
            # Validate inputs
            is_valid, error_message = session_manager.validate_training_entry(
                description, days, hours, minutes, seconds, troops_per_batch, points_per_troop
            )
            
            if is_valid:
                # Create new entry
                new_entry = {
                    'description': description.strip(),
                    'days': days,
                    'hours': hours,
                    'minutes': minutes,
                    'seconds': seconds,
                    'troops_per_batch': troops_per_batch,
                    'points_per_troop': points_per_troop
                }
                
                # Add entry via session manager
                success, message = session_manager.add_entry(TRAINING_CATEGORY, new_entry)
                
                if success:
                    st.success(message)
                    st.experimental_rerun()
                else:
                    st.error(f"Failed to add entry: {message}")
            else:
                st.error(f"Validation error: {error_message}")
        
        # Show current entries count
        entry_count = session_manager.get_entry_count(TRAINING_CATEGORY)
        if entry_count[TRAINING_CATEGORY] > 0:
            st.info(f"Current entries: {entry_count[TRAINING_CATEGORY]}")

def create_efficiency_dataframe(
    construction_entries: List[Dict[str, Any]],
    research_entries: List[Dict[str, Any]],
    training_entries: List[Dict[str, Any]]
) -> pd.DataFrame:
    """
    Create a DataFrame with all activities and their efficiency metrics.
    
    Args:
        construction_entries (List[Dict[str, Any]]): Construction entries
        research_entries (List[Dict[str, Any]]): Research entries
        training_entries (List[Dict[str, Any]]): Training entries
    
    Returns:
        pd.DataFrame: DataFrame with all activities and efficiency data
    """
    data = []
    
    # Add construction entries
    for entry in construction_entries:
        points = calculate_construction_points(entry['power'], entry['points_per_power'])
        efficiency = points / entry['speedup_minutes'] if entry['speedup_minutes'] > 0 else 0.0
        
        data.append({
            'id': entry.get('id', ''),
            'Activity Type': 'Construction',
            'Description': entry.get('description', f"Power: {entry['power']:.0f}"),
            'Power': entry['power'],
            'Total Points': points,
            'Speed-up Minutes': entry['speedup_minutes'],
            'Efficiency (Points/Min)': efficiency,
            'Points per Power': entry['points_per_power']
        })
    
    # Add research entries
    for entry in research_entries:
        points = calculate_research_points(entry['power'], entry['points_per_power'])
        efficiency = points / entry['speedup_minutes'] if entry['speedup_minutes'] > 0 else 0.0
        
        data.append({
            'id': entry.get('id', ''),
            'Activity Type': 'Research',
            'Description': entry.get('description', ''),
            'Power': entry['power'],
            'Total Points': points,
            'Speed-up Minutes': entry['speedup_minutes'],
            'Efficiency (Points/Min)': efficiency,
            'Points per Power': entry['points_per_power']
        })
    
    # Add training entries
    for entry in training_entries:
        training_params = {
            'days': entry['days'],
            'hours': entry['hours'],
            'minutes': entry['minutes'],
            'seconds': entry['seconds'],
            'troops_per_batch': entry['troops_per_batch'],
            'points_per_troop': entry['points_per_troop']
        }
        
        # Calculate base training time for validation
        base_training_time = (entry['days'] * 24 * 60) + (entry['hours'] * 60) + entry['minutes'] + (entry['seconds'] / 60)
        
        # Check if training time is valid
        if base_training_time <= 0:
            # Add entry with warning for invalid training time
            data.append({
                'id': entry.get('id', ''),
                'Activity Type': 'Training',
                'Description': f"{entry.get('description', '')} ⚠️ (Invalid: Zero training time)",
                'Power': 0.0,  # Training doesn't use power
                'Total Points': 0.0,
                'Speed-up Minutes': 0.0,
                'Efficiency (Points/Min)': 0.0,
                'Points per Power': 0  # Training doesn't use points per power
            })
        else:
            training_points, training_speedups = calculate_training_points(training_params)
            efficiency = training_points / training_speedups if training_speedups > 0 else 0.0
            
            data.append({
                'id': entry.get('id', ''),
                'Activity Type': 'Training',
                'Description': entry.get('description', ''),
                'Power': 0.0,  # Training doesn't use power
                'Total Points': training_points,
                'Speed-up Minutes': training_speedups,
                'Efficiency (Points/Min)': efficiency,
                'Points per Power': 0  # Training doesn't use points per power
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

def handle_data_editor_changes(df: pd.DataFrame, category: str) -> None:
    """
    Handle changes from the data editor.
    
    Args:
        df (pd.DataFrame): Updated DataFrame from data editor
        category (str): Category being edited
    """
    session_manager = get_session_manager()
    
    # Get current entries for this category
    current_entries = session_manager.get_entries(category)
    
    # Find deleted entries (entries that were in current_entries but not in df)
    current_ids = {entry['id'] for entry in current_entries}
    updated_ids = {row['id'] for _, row in df.iterrows() if pd.notna(row['id'])}
    
    deleted_ids = current_ids - updated_ids
    
    # Delete removed entries
    for entry_id in deleted_ids:
        success, message = session_manager.delete_entry(category, entry_id)
        if not success:
            st.error(f"Failed to delete entry {entry_id}: {message}")
    
    # Update modified entries
    for _, row in df.iterrows():
        if pd.notna(row['id']):
            entry_id = row['id']
            
            # Find the original entry
            original_entry = next((entry for entry in current_entries if entry['id'] == entry_id), None)
            
            if original_entry:
                # Create updated entry based on category
                if category == CONSTRUCTION_CATEGORY:
                    updated_entry = {
                        'description': row['Description'],
                        'power': row['Power'],
                        'speedup_minutes': row['Speed-up Minutes'],
                        'points_per_power': row['Points per Power']
                    }
                elif category == RESEARCH_CATEGORY:
                    updated_entry = {
                        'description': row['Description'],
                        'power': row['Power'],
                        'speedup_minutes': row['Speed-up Minutes'],
                        'points_per_power': row['Points per Power']
                    }
                elif category == TRAINING_CATEGORY:
                    # For training, we need to reconstruct the time parameters
                    # This is a simplified approach - in practice, you might want to store time separately
                    updated_entry = {
                        'description': row['Description'],
                        'days': 0,  # Would need to be calculated from speedup_minutes
                        'hours': 0,
                        'minutes': 0,
                        'seconds': 0,
                        'troops_per_batch': 426,  # Would need to be stored separately
                        'points_per_troop': 830.0  # Would need to be stored separately
                    }
                
                # Update the entry
                success, message = session_manager.update_entry(category, entry_id, updated_entry)
                if not success:
                    st.error(f"Failed to update entry {entry_id}: {message}")

def render_hall_of_chiefs_tab() -> None:
    """Render the Hall of Chiefs Points Efficiency tab."""
    st.header("Hall of Chiefs Points Efficiency")
    st.caption("Compare points gained from Construction, Research, and Training activities relative to speed-up minutes spent.")
    
    # Get session manager
    session_manager = get_session_manager()
    
    # Render sidebar sections
    render_construction_sidebar()
    render_research_sidebar()
    render_training_sidebar()
    
    # Get all entries
    all_entries = session_manager.get_all_entries()
    construction_entries = all_entries[CONSTRUCTION_CATEGORY]
    research_entries = all_entries[RESEARCH_CATEGORY]
    training_entries = all_entries[TRAINING_CATEGORY]
    
    # Check for invalid training entries and show warning
    invalid_training_entries = []
    for entry in training_entries:
        base_training_time = (entry['days'] * 24 * 60) + (entry['hours'] * 60) + entry['minutes'] + (entry['seconds'] / 60)
        if base_training_time <= 0:
            invalid_training_entries.append(entry.get('description', 'Unknown'))
    
    if invalid_training_entries:
        st.warning(
            f"⚠️ **Invalid Training Entries Detected**: The following training entries have zero or invalid training time and will show zero points: {', '.join(invalid_training_entries)}. "
            "Please edit these entries to include valid training times."
        )
    
    # Create efficiency DataFrame
    df = create_efficiency_dataframe(construction_entries, research_entries, training_entries)
    
    # Calculate summary metrics
    summary = calculate_summary_metrics(df)
    
    # Remove All Entries button with proper confirmation dialog
    if not df.empty:
        st.subheader("Manage Entries")
        col1, col2 = st.columns([1, 3])
        with col1:
            if not session_manager.get_clear_all_confirmation():
                if st.button(
                    "🗑️ Remove All Entries",
                    type="primary",
                    help="Clear all entries from all categories"
                ):
                    session_manager.set_clear_all_confirmation(True)
                    st.experimental_rerun()
            else:
                # Show confirmation dialog
                st.warning("Are you sure you want to remove all entries?")
                col_confirm1, col_confirm2 = st.columns(2)
                with col_confirm1:
                    if st.button("Yes, Remove All", type="primary"):
                        success, message = session_manager.delete_all_entries()
                        session_manager.set_clear_all_confirmation(False)
                        if success:
                            st.success(message)
                        else:
                            st.error(f"Failed to remove entries: {message}")
                        st.experimental_rerun()
                with col_confirm2:
                    if st.button("Cancel"):
                        session_manager.set_clear_all_confirmation(False)
                        st.info("Operation cancelled.")
                        st.experimental_rerun()
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
    
    # Display category-specific tables with data editor
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
            
            # Display category table with data editor
            display_df = category_df.drop(['Activity Type', 'id'], axis=1, errors='ignore')
            
            # Use data editor for inline editing
            edited_df = st.experimental_data_editor(
                display_df,
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic"
            )
            
            # Handle changes from data editor
            if edited_df is not None and not edited_df.equals(display_df):
                handle_data_editor_changes(category_df, category.lower())
                st.success("Changes saved successfully!")
                st.experimental_rerun()
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