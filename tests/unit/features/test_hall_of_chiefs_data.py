"""
Unit tests for Hall of Chiefs Data Management Module.
"""

import pytest
import json
import os
import tempfile
from unittest.mock import patch, mock_open
from features.hall_of_chiefs_data import (
    HallOfChiefsDataManager,
    get_data_manager,
    CONSTRUCTION_CATEGORY,
    RESEARCH_CATEGORY,
    TRAINING_CATEGORY
)


class TestHallOfChiefsDataManager:
    """Test the HallOfChiefsDataManager class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_dir = tempfile.mkdtemp()
        self.test_data_file = os.path.join(self.temp_dir, "test_hall_of_chiefs_data.json")
        self.data_manager = HallOfChiefsDataManager(self.test_data_file)
    
    def teardown_method(self):
        """Clean up test fixtures."""
        # Remove temporary files
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)
    
    def test_init_creates_data_file(self):
        """Test that initialization creates the data file with proper structure."""
        assert os.path.exists(self.test_data_file)
        
        with open(self.test_data_file, 'r') as f:
            data = json.load(f)
        
        assert CONSTRUCTION_CATEGORY in data
        assert RESEARCH_CATEGORY in data
        assert TRAINING_CATEGORY in data
        assert "metadata" in data
        assert data[CONSTRUCTION_CATEGORY] == []
        assert data[RESEARCH_CATEGORY] == []
        assert data[TRAINING_CATEGORY] == []
    
    def test_add_construction_entry_valid(self):
        """Test adding a valid construction entry."""
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        
        success, message = self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert success
        assert "added successfully" in message
        
        # Verify entry was added
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Test Building'
        assert entries[0]['power'] == 100.0
        assert 'id' in entries[0]
        assert 'created_at' in entries[0]
    
    def test_add_research_entry_valid(self):
        """Test adding a valid research entry."""
        entry = {
            'description': 'Test Research',
            'power': 50.0,
            'speedup_minutes': 120.0,
            'points_per_power': 45
        }
        
        success, message = self.data_manager.add_entry(RESEARCH_CATEGORY, entry)
        
        assert success
        assert "added successfully" in message
        
        # Verify entry was added
        entries = self.data_manager.get_entries(RESEARCH_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Test Research'
        assert entries[0]['power'] == 50.0
        assert entries[0]['points_per_power'] == 45
    
    def test_add_training_entry_valid(self):
        """Test adding a valid training entry."""
        entry = {
            'description': 'Test Training',
            'days': 0,
            'hours': 2,
            'minutes': 30,
            'seconds': 0,
            'troops_per_batch': 426,
            'points_per_troop': 830.0
        }
        
        success, message = self.data_manager.add_entry(TRAINING_CATEGORY, entry)
        
        assert success
        assert "added successfully" in message
        
        # Verify entry was added
        entries = self.data_manager.get_entries(TRAINING_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Test Training'
        assert entries[0]['troops_per_batch'] == 426
        assert entries[0]['points_per_troop'] == 830.0
    
    def test_add_entry_invalid_category(self):
        """Test adding entry with invalid category."""
        entry = {'description': 'Test'}
        
        success, message = self.data_manager.add_entry('invalid_category', entry)
        
        assert not success
        assert "Invalid category" in message
    
    def test_add_construction_entry_invalid_power(self):
        """Test adding construction entry with invalid power."""
        entry = {
            'description': 'Test Building',
            'power': 0.0,  # Invalid: power must be > 0
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        
        success, message = self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert not success
        assert "Power must be greater than 0" in message
    
    def test_add_construction_entry_invalid_points_per_power(self):
        """Test adding construction entry with invalid points per power."""
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 50  # Invalid: must be 30 or 45
        }
        
        success, message = self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert not success
        assert "Points per power must be 30 or 45" in message
    
    def test_add_training_entry_invalid_troops_per_batch(self):
        """Test adding training entry with invalid troops per batch."""
        entry = {
            'description': 'Test Training',
            'days': 0,
            'hours': 2,
            'minutes': 30,
            'seconds': 0,
            'troops_per_batch': 0,  # Invalid: must be > 0
            'points_per_troop': 830.0
        }
        
        success, message = self.data_manager.add_entry(TRAINING_CATEGORY, entry)
        
        assert not success
        assert "Troops per batch must be greater than 0" in message
    
    def test_add_entry_missing_required_field(self):
        """Test adding entry with missing required field."""
        entry = {
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
            # Missing 'description'
        }
        
        success, message = self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        assert not success
        assert "Missing required field: description" in message
    
    def test_get_entries_empty(self):
        """Test getting entries from empty category."""
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        assert entries == []
    
    def test_get_all_entries(self):
        """Test getting all entries from all categories."""
        # Add entries to different categories
        construction_entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        research_entry = {
            'description': 'Test Research',
            'power': 50.0,
            'speedup_minutes': 120.0,
            'points_per_power': 45
        }
        
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, construction_entry)
        self.data_manager.add_entry(RESEARCH_CATEGORY, research_entry)
        
        all_entries = self.data_manager.get_all_entries()
        
        assert len(all_entries[CONSTRUCTION_CATEGORY]) == 1
        assert len(all_entries[RESEARCH_CATEGORY]) == 1
        assert len(all_entries[TRAINING_CATEGORY]) == 0
    
    def test_update_entry_valid(self):
        """Test updating an existing entry."""
        # Add an entry first
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        # Get the entry ID
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        entry_id = entries[0]['id']
        
        # Update the entry
        updated_entry = {
            'description': 'Updated Building',
            'power': 150.0,
            'speedup_minutes': 90.0,
            'points_per_power': 45
        }
        
        success, message = self.data_manager.update_entry(CONSTRUCTION_CATEGORY, entry_id, updated_entry)
        
        assert success
        assert "updated successfully" in message
        
        # Verify entry was updated
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        assert entries[0]['description'] == 'Updated Building'
        assert entries[0]['power'] == 150.0
        assert entries[0]['points_per_power'] == 45
        assert 'updated_at' in entries[0]
    
    def test_update_entry_not_found(self):
        """Test updating a non-existent entry."""
        updated_entry = {
            'description': 'Updated Building',
            'power': 150.0,
            'speedup_minutes': 90.0,
            'points_per_power': 45
        }
        
        success, message = self.data_manager.update_entry(CONSTRUCTION_CATEGORY, 'non_existent_id', updated_entry)
        
        assert not success
        assert "not found" in message
    
    def test_delete_entry_valid(self):
        """Test deleting an existing entry."""
        # Add an entry first
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        # Get the entry ID
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        entry_id = entries[0]['id']
        
        # Delete the entry
        success, message = self.data_manager.delete_entry(CONSTRUCTION_CATEGORY, entry_id)
        
        assert success
        assert "deleted successfully" in message
        
        # Verify entry was deleted
        entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        assert len(entries) == 0
    
    def test_delete_entry_not_found(self):
        """Test deleting a non-existent entry."""
        success, message = self.data_manager.delete_entry(CONSTRUCTION_CATEGORY, 'non_existent_id')
        
        assert not success
        assert "not found" in message
    
    def test_delete_all_entries_specific_category(self):
        """Test deleting all entries from a specific category."""
        # Add entries to different categories
        construction_entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        research_entry = {
            'description': 'Test Research',
            'power': 50.0,
            'speedup_minutes': 120.0,
            'points_per_power': 45
        }
        
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, construction_entry)
        self.data_manager.add_entry(RESEARCH_CATEGORY, research_entry)
        
        # Delete all construction entries
        success, message = self.data_manager.delete_all_entries(CONSTRUCTION_CATEGORY)
        
        assert success
        assert "deleted" in message
        
        # Verify only construction entries were deleted
        construction_entries = self.data_manager.get_entries(CONSTRUCTION_CATEGORY)
        research_entries = self.data_manager.get_entries(RESEARCH_CATEGORY)
        
        assert len(construction_entries) == 0
        assert len(research_entries) == 1
    
    def test_delete_all_entries_all_categories(self):
        """Test deleting all entries from all categories."""
        # Add entries to different categories
        construction_entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        research_entry = {
            'description': 'Test Research',
            'power': 50.0,
            'speedup_minutes': 120.0,
            'points_per_power': 45
        }
        
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, construction_entry)
        self.data_manager.add_entry(RESEARCH_CATEGORY, research_entry)
        
        # Delete all entries
        success, message = self.data_manager.delete_all_entries()
        
        assert success
        assert "all categories" in message
        
        # Verify all entries were deleted
        all_entries = self.data_manager.get_all_entries()
        assert len(all_entries[CONSTRUCTION_CATEGORY]) == 0
        assert len(all_entries[RESEARCH_CATEGORY]) == 0
        assert len(all_entries[TRAINING_CATEGORY]) == 0
    
    def test_get_entry_count(self):
        """Test getting entry counts."""
        # Add entries
        construction_entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        research_entry = {
            'description': 'Test Research',
            'power': 50.0,
            'speedup_minutes': 120.0,
            'points_per_power': 45
        }
        
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, construction_entry)
        self.data_manager.add_entry(RESEARCH_CATEGORY, research_entry)
        
        # Test specific category count
        construction_count = self.data_manager.get_entry_count(CONSTRUCTION_CATEGORY)
        assert construction_count[CONSTRUCTION_CATEGORY] == 1
        
        # Test all categories count
        all_counts = self.data_manager.get_entry_count()
        assert all_counts[CONSTRUCTION_CATEGORY] == 1
        assert all_counts[RESEARCH_CATEGORY] == 1
        assert all_counts[TRAINING_CATEGORY] == 0
    
    def test_backup_data(self):
        """Test creating a backup of the data."""
        # Add some data
        entry = {
            'description': 'Test Building',
            'power': 100.0,
            'speedup_minutes': 60.0,
            'points_per_power': 30
        }
        self.data_manager.add_entry(CONSTRUCTION_CATEGORY, entry)
        
        # Create backup
        backup_path = os.path.join(self.temp_dir, "backup.json")
        success, message = self.data_manager.backup_data(backup_path)
        
        assert success
        assert "Backup created successfully" in message
        assert os.path.exists(backup_path)
        
        # Verify backup contains the same data
        with open(backup_path, 'r') as f:
            backup_data = json.load(f)
        
        with open(self.test_data_file, 'r') as f:
            original_data = json.load(f)
        
        assert backup_data == original_data
        
        # Clean up backup
        os.remove(backup_path)
    
    def test_read_data_file_not_found(self):
        """Test reading data when file doesn't exist."""
        # Remove the file
        os.remove(self.test_data_file)
        
        # Reading should recreate the file
        data = self.data_manager._read_data()
        assert CONSTRUCTION_CATEGORY in data
        assert RESEARCH_CATEGORY in data
        assert TRAINING_CATEGORY in data
    
    def test_read_data_invalid_json(self):
        """Test reading data with invalid JSON."""
        # Write invalid JSON to file
        with open(self.test_data_file, 'w') as f:
            f.write("invalid json")
        
        # Reading should raise an error
        with pytest.raises(ValueError, match="Invalid JSON"):
            self.data_manager._read_data()

    def test_add_training_entry_with_zero_time(self):
        """Test adding training entry with zero training time."""
        entry = {
            'description': 'Test Training',
            'days': 0,
            'hours': 0,
            'minutes': 0,
            'seconds': 0,
            'troops_per_batch': 100,
            'points_per_troop': 50.0
        }
        
        success, message = self.data_manager.add_entry(TRAINING_CATEGORY, entry)
        assert success
        assert "added successfully" in message
        
        # Verify entry was added despite zero time
        entries = self.data_manager.get_entries(TRAINING_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Test Training'
    
    def test_add_training_entry_with_negative_time(self):
        """Test adding training entry with negative time components."""
        entry = {
            'description': 'Test Training',
            'days': 0,
            'hours': -1,  # Invalid negative hours
            'minutes': 30,
            'seconds': 0,
            'troops_per_batch': 100,
            'points_per_troop': 50.0
        }
        
        success, message = self.data_manager.add_entry(TRAINING_CATEGORY, entry)
        assert not success
        assert "Time values cannot be negative" in message
    
    def test_add_training_entry_with_valid_time(self):
        """Test adding training entry with valid training time."""
        entry = {
            'description': 'Valid Training',
            'days': 0,
            'hours': 2,
            'minutes': 30,
            'seconds': 0,
            'troops_per_batch': 100,
            'points_per_troop': 50.0
        }
        
        success, message = self.data_manager.add_entry(TRAINING_CATEGORY, entry)
        assert success
        assert "added successfully" in message
        
        # Verify entry was added
        entries = self.data_manager.get_entries(TRAINING_CATEGORY)
        assert len(entries) == 1
        assert entries[0]['description'] == 'Valid Training'
        assert entries[0]['hours'] == 2
        assert entries[0]['minutes'] == 30


class TestGetDataManager:
    """Test the get_data_manager function."""
    
    def test_get_data_manager_singleton(self):
        """Test that get_data_manager returns the same instance."""
        manager1 = get_data_manager()
        manager2 = get_data_manager()
        
        assert manager1 is manager2
    
    def test_get_data_manager_creates_file(self):
        """Test that get_data_manager creates the data file."""
        # Use a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Remove the file so it doesn't exist
            if os.path.exists(temp_file):
                os.remove(temp_file)
            
            # Create manager with temporary file
            manager = HallOfChiefsDataManager(temp_file)
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Verify file has proper structure
            with open(temp_file, 'r') as f:
                data = json.load(f)
            
            assert CONSTRUCTION_CATEGORY in data
            assert RESEARCH_CATEGORY in data
            assert TRAINING_CATEGORY in data
        finally:
            # Clean up
            if os.path.exists(temp_file):
                os.remove(temp_file) 