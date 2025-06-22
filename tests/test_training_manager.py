"""
Tests for the training manager module.
"""

import pytest
from features.training_manager import (
    render_training_sidebar,
    render_training_analysis
)
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)

def test_render_training_sidebar(mock_session_state):
    """Test rendering training sidebar and parameter updates."""
    params = render_training_sidebar()
    
    # Verify returned parameters
    assert isinstance(params, dict)
    assert all(key in params for key in [
        'base_training_time',
        'troops_per_batch',
        'points_per_troop'
    ])
    
    # Verify session state was updated
    assert mock_session_state.training_params['troops_per_batch'] == params['troops_per_batch']
    assert mock_session_state.training_params['points_per_troop'] == params['points_per_troop']
    assert mock_session_state.training_params['days'] == 0
    assert mock_session_state.training_params['hours'] == 4

def test_render_training_analysis(mock_session_state):
    """Test rendering training analysis results."""
    # Test with default parameters
    params = {
        'base_training_time': 290.0,  # 4h 50m
        'troops_per_batch': 426,
        'points_per_troop': 830.0
    }
    
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    total_speedups = mock_session_state.speedup_inventory['general'] + mock_session_state.speedup_inventory['training']
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        params['base_training_time'],
        points_per_batch,
        0.0
    )
    assert isinstance(batches, int)
    assert isinstance(total_points, float)
    
    # Calculate efficiency metrics
    efficiency = calculate_efficiency_metrics(
        total_speedups,
        total_points
    )
    assert isinstance(efficiency, dict)
    assert 'points_per_minute' in efficiency
    assert 'time_per_point' in efficiency

def test_total_points_gained_metric(mock_session_state):
    """Test the new 'Total Points Gained with Speedups' metric calculation."""
    params = {
        'base_training_time': 60.0,  # 1 hour
        'troops_per_batch': 100,
        'points_per_troop': 10.0
    }
    
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    total_speedups = mock_session_state.speedup_inventory['general'] + mock_session_state.speedup_inventory['training']
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        params['base_training_time'],
        points_per_batch,
        0.0
    )
    
    # Verify the calculation is correct
    expected_batches = int(total_speedups // params['base_training_time'])
    expected_total_points = expected_batches * points_per_batch
    assert total_points == expected_total_points

def test_edge_cases(mock_session_state):
    """Test edge cases in training calculations."""
    # Test with zero values
    params = {
        'base_training_time': 0.0,
        'troops_per_batch': 0,
        'points_per_troop': 0.0
    }

    # Test that zero base time raises ValueError
    with pytest.raises(ValueError):
        points_per_batch = params['troops_per_batch'] * params['points_per_troop']
        calculate_batches_and_points(
            mock_session_state.speedup_inventory['general'] + mock_session_state.speedup_inventory['training'],
            params['base_training_time'],
            points_per_batch,
            0.0
        )

    # Test with maximum values
    params = {
        'base_training_time': float('inf'),
        'troops_per_batch': 1000000,
        'points_per_troop': float('inf')
    }
    
    with pytest.raises(ValueError):
        points_per_batch = params['troops_per_batch'] * params['points_per_troop']
        calculate_batches_and_points(
            mock_session_state.speedup_inventory['general'] + mock_session_state.speedup_inventory['training'],
            params['base_training_time'],
            points_per_batch,
            0.0
        )

def test_input_validation():
    """Test input validation in training calculations."""
    # Test negative values
    with pytest.raises(ValueError):
        calculate_batches_and_points(-100, 60.0, 1000.0, 0.0)
    
    # Test invalid speed-up values
    with pytest.raises(ValueError):
        calculate_batches_and_points(
            total_speedups=100.0,
            base_training_time=-10.0,
            points_per_batch=100.0,
            current_points=0.0
        )

def test_metric_layout_improvements(mock_session_state):
    """Test that the new layout works correctly."""
    params = {
        'base_training_time': 60.0,
        'troops_per_batch': 100,
        'points_per_troop': 10.0
    }
    
    # The function should run without errors with the new layout
    render_training_analysis(params)
    # This test verifies the new layout doesn't cause issues

def test_speedup_allocation_display(mock_session_state):
    """Test that speed-up allocation metrics are displayed correctly."""
    params = {
        'base_training_time': 60.0,
        'troops_per_batch': 100,
        'points_per_troop': 10.0
    }
    
    # The function should run without errors and display speed-up allocation
    render_training_analysis(params)
    # This test verifies the speed-up allocation section works correctly 