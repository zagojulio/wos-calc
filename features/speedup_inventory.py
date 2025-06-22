"""
Speed-up Inventory Manager for Whiteout Survival Calculator
Handles speed-up inventory sidebar functionality and calculations.
"""

import streamlit as st
from utils.session_manager import get_speedup_inventory, update_speedup_inventory
from typing import Dict, Any

def render_speedup_inventory_sidebar() -> Dict[str, float]:
    """
    Render speed-up inventory section in the sidebar.
    
    Returns:
        Dict[str, float]: Current speed-up inventory values
    """
    with st.sidebar.expander("Speed-up Minutes Inventory", expanded=True):
        st.subheader("Available Speed-ups by Category")
        
        # General speed-ups (usable for any category)
        general_speedups = st.number_input(
            "General",
            min_value=0.0,
            step=100.0,
            help="General purpose speed-up minutes (usable for any category)",
            key="speedup_general"
        )
        
        # Construction speed-ups (specific to construction only)
        construction_speedups = st.number_input(
            "Construction",
            min_value=0.0,
            step=100.0,
            help="Speed-up minutes specifically for construction activities",
            key="speedup_construction"
        )
        
        # Training speed-ups (specific to training only)
        training_speedups = st.number_input(
            "Training",
            min_value=0.0,
            step=100.0,
            help="Speed-up minutes specifically for troop training",
            key="speedup_training"
        )
        
        # Research speed-ups (specific to research only)
        research_speedups = st.number_input(
            "Research",
            min_value=0.0,
            step=100.0,
            help="Speed-up minutes specifically for research activities",
            key="speedup_research"
        )
        
        # Calculate total available speed-ups
        total_speedups = general_speedups + construction_speedups + training_speedups + research_speedups
        
        # Display total
        st.metric(
            "Total Speed-up Minutes",
            f"{total_speedups:,.0f}",
            help="Total speed-up minutes across all categories"
        )
        
        # Sync widget values with speedup_inventory session state
        new_inventory = {
            'general': general_speedups,
            'construction': construction_speedups,
            'training': training_speedups,
            'research': research_speedups
        }
        update_speedup_inventory(new_inventory)
        
        return new_inventory

def calculate_available_speedups_for_category(
    category: str,
    required_minutes: float,
    inventory: Dict[str, float]
) -> Dict[str, float]:
    """
    Calculate available speed-ups for a specific category.
    
    Args:
        category (str): The category ('construction', 'training', 'research')
        required_minutes (float): Minutes needed for the activity
        inventory (Dict[str, float]): Current speed-up inventory
    
    Returns:
        Dict[str, float]: Dictionary with allocated speed-ups and remaining inventory
    """
    if category not in ['construction', 'training', 'research']:
        raise ValueError(f"Invalid category: {category}")
    
    # Start with category-specific speed-ups
    category_speedups = inventory.get(category, 0.0)
    general_speedups = inventory.get('general', 0.0)
    
    # Calculate how much we can use from each pool
    category_used = min(category_speedups, required_minutes)
    remaining_after_category = required_minutes - category_used
    
    # Use general speed-ups for the remainder
    general_used = min(general_speedups, remaining_after_category)
    
    # Calculate remaining inventory
    remaining_category = category_speedups - category_used
    remaining_general = general_speedups - general_used
    
    return {
        'category_used': category_used,
        'general_used': general_used,
        'total_used': category_used + general_used,
        'remaining_category': remaining_category,
        'remaining_general': remaining_general,
        'can_complete': (category_used + general_used) >= required_minutes
    }

def get_total_speedups_for_category(
    category: str,
    inventory: Dict[str, float]
) -> float:
    """
    Get total available speed-ups for a specific category.
    
    Args:
        category (str): The category ('construction', 'training', 'research')
        inventory (Dict[str, float]): Current speed-up inventory
    
    Returns:
        float: Total available speed-ups for the category
    """
    if category not in ['construction', 'training', 'research']:
        raise ValueError(f"Invalid category: {category}")
    
    category_speedups = inventory.get(category, 0.0)
    general_speedups = inventory.get('general', 0.0)
    
    return category_speedups + general_speedups 