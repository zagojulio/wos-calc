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

def render_training_sidebar():
    """Render training parameters in the sidebar."""
    with st.sidebar.expander("Training Parameters", expanded=True):
        st.subheader("Speed-up Minutes")
        general_speedups = st.number_input(
            "General Speed-ups",
            min_value=0.0,
            value=get_training_params().get('general_speedups', 18000.0),
            step=100.0,
            help="General purpose speed-up minutes available",
            key="general_speedups"
        )
        training_speedups = st.number_input(
            "Troop Training Speed-ups",
            min_value=0.0,
            value=get_training_params().get('training_speedups', 1515.0),
            step=100.0,
            help="Speed-up minutes specifically for troop training",
            key="training_speedups"
        )
        total_speedups = general_speedups + training_speedups

        st.subheader("Base Training Time")
        col1, col2 = st.columns(2)
        with col1:
            days = st.number_input(
                "Days",
                min_value=0,
                value=get_training_params().get('days', 0),
                step=1,
                key="days"
            )
            minutes = st.number_input(
                "Minutes",
                min_value=0,
                max_value=59,
                value=get_training_params().get('minutes', 50),
                step=1,
                key="minutes"
            )
        with col2:
            hours = st.number_input(
                "Hours",
                min_value=0,
                max_value=23,
                value=get_training_params().get('hours', 4),
                step=1,
                key="hours"
            )
            seconds = st.number_input(
                "Seconds",
                min_value=0,
                max_value=59,
                value=get_training_params().get('seconds', 0),
                step=1,
                key="seconds"
            )
        base_training_time = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)

        st.subheader("Training Configuration")
        troops_per_batch = st.number_input(
            "Troops per Batch",
            min_value=1,
            value=get_training_params().get('troops_per_batch', 426),
            step=1,
            help="Number of troops trained in each batch",
            key="troops_per_batch"
        )
        points_per_troop = st.number_input(
            "Points per Troop",
            min_value=1.0,
            value=get_training_params().get('points_per_troop', 830.0),
            step=1.0,
            help="Base points earned per troop",
            key="points_per_troop"
        )

        # Update session state with new values
        update_training_params({
            'general_speedups': general_speedups,
            'training_speedups': training_speedups,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'troops_per_batch': troops_per_batch,
            'points_per_troop': points_per_troop
        })

        return {
            'general_speedups': general_speedups,
            'training_speedups': training_speedups,
            'base_training_time': base_training_time,
            'troops_per_batch': troops_per_batch,
            'points_per_troop': points_per_troop
        }

def render_training_analysis(params):
    """Render training analysis results."""
    # Validate input parameters
    if params['general_speedups'] < 0:
        raise ValueError("General speedups cannot be negative")
    if params['training_speedups'] < 0:
        raise ValueError("Training speedups cannot be negative")
    if params['base_training_time'] < 0:
        raise ValueError("Base training time cannot be negative")
    if params['troops_per_batch'] < 0:
        raise ValueError("Troops per batch cannot be negative")
    if params['points_per_troop'] < 0:
        raise ValueError("Points per troop cannot be negative")

    # Calculate initial values
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    total_speedups = params['general_speedups'] + params['training_speedups']
    current_points = 0.0

    # Calculate batches and points
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        params['base_training_time'],
        points_per_batch,
        current_points
    )

    # Calculate efficiency metrics
    efficiency = calculate_efficiency_metrics(
        total_speedups,
        total_points
    )

    # Calculate remaining speedups
    remaining_speedups = total_speedups - (batches * params['base_training_time'])

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