"""
Session Manager for Whiteout Survival Calculator
Handles Streamlit session state management.
"""

import streamlit as st
from typing import Dict, Any

def init_session_state():
    """Initialize all session state variables."""
    if 'auto_purchases' not in st.session_state:
        st.session_state.auto_purchases = None

    if 'manual_purchases' not in st.session_state:
        st.session_state.manual_purchases = None

    # Initialize training parameters - only set defaults if not already present
    if 'training_params' not in st.session_state:
        st.session_state.training_params = {
            'days': 0,
            'hours': 4,
            'minutes': 50,
            'seconds': 0,
            'troops_per_batch': 426,
            'points_per_troop': 830.0
        }

    # Initialize speed-up inventory - only set defaults if not already present
    if 'speedup_inventory' not in st.session_state:
        st.session_state.speedup_inventory = {
            'general': 18000.0,
            'construction': 0.0,
            'training': 1515.0,
            'research': 0.0
        }

    # Initialize widget keys for training parameters - only set defaults if not already present
    if 'days' not in st.session_state:
        st.session_state.days = st.session_state.training_params['days']
    if 'hours' not in st.session_state:
        st.session_state.hours = st.session_state.training_params['hours']
    if 'minutes' not in st.session_state:
        st.session_state.minutes = st.session_state.training_params['minutes']
    if 'seconds' not in st.session_state:
        st.session_state.seconds = st.session_state.training_params['seconds']
    if 'troops_per_batch' not in st.session_state:
        st.session_state.troops_per_batch = st.session_state.training_params['troops_per_batch']
    if 'points_per_troop' not in st.session_state:
        st.session_state.points_per_troop = st.session_state.training_params['points_per_troop']

    # Initialize widget keys for speed-up inventory - only set defaults if not already present
    if 'speedup_general' not in st.session_state:
        st.session_state.speedup_general = st.session_state.speedup_inventory['general']
    if 'speedup_construction' not in st.session_state:
        st.session_state.speedup_construction = st.session_state.speedup_inventory['construction']
    if 'speedup_training' not in st.session_state:
        st.session_state.speedup_training = st.session_state.speedup_inventory['training']
    if 'speedup_research' not in st.session_state:
        st.session_state.speedup_research = st.session_state.speedup_inventory['research']

    # Initialize Hall of Chiefs session state
    if 'hall_of_chiefs_construction_entries' not in st.session_state:
        st.session_state.hall_of_chiefs_construction_entries = []
    
    if 'hall_of_chiefs_research_entries' not in st.session_state:
        st.session_state.hall_of_chiefs_research_entries = []

def update_training_params(params: Dict[str, Any]):
    """Update training parameters in session state."""
    st.session_state.training_params.update(params)

def get_training_params() -> Dict[str, Any]:
    """Get current training parameters from session state."""
    return st.session_state.training_params

def update_speedup_inventory(inventory: Dict[str, float]):
    """Update speed-up inventory in session state."""
    st.session_state.speedup_inventory.update(inventory)

def get_speedup_inventory() -> Dict[str, float]:
    """Get current speed-up inventory from session state."""
    return st.session_state.speedup_inventory

def update_purchases(auto_purchases=None, manual_purchases=None):
    """Update purchase data in session state."""
    if auto_purchases is not None:
        st.session_state.auto_purchases = auto_purchases
    if manual_purchases is not None:
        st.session_state.manual_purchases = manual_purchases

def get_purchases():
    """Get current purchase data from session state."""
    return st.session_state.auto_purchases, st.session_state.manual_purchases

def load_purchases_to_session(auto_path=None, manual_path=None):
    """Load purchases into session state."""
    from features.purchase_manager import load_purchases
    auto_purchases, manual_purchases = load_purchases(auto_path, manual_path)
    update_purchases(auto_purchases, manual_purchases)
    return auto_purchases, manual_purchases 