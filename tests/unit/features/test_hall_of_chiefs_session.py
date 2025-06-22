"""
Unit tests for Hall of Chiefs Session Management Module.
"""

import pytest
import streamlit as st
from unittest.mock import patch, MagicMock
from features.hall_of_chiefs_session import (
    HallOfChiefsSessionManager,
    get_session_manager,
    CONSTRUCTION_CATEGORY,
    RESEARCH_CATEGORY,
    TRAINING_CATEGORY
)


class TestHallOfChiefsSessionManager:
    """Test the HallOfChiefsSessionManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Mock streamlit session state
        self.mock_session_state = {}
        
        with patch('streamlit.session_state', self.mock_session_state):
            self.session_manager = HallOfChiefsSessionManager()
    
    def test_init_session_state(self):
        """Test session state initialization."""
        assert 'hall_of_chiefs_data' in self.mock_session_state
        assert 'hall_of_chiefs_clear_inputs' in self.mock_session_state
        assert 'hall_of_chiefs_delete_confirm' in self.mock_session_state
        assert 'hall_of_chiefs_clear_all_confirm' in self.mock_session_state
        assert 'hall_of_chiefs_data_loaded' in self.mock_session_state
        
        # Check data structure
        data = self.mock_session_state['hall_of_chiefs_data']
        assert CONSTRUCTION_CATEGORY in data
        assert RESEARCH_CATEGORY in data
        assert TRAINING_CATEGORY in data
        assert data[CONSTRUCTION_CATEGORY] == []
        assert data[RESEARCH_CATEGORY] == []
        assert data[TRAINING_CATEGORY] == []
        
        # Check clear inputs structure
        clear_inputs = self.mock_session_state['hall_of_chiefs_clear_inputs']
        assert clear_inputs[CONSTRUCTION_CATEGORY] is False
        assert clear_inputs[RESEARCH_CATEGORY] is False
        assert clear_inputs[TRAINING_CATEGORY] is False
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_load_data_from_persistence_success(self, mock_get_data_manager):
        """Test loading data from persistence successfully."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock data from persistence
        mock_data = {
            CONSTRUCTION_CATEGORY: [{'id': '1', 'description': 'Test'}],
            RESEARCH_CATEGORY: [],
            TRAINING_CATEGORY: []
        }
        mock_data_manager.get_all_entries.return_value = mock_data
        
        with patch('streamlit.session_state', self.mock_session_state):
            session_manager = HallOfChiefsSessionManager()
            
            # Verify data was loaded
            assert session_manager.get_entries(CONSTRUCTION_CATEGORY) == [{'id': '1', 'description': 'Test'}]
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_load_data_from_persistence_error(self, mock_get_data_manager):
        """Test loading data from persistence with error."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock error
        mock_data_manager.get_all_entries.side_effect = Exception("Test error")
        
        with patch('streamlit.session_state', self.mock_session_state):
            with patch('streamlit.error') as mock_error:
                session_manager = HallOfChiefsSessionManager()
                
                # Verify error was logged
                mock_error.assert_called_once()
                
                # Verify empty data was initialized
                assert session_manager.get_entries(CONSTRUCTION_CATEGORY) == []
    
    def test_get_entries(self):
        """Test getting entries for a specific category."""
        # Set up test data
        self.mock_session_state['hall_of_chiefs_data'] = {
            CONSTRUCTION_CATEGORY: [{'id': '1', 'description': 'Test'}],
            RESEARCH_CATEGORY: [],
            TRAINING_CATEGORY: []
        }
        
        entries = self.session_manager.get_entries(CONSTRUCTION_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Test'
    
    def test_get_entries_invalid_category(self):
        """Test getting entries with invalid category."""
        with pytest.raises(ValueError, match="Invalid category"):
            self.session_manager.get_entries('invalid_category')
    
    def test_get_all_entries(self):
        """Test getting all entries."""
        # Set up test data
        test_data = {
            CONSTRUCTION_CATEGORY: [{'id': '1', 'description': 'Test1'}],
            RESEARCH_CATEGORY: [{'id': '2', 'description': 'Test2'}],
            TRAINING_CATEGORY: []
        }
        self.mock_session_state['hall_of_chiefs_data'] = test_data
        
        all_entries = self.session_manager.get_all_entries()
        assert all_entries == test_data
        # Verify it's a copy, not the original
        assert all_entries is not test_data
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_add_entry_success(self, mock_get_data_manager):
        """Test adding entry successfully."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock successful add
        mock_data_manager.add_entry.return_value = (True, "Entry added successfully")
        
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        
        success, message = self.session_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert success
        assert "Entry added successfully" in message
        
        # Verify data manager was called
        mock_data_manager.add_entry.assert_called_once_with(CONSTRUCTION_CATEGORY, entry)
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_add_entry_failure(self, mock_get_data_manager):
        """Test adding entry with failure."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock failed add
        mock_data_manager.add_entry.return_value = (False, "Validation failed")
        
        entry = {'description': 'Test'}
        
        success, message = self.session_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert not success
        assert "Validation failed" in message
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_update_entry_success(self, mock_get_data_manager):
        """Test updating entry successfully."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock successful update
        mock_data_manager.update_entry.return_value = (True, "Entry updated successfully")
        
        entry = {
            'description': 'Updated Building',
            'power': 150.0,
            'speedup_minutes': 90.0,
            'points_per_power': 45
        }
        
        success, message = self.session_manager.update_entry(CONSTRUCTION_CATEGORY, 'test_id', entry)
        
        assert success
        assert "Entry updated successfully" in message
        
        # Verify data manager was called
        mock_data_manager.update_entry.assert_called_once_with(CONSTRUCTION_CATEGORY, 'test_id', entry)
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_delete_entry_success(self, mock_get_data_manager):
        """Test deleting entry successfully."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock successful delete
        mock_data_manager.delete_entry.return_value = (True, "Entry deleted successfully")
        
        success, message = self.session_manager.delete_entry(CONSTRUCTION_CATEGORY, 'test_id')
        
        assert success
        assert "Entry deleted successfully" in message
        
        # Verify data manager was called
        mock_data_manager.delete_entry.assert_called_once_with(CONSTRUCTION_CATEGORY, 'test_id')
    
    @patch('features.hall_of_chiefs_session.get_data_manager')
    def test_delete_all_entries_success(self, mock_get_data_manager):
        """Test deleting all entries successfully."""
        mock_data_manager = MagicMock()
        mock_get_data_manager.return_value = mock_data_manager
        
        # Mock successful delete
        mock_data_manager.delete_all_entries.return_value = (True, "All entries deleted")
        
        success, message = self.session_manager.delete_all_entries()
        
        assert success
        assert "All entries deleted" in message
        
        # Verify data manager was called
        mock_data_manager.delete_all_entries.assert_called_once_with(None)
    
    def test_get_entry_count(self):
        """Test getting entry counts."""
        # Set up test data
        test_data = {
            CONSTRUCTION_CATEGORY: [{'id': '1'}, {'id': '2'}],
            RESEARCH_CATEGORY: [{'id': '3'}],
            TRAINING_CATEGORY: []
        }
        self.mock_session_state['hall_of_chiefs_data'] = test_data
        
        # Test specific category
        construction_count = self.session_manager.get_entry_count(CONSTRUCTION_CATEGORY)
        assert construction_count[CONSTRUCTION_CATEGORY] == 2
        
        # Test all categories
        all_counts = self.session_manager.get_entry_count()
        assert all_counts[CONSTRUCTION_CATEGORY] == 2
        assert all_counts[RESEARCH_CATEGORY] == 1
        assert all_counts[TRAINING_CATEGORY] == 0
    
    def test_should_clear_inputs(self):
        """Test checking if inputs should be cleared."""
        # Set up test data
        self.mock_session_state['hall_of_chiefs_clear_inputs'] = {
            CONSTRUCTION_CATEGORY: True,
            RESEARCH_CATEGORY: False,
            TRAINING_CATEGORY: False
        }
        
        assert self.session_manager.should_clear_inputs(CONSTRUCTION_CATEGORY) is True
        assert self.session_manager.should_clear_inputs(RESEARCH_CATEGORY) is False
        assert self.session_manager.should_clear_inputs(TRAINING_CATEGORY) is False
    
    def test_reset_clear_inputs_flag(self):
        """Test resetting clear inputs flag."""
        # Set up test data
        self.mock_session_state['hall_of_chiefs_clear_inputs'] = {
            CONSTRUCTION_CATEGORY: True,
            RESEARCH_CATEGORY: False,
            TRAINING_CATEGORY: False
        }
        
        self.session_manager.reset_clear_inputs_flag(CONSTRUCTION_CATEGORY)
        
        assert self.mock_session_state['hall_of_chiefs_clear_inputs'][CONSTRUCTION_CATEGORY] is False
        assert self.mock_session_state['hall_of_chiefs_clear_inputs'][RESEARCH_CATEGORY] is False
    
    def test_delete_confirmation_management(self):
        """Test delete confirmation state management."""
        # Test setting confirmation
        self.session_manager.set_delete_confirmation('test_id', CONSTRUCTION_CATEGORY)
        
        confirm = self.mock_session_state['hall_of_chiefs_delete_confirm']
        assert confirm['entry_id'] == 'test_id'
        assert confirm['category'] == CONSTRUCTION_CATEGORY
        
        # Test getting confirmation
        entry_id, category = self.session_manager.get_delete_confirmation()
        assert entry_id == 'test_id'
        assert category == CONSTRUCTION_CATEGORY
        
        # Test clearing confirmation
        self.session_manager.clear_delete_confirmation()
        
        confirm = self.mock_session_state['hall_of_chiefs_delete_confirm']
        assert confirm['entry_id'] is None
        assert confirm['category'] is None
    
    def test_clear_all_confirmation_management(self):
        """Test clear all confirmation state management."""
        # Test setting confirmation
        self.session_manager.set_clear_all_confirmation(True)
        assert self.session_manager.get_clear_all_confirmation() is True
        
        # Test getting confirmation
        assert self.mock_session_state['hall_of_chiefs_clear_all_confirm'] is True
        
        # Test setting to False
        self.session_manager.set_clear_all_confirmation(False)
        assert self.session_manager.get_clear_all_confirmation() is False
    
    def test_validate_construction_entry_valid(self):
        """Test validating valid construction entry."""
        is_valid, error_message = self.session_manager.validate_construction_entry(
            'Test Building', 100.0, 60.0, 30
        )
        
        assert is_valid
        assert error_message == ""
    
    def test_validate_construction_entry_invalid(self):
        """Test validating invalid construction entry."""
        # Test empty description
        is_valid, error_message = self.session_manager.validate_construction_entry(
            '', 100.0, 60.0, 30
        )
        assert not is_valid
        assert "Description is required" in error_message
        
        # Test zero power
        is_valid, error_message = self.session_manager.validate_construction_entry(
            'Test Building', 0.0, 60.0, 30
        )
        assert not is_valid
        assert "Power must be greater than 0" in error_message
        
        # Test negative speedup
        is_valid, error_message = self.session_manager.validate_construction_entry(
            'Test Building', 100.0, -10.0, 30
        )
        assert not is_valid
        assert "Speed-up minutes cannot be negative" in error_message
        
        # Test invalid points per power
        is_valid, error_message = self.session_manager.validate_construction_entry(
            'Test Building', 100.0, 60.0, 50
        )
        assert not is_valid
        assert "Points per power must be 30 or 45" in error_message
    
    def test_validate_research_entry_valid(self):
        """Test validating valid research entry."""
        is_valid, error_message = self.session_manager.validate_research_entry(
            'Test Research', 50.0, 120.0, 45
        )
        
        assert is_valid
        assert error_message == ""
    
    def test_validate_research_entry_invalid(self):
        """Test validating invalid research entry."""
        # Test empty description
        is_valid, error_message = self.session_manager.validate_research_entry(
            '', 50.0, 120.0, 45
        )
        assert not is_valid
        assert "Description is required" in error_message
        
        # Test zero power
        is_valid, error_message = self.session_manager.validate_research_entry(
            'Test Research', 0.0, 120.0, 45
        )
        assert not is_valid
        assert "Power must be greater than 0" in error_message
    
    def test_validate_training_entry_valid(self):
        """Test validating valid training entry."""
        is_valid, error_message = self.session_manager.validate_training_entry(
            'Test Training', 0, 2, 30, 0, 426, 830.0
        )
        
        assert is_valid
        assert error_message == ""
    
    def test_validate_training_entry_invalid(self):
        """Test validating invalid training entry."""
        # Test empty description
        is_valid, error_message = self.session_manager.validate_training_entry(
            '', 0, 2, 30, 0, 426, 830.0
        )
        assert not is_valid
        assert "Description is required" in error_message
        
        # Test zero troops per batch
        is_valid, error_message = self.session_manager.validate_training_entry(
            'Test Training', 0, 2, 30, 0, 0, 830.0
        )
        assert not is_valid
        assert "Troops per batch must be greater than 0" in error_message
        
        # Test zero points per troop
        is_valid, error_message = self.session_manager.validate_training_entry(
            'Test Training', 0, 2, 30, 0, 426, 0.0
        )
        assert not is_valid
        assert "Points per troop must be greater than 0" in error_message
        
        # Test negative time values
        is_valid, error_message = self.session_manager.validate_training_entry(
            'Test Training', -1, 2, 30, 0, 426, 830.0
        )
        assert not is_valid
        assert "Time values cannot be negative" in error_message
        
        # Test zero total time
        is_valid, error_message = self.session_manager.validate_training_entry(
            'Test Training', 0, 0, 0, 0, 426, 830.0
        )
        assert not is_valid
        assert "At least some time must be specified" in error_message


class TestGetSessionManager:
    """Test the get_session_manager function."""
    
    def test_get_session_manager_singleton(self):
        """Test that get_session_manager returns the same instance."""
        with patch('streamlit.session_state', {}):
            manager1 = get_session_manager()
            manager2 = get_session_manager()
            
            assert manager1 is manager2 