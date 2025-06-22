"""
Tests for Hall of Chiefs functionality.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from features.hall_of_chiefs import (
    calculate_construction_points,
    calculate_research_points,
    calculate_training_points,
    create_efficiency_dataframe,
    calculate_summary_metrics
)
from features.hall_of_chiefs_session import get_session_manager
from utils.session_manager import init_session_state

def test_calculate_construction_points():
    """Test construction points calculation."""
    # Test with 30 points per power
    points = calculate_construction_points(1000.0, 30)
    assert points == 30000.0
    
    # Test with 45 points per power
    points = calculate_construction_points(1000.0, 45)
    assert points == 45000.0
    
    # Test with zero power
    points = calculate_construction_points(0.0, 30)
    assert points == 0.0

def test_calculate_research_points():
    """Test research points calculation."""
    # Test with 30 points per power
    points = calculate_research_points(1000.0, 30)
    assert points == 30000.0
    
    # Test with 45 points per power
    points = calculate_research_points(1000.0, 45)
    assert points == 45000.0
    
    # Test with zero power
    points = calculate_research_points(0.0, 30)
    assert points == 0.0

def test_calculate_training_points():
    """Test training points calculation."""
    # Test with valid training parameters
    params = {
        'days': 1,
        'hours': 2,
        'minutes': 30,
        'seconds': 0,
        'troops_per_batch': 100,
        'points_per_troop': 50.0
    }
    
    points, speedups = calculate_training_points(params)
    
    # Calculate expected values
    base_time = (1 * 24 * 60) + (2 * 60) + 30  # 1590 minutes
    expected_points = 100 * 50.0  # 5000 points
    expected_speedups = base_time  # 1590 minutes
    
    assert points == expected_points
    assert speedups == expected_speedups
    
    # Test with zero time
    params_zero = {
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0,
        'troops_per_batch': 100,
        'points_per_troop': 50.0
    }
    
    points, speedups = calculate_training_points(params_zero)
    assert points == 0.0
    assert speedups == 0.0

def test_create_efficiency_dataframe():
    """Test efficiency dataframe creation."""
    construction_entries = [
        {'description': 'Test Construction', 'power': 1000.0, 'speedup_minutes': 500.0, 'points_per_power': 30}
    ]
    research_entries = [
        {'description': 'Test Research', 'power': 800.0, 'speedup_minutes': 400.0, 'points_per_power': 45}
    ]
    training_entries = [
        {
            'description': 'Test Training',
            'days': 1,
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'troops_per_batch': 100,
            'points_per_troop': 50.0
        }
    ]
    
    df = create_efficiency_dataframe(construction_entries, research_entries, training_entries)
    
    assert not df.empty
    assert len(df) == 3
    assert 'Activity Type' in df.columns
    assert 'Description' in df.columns
    assert 'Total Points' in df.columns
    assert 'Speed-up Minutes' in df.columns
    assert 'Efficiency (pts/min)' in df.columns
    
    # Check construction entry
    construction_row = df[df['Activity Type'] == 'Construction'].iloc[0]
    assert construction_row['Description'] == 'Test Construction'
    assert construction_row['Total Points'] == 30000.0
    assert construction_row['Speed-up Minutes'] == 500.0
    assert construction_row['Efficiency (pts/min)'] == 60.0
    
    # Check research entry
    research_row = df[df['Activity Type'] == 'Research'].iloc[0]
    assert research_row['Description'] == 'Test Research'
    assert research_row['Total Points'] == 36000.0
    assert research_row['Speed-up Minutes'] == 400.0
    assert research_row['Efficiency (pts/min)'] == 90.0
    
    # Check training entry
    training_row = df[df['Activity Type'] == 'Training'].iloc[0]
    assert training_row['Description'] == 'Test Training'
    assert training_row['Total Points'] == 5000.0
    assert training_row['Speed-up Minutes'] == 1440.0  # 1 day in minutes
    assert training_row['Efficiency (pts/min)'] == pytest.approx(3.472, rel=1e-3)

def test_calculate_summary_metrics():
    """Test summary metrics calculation."""
    construction_entries = [
        {'description': 'Test Construction', 'power': 1000.0, 'speedup_minutes': 500.0, 'points_per_power': 30}
    ]
    research_entries = [
        {'description': 'Test Research', 'power': 800.0, 'speedup_minutes': 400.0, 'points_per_power': 45}
    ]
    training_entries = [
        {
            'description': 'Test Training',
            'days': 1,
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'troops_per_batch': 100,
            'points_per_troop': 50.0
        }
    ]
    
    df = create_efficiency_dataframe(construction_entries, research_entries, training_entries)
    summary = calculate_summary_metrics(df)
    
    assert 'total_points_by_type' in summary
    assert 'total_speedups_by_type' in summary
    assert 'avg_efficiency_by_type' in summary
    
    assert summary['total_points_by_type']['Construction'] == 30000.0
    assert summary['total_points_by_type']['Research'] == 36000.0
    assert summary['total_points_by_type']['Training'] == 5000.0
    
    assert summary['total_speedups_by_type']['Construction'] == 500.0
    assert summary['total_speedups_by_type']['Research'] == 400.0
    assert summary['total_speedups_by_type']['Training'] == 1440.0

def test_training_sidebar_widgets_no_value_parameter():
    """Test that training sidebar widgets don't have explicit value parameters that cause Streamlit warnings."""
    from features.hall_of_chiefs import render_training_sidebar
    
    # Mock session state
    mock_session_state = {
        'new_training_description': '',
        'new_training_days': 0,
        'new_training_hours': 0,
        'new_training_minutes': 0,
        'new_training_seconds': 0,
        'new_training_troops_per_batch': 426,
        'new_training_points_per_troop': 830.0
    }
    
    with patch('streamlit.session_state', mock_session_state), \
         patch('streamlit.number_input') as mock_number_input, \
         patch('streamlit.text_input') as mock_text_input, \
         patch('streamlit.button') as mock_button, \
         patch('streamlit.columns') as mock_columns, \
         patch('streamlit.write'), \
         patch('streamlit.sidebar.expander') as mock_expander, \
         patch('streamlit.subheader'), \
         patch('streamlit.success'), \
         patch('streamlit.error'), \
         patch('streamlit.info'), \
         patch('streamlit.experimental_rerun'):
        
        # Mock columns to return context managers
        def mock_columns_side_effect(n):
            return [Mock() for _ in range(n)]
        mock_columns.side_effect = mock_columns_side_effect
        
        # Mock expander to return context manager
        mock_expander.return_value.__enter__ = Mock()
        mock_expander.return_value.__exit__ = Mock()
        
        # Mock number_input to return values from session state
        def mock_number_input_side_effect(*args, **kwargs):
            key = kwargs.get('key', '')
            if 'days' in key:
                return mock_session_state['new_training_days']
            elif 'hours' in key:
                return mock_session_state['new_training_hours']
            elif 'minutes' in key:
                return mock_session_state['new_training_minutes']
            elif 'seconds' in key:
                return mock_session_state['new_training_seconds']
            elif 'troops_per_batch' in key:
                return mock_session_state['new_training_troops_per_batch']
            elif 'points_per_troop' in key:
                return mock_session_state['new_training_points_per_troop']
            return 0
        
        mock_number_input.side_effect = mock_number_input_side_effect
        
        # Mock text_input
        mock_text_input.return_value = mock_session_state['new_training_description']
        
        # Mock button
        mock_button.return_value = False
        
        # Call the function
        render_training_sidebar()
        
        # Verify that number_input was called without explicit value parameters
        # (only key parameter should be used for session state binding)
        for call in mock_number_input.call_args_list:
            args, kwargs = call
            # Check that no explicit 'value' parameter was passed
            assert 'value' not in kwargs, f"Widget {kwargs.get('key', 'unknown')} has explicit value parameter"
            
            # Verify that key parameter is present for session state binding
            assert 'key' in kwargs, f"Widget missing key parameter for session state binding"

