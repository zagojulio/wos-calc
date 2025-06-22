"""
Integration tests for Pack Value Comparison tab functionality.
"""

import pytest
import streamlit as st
import pandas as pd
import json
import os
import tempfile
from unittest.mock import patch, MagicMock
from contextlib import contextmanager
from features.pack_value_comparison import (
    render_pack_value_comparison_tab,
    calculate_total_minutes,
    calculate_cost_per_minute,
    load_pack_history,
    save_pack_history
)

# Helper for mocking st.columns
@contextmanager
def dummy_column():
    yield None

def mock_columns(n):
    # n is a list of floats/ints, return a list of context managers
    return [dummy_column() for _ in n]

class MockSessionState:
    """Mock session state that supports both attribute and dict access."""
    
    def __init__(self, **kwargs):
        self._data = kwargs
    
    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")
    
    def __setattr__(self, name, value):
        if name == '_data':
            super().__setattr__(name, value)
        else:
            self._data[name] = value
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __contains__(self, key):
        return key in self._data
    
    def get(self, key, default=None):
        return self._data.get(key, default)

class TestPackValueComparisonIntegration:
    """Integration tests for pack value comparison functionality."""
    
    def setup_method(self):
        """Setup test environment before each test."""
        # Use mkstemp for a safe temp file path
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        self.temp_file_path = path
    
    def teardown_method(self):
        """Cleanup after each test."""
        if os.path.exists(self.temp_file_path):
            os.unlink(self.temp_file_path)
    
    @patch('features.pack_value_comparison.PACKS_JSON_PATH')
    def test_complete_pack_addition_flow(self, mock_path):
        """Test complete flow of adding a pack with new speedup inputs."""
        mock_path.__str__ = lambda: self.temp_file_path
        import features.pack_value_comparison as pvc
        pvc.PACKS_JSON_PATH = self.temp_file_path
        # Ensure the temp file is empty before the test
        with open(self.temp_file_path, 'w') as f:
            f.write('[]')
        
        # Test data
        pack_name = "Test Pack"
        price = 15.0
        hour_speedups = 2
        five_min_speedups = 10
        
        # Calculate expected values
        expected_total_minutes = calculate_total_minutes(hour_speedups, five_min_speedups)
        expected_cost_per_minute = calculate_cost_per_minute(price, expected_total_minutes)
        
        def button_side_effect(label, *args, **kwargs):
            return label == "Add Pack"
        
        # Mock Streamlit components
        with patch('streamlit.text_input') as mock_text_input, \
             patch('streamlit.number_input') as mock_number_input, \
             patch('streamlit.button', side_effect=button_side_effect) as mock_button, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.success') as mock_success, \
             patch('streamlit.experimental_rerun') as mock_rerun, \
             patch('streamlit.columns', side_effect=mock_columns):
            
            # Setup mock returns
            mock_text_input.return_value = pack_name
            mock_number_input.side_effect = [price, hour_speedups, five_min_speedups]
            
            # Use proper session state mock
            session_state = MockSessionState(pack_value_history=[])
            with patch('streamlit.session_state', session_state):
                # Call the function
                render_pack_value_comparison_tab()
                
                # Verify metric was called with correct total minutes
                mock_metric.assert_called_with("Total Minutes", expected_total_minutes)
                
                # Verify success message was shown
                mock_success.assert_called_with(f"Pack '{pack_name}' added.")
                
                # Verify rerun was called
                mock_rerun.assert_called()
    
    @patch('features.pack_value_comparison.PACKS_JSON_PATH')
    def test_validation_with_zero_speedups(self, mock_path):
        """Test validation when both speedup inputs are zero."""
        mock_path.__str__ = lambda: self.temp_file_path
        import features.pack_value_comparison as pvc
        pvc.PACKS_JSON_PATH = self.temp_file_path
        
        # Test data with zero speedups
        pack_name = "Test Pack"
        price = 15.0
        hour_speedups = 0
        five_min_speedups = 0
        
        # Mock Streamlit components
        with patch('streamlit.text_input') as mock_text_input, \
             patch('streamlit.number_input') as mock_number_input, \
             patch('streamlit.button') as mock_button, \
             patch('streamlit.error') as mock_error, \
             patch('streamlit.metric') as mock_metric, \
             patch('streamlit.columns', side_effect=mock_columns):
            
            # Setup mock returns
            mock_text_input.return_value = pack_name
            mock_number_input.side_effect = [price, hour_speedups, five_min_speedups]
            mock_button.return_value = True
            
            # Use proper session state mock
            session_state = MockSessionState(pack_value_history=[], add_pack_btn=True)
            with patch('streamlit.session_state', session_state):
                # Call the function
                render_pack_value_comparison_tab()
                
                # Verify error message was shown
                mock_error.assert_called_with("At least one speedup must be greater than 0.")
    
    @patch('features.pack_value_comparison.PACKS_JSON_PATH')
    def test_data_persistence_and_loading(self, mock_path):
        """Test that data is properly saved and loaded."""
        mock_path.__str__ = lambda: self.temp_file_path
        import features.pack_value_comparison as pvc
        pvc.PACKS_JSON_PATH = self.temp_file_path
        
        # Test data
        test_data = [
            {
                "Pack Name": "Pack 1",
                "Price": 10.0,
                "60min Speedups": 1,
                "5min Speedups": 5,
                "Total Speedup Minutes": 85,
                "Cost per Minute": 0.1176
            },
            {
                "Pack Name": "Pack 2", 
                "Price": 20.0,
                "60min Speedups": 2,
                "5min Speedups": 10,
                "Total Speedup Minutes": 130,
                "Cost per Minute": 0.1538
            }
        ]
        
        # Save test data using the actual save function
        save_pack_history(test_data)
        
        # Verify file was created and contains correct data
        assert os.path.exists(self.temp_file_path)
        
        # Read the file directly to verify content
        with open(self.temp_file_path, 'r') as f:
            saved_data = json.load(f)
        
        assert saved_data == test_data
        
        # Test loading using the actual load function
        loaded_data = load_pack_history()
        assert loaded_data == test_data
    
    def test_calculation_edge_cases(self):
        """Test calculation functions with edge cases."""
        # Test division by zero in cost calculation
        cost = calculate_cost_per_minute(10.0, 0)
        assert cost == 0.0
        
        # Test negative minutes
        cost = calculate_cost_per_minute(10.0, -5)
        assert cost == 0.0
        
        # Test large numbers
        total = calculate_total_minutes(1000, 5000)
        assert total == 85000
        
        # Test mixed positive and negative (should still calculate)
        total = calculate_total_minutes(1, -2)
        assert total == 50
    
    @patch('features.pack_value_comparison.PACKS_JSON_PATH')
    def test_table_display_with_new_columns(self, mock_path):
        """Test that the table displays all new columns correctly."""
        mock_path.__str__ = lambda: self.temp_file_path
        import features.pack_value_comparison as pvc
        pvc.PACKS_JSON_PATH = self.temp_file_path
        
        # Test data with new column structure
        test_data = [
            {
                "Pack Name": "Test Pack",
                "Price": 15.0,
                "60min Speedups": 2,
                "5min Speedups": 10,
                "Total Speedup Minutes": 130,
                "Cost per Minute": 0.1154
            }
        ]
        
        # Save test data using the actual save function
        save_pack_history(test_data)
        
        # Mock Streamlit components for table display
        with patch('streamlit.selectbox') as mock_selectbox, \
             patch('streamlit.radio') as mock_radio, \
             patch('streamlit.dataframe') as mock_dataframe, \
             patch('streamlit.info') as mock_info, \
             patch('streamlit.columns', side_effect=mock_columns):
            
            # Setup mock returns
            mock_selectbox.return_value = "Cost per Minute"
            mock_radio.return_value = "Ascending"
            
            # Use proper session state mock
            session_state = MockSessionState(pack_value_history=test_data)
            with patch('streamlit.session_state', session_state):
                # Call the function
                render_pack_value_comparison_tab()
                
                # Verify dataframe was called with correct data
                mock_dataframe.assert_called_once()
                call_args = mock_dataframe.call_args
                df = call_args[0][0]  # First argument is the dataframe
                
                # Verify all expected columns are present
                expected_columns = [
                    "Pack Name", "Price", "60min Speedups", "5min Speedups", 
                    "Total Speedup Minutes", "Cost per Minute"
                ]
                assert list(df.columns) == expected_columns
                
                # Verify data is correct
                assert df.iloc[0]["Pack Name"] == "Test Pack"
                assert df.iloc[0]["60min Speedups"] == 2
                assert df.iloc[0]["5min Speedups"] == 10
                assert df.iloc[0]["Total Speedup Minutes"] == 130 