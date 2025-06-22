"""
Tests for session state persistence functionality.
"""

import pytest
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
from utils.session_manager import init_session_state, get_training_params, get_speedup_inventory
from features.training_manager import render_training_sidebar
from features.speedup_inventory import render_speedup_inventory_sidebar

class MockSessionState:
    """Mock session state that behaves more like the real Streamlit session state."""
    
    def __init__(self):
        super().__setattr__('_data', {
            'training_params': {
                'days': 0,
                'hours': 0,
                'minutes': 0,
                'seconds': 0,
                'troops_per_batch': 0,
                'points_per_troop': 0.0
            },
            'speedup_inventory': {
                'general': 0.0,
                'construction': 0.0,
                'training': 0.0,
                'research': 0.0
            }
        })
    
    def __contains__(self, key):
        return key in self._data
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def update(self, data):
        self._data.update(data)
    
    def __getattr__(self, key):
        if key == '_data':
            return super().__getattribute__('_data')
        try:
            return self._data[key]
        except KeyError:
            raise AttributeError(f"MockSessionState has no attribute '{key}'")
    
    def __setattr__(self, key, value):
        if key == '_data':
            super().__setattr__(key, value)
        else:
            self._data[key] = value

@pytest.fixture
def mock_session_state():
    """Mock session state for testing."""
    session_state = MockSessionState()
    
    with patch('streamlit.session_state', session_state):
        yield session_state

def test_session_state_initialization_preserves_existing_values(mock_session_state):
    """Test that session state initialization doesn't overwrite existing values."""
    # Set up existing values in session state
    mock_session_state['training_params'] = {
        'days': 5,
        'hours': 10,
        'minutes': 30,
        'seconds': 15,
        'troops_per_batch': 500,
        'points_per_troop': 1000.0
    }
    mock_session_state['speedup_inventory'] = {
        'general': 25000.0,
        'construction': 1500.0,
        'training': 2000.0,
        'research': 800.0
    }
    mock_session_state['days'] = 5
    mock_session_state['hours'] = 10
    mock_session_state['minutes'] = 30
    mock_session_state['seconds'] = 15
    mock_session_state['troops_per_batch'] = 500
    mock_session_state['points_per_troop'] = 1000.0
    mock_session_state['speedup_general'] = 25000.0
    mock_session_state['speedup_construction'] = 1500.0
    mock_session_state['speedup_training'] = 2000.0
    mock_session_state['speedup_research'] = 800.0
    
    # Initialize session state
    init_session_state()
    
    # Verify that existing values were not overwritten
    assert mock_session_state['training_params']['days'] == 5
    assert mock_session_state['training_params']['hours'] == 10
    assert mock_session_state['training_params']['minutes'] == 30
    assert mock_session_state['training_params']['seconds'] == 15
    assert mock_session_state['training_params']['troops_per_batch'] == 500
    assert mock_session_state['training_params']['points_per_troop'] == 1000.0
    
    assert mock_session_state['speedup_inventory']['general'] == 25000.0
    assert mock_session_state['speedup_inventory']['construction'] == 1500.0
    assert mock_session_state['speedup_inventory']['training'] == 2000.0
    assert mock_session_state['speedup_inventory']['research'] == 800.0

def test_session_state_initialization_sets_defaults_when_empty(mock_session_state):
    """Test that session state initialization sets defaults when values don't exist."""
    # Initialize session state (empty)
    init_session_state()
    
    # Verify that empty defaults were set
    assert 'training_params' in mock_session_state
    assert mock_session_state['training_params']['days'] == 0
    assert mock_session_state['training_params']['hours'] == 0
    assert mock_session_state['training_params']['minutes'] == 0
    assert mock_session_state['training_params']['seconds'] == 0
    assert mock_session_state['training_params']['troops_per_batch'] == 0
    assert mock_session_state['training_params']['points_per_troop'] == 0.0
    
    assert 'speedup_inventory' in mock_session_state
    assert mock_session_state['speedup_inventory']['general'] == 0.0
    assert mock_session_state['speedup_inventory']['construction'] == 0.0
    assert mock_session_state['speedup_inventory']['training'] == 0.0
    assert mock_session_state['speedup_inventory']['research'] == 0.0

def test_training_sidebar_persistence(mock_session_state):
    """Test that training sidebar values persist correctly."""
    # Initialize session state
    init_session_state()
    
    # Set up widget values
    mock_session_state['days'] = 2
    mock_session_state['hours'] = 6
    mock_session_state['minutes'] = 30
    mock_session_state['seconds'] = 45
    mock_session_state['troops_per_batch'] = 300
    mock_session_state['points_per_troop'] = 750.0
    
    # Mock the number_input widgets to return the session state values
    with patch('streamlit.number_input') as mock_number_input:
        mock_number_input.side_effect = [
            mock_session_state['days'],
            mock_session_state['minutes'],
            mock_session_state['hours'],
            mock_session_state['seconds'],
            mock_session_state['troops_per_batch'],
            mock_session_state['points_per_troop']
        ]
        
        # Render training sidebar
        result = render_training_sidebar()
    
    # Verify that the result contains the expected values
    assert result['troops_per_batch'] == 300
    assert result['points_per_troop'] == 750.0
    assert result['base_training_time'] == (2 * 24 * 60) + (6 * 60) + 30 + (45 / 60)
    
    # Verify that training_params was updated
    assert mock_session_state['training_params']['days'] == 2
    assert mock_session_state['training_params']['hours'] == 6
    assert mock_session_state['training_params']['minutes'] == 30
    assert mock_session_state['training_params']['seconds'] == 45
    assert mock_session_state['training_params']['troops_per_batch'] == 300
    assert mock_session_state['training_params']['points_per_troop'] == 750.0

def test_speedup_inventory_sidebar_persistence(mock_session_state):
    """Test that speed-up inventory sidebar values persist correctly."""
    # Initialize session state
    init_session_state()
    
    # Set up widget values
    mock_session_state['speedup_general'] = 20000.0
    mock_session_state['speedup_construction'] = 1200.0
    mock_session_state['speedup_training'] = 1800.0
    mock_session_state['speedup_research'] = 600.0
    
    # Mock the number_input widgets to return the session state values
    with patch('streamlit.number_input') as mock_number_input:
        mock_number_input.side_effect = [
            mock_session_state['speedup_general'],
            mock_session_state['speedup_construction'],
            mock_session_state['speedup_training'],
            mock_session_state['speedup_research']
        ]
        
        # Render speed-up inventory sidebar
        result = render_speedup_inventory_sidebar()
    
    # Verify that the result contains the expected values
    assert result['general'] == 20000.0
    assert result['construction'] == 1200.0
    assert result['training'] == 1800.0
    assert result['research'] == 600.0
    
    # Verify that speedup_inventory was updated
    assert mock_session_state['speedup_inventory']['general'] == 20000.0
    assert mock_session_state['speedup_inventory']['construction'] == 1200.0
    assert mock_session_state['speedup_inventory']['training'] == 1800.0
    assert mock_session_state['speedup_inventory']['research'] == 600.0

def test_session_state_sync_between_widgets_and_data(mock_session_state):
    """Test that widget values are properly synced with session state data."""
    # Initialize session state
    init_session_state()
    
    # Simulate user changing widget values
    mock_session_state['days'] = 3
    mock_session_state['hours'] = 8
    mock_session_state['minutes'] = 15
    mock_session_state['seconds'] = 30
    mock_session_state['troops_per_batch'] = 400
    mock_session_state['points_per_troop'] = 900.0
    
    mock_session_state['speedup_general'] = 22000.0
    mock_session_state['speedup_construction'] = 1000.0
    mock_session_state['speedup_training'] = 1600.0
    mock_session_state['speedup_research'] = 700.0
    
    # Mock the widgets
    with patch('streamlit.number_input') as mock_number_input:
        mock_number_input.side_effect = [
            # Training widgets
            mock_session_state['days'],
            mock_session_state['minutes'],
            mock_session_state['hours'],
            mock_session_state['seconds'],
            mock_session_state['troops_per_batch'],
            mock_session_state['points_per_troop'],
            # Speed-up widgets
            mock_session_state['speedup_general'],
            mock_session_state['speedup_construction'],
            mock_session_state['speedup_training'],
            mock_session_state['speedup_research']
        ]
        
        # Render both sidebars
        training_result = render_training_sidebar()
        speedup_result = render_speedup_inventory_sidebar()
    
    # Verify that the results reflect the widget values
    assert training_result['troops_per_batch'] == 400
    assert training_result['points_per_troop'] == 900.0
    assert speedup_result['general'] == 22000.0
    assert speedup_result['training'] == 1600.0
    
    # Verify that session state data was updated
    assert mock_session_state['training_params']['days'] == 3
    assert mock_session_state['training_params']['hours'] == 8
    assert mock_session_state['training_params']['minutes'] == 15
    assert mock_session_state['training_params']['seconds'] == 30
    assert mock_session_state['training_params']['troops_per_batch'] == 400
    assert mock_session_state['training_params']['points_per_troop'] == 900.0
    
    assert mock_session_state['speedup_inventory']['general'] == 22000.0
    assert mock_session_state['speedup_inventory']['construction'] == 1000.0
    assert mock_session_state['speedup_inventory']['training'] == 1600.0
    assert mock_session_state['speedup_inventory']['research'] == 700.0

def test_persistence_across_multiple_initializations(mock_session_state):
    """Test that values persist across multiple session state initializations."""
    # First initialization
    init_session_state()
    
    # Simulate user setting values
    mock_session_state['days'] = 1
    mock_session_state['hours'] = 12
    mock_session_state['minutes'] = 45
    mock_session_state['seconds'] = 20
    mock_session_state['troops_per_batch'] = 350
    mock_session_state['points_per_troop'] = 850.0
    
    mock_session_state['speedup_general'] = 18000.0
    mock_session_state['speedup_construction'] = 500.0
    mock_session_state['speedup_training'] = 1200.0
    mock_session_state['speedup_research'] = 300.0
    
    # Second initialization (simulating app reload)
    init_session_state()
    
    # Verify that user values were preserved
    assert mock_session_state['days'] == 1
    assert mock_session_state['hours'] == 12
    assert mock_session_state['minutes'] == 45
    assert mock_session_state['seconds'] == 20
    assert mock_session_state['troops_per_batch'] == 350
    assert mock_session_state['points_per_troop'] == 850.0
    
    assert mock_session_state['speedup_general'] == 18000.0
    assert mock_session_state['speedup_construction'] == 500.0
    assert mock_session_state['speedup_training'] == 1200.0
    assert mock_session_state['speedup_research'] == 300.0 