"""
Tests for the session manager module.
"""

import pytest
from utils.session_manager import (
    init_session_state,
    update_speedup_inventory,
    get_speedup_inventory,
    update_purchases,
    get_purchases,
    load_purchases_to_session
)

def test_init_session_state(mock_session_state):
    """Test session state initialization."""
    init_session_state()
    assert mock_session_state.auto_purchases is None
    assert mock_session_state.manual_purchases is None
    assert mock_session_state.speedup_inventory == {
        'general': 18000.0,
        'construction': 0.0,
        'training': 1515.0,
        'research': 0.0
    }
    # Test Hall of Chiefs session state initialization
    assert mock_session_state.hall_of_chiefs_construction_entries == []
    assert mock_session_state.hall_of_chiefs_research_entries == []
    assert mock_session_state.clear_construction_inputs == False
    assert mock_session_state.clear_research_inputs == False

def test_update_speedup_inventory(mock_session_state):
    """Test updating speed-up inventory."""
    new_inventory = {
        'general': 20000.0,
        'construction': 1000.0,
        'training': 2000.0,
        'research': 500.0
    }
    update_speedup_inventory(new_inventory)
    assert mock_session_state.speedup_inventory == new_inventory

def test_get_speedup_inventory(mock_session_state):
    """Test retrieving speed-up inventory."""
    inventory = get_speedup_inventory()
    assert inventory == mock_session_state.speedup_inventory
    assert inventory['general'] == 18000.0
    assert inventory['training'] == 1515.0

def test_update_purchases(mock_session_state, sample_auto_purchases, sample_manual_purchases):
    """Test updating purchase data."""
    auto_df, _ = sample_auto_purchases
    manual_df, _ = sample_manual_purchases
    
    update_purchases(auto_df, manual_df)
    assert mock_session_state.auto_purchases.equals(auto_df)
    assert mock_session_state.manual_purchases.equals(manual_df)
    
    # Test partial updates
    update_purchases(auto_df)
    assert mock_session_state.auto_purchases.equals(auto_df)
    assert mock_session_state.manual_purchases.equals(manual_df)  # Should remain unchanged

def test_get_purchases(mock_session_state, sample_auto_purchases, sample_manual_purchases):
    """Test retrieving purchase data."""
    auto_df, _ = sample_auto_purchases
    manual_df, _ = sample_manual_purchases
    
    mock_session_state.auto_purchases = auto_df
    mock_session_state.manual_purchases = manual_df
    
    retrieved_auto, retrieved_manual = get_purchases()
    assert retrieved_auto.equals(auto_df)
    assert retrieved_manual.equals(manual_df)

def test_load_purchases_to_session(mock_session_state, sample_auto_purchases, sample_manual_purchases):
    """Test loading purchases into session state."""
    auto_df, auto_path = sample_auto_purchases
    manual_df, manual_path = sample_manual_purchases
    
    loaded_auto, loaded_manual = load_purchases_to_session(auto_path, manual_path)
    assert loaded_auto.equals(auto_df)
    assert loaded_manual.equals(manual_df)
    assert mock_session_state.auto_purchases.equals(auto_df)
    assert mock_session_state.manual_purchases.equals(manual_df) 