"""
Tests for the training manager module.
"""

import pytest
from features.training_manager import (
    render_training_sidebar,
    render_training_analysis
)
from calculations import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)

def test_render_training_sidebar(mock_session_state):
    """Test rendering training sidebar and parameter updates."""
    params = render_training_sidebar()
    
    # Verify returned parameters
    assert isinstance(params, dict)
    assert all(key in params for key in [
        'general_speedups',
        'training_speedups',
        'base_training_time',
        'troops_per_batch',
        'time_reduction_bonus',
        'points_per_troop',
        'target_points'
    ])
    
    # Verify session state was updated
    assert mock_session_state.training_params['general_speedups'] == params['general_speedups']
    assert mock_session_state.training_params['training_speedups'] == params['training_speedups']
    assert mock_session_state.training_params['troops_per_batch'] == params['troops_per_batch']
    assert mock_session_state.training_params['time_reduction_bonus'] == params['time_reduction_bonus'] * 100
    assert mock_session_state.training_params['points_per_troop'] == params['points_per_troop']
    assert mock_session_state.training_params['target_points'] == params['target_points']

def test_render_training_analysis():
    """Test rendering training analysis results."""
    # Test with default parameters
    params = {
        'general_speedups': 18000.0,
        'training_speedups': 1515.0,
        'base_training_time': 290.0,  # 4h 50m
        'troops_per_batch': 426,
        'time_reduction_bonus': 0.2,  # 20%
        'points_per_troop': 830.0,
        'target_points': 10000.0
    }
    
    # Verify calculations
    effective_time = calculate_effective_training_time(
        params['base_training_time'],
        params['time_reduction_bonus']
    )
    assert effective_time == params['base_training_time'] * (1 - params['time_reduction_bonus'])
    
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    total_speedups = params['general_speedups'] + params['training_speedups']
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        effective_time,
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
    
    speedups_needed = calculate_speedups_needed(
        params['target_points'],
        points_per_batch,
        0.0,
        effective_time
    )
    assert speedups_needed >= 0

def test_total_points_gained_metric():
    """Test the new 'Total Points Gained with Speedups' metric calculation."""
    params = {
        'general_speedups': 1000.0,
        'training_speedups': 500.0,
        'base_training_time': 60.0,  # 1 hour
        'troops_per_batch': 100,
        'time_reduction_bonus': 0.1,  # 10%
        'points_per_troop': 10.0,
        'target_points': 5000.0
    }
    
    # Calculate expected total points
    effective_time = calculate_effective_training_time(
        params['base_training_time'],
        params['time_reduction_bonus']
    )
    points_per_batch = params['troops_per_batch'] * params['points_per_troop']
    total_speedups = params['general_speedups'] + params['training_speedups']
    batches, total_points = calculate_batches_and_points(
        total_speedups,
        effective_time,
        points_per_batch,
        0.0
    )
    
    # Verify the calculation is correct
    expected_batches = int(total_speedups // effective_time)
    expected_total_points = expected_batches * points_per_batch
    assert total_points == expected_total_points

def test_edge_cases():
    """Test edge cases in training calculations."""
    # Test with zero values
    params = {
        'general_speedups': 0.0,
        'training_speedups': 0.0,
        'base_training_time': 0.0,
        'troops_per_batch': 0,
        'time_reduction_bonus': 0.0,
        'points_per_troop': 0.0,
        'target_points': 0.0
    }

    effective_time = calculate_effective_training_time(
        params['base_training_time'],
        params['time_reduction_bonus']
    )
    assert effective_time == 0.0

    # Test that zero effective time raises ValueError
    with pytest.raises(ValueError):
        points_per_batch = params['troops_per_batch'] * params['points_per_troop']
        calculate_batches_and_points(
            params['general_speedups'] + params['training_speedups'],
            effective_time,
            points_per_batch,
            0.0
        )

    # Test with maximum values
    params = {
        'general_speedups': float('inf'),
        'training_speedups': float('inf'),
        'base_training_time': float('inf'),
        'troops_per_batch': 1000000,
        'time_reduction_bonus': 1.0,
        'points_per_troop': float('inf'),
        'target_points': float('inf')
    }
    
    with pytest.raises(ValueError):
        calculate_effective_training_time(
            params['base_training_time'],
            params['time_reduction_bonus']
        )
    
    with pytest.raises(ValueError):
        points_per_batch = params['troops_per_batch'] * params['points_per_troop']
        calculate_batches_and_points(
            params['general_speedups'] + params['training_speedups'],
            60.0,  # Use valid effective time
            points_per_batch,
            0.0
        )

def test_input_validation():
    """Test input validation in training calculations."""
    # Test negative values
    with pytest.raises(ValueError):
        calculate_effective_training_time(-100.0, 0.2)
    
    with pytest.raises(ValueError):
        calculate_batches_and_points(-100, 60.0, 1000.0, 0.0)
    
    # Test invalid bonus percentage
    with pytest.raises(ValueError):
        calculate_effective_training_time(100.0, 1.5)  # 150% reduction
    
    # Test invalid speed-up values
    with pytest.raises(ValueError):
        calculate_speedups_needed(
            target_points=1000.0,
            points_per_batch=100.0,
            current_points=-1000.0,
            effective_training_time=10.0
        )

def test_metric_layout_improvements():
    """Test that the new 3-column layout works correctly."""
    params = {
        'general_speedups': 1000.0,
        'training_speedups': 500.0,
        'base_training_time': 60.0,
        'troops_per_batch': 100,
        'time_reduction_bonus': 0.1,
        'points_per_troop': 10.0,
        'target_points': 5000.0
    }
    
    # The function should run without errors with the new layout
    render_training_analysis(params)
    # This test verifies the new 3-column layout doesn't cause issues 