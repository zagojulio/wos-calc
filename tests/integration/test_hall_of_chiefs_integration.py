"""
Integration tests for Hall of Chiefs Points Efficiency tab.
"""

import pytest
import streamlit as st
import pandas as pd
from unittest.mock import patch, MagicMock
from features.hall_of_chiefs import (
    render_hall_of_chiefs_tab,
    init_hall_of_chiefs_session_state,
    CONSTRUCTION_ENTRIES_KEY,
    RESEARCH_ENTRIES_KEY
)

DEFAULT_TRAINING_PARAMS = {
    'general_speedups': 18000.0,
    'training_speedups': 1515.0,
    'days': 0,
    'hours': 4,
    'minutes': 50,
    'seconds': 0,
    'base_training_time': 290.0,
    'troops_per_batch': 426,
    'points_per_troop': 830.0
}

class TestHallOfChiefsIntegration:
    """Integration tests for Hall of Chiefs tab functionality."""
    
    def setup_method(self):
        """Set up test environment."""
        # Reset session state keys to empty lists
        if hasattr(st, 'session_state'):
            st.session_state[CONSTRUCTION_ENTRIES_KEY] = []
            st.session_state[RESEARCH_ENTRIES_KEY] = []
    
    @patch('streamlit.header')
    @patch('streamlit.caption')
    @patch('streamlit.subheader')
    @patch('streamlit.info')
    @patch('streamlit.dataframe')
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.radio')
    @patch('streamlit.download_button')
    @patch('features.hall_of_chiefs.render_construction_sidebar')
    @patch('features.hall_of_chiefs.render_research_sidebar')
    @patch('features.hall_of_chiefs.create_efficiency_dataframe')
    @patch('features.hall_of_chiefs.calculate_summary_metrics')
    @patch('utils.session_manager.get_training_params')
    def test_render_hall_of_chiefs_tab_empty_state(
        self, mock_get_training_params, mock_calculate_summary, 
        mock_create_dataframe, mock_render_research, mock_render_construction,
        mock_download_button, mock_radio, mock_selectbox, mock_columns,
        mock_metric, mock_dataframe, mock_info, mock_subheader, mock_caption, mock_header
    ):
        """Test rendering Hall of Chiefs tab with empty state."""
        # Patch columns to return exactly 2 or 3 columns as needed
        def columns_side_effect(n):
            return tuple(MagicMock() for _ in range(n))
        mock_columns.side_effect = columns_side_effect

        # Mock return values
        mock_get_training_params.return_value = DEFAULT_TRAINING_PARAMS.copy()
        mock_render_construction.return_value = []
        mock_render_research.return_value = []
        mock_create_dataframe.return_value = pd.DataFrame()
        mock_calculate_summary.return_value = {
            'research_avg_efficiency': 0.0,
            'total_points_by_type': {},
            'total_speedups_by_type': {},
            'overall_total_points': 0.0,
            'overall_total_speedups': 0.0
        }
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify initialization
        mock_header.assert_called_once_with("Hall of Chiefs Points Efficiency")
        mock_caption.assert_called_once()
        
        # Verify sidebar rendering
        mock_render_construction.assert_called_once()
        mock_render_research.assert_called_once()
        
        # Verify data processing
        mock_create_dataframe.assert_called_once_with([], [], DEFAULT_TRAINING_PARAMS)
        mock_calculate_summary.assert_called_once()
        
        # Verify empty state message
        mock_info.assert_called_once_with("No data available. Add entries in the sidebar to see efficiency comparisons.")
    
    @patch('streamlit.header')
    @patch('streamlit.caption')
    @patch('streamlit.subheader')
    @patch('streamlit.info')
    @patch('streamlit.dataframe')
    @patch('streamlit.metric')
    @patch('streamlit.columns')
    @patch('streamlit.selectbox')
    @patch('streamlit.radio')
    @patch('streamlit.download_button')
    @patch('features.hall_of_chiefs.render_construction_sidebar')
    @patch('features.hall_of_chiefs.render_research_sidebar')
    @patch('features.hall_of_chiefs.create_efficiency_dataframe')
    @patch('features.hall_of_chiefs.calculate_summary_metrics')
    @patch('utils.session_manager.get_training_params')
    def test_render_hall_of_chiefs_tab_with_data(
        self, mock_get_training_params, mock_calculate_summary, 
        mock_create_dataframe, mock_render_research, mock_render_construction,
        mock_download_button, mock_radio, mock_selectbox, mock_columns,
        mock_metric, mock_dataframe, mock_info, mock_subheader, mock_caption, mock_header
    ):
        """Test rendering Hall of Chiefs tab with data."""
        # Patch columns to return exactly 2 or 3 columns as needed
        def columns_side_effect(n):
            return tuple(MagicMock() for _ in range(n))
        mock_columns.side_effect = columns_side_effect

        # Mock training parameters
        training_params = DEFAULT_TRAINING_PARAMS.copy()
        training_params.update({
            'troops_per_batch': 100,
            'general_speedups': 1000.0,
            'training_speedups': 500.0
        })
        mock_get_training_params.return_value = training_params
        
        # Mock sidebar entries
        mock_render_construction.return_value = [
            {'power': 100.0, 'speedup_minutes': 60.0, 'points_per_power': 30}
        ]
        mock_render_research.return_value = [
            {'description': 'Research 1', 'speedup_minutes': 100.0, 'points_per_power': 30}
        ]
        
        # Mock DataFrame
        test_df = pd.DataFrame([
            {
                'Activity Type': 'Construction',
                'Description': 'Power: 100',
                'Total Points': 3000.0,
                'Speed-up Minutes': 60.0,
                'Efficiency (Points/Min)': 50.0
            },
            {
                'Activity Type': 'Research',
                'Description': 'Research 1',
                'Total Points': 300.0,
                'Speed-up Minutes': 100.0,
                'Efficiency (Points/Min)': 3.0
            }
        ])
        mock_create_dataframe.return_value = test_df
        
        # Mock summary metrics
        mock_calculate_summary.return_value = {
            'research_avg_efficiency': 3.0,
            'total_points_by_type': {
                'Construction': 3000.0,
                'Research': 300.0
            },
            'total_speedups_by_type': {
                'Construction': 60.0,
                'Research': 100.0
            },
            'overall_total_points': 3300.0,
            'overall_total_speedups': 160.0
        }
        
        # Mock sort options
        mock_selectbox.return_value = 'Efficiency (Points/Min)'
        mock_radio.return_value = 'Descending'
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify metrics are displayed
        assert mock_metric.call_count >= 3  # At least 3 metrics should be called
        
        # Verify DataFrame is displayed
        mock_dataframe.assert_called_once()
        
        # Verify download button is available
        mock_download_button.assert_called_once()
        
        # Verify no empty state message
        mock_info.assert_not_called()
    
    def test_session_state_initialization(self):
        """Test session state initialization."""
        # Reset session state keys to empty lists
        if hasattr(st, 'session_state'):
            st.session_state[CONSTRUCTION_ENTRIES_KEY] = []
            st.session_state[RESEARCH_ENTRIES_KEY] = []
        
        # Initialize
        init_hall_of_chiefs_session_state()
        
        # Verify session state keys are created
        assert CONSTRUCTION_ENTRIES_KEY in st.session_state
        assert RESEARCH_ENTRIES_KEY in st.session_state
        assert st.session_state[CONSTRUCTION_ENTRIES_KEY] == []
        assert st.session_state[RESEARCH_ENTRIES_KEY] == []
    
    @patch('streamlit.sidebar.expander')
    @patch('streamlit.button')
    @patch('streamlit.number_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.write')
    @patch('streamlit.container')
    @patch('streamlit.columns')
    def test_construction_sidebar_interaction(
        self, mock_columns, mock_container, mock_write, mock_selectbox,
        mock_number_input, mock_button, mock_expander
    ):
        from features.hall_of_chiefs import render_construction_sidebar
        # Patch columns to return 2 columns
        mock_columns.side_effect = lambda n: tuple(MagicMock() for _ in range(n))
        # Mock expander context
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_context
        # Mock container
        mock_container_context = MagicMock()
        mock_container.return_value.__enter__.return_value = mock_container_context
        # Mock inputs
        mock_number_input.return_value = 100.0
        mock_selectbox.return_value = 30
        mock_button.return_value = False  # Remove button not clicked
        # Initialize session state
        init_hall_of_chiefs_session_state()
        # Add a construction entry
        st.session_state[CONSTRUCTION_ENTRIES_KEY] = [
            {'power': 0.0, 'speedup_minutes': 0.0, 'points_per_power': 30}
        ]
        # Render sidebar
        result = render_construction_sidebar()
        # Verify result
        assert len(result) == 1
        assert result[0]['power'] == 100.0
        assert result[0]['speedup_minutes'] == 100.0
        assert result[0]['points_per_power'] == 30
    
    @patch('streamlit.sidebar.expander')
    @patch('streamlit.button')
    @patch('streamlit.number_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.text_input')
    @patch('streamlit.write')
    @patch('streamlit.container')
    @patch('streamlit.columns')
    def test_research_sidebar_interaction(
        self, mock_columns, mock_container, mock_write, mock_text_input,
        mock_selectbox, mock_number_input, mock_button, mock_expander
    ):
        from features.hall_of_chiefs import render_research_sidebar
        # Patch columns to return 2 columns
        mock_columns.side_effect = lambda n: tuple(MagicMock() for _ in range(n))
        # Mock expander context
        mock_expander_context = MagicMock()
        mock_expander.return_value.__enter__.return_value = mock_expander_context
        # Mock container
        mock_container_context = MagicMock()
        mock_container.return_value.__enter__.return_value = mock_container_context
        # Mock inputs
        mock_text_input.return_value = "Test Research"
        mock_number_input.return_value = 100.0
        mock_selectbox.return_value = 45
        mock_button.return_value = False  # Remove button not clicked
        # Initialize session state
        init_hall_of_chiefs_session_state()
        # Add a research entry
        st.session_state[RESEARCH_ENTRIES_KEY] = [
            {'description': '', 'speedup_minutes': 0.0, 'points_per_power': 30}
        ]
        # Render sidebar
        result = render_research_sidebar()
        # Verify result
        assert len(result) == 1
        assert result[0]['description'] == "Test Research"
        assert result[0]['speedup_minutes'] == 100.0
        assert result[0]['points_per_power'] == 45
    
    @patch('features.hall_of_chiefs.calculate_training_points')
    def test_efficiency_dataframe_with_training(
        self, mock_calculate_training
    ):
        from features.hall_of_chiefs import create_efficiency_dataframe
        # Mock training calculation
        mock_calculate_training.return_value = (5000.0, 200.0)
        # Test data
        construction_entries = [
            {'power': 100.0, 'speedup_minutes': 60.0, 'points_per_power': 30}
        ]
        research_entries = [
            {'description': 'Research 1', 'speedup_minutes': 100.0, 'points_per_power': 30}
        ]
        training_params = {
            'troops_per_batch': 100,
            'general_speedups': 1000.0,
            'training_speedups': 500.0
        }
        # Create DataFrame
        df = create_efficiency_dataframe(construction_entries, research_entries, training_params)
        # Verify DataFrame structure
        assert len(df) == 3
        assert list(df.columns) == [
            'Activity Type', 'Description', 'Total Points', 
            'Speed-up Minutes', 'Efficiency (Points/Min)'
        ]
        # Verify activity types
        activity_types = df['Activity Type'].tolist()
        assert 'Construction' in activity_types
        assert 'Research' in activity_types
        assert 'Training' in activity_types
        # Verify training data
        training_row = df[df['Activity Type'] == 'Training'].iloc[0]
        assert training_row['Total Points'] == 5000.0
        assert training_row['Speed-up Minutes'] == 200.0
        assert training_row['Efficiency (Points/Min)'] == 25.0 