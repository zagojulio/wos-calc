"""
Tests for the speed-up inventory module.
"""

import pytest
from features.speedup_inventory import (
    render_speedup_inventory_sidebar,
    calculate_available_speedups_for_category,
    get_total_speedups_for_category
)

def test_render_speedup_inventory_sidebar(mock_session_state):
    """Test rendering speed-up inventory sidebar."""
    # Initialize the mock session state with the expected widget values
    mock_session_state['speedup_general'] = 18000.0
    mock_session_state['speedup_construction'] = 0.0
    mock_session_state['speedup_training'] = 1515.0
    mock_session_state['speedup_research'] = 0.0
    
    inventory = render_speedup_inventory_sidebar()
    
    # Verify returned inventory structure
    assert isinstance(inventory, dict)
    assert all(key in inventory for key in ['general', 'construction', 'training', 'research'])
    assert inventory['general'] == 18000.0
    assert inventory['training'] == 1515.0
    assert inventory['construction'] == 0.0
    assert inventory['research'] == 0.0

def test_calculate_available_speedups_for_category_training():
    """Test calculating available speed-ups for training category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    # Test case 1: Use only training speed-ups
    result = calculate_available_speedups_for_category('training', 200.0, inventory)
    assert result['category_used'] == 200.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 200.0
    assert result['remaining_category'] == 100.0
    assert result['remaining_general'] == 1000.0
    assert result['can_complete'] is True
    
    # Test case 2: Use training + general speed-ups
    result = calculate_available_speedups_for_category('training', 500.0, inventory)
    assert result['category_used'] == 300.0
    assert result['general_used'] == 200.0
    assert result['total_used'] == 500.0
    assert result['remaining_category'] == 0.0
    assert result['remaining_general'] == 800.0
    assert result['can_complete'] is True
    
    # Test case 3: Not enough speed-ups
    result = calculate_available_speedups_for_category('training', 1500.0, inventory)
    assert result['category_used'] == 300.0
    assert result['general_used'] == 1000.0
    assert result['total_used'] == 1300.0
    assert result['remaining_category'] == 0.0
    assert result['remaining_general'] == 0.0
    assert result['can_complete'] is False

def test_calculate_available_speedups_for_category_construction():
    """Test calculating available speed-ups for construction category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    result = calculate_available_speedups_for_category('construction', 300.0, inventory)
    assert result['category_used'] == 300.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 300.0
    assert result['remaining_category'] == 200.0
    assert result['remaining_general'] == 1000.0
    assert result['can_complete'] is True

def test_calculate_available_speedups_for_category_research():
    """Test calculating available speed-ups for research category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    result = calculate_available_speedups_for_category('research', 150.0, inventory)
    assert result['category_used'] == 150.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 150.0
    assert result['remaining_category'] == 50.0
    assert result['remaining_general'] == 1000.0
    assert result['can_complete'] is True

def test_calculate_available_speedups_for_category_invalid():
    """Test calculating available speed-ups with invalid category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    with pytest.raises(ValueError, match="Invalid category"):
        calculate_available_speedups_for_category('invalid', 100.0, inventory)

def test_get_total_speedups_for_category():
    """Test getting total speed-ups for a category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    # Test training category
    total_training = get_total_speedups_for_category('training', inventory)
    assert total_training == 1300.0  # 300 + 1000
    
    # Test construction category
    total_construction = get_total_speedups_for_category('construction', inventory)
    assert total_construction == 1500.0  # 500 + 1000
    
    # Test research category
    total_research = get_total_speedups_for_category('research', inventory)
    assert total_research == 1200.0  # 200 + 1000

def test_get_total_speedups_for_category_invalid():
    """Test getting total speed-ups with invalid category."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    with pytest.raises(ValueError, match="Invalid category"):
        get_total_speedups_for_category('invalid', inventory)

def test_calculate_available_speedups_edge_cases():
    """Test edge cases for speed-up calculations."""
    inventory = {
        'general': 0.0,
        'construction': 0.0,
        'training': 0.0,
        'research': 0.0
    }
    
    # Test with zero inventory
    result = calculate_available_speedups_for_category('training', 100.0, inventory)
    assert result['category_used'] == 0.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 0.0
    assert result['can_complete'] is False
    
    # Test with zero required minutes
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    result = calculate_available_speedups_for_category('training', 0.0, inventory)
    assert result['category_used'] == 0.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 0.0
    assert result['can_complete'] is True 