def test_speedup_visualization_displays_correct_data():
    """Test that speed-up visualization displays correct data from session state."""
    from features.hall_of_chiefs import render_hall_of_chiefs_tab
    
    # Mock session state with speedup inventory
    mock_session_state = {
        'speedup_inventory': {
            'general': 18000.0,
            'construction': 1200.0,
            'training': 1515.0,
            'research': 800.0
        }
    }
    
    # Mock all the necessary functions
    patches = [
        patch('streamlit.session_state', mock_session_state),
        patch('streamlit.header'),
        patch('streamlit.caption'),
        patch('streamlit.subheader'),
        patch('streamlit.metric'),
        patch('streamlit.progress'),
        patch('streamlit.divider'),
        patch('streamlit.columns'),
        patch('streamlit.write'),
        patch('streamlit.warning'),
        patch('streamlit.dataframe'),
        patch('streamlit.button'),
        patch('streamlit.info'),
        patch('streamlit.success'),
        patch('streamlit.error'),
        patch('streamlit.experimental_rerun'),
        patch('streamlit.experimental_data_editor'),
        patch('streamlit.download_button'),
        patch('features.hall_of_chiefs.render_construction_sidebar'),
        patch('features.hall_of_chiefs.render_research_sidebar'),
        patch('features.hall_of_chiefs.render_training_sidebar'),
        patch('features.hall_of_chiefs.get_session_manager')
    ]
    
    with patch.multiple('streamlit', 
                       session_state=mock_session_state,
                       header=Mock(),
                       caption=Mock(),
                       subheader=Mock(),
                       metric=Mock(),
                       progress=Mock(),
                       divider=Mock(),
                       columns=Mock(return_value=[Mock() for _ in range(5)]),
                       write=Mock(),
                       warning=Mock(),
                       dataframe=Mock(),
                       button=Mock(),
                       info=Mock(),
                       success=Mock(),
                       error=Mock(),
                       experimental_rerun=Mock(),
                       experimental_data_editor=Mock(),
                       download_button=Mock()), \
         patch.multiple('features.hall_of_chiefs',
                       render_construction_sidebar=Mock(),
                       render_research_sidebar=Mock(),
                       render_training_sidebar=Mock(),
                       get_session_manager=Mock()) as mocks:
        
        # Mock session manager
        mocks['get_session_manager'].return_value = Mock()
        mocks['get_session_manager'].return_value.get_all_entries.return_value = {
            'construction': [],
            'research': [],
            'training': []
        }
        mocks['get_session_manager'].return_value.get_clear_all_confirmation.return_value = False
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify that metric was called for each speed-up category
        metric_calls = mocks['metric'].call_args_list
        
        # Check that we have the expected number of metric calls (5: general, construction, training, research, total)
        assert len(metric_calls) >= 5
        
        # Verify the metric calls contain the correct data
        metric_labels = [call[0][0] for call in metric_calls[:5]]  # First 5 calls
        metric_values = [call[0][1] for call in metric_calls[:5]]
        
        assert "General" in metric_labels
        assert "Construction" in metric_labels
        assert "Training" in metric_labels
        assert "Research" in metric_labels
        assert "Total" in metric_labels
        
        # Check that the values match the session state
        total_expected = sum(mock_session_state['speedup_inventory'].values())
        assert f"{total_expected:,.0f}" in metric_values
        
        # Verify progress bar was called with correct percentage
        progress_calls = mocks['progress'].call_args_list
        if progress_calls:
            progress_call = progress_calls[0]
            args, kwargs = progress_call
            # Check that progress is called with a percentage between 0 and 1
            assert 0 <= args[0] <= 1
            # Check that the text contains the total speedup minutes
            assert f"{total_expected:,.0f}" in args[1]

