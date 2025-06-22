"""
Session Manager for Whiteout Survival Calculator
Handles Streamlit session state management.
"""

import streamlit as st
import json
import os
from datetime import datetime
from typing import Dict, Any

# Constants
SPEEDUP_INVENTORY_FILE = "data/speedup_inventory.json"

def load_speedup_inventory_from_file() -> Dict[str, float]:
    """
    Load speedup inventory from JSON file.
    
    Returns:
        Dict[str, float]: Speedup inventory data
    """
    try:
        if os.path.exists(SPEEDUP_INVENTORY_FILE):
            with open(SPEEDUP_INVENTORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Extract only the speedup categories, ignore metadata
                return {
                    'general': data.get('general', 18000.0),
                    'construction': data.get('construction', 0.0),
                    'training': data.get('training', 1515.0),
                    'research': data.get('research', 0.0)
                }
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        st.warning(f"Could not load speedup inventory from file: {str(e)}. Using defaults.")
    
    # Return default values if file doesn't exist or is invalid
    return {
        'general': 18000.0,
        'construction': 0.0,
        'training': 1515.0,
        'research': 0.0
    }

def save_speedup_inventory_to_file(inventory: Dict[str, float]) -> bool:
    """
    Save speedup inventory to JSON file.
    
    Args:
        inventory (Dict[str, float]): Speedup inventory data to save
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(SPEEDUP_INVENTORY_FILE), exist_ok=True)
        
        # Prepare data with metadata
        data = {
            'general': inventory.get('general', 0.0),
            'construction': inventory.get('construction', 0.0),
            'training': inventory.get('training', 0.0),
            'research': inventory.get('research', 0.0),
            'metadata': {
                'created': datetime.now().isoformat(),
                'version': '1.0',
                'last_updated': datetime.now().isoformat()
            }
        }
        
        # Write to file
        with open(SPEEDUP_INVENTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        st.error(f"Failed to save speedup inventory to file: {str(e)}")
        return False

def init_session_state():
    """Initialize all session state variables."""
    if 'auto_purchases' not in st.session_state:
        st.session_state.auto_purchases = None

    if 'manual_purchases' not in st.session_state:
        st.session_state.manual_purchases = None

    # Initialize speed-up inventory from JSON file
    if 'speedup_inventory' not in st.session_state:
        st.session_state.speedup_inventory = load_speedup_inventory_from_file()

    # Initialize widget keys for speed-up inventory - only set if not already present
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
    
    # Initialize Hall of Chiefs clear input flags
    if 'clear_construction_inputs' not in st.session_state:
        st.session_state.clear_construction_inputs = False
    
    if 'clear_research_inputs' not in st.session_state:
        st.session_state.clear_research_inputs = False

def get_speedup_inventory() -> Dict[str, float]:
    """Get current speed-up inventory from session state."""
    return st.session_state.speedup_inventory

def update_speedup_inventory(inventory: Dict[str, float]):
    """Update speed-up inventory in session state."""
    st.session_state.speedup_inventory.update(inventory)

def persist_speedup_inventory(inventory: Dict[str, float]) -> bool:
    """
    Persist speedup inventory to JSON file.
    
    Args:
        inventory (Dict[str, float]): Speedup inventory to persist
        
    Returns:
        bool: True if successful, False otherwise
    """
    return save_speedup_inventory_to_file(inventory)

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