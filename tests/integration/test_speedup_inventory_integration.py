"""
Integration tests for the speed-up inventory system.
"""

import pytest
from features.speedup_inventory import (
    render_speedup_inventory_sidebar,
    calculate_available_speedups_for_category,
    get_total_speedups_for_category
)
from features.training_manager import render_training_sidebar, render_training_analysis
from utils.session_manager import (
    init_session_state,
    get_speedup_inventory,
    update_speedup_inventory,
    get_training_params
)
from calculations import calculate_batches_and_points

def test_speedup_inventory_integration_flow(mock_session_state):
    """Test the complete integration flow of speed-up inventory with training."""
    # Initialize session state
    init_session_state()
    
    # Verify initial state
    inventory = get_speedup_inventory()
    assert inventory['general'] == 18000.0
    assert inventory['training'] == 1515.0
    assert inventory['construction'] == 0.0
    assert inventory['research'] == 0.0
    
    # Test speed-up inventory sidebar rendering
    rendered_inventory = render_speedup_inventory_sidebar()
    assert rendered_inventory == inventory
    
    # Test training sidebar rendering (should not include speed-ups)
    training_params = render_training_sidebar()
    assert 'base_training_time' in training_params
    assert 'troops_per_batch' in training_params
    assert 'points_per_troop' in training_params
    assert 'general_speedups' not in training_params
    assert 'training_speedups' not in training_params
    
    # Test training analysis with speed-up inventory
    render_training_analysis(training_params)
    
    # Verify that training calculations use the speed-up inventory
    total_training_speedups = get_total_speedups_for_category('training', inventory)
    expected_total = inventory['general'] + inventory['training']
    assert total_training_speedups == expected_total

def test_speedup_allocation_logic():
    """Test the speed-up allocation logic for different scenarios."""
    # Scenario 1: Use only category-specific speed-ups
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    result = calculate_available_speedups_for_category('training', 200.0, inventory)
    assert result['category_used'] == 200.0
    assert result['general_used'] == 0.0
    assert result['total_used'] == 200.0
    assert result['can_complete'] is True
    
    # Scenario 2: Use category-specific + general speed-ups
    result = calculate_available_speedups_for_category('training', 500.0, inventory)
    assert result['category_used'] == 300.0
    assert result['general_used'] == 200.0
    assert result['total_used'] == 500.0
    assert result['can_complete'] is True
    
    # Scenario 3: Not enough speed-ups
    result = calculate_available_speedups_for_category('training', 1500.0, inventory)
    assert result['category_used'] == 300.0
    assert result['general_used'] == 1000.0
    assert result['total_used'] == 1300.0
    assert result['can_complete'] is False

def test_session_state_persistence(mock_session_state):
    """Test that speed-up inventory persists correctly in session state."""
    # Initialize session state
    init_session_state()
    
    # Update speed-up inventory
    new_inventory = {
        'general': 20000.0,
        'construction': 1000.0,
        'training': 2000.0,
        'research': 500.0
    }
    update_speedup_inventory(new_inventory)
    
    # Verify the update
    retrieved_inventory = get_speedup_inventory()
    assert retrieved_inventory == new_inventory
    
    # Verify that training calculations use the updated inventory
    total_training_speedups = get_total_speedups_for_category('training', retrieved_inventory)
    expected_total = new_inventory['general'] + new_inventory['training']
    assert total_training_speedups == expected_total

def test_training_calculation_with_speedup_inventory(mock_session_state):
    """Test that training calculations work correctly with the new speed-up inventory."""
    # Initialize session state
    init_session_state()
    
    # Set up training parameters
    training_params = {
        'base_training_time': 60.0,  # 1 hour
        'troops_per_batch': 100,
        'points_per_troop': 10.0
    }
    
    # Get speed-up inventory
    inventory = get_speedup_inventory()
    total_training_speedups = get_total_speedups_for_category('training', inventory)
    
    # Calculate batches and points
    points_per_batch = training_params['troops_per_batch'] * training_params['points_per_troop']
    batches, total_points = calculate_batches_and_points(
        total_training_speedups,
        training_params['base_training_time'],
        points_per_batch,
        0.0
    )
    
    # Verify calculations
    expected_batches = int(total_training_speedups // training_params['base_training_time'])
    expected_total_points = expected_batches * points_per_batch
    
    assert batches == expected_batches
    assert total_points == expected_total_points
    
    # Verify that the calculation uses the correct speed-up allocation
    assert total_training_speedups == inventory['general'] + inventory['training']

def test_multiple_category_speedup_usage():
    """Test that multiple categories can use speed-ups without interference."""
    inventory = {
        'general': 1000.0,
        'construction': 500.0,
        'training': 300.0,
        'research': 200.0
    }
    
    # Test construction usage
    construction_result = calculate_available_speedups_for_category('construction', 400.0, inventory)
    assert construction_result['category_used'] == 400.0
    assert construction_result['general_used'] == 0.0
    assert construction_result['can_complete'] is True
    
    # Test research usage (should not be affected by construction usage)
    research_result = calculate_available_speedups_for_category('research', 150.0, inventory)
    assert research_result['category_used'] == 150.0
    assert research_result['general_used'] == 0.0
    assert research_result['can_complete'] is True
    
    # Test training usage (should not be affected by other categories)
    training_result = calculate_available_speedups_for_category('training', 250.0, inventory)
    assert training_result['category_used'] == 250.0
    assert training_result['general_used'] == 0.0
    assert training_result['can_complete'] is True

def test_general_speedup_priority():
    """Test that general speed-ups are used after category-specific ones."""
    inventory = {
        'general': 1000.0,
        'construction': 100.0,
        'training': 50.0,
        'research': 25.0
    }
    
    # Test that construction uses its own speed-ups first, then general
    result = calculate_available_speedups_for_category('construction', 200.0, inventory)
    assert result['category_used'] == 100.0  # All construction speed-ups used
    assert result['general_used'] == 100.0   # 100 from general
    assert result['total_used'] == 200.0
    assert result['can_complete'] is True
    
    # Verify remaining inventory
    assert result['remaining_category'] == 0.0
    assert result['remaining_general'] == 900.0  # 1000 - 100 used 