def test_speedup_visualization_updates_with_session_state():
    """Test that speed-up visualization updates when session state changes."""
    from features.hall_of_chiefs import render_hall_of_chiefs_tab
    
    # Mock session state with different speedup inventory
    mock_session_state = {
        'speedup_inventory': {
            'general': 5000.0,
            'construction': 2000.0,
            'training': 3000.0,
            'research': 1000.0
        }
    }
    
    with patch.multiple('streamlit', 
                       session_state=mock_session_state,
                       header=Mock(),
                       caption=Mock(),
                       subheader=Mock(),
                       metric=Mock(),
                       progress=Mock(),
                       divider=Mock(),
                       columns=Mock(return_value=[Mock() for _ in range(5)]),
                       write=Mock(),
                       warning=Mock(),
                       dataframe=Mock(),
                       button=Mock(),
                       info=Mock(),
                       success=Mock(),
                       error=Mock(),
                       experimental_rerun=Mock(),
                       experimental_data_editor=Mock(),
                       download_button=Mock()), \
         patch.multiple('features.hall_of_chiefs',
                       render_construction_sidebar=Mock(),
                       render_research_sidebar=Mock(),
                       render_training_sidebar=Mock(),
                       get_session_manager=Mock()) as mocks:
        
        # Mock session manager
        mocks['get_session_manager'].return_value = Mock()
        mocks['get_session_manager'].return_value.get_all_entries.return_value = {
            'construction': [],
            'research': [],
            'training': []
        }
        mocks['get_session_manager'].return_value.get_clear_all_confirmation.return_value = False
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify that metric was called with the updated values
        metric_calls = mocks['metric'].call_args_list
        
        # Check that the values match the updated session state
        total_expected = sum(mock_session_state['speedup_inventory'].values())  # 11000.0
        metric_values = [call[0][1] for call in metric_calls[:5]]
        
        assert f"{total_expected:,.0f}" in metric_values  # "11,000"
        
        # Verify progress bar shows correct percentage
        progress_calls = mocks['progress'].call_args_list
        if progress_calls:
            progress_call = progress_calls[0]
            args, kwargs = progress_call
            # With 11000 minutes and max_display of 50000, percentage should be 22%
            expected_percentage = 11000.0 / 50000.0
            assert abs(args[0] - expected_percentage) < 0.01 