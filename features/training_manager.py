"""
Training Manager for Whiteout Survival Calculator
Handles training tab functionality and calculations.
"""

import streamlit as st
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)
from utils.session_manager import get_training_params, update_training_params
from features.speedup_inventory import get_speedup_inventory, get_total_speedups_for_category
from typing import Dict, Any, Tuple

def validate_training_inputs(
    days: int,
    hours: int,
    minutes: int,
    seconds: int,
    troops_per_batch: int,
    points_per_troop: float
) -> Tuple[bool, str]:
    """
    Validate training input parameters.
    
    Args:
        days (int): Training days
        hours (int): Training hours
        minutes (int): Training minutes
        seconds (int): Training seconds
        troops_per_batch (int): Troops per batch
        points_per_troop (float): Points per troop
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    # Validate time components
    if days < 0:
        return False, "Days cannot be negative"
    if hours < 0 or hours > 23:
        return False, "Hours must be between 0 and 23"
    if minutes < 0 or minutes > 59:
        return False, "Minutes must be between 0 and 59"
    if seconds < 0 or seconds > 59:
        return False, "Seconds must be between 0 and 59"
    
    # Calculate total training time
    total_time = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)
    if total_time <= 0:
        return False, "Total training time must be greater than 0"
    
    # Validate training configuration
    if troops_per_batch <= 0:
        return False, "Troops per batch must be greater than 0"
    if points_per_troop <= 0:
        return False, "Points per troop must be greater than 0"
    
    return True, ""

def render_training_sidebar():
    """Render training parameters in the sidebar."""
    with st.sidebar.expander("Training Tab Parameters", expanded=True):
        st.subheader("Base Training Time")
        col1, col2 = st.columns(2)
        with col1:
            days = st.number_input(
                "Days",
                min_value=0,
                step=1,
                key="days"
            )
            minutes = st.number_input(
                "Minutes",
                min_value=0,
                max_value=59,
                step=1,
                key="minutes"
            )
        with col2:
            hours = st.number_input(
                "Hours",
                min_value=0,
                max_value=23,
                step=1,
                key="hours"
            )
            seconds = st.number_input(
                "Seconds",
                min_value=0,
                max_value=59,
                step=1,
                key="seconds"
            )
        base_training_time = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)

        st.subheader("Training Configuration")
        troops_per_batch = st.number_input(
            "Troops per Batch",
            min_value=1,
            step=1,
            help="Number of troops trained in each batch",
            key="troops_per_batch"
        )
        points_per_troop = st.number_input(
            "Points per Troop",
            min_value=1.0,
            step=1.0,
            help="Base points earned per troop",
            key="points_per_troop"
        )

        # Validate inputs
        is_valid, error_message = validate_training_inputs(
            days, hours, minutes, seconds, troops_per_batch, points_per_troop
        )
        
        if not is_valid:
            st.error(f"⚠️ {error_message}")
            st.info("Please correct the input values above to proceed with calculations.")
        else:
            # Show training time summary
            st.success(f"✅ Training time: {days}d {hours}h {minutes}m {seconds}s ({base_training_time:.1f} minutes)")
            st.info(f"Points per batch: {troops_per_batch * points_per_troop:,.0f}")

        # Sync widget values with training_params session state
        update_training_params({
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'troops_per_batch': troops_per_batch,
            'points_per_troop': points_per_troop
        })

        return {
            'base_training_time': base_training_time,
            'troops_per_batch': troops_per_batch,
            'points_per_troop': points_per_troop,
            'is_valid': is_valid
        }

def render_training_analysis(params):
    """Render training analysis results."""
    # Validate that we have valid parameters
    if not params.get('is_valid', False):
        st.warning("⚠️ Please fix the training parameters in the sidebar before viewing analysis.")
        return
    
    # Get speed-up inventory
    inventory = get_speedup_inventory()
    total_training_speedups = get_total_speedups_for_category('training', inventory)
    
    # Additional validation for analysis
    if total_training_speedups < 0:
        st.error("❌ Training speedups cannot be negative")
        return
    if params['base_training_time'] <= 0:
        st.error("❌ Base training time must be greater than 0")
        return
    if params['troops_per_batch'] <= 0:
        st.error("❌ Troops per batch must be greater than 0")
        return
    if params['points_per_troop'] <= 0:
        st.error("❌ Points per troop must be greater than 0")
        return

    try:
        # Calculate initial values
        points_per_batch = params['troops_per_batch'] * params['points_per_troop']
        current_points = 0.0

        # Calculate batches and points
        batches, total_points = calculate_batches_and_points(
            total_training_speedups,
            params['base_training_time'],
            points_per_batch,
            current_points
        )

        # Calculate efficiency metrics
        efficiency = calculate_efficiency_metrics(
            total_training_speedups,
            total_points
        )

        # Calculate remaining speedups
        remaining_speedups = total_training_speedups - (batches * params['base_training_time'])

        # Display results with improved layout
        st.subheader("Training Analysis Results")
        
        # First row of metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Base Training Time", 
                f"{params['base_training_time']:.1f} minutes",
                help="Base training time per batch"
            )
        with col2:
            st.metric(
                "Total Points per Batch", 
                f"{points_per_batch:,.0f}",
                help="Points earned from training one batch of troops"
            )
        with col3:
            st.metric(
                "Total Points Gained with Speedups", 
                f"{total_points:,.0f}",
                help="Total points you can earn using all available speedups"
            )
        
        # Second row of metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Batches Possible", 
                f"{batches:,}",
                help="Number of batches you can train with available speedups"
            )
        with col2:
            st.metric(
                "Total Training Time", 
                f"{batches * params['base_training_time']:,.1f} minutes",
                help="Total time needed to train all possible batches"
            )
        with col3:
            st.metric(
                "Speed-ups Remaining", 
                f"{remaining_speedups:,.0f}",
                help="Speed-up minutes left after training all possible batches"
            )
        
        # Third row - Speed-up breakdown
        st.subheader("Speed-up Allocation")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "General Speed-ups Available",
                f"{inventory.get('general', 0.0):,.0f}",
                help="General purpose speed-ups available"
            )
        with col2:
            st.metric(
                "Training Speed-ups Available",
                f"{inventory.get('training', 0.0):,.0f}",
                help="Training-specific speed-ups available"
            )
        with col3:
            st.metric(
                "Total Training Speed-ups",
                f"{total_training_speedups:,.0f}",
                help="Total speed-ups available for training (general + training)"
            )
        with col4:
            st.metric(
                "Speed-ups Used",
                f"{batches * params['base_training_time']:,.0f}",
                help="Speed-ups used for training"
            )
        
        # Efficiency metrics
        st.subheader("Efficiency Metrics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Points per Minute",
                f"{efficiency['points_per_minute']:.2f}",
                help="Points earned per speed-up minute used"
            )
        with col2:
            st.metric(
                "Minutes per Point",
                f"{efficiency['time_per_point']:.2f}",
                help="Speed-up minutes needed per point earned"
            )
        with col3:
            st.metric(
                "Efficiency Score",
                f"{efficiency['efficiency_score']:.0f}",
                help="Normalized efficiency score (higher is better)"
            )
    
    except ValueError as e:
        st.error(f"❌ Calculation error: {str(e)}")
        st.info("Please check your input values and try again.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.info("Please refresh the page and try again.") 