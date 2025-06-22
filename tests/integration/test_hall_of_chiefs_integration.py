"""
Integration tests for Hall of Chiefs module.
"""

import pytest
import streamlit as st
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock
from features.hall_of_chiefs import (
    render_hall_of_chiefs_tab,
    calculate_construction_points,
    calculate_research_points,
    create_efficiency_dataframe,
    calculate_summary_metrics
)
from features.hall_of_chiefs_data import CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY
from features.hall_of_chiefs_session import get_session_manager
from utils.session_manager import init_session_state

def columns_side_effect(n):
    if isinstance(n, int):
        return [MagicMock() for _ in range(n)]
    elif isinstance(n, (list, tuple)):
        return [MagicMock() for _ in range(len(n))]
    else:
        raise TypeError(f"Unsupported columns arg: {n}")

class DummyExpander:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class TestHallOfChiefsIntegration:
    """Integration tests for Hall of Chiefs functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create temporary directory for test data
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_hall_of_chiefs_data.json")
        
        # Mock streamlit session state
        self.mock_session_state = {
            'hall_of_chiefs_data': {
                CONSTRUCTION_CATEGORY: [],
                RESEARCH_CATEGORY: [],
                TRAINING_CATEGORY: []
            },
            'hall_of_chiefs_clear_inputs': {
                CONSTRUCTION_CATEGORY: False,
                RESEARCH_CATEGORY: False,
                TRAINING_CATEGORY: False
            },
            'hall_of_chiefs_delete_confirm': {
                'entry_id': None,
                'category': None
            },
            'hall_of_chiefs_clear_all_confirm': False,
            'hall_of_chiefs_data_loaded': True
        }
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Remove temporary files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    @patch('utils.session_manager.get_speedup_inventory', return_value={
        'general': 18000.0,
        'construction': 1200.0,
        'training': 1515.0,
        'research': 800.0
    })
    @patch('streamlit.session_state')
    @patch('streamlit.sidebar')
    @patch('streamlit.header')
    @patch('streamlit.caption')
    @patch('streamlit.subheader')
    @patch('streamlit.dataframe')
    @patch('streamlit.metric')
    @patch('streamlit.info')
    @patch('streamlit.experimental_data_editor')
    @patch('streamlit.button')
    @patch('streamlit.text_input')
    @patch('streamlit.number_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.columns', side_effect=columns_side_effect)
    @patch('streamlit.expander', return_value=DummyExpander())
    @patch('streamlit.write')
    @patch('streamlit.success')
    @patch('streamlit.error')
    @patch('streamlit.warning')
    @patch('streamlit.download_button')
    @patch('streamlit.experimental_rerun')
    def test_render_hall_of_chiefs_tab_empty_state(
        self, mock_rerun, mock_download, mock_warning, mock_error,
        mock_success, mock_write, mock_expander, mock_columns,
        mock_selectbox, mock_number_input, mock_text_input,
        mock_button, mock_data_editor, mock_info, mock_metric,
        mock_dataframe, mock_subheader, mock_caption, mock_header,
        mock_sidebar, mock_session_state, mock_get_speedup_inventory
    ):
        """Test rendering Hall of Chiefs tab with empty state."""
        # Set up mocks
        mock_session_state.__getitem__.side_effect = lambda key: {
            'speedup_inventory': {
                'general': 18000.0,
                'construction': 1200.0,
                'training': 1515.0,
                'research': 800.0
            },
            'hall_of_chiefs_construction_entries': [],
            'hall_of_chiefs_research_entries': [],
            'hall_of_chiefs_training_entries': [],
            'hall_of_chiefs_data': {
                'construction': [],
                'research': [],
                'training': []
            },
            'hall_of_chiefs_clear_inputs': {
                'construction': False,
                'research': False,
                'training': False
            },
            'hall_of_chiefs_clear_all_confirm': False,
            'hall_of_chiefs_delete_confirm': None
        }[key]
        mock_session_state.get.side_effect = lambda key, default=None: {
            'speedup_inventory': {
                'general': 18000.0,
                'construction': 1200.0,
                'training': 1515.0,
                'research': 800.0
            }
        }.get(key, default)
        
        # Mock sidebar expander
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()
        
        # Mock columns
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        
        # Mock data editor
        mock_data_editor.return_value = None
        
        # Mock button returns
        mock_button.side_effect = [False, False, False]  # Add buttons return False
        
        # Mock text inputs
        mock_text_input.return_value = ""
        
        # Mock number inputs
        mock_number_input.return_value = 0.0
        
        # Mock selectbox
        mock_selectbox.return_value = 30
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify basic UI elements were called
        mock_header.assert_called_once()
        mock_caption.assert_called_once()
        mock_subheader.assert_called()
        
        # Verify info messages for empty state
        mock_info.assert_called()
    
    @patch('utils.session_manager.get_speedup_inventory', return_value={
        'general': 18000.0,
        'construction': 1200.0,
        'training': 1515.0,
        'research': 800.0
    })
    @patch('streamlit.session_state')
    @patch('streamlit.sidebar')
    @patch('streamlit.header')
    @patch('streamlit.caption')
    @patch('streamlit.subheader')
    @patch('streamlit.dataframe')
    @patch('streamlit.metric')
    @patch('streamlit.info')
    @patch('streamlit.experimental_data_editor')
    @patch('streamlit.button')
    @patch('streamlit.text_input')
    @patch('streamlit.number_input')
    @patch('streamlit.selectbox')
    @patch('streamlit.columns', side_effect=columns_side_effect)
    @patch('streamlit.expander', return_value=DummyExpander())
    @patch('streamlit.write')
    @patch('streamlit.success')
    @patch('streamlit.error')
    @patch('streamlit.warning')
    @patch('streamlit.download_button')
    @patch('streamlit.experimental_rerun')
    def test_render_hall_of_chiefs_tab_with_data(
        self, mock_rerun, mock_download, mock_warning, mock_error, 
        mock_success, mock_info, mock_write, mock_expander, 
        mock_columns, mock_selectbox, mock_number_input, 
        mock_text_input, mock_button, mock_data_editor, 
        mock_metric, mock_dataframe, mock_subheader, 
        mock_caption, mock_header, mock_sidebar, mock_session_state, mock_get_speedup_inventory
    ):
        """Test rendering Hall of Chiefs tab with data."""
        # Set up test data
        self.mock_session_state['hall_of_chiefs_data'] = {
            CONSTRUCTION_CATEGORY: [
                {
                    'id': 'construction_1',
                    'description': 'Test Building',
                    'power': 100.0,
                    'speedup_minutes': 60.0,
                    'points_per_power': 30,
                    'created_at': '2024-01-01T00:00:00'
                }
            ],
            RESEARCH_CATEGORY: [
                {
                    'id': 'research_1',
                    'description': 'Test Research',
                    'power': 50.0,
                    'speedup_minutes': 120.0,
                    'points_per_power': 45,
                    'created_at': '2024-01-01T00:00:00'
                }
            ],
            TRAINING_CATEGORY: []
        }
        # Set up mocks
        mock_session_state.__getitem__.side_effect = lambda key: {
            'speedup_inventory': {
                'general': 18000.0,
                'construction': 1200.0,
                'training': 1515.0,
                'research': 800.0
            },
            'hall_of_chiefs_construction_entries': [],
            'hall_of_chiefs_research_entries': [],
            'hall_of_chiefs_training_entries': [],
            'hall_of_chiefs_data': self.mock_session_state['hall_of_chiefs_data'],
            'hall_of_chiefs_clear_inputs': {
                'construction': False,
                'research': False,
                'training': False
            },
            'hall_of_chiefs_clear_all_confirm': False,
            'hall_of_chiefs_delete_confirm': None
        }[key]
        mock_session_state.get.side_effect = lambda key, default=None: {
            'speedup_inventory': {
                'general': 18000.0,
                'construction': 1200.0,
                'training': 1515.0,
                'research': 800.0
            }
        }.get(key, default)
        
        # Mock sidebar expander
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()
        
        # Mock columns
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        
        # Mock data editor
        mock_data_editor.return_value = None
        
        # Mock button returns
        mock_button.side_effect = [False, False, False]  # Add buttons return False
        
        # Mock text inputs
        mock_text_input.return_value = ""
        
        # Mock number inputs
        mock_number_input.return_value = 0.0
        
        # Mock selectbox
        mock_selectbox.return_value = 30
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify metrics were called for data
        mock_metric.assert_called()
        
        # Verify data editor was called for categories with data
        assert mock_data_editor.call_count >= 2  # At least for Construction and Research
        
        # Verify download button was called
        mock_download.assert_called_once()
    
    def test_calculate_construction_points(self):
        """Test construction points calculation."""
        points = calculate_construction_points(100.0, 30)
        assert points == 3000.0
        
        points = calculate_construction_points(50.0, 45)
        assert points == 2250.0
    
    def test_calculate_research_points(self):
        """Test research points calculation."""
        points = calculate_research_points(10.0, 30)
        assert points == 300.0
        
        points = calculate_research_points(5.0, 45)
        assert points == 225.0
    
    def test_create_efficiency_dataframe(self):
        """Test efficiency DataFrame creation."""
        construction_entries = [
            {
                'id': '1',
                'description': 'Test Building',
                'power': 100.0,
                'speedup_minutes': 60.0,
                'points_per_power': 30
            }
        ]
        
        research_entries = [
            {
                'id': '2',
                'description': 'Test Research',
                'power': 50.0,
                'speedup_minutes': 120.0,
                'points_per_power': 45
            }
        ]
        
        training_entries = []
        
        df = create_efficiency_dataframe(construction_entries, research_entries, training_entries)
        
        assert len(df) == 2
        assert 'Activity Type' in df.columns
        assert 'Description' in df.columns
        assert 'Power' in df.columns
        assert 'Total Points' in df.columns
        assert 'Speed-up Minutes' in df.columns
        assert 'Efficiency (Points/Min)' in df.columns
        
        # Check construction entry
        construction_row = df[df['Activity Type'] == 'Construction'].iloc[0]
        assert construction_row['Description'] == 'Test Building'
        assert construction_row['Power'] == 100.0
        assert construction_row['Total Points'] == 3000.0
        assert construction_row['Speed-up Minutes'] == 60.0
        assert construction_row['Efficiency (Points/Min)'] == 50.0
        
        # Check research entry
        research_row = df[df['Activity Type'] == 'Research'].iloc[0]
        assert research_row['Description'] == 'Test Research'
        assert research_row['Power'] == 50.0
        assert research_row['Total Points'] == 2250.0
        assert research_row['Speed-up Minutes'] == 120.0
        assert research_row['Efficiency (Points/Min)'] == 18.75
    
    def test_calculate_summary_metrics(self):
        """Test summary metrics calculation."""
        # Create test DataFrame
        data = [
            {
                'Activity Type': 'Construction',
                'Description': 'Test Building',
                'Power': 100.0,
                'Total Points': 3000.0,
                'Speed-up Minutes': 60.0,
                'Efficiency (Points/Min)': 50.0
            },
            {
                'Activity Type': 'Research',
                'Description': 'Test Research',
                'Power': 50.0,
                'Total Points': 2250.0,
                'Speed-up Minutes': 120.0,
                'Efficiency (Points/Min)': 18.75
            }
        ]
        
        df = pd.DataFrame(data)
        summary = calculate_summary_metrics(df)
        
        assert summary['research_avg_efficiency'] == 18.75
        assert summary['total_points_by_type']['Construction'] == 3000.0
        assert summary['total_points_by_type']['Research'] == 2250.0
        assert summary['total_speedups_by_type']['Construction'] == 60.0
        assert summary['total_speedups_by_type']['Research'] == 120.0
        assert summary['overall_total_points'] == 5250.0
        assert summary['overall_total_speedups'] == 180.0
    
    def test_calculate_summary_metrics_empty(self):
        """Test summary metrics calculation with empty DataFrame."""
        df = pd.DataFrame()
        summary = calculate_summary_metrics(df)
        
        assert summary['research_avg_efficiency'] == 0.0
        assert summary['total_points_by_type'] == {}
        assert summary['total_speedups_by_type'] == {}
        assert summary['overall_total_points'] == 0.0
        assert summary['overall_total_speedups'] == 0.0
    
    @patch('features.hall_of_chiefs.st.number_input', side_effect=lambda *args, **kwargs: 42.0)
    @patch('features.hall_of_chiefs.st.text_input', side_effect=lambda *args, **kwargs: "Test Building")
    @patch('streamlit.experimental_rerun')
    @patch('streamlit.download_button')
    @patch('streamlit.warning')
    @patch('streamlit.error')
    @patch('streamlit.success')
    @patch('streamlit.write')
    @patch('streamlit.expander', return_value=DummyExpander())
    @patch('streamlit.columns', side_effect=columns_side_effect)
    @patch('streamlit.selectbox')
    @patch('streamlit.number_input')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.experimental_data_editor')
    @patch('streamlit.info')
    @patch('streamlit.metric')
    @patch('streamlit.dataframe')
    @patch('streamlit.subheader')
    @patch('streamlit.caption')
    @patch('streamlit.header')
    @patch('streamlit.sidebar')
    @patch('streamlit.session_state')
    @patch('utils.session_manager.get_speedup_inventory', return_value={
        'general': 18000.0,
        'construction': 1200.0,
        'training': 1515.0,
        'research': 800.0
    })
    def test_add_construction_entry_flow(
        self, mock_get_speedup_inventory, mock_session_state, mock_sidebar, mock_header, mock_caption, mock_subheader, mock_dataframe, mock_metric, mock_info, mock_data_editor, mock_button, mock_text_input, mock_number_input, mock_selectbox, mock_columns, mock_expander, mock_write, mock_success, mock_error, mock_warning, mock_download, mock_rerun, mock_text_input_side_effect, mock_number_input_side_effect
    ):
        """Test the flow of adding a construction entry."""
        # Clear state
        mock_session_state['hall_of_chiefs_construction_entries'] = []
        mock_session_state['hall_of_chiefs_data']['construction'] = []
        # Mock sidebar expander
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()
        
        # Mock columns
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        
        # Mock data editor
        mock_data_editor.return_value = None
        
        # Mock button returns - first button (Add Construction Entry) returns True
        mock_button.side_effect = [True, False, False]
        
        # Mock selectbox
        mock_selectbox.return_value = 30
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify success message was called (indicating entry was added)
        mock_success.assert_called()
        
        # Verify rerun was called
        mock_rerun.assert_called()
    
    @patch('features.hall_of_chiefs.st.number_input', side_effect=lambda *args, **kwargs: 42.0)
    @patch('features.hall_of_chiefs.st.text_input', side_effect=lambda *args, **kwargs: "Test Research")
    @patch('streamlit.experimental_rerun')
    @patch('streamlit.download_button')
    @patch('streamlit.warning')
    @patch('streamlit.error')
    @patch('streamlit.success')
    @patch('streamlit.write')
    @patch('streamlit.expander', return_value=DummyExpander())
    @patch('streamlit.columns', side_effect=columns_side_effect)
    @patch('streamlit.selectbox')
    @patch('streamlit.number_input')
    @patch('streamlit.text_input')
    @patch('streamlit.button')
    @patch('streamlit.experimental_data_editor')
    @patch('streamlit.info')
    @patch('streamlit.metric')
    @patch('streamlit.dataframe')
    @patch('streamlit.subheader')
    @patch('streamlit.caption')
    @patch('streamlit.header')
    @patch('streamlit.sidebar')
    @patch('streamlit.session_state')
    @patch('utils.session_manager.get_speedup_inventory', return_value={
        'general': 18000.0,
        'construction': 1200.0,
        'training': 1515.0,
        'research': 800.0
    })
    def test_add_research_entry_flow(
        self, mock_get_speedup_inventory, mock_session_state, mock_sidebar, mock_header, mock_caption, mock_subheader, mock_dataframe, mock_metric, mock_info, mock_data_editor, mock_button, mock_text_input, mock_number_input, mock_selectbox, mock_columns, mock_expander, mock_write, mock_success, mock_error, mock_warning, mock_download, mock_rerun, mock_text_input_side_effect, mock_number_input_side_effect
    ):
        """Test the flow of adding a research entry."""
        # Clear state
        mock_session_state['hall_of_chiefs_research_entries'] = []
        mock_session_state['hall_of_chiefs_data']['research'] = []
        # Mock sidebar expander
        mock_expander.return_value.__enter__ = MagicMock()
        mock_expander.return_value.__exit__ = MagicMock()
        
        # Mock columns
        mock_columns.return_value = [MagicMock(), MagicMock(), MagicMock(), MagicMock(), MagicMock()]
        
        # Mock data editor
        mock_data_editor.return_value = None
        
        # Mock button returns - second button (Add Research Entry) returns True
        mock_button.side_effect = [False, True, False]
        
        # Mock selectbox
        mock_selectbox.return_value = 45
        
        # Call the function
        render_hall_of_chiefs_tab()
        
        # Verify success message was called (indicating entry was added)
        mock_success.assert_called()
        
        # Verify rerun was called
        mock_rerun.assert_called()
    
    def test_ui_handles_invalid_training_time_gracefully(self, mock_session_state):
        import tempfile
        from unittest.mock import patch
        # Use a temporary data file for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_data_file = f.name
            f.write('{"construction": [], "research": [], "training": [], "metadata": {"created": "2024-01-01", "version": "1.0"}}')
        try:
            with patch('features.hall_of_chiefs_data.HALL_OF_CHIEFS_DATA_FILE', temp_data_file):
                # Clear all relevant state
                mock_session_state['hall_of_chiefs_training_entries'] = []
                mock_session_state['hall_of_chiefs_data']['training'] = []
                mock_session_state['hall_of_chiefs_construction_entries'] = []
                mock_session_state['hall_of_chiefs_data']['construction'] = []
                mock_session_state['hall_of_chiefs_research_entries'] = []
                mock_session_state['hall_of_chiefs_data']['research'] = []
                # Initialize session state
                init_session_state()
                # Add an invalid training entry with zero time
                session_manager = get_session_manager()
                invalid_entry = {
                    'description': 'Invalid Training',
                    'days': 0,
                    'hours': 0,
                    'minutes': 0,
                    'seconds': 0,
                    'troops_per_batch': 100,
                    'points_per_troop': 50.0
                }
                success, message = session_manager.add_entry('training', invalid_entry)
                assert success
                # Verify the entry was added
                entries = session_manager.get_entries('training')
                assert len(entries) == 1
                assert entries[0]['description'] == 'Invalid Training'
                # Test that calculate_training_points handles invalid time
                from features.hall_of_chiefs import calculate_training_points
                training_params = {
                    'days': 0,
                    'hours': 0,
                    'minutes': 0,
                    'seconds': 0,
                    'troops_per_batch': 100,
                    'points_per_troop': 50.0
                }
                points, speedups = calculate_training_points(training_params)
                assert points == 0.0
                assert speedups == 0.0
        finally:
            import os
            os.unlink(temp_data_file)

    def test_row_deletion_with_confirmation(self, mock_session_state):
        import tempfile
        from unittest.mock import patch
        import os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_data_file = f.name
            f.write('{"construction": [], "research": [], "training": [], "metadata": {"created": "2024-01-01", "version": "1.0"}}')
        try:
            with patch('features.hall_of_chiefs_data.HALL_OF_CHIEFS_DATA_FILE', temp_data_file):
                # Clear all relevant state
                mock_session_state['hall_of_chiefs_training_entries'] = []
                mock_session_state['hall_of_chiefs_data']['training'] = []
                mock_session_state['hall_of_chiefs_construction_entries'] = []
                mock_session_state['hall_of_chiefs_data']['construction'] = []
                mock_session_state['hall_of_chiefs_research_entries'] = []
                mock_session_state['hall_of_chiefs_data']['research'] = []
                # Initialize session state
                init_session_state()
                # Add a test entry
                session_manager = get_session_manager()
                test_entry = {
                    'description': 'Test Construction',
                    'power': 100.0,
                    'speedup_minutes': 60.0,
                    'points_per_power': 30
                }
                success, message = session_manager.add_entry('construction', test_entry)
                assert success
                # Verify entry was added
                entries = session_manager.get_entries('construction')
                assert len(entries) == 1
        finally:
            os.unlink(temp_data_file)

    def test_row_deletion_cancellation(self, mock_session_state):
        import tempfile
        from unittest.mock import patch
        import os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_data_file = f.name
            f.write('{"construction": [], "research": [], "training": [], "metadata": {"created": "2024-01-01", "version": "1.0"}}')
        try:
            with patch('features.hall_of_chiefs_data.HALL_OF_CHIEFS_DATA_FILE', temp_data_file):
                # Clear all relevant state
                mock_session_state['hall_of_chiefs_training_entries'] = []
                mock_session_state['hall_of_chiefs_data']['training'] = []
                mock_session_state['hall_of_chiefs_construction_entries'] = []
                mock_session_state['hall_of_chiefs_data']['construction'] = []
                mock_session_state['hall_of_chiefs_research_entries'] = []
                mock_session_state['hall_of_chiefs_data']['research'] = []
                # Initialize session state
                init_session_state()
                # Add a test entry
                session_manager = get_session_manager()
                test_entry = {
                    'description': 'Test Research',
                    'power': 50.0,
                    'speedup_minutes': 30.0,
                    'points_per_power': 45
                }
                success, message = session_manager.add_entry('research', test_entry)
                assert success
                # Verify entry was added
                entries = session_manager.get_entries('research')
                assert len(entries) == 1
        finally:
            os.unlink(temp_data_file)
        
        # Clear training entries and data
        mock_session_state['hall_of_chiefs_training_entries'] = []
        mock_session_state['hall_of_chiefs_data']['training'] = [] 