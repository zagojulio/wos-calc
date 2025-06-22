"""
Tests for the training manager module.
"""

import pytest
from features.training_manager import (
    render_training_sidebar,
    render_training_analysis,
    validate_training_inputs
)
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)
from unittest.mock import patch
from contextlib import contextmanager

def test_validate_training_inputs_valid():
    """Test validation with valid inputs."""
    is_valid, error_message = validate_training_inputs(
        days=0, hours=4, minutes=50, seconds=0,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert is_valid
    assert error_message == ""

def test_validate_training_inputs_invalid_time():
    """Test validation with invalid time inputs."""
    # Test negative days
    is_valid, error_message = validate_training_inputs(
        days=-1, hours=4, minutes=50, seconds=0,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert not is_valid
    assert "Days cannot be negative" in error_message
    
    # Test invalid hours
    is_valid, error_message = validate_training_inputs(
        days=0, hours=24, minutes=50, seconds=0,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert not is_valid
    assert "Hours must be between 0 and 23" in error_message
    
    # Test invalid minutes
    is_valid, error_message = validate_training_inputs(
        days=0, hours=4, minutes=60, seconds=0,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert not is_valid
    assert "Minutes must be between 0 and 59" in error_message
    
    # Test invalid seconds
    is_valid, error_message = validate_training_inputs(
        days=0, hours=4, minutes=50, seconds=60,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert not is_valid
    assert "Seconds must be between 0 and 59" in error_message

def test_validate_training_inputs_zero_time():
    """Test validation with zero total training time."""
    is_valid, error_message = validate_training_inputs(
        days=0, hours=0, minutes=0, seconds=0,
        troops_per_batch=426, points_per_troop=830.0
    )
    assert not is_valid
    assert "Total training time must be greater than 0" in error_message

def test_validate_training_inputs_invalid_config():
    """Test validation with invalid training configuration."""
    # Test zero troops per batch
    is_valid, error_message = validate_training_inputs(
        days=0, hours=4, minutes=50, seconds=0,
        troops_per_batch=0, points_per_troop=830.0
    )
    assert not is_valid
    assert "Troops per batch must be greater than 0" in error_message
    
    # Test zero points per troop
    is_valid, error_message = validate_training_inputs(
        days=0, hours=4, minutes=50, seconds=0,
        troops_per_batch=426, points_per_troop=0.0
    )
    assert not is_valid
    assert "Points per troop must be greater than 0" in error_message

@contextmanager
def dummy_context():
    yield None

def test_render_training_sidebar(mock_session_state):
    """Test rendering training sidebar and parameter updates."""
    # Mock the session state and Streamlit widgets/context managers
    with patch('streamlit.session_state', mock_session_state), \
         patch('streamlit.number_input') as mock_number_input, \
         patch('streamlit.subheader'), \
         patch('streamlit.columns', return_value=[dummy_context(), dummy_context()]), \
         patch('streamlit.sidebar.expander', return_value=dummy_context()), \
         patch('streamlit.error'), \
         patch('streamlit.info'), \
         patch('streamlit.success'):
        
        # Set up mock number_input to return values from session state
        def mock_number_input_side_effect(*args, **kwargs):
            key = kwargs.get('key', '')
            if key == 'days':
                return mock_session_state.training_params['days']
            elif key == 'hours':
                return mock_session_state.training_params['hours']
            elif key == 'minutes':
                return mock_session_state.training_params['minutes']
            elif key == 'seconds':
                return mock_session_state.training_params['seconds']
            elif key == 'troops_per_batch':
                return mock_session_state.training_params['troops_per_batch']
            elif key == 'points_per_troop':
                return mock_session_state.training_params['points_per_troop']
            return 0
        
        mock_number_input.side_effect = mock_number_input_side_effect
        
        params = render_training_sidebar()
        
        # Verify returned parameters
        assert isinstance(params, dict)
        assert all(key in params for key in [
            'base_training_time',
            'troops_per_batch',
            'points_per_troop',
            'is_valid'
        ])
        
        # Verify the parameters match the mock session state values
        assert params['troops_per_batch'] == mock_session_state.training_params['troops_per_batch']
        assert params['points_per_troop'] == mock_session_state.training_params['points_per_troop']
        assert params['is_valid'] == True  # Should be valid with default values

def test_render_training_analysis(mock_session_state):
    """Test rendering training analysis results."""
    # Test with valid parameters
    params = {
        'base_training_time': 290.0,  # 4h 50m
        'troops_per_batch': 426,
        'points_per_troop': 830.0,
        'is_valid': True
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

def test_render_training_analysis_invalid_params(mock_session_state):
    """Test rendering training analysis with invalid parameters."""
    # Test with invalid parameters
    params = {
        'base_training_time': 0.0,  # Invalid: zero time
        'troops_per_batch': 426,
        'points_per_troop': 830.0,
        'is_valid': False
    }
    
    # Should show warning and return early
    render_training_analysis(params)
    # No exception should be raised

def test_total_points_gained_metric(mock_session_state):
    """Test the new 'Total Points Gained with Speedups' metric calculation."""
    params = {
        'base_training_time': 60.0,  # 1 hour
        'troops_per_batch': 100,
        'points_per_troop': 10.0,
        'is_valid': True
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
    # Test with zero values - should be caught by validation
    params = {
        'base_training_time': 0.0,
        'troops_per_batch': 0,
        'points_per_troop': 0.0,
        'is_valid': False
    }

    # Should not raise exception due to validation
    render_training_analysis(params)

    # Test with maximum values
    params = {
        'base_training_time': float('inf'),
        'troops_per_batch': 1000000,
        'points_per_troop': float('inf'),
        'is_valid': True
    }
    
    # Should raise ValueError for infinite values
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

def test_speedup_allocation_display(mock_session_state):
    """Test that speed-up allocation metrics are displayed correctly."""
    params = {
        'base_training_time': 60.0,
        'troops_per_batch': 100,
        'points_per_troop': 10.0,
        'is_valid': True
    }
    
    # The function should run without errors and display speed-up allocation
    render_training_analysis(params)
    # This test verifies the speed-up allocation section works correctly 