"""
Tests for the session manager module.
"""

import pytest
from utils.session_manager import (
    init_session_state,
    update_training_params,
    get_training_params,
    update_purchases,
    get_purchases,
    load_purchases_to_session
)

def test_init_session_state(mock_session_state):
    """Test session state initialization."""
    init_session_state()
    assert mock_session_state.auto_purchases is None
    assert mock_session_state.manual_purchases is None
    assert mock_session_state.training_params == {
        'general_speedups': 18000.0,
        'training_speedups': 1515.0,
        'days': 0,
        'hours': 4,
        'minutes': 50,
        'seconds': 0,
        'troops_per_batch': 426,
        'points_per_troop': 830.0
    }

def test_update_training_params(mock_session_state):
    """Test updating training parameters."""
    new_params = {
        'general_speedups': 20000.0,
        'training_speedups': 2000.0
    }
    update_training_params(new_params)
    assert mock_session_state.training_params['general_speedups'] == 20000.0
    assert mock_session_state.training_params['training_speedups'] == 2000.0
    # Verify other params remain unchanged
    assert mock_session_state.training_params['days'] == 0
    assert mock_session_state.training_params['hours'] == 4

def test_get_training_params(mock_session_state):
    """Test retrieving training parameters."""
    params = get_training_params()
    assert params == mock_session_state.training_params
    assert params['general_speedups'] == 18000.0
    assert params['training_speedups'] == 1515.0

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