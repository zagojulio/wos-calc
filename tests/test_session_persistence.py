"""
Tests for session state persistence functionality.
"""

import pytest
import streamlit as st
from unittest.mock import Mock, patch, MagicMock
from utils.session_manager import init_session_state, get_speedup_inventory, update_speedup_inventory
from features.speedup_inventory import render_speedup_inventory_sidebar

class MockSessionState:
    """Mock session state that behaves more like the real Streamlit session state."""
    
    def __init__(self):
        super().__setattr__('_data', {
            'speedup_inventory': {
                'general': 18000.0,  # Safe default: 18k general speedups
                'construction': 0.0,
                'training': 1515.0,  # Safe default: 1515 training speedups
                'research': 0.0
            },
            'hall_of_chiefs_construction_entries': [],
            'hall_of_chiefs_research_entries': [],
            'clear_construction_inputs': False,
            'clear_research_inputs': False
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
    mock_session_state['speedup_inventory'] = {
        'general': 25000.0,
        'construction': 1500.0,
        'training': 2000.0,
        'research': 800.0
    }
    mock_session_state['speedup_general'] = 25000.0
    mock_session_state['speedup_construction'] = 1500.0
    mock_session_state['speedup_training'] = 2000.0
    mock_session_state['speedup_research'] = 800.0
    
    # Initialize session state
    init_session_state()
    
    # Verify that existing values were not overwritten
    assert mock_session_state['speedup_inventory']['general'] == 25000.0
    assert mock_session_state['speedup_inventory']['construction'] == 1500.0
    assert mock_session_state['speedup_inventory']['training'] == 2000.0
    assert mock_session_state['speedup_inventory']['research'] == 800.0

def test_session_state_initialization_sets_defaults_when_empty(mock_session_state):
    """Test that session state initialization sets safe defaults when values don't exist."""
    # Initialize session state (empty)
    init_session_state()
    
    # Verify that safe defaults were set
    assert 'speedup_inventory' in mock_session_state
    assert mock_session_state['speedup_inventory']['general'] == 18000.0  # Safe default
    assert mock_session_state['speedup_inventory']['construction'] == 0.0
    assert mock_session_state['speedup_inventory']['training'] == 1515.0  # Safe default
    assert mock_session_state['speedup_inventory']['research'] == 0.0

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
    mock_session_state['speedup_general'] = 22000.0
    mock_session_state['speedup_construction'] = 1000.0
    mock_session_state['speedup_training'] = 1600.0
    mock_session_state['speedup_research'] = 700.0
    
    # Mock the widgets
    with patch('streamlit.number_input') as mock_number_input:
        mock_number_input.side_effect = [
            # Speed-up widgets
            mock_session_state['speedup_general'],
            mock_session_state['speedup_construction'],
            mock_session_state['speedup_training'],
            mock_session_state['speedup_research']
        ]
        
        # Render speedup sidebar
        speedup_result = render_speedup_inventory_sidebar()
    
    # Verify that the results reflect the widget values
    assert speedup_result['general'] == 22000.0
    assert speedup_result['training'] == 1600.0
    
    # Verify that session state data was updated
    assert mock_session_state['speedup_inventory']['general'] == 22000.0
    assert mock_session_state['speedup_inventory']['construction'] == 1000.0
    assert mock_session_state['speedup_inventory']['training'] == 1600.0
    assert mock_session_state['speedup_inventory']['research'] == 700.0

def test_persistence_across_multiple_initializations(mock_session_state):
    """Test that session state persists correctly across multiple initializations."""
    # Initialize session state
    init_session_state()
    
    # Set some values
    mock_session_state['speedup_inventory']['general'] = 30000.0
    mock_session_state['speedup_inventory']['training'] = 2500.0
    
    # Initialize again (simulating page refresh)
    init_session_state()
    
    # Verify that values persisted
    assert mock_session_state['speedup_inventory']['general'] == 30000.0
    assert mock_session_state['speedup_inventory']['training'] == 2500.0

def test_get_speedup_inventory_returns_current_state(mock_session_state):
    """Test that get_speedup_inventory returns the current session state."""
    # Initialize session state
    init_session_state()
    
    # Modify the inventory
    mock_session_state['speedup_inventory']['general'] = 50000.0
    
    # Get the inventory
    inventory = get_speedup_inventory()
    
    # Verify it returns the current state
    assert inventory['general'] == 50000.0
    assert inventory['training'] == 1515.0  # Default value

def test_update_speedup_inventory_updates_session_state(mock_session_state):
    """Test that update_speedup_inventory correctly updates session state."""
    # Initialize session state
    init_session_state()
    
    # Update inventory
    new_inventory = {
        'general': 40000.0,
        'construction': 2000.0,
        'training': 3000.0,
        'research': 1000.0
    }
    update_speedup_inventory(new_inventory)
    
    # Verify session state was updated
    assert mock_session_state['speedup_inventory']['general'] == 40000.0
    assert mock_session_state['speedup_inventory']['construction'] == 2000.0
    assert mock_session_state['speedup_inventory']['training'] == 3000.0
    assert mock_session_state['speedup_inventory']['research'] == 1000.0 