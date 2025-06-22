"""
Hall of Chiefs Data Management Module
Handles CRUD operations and JSON persistence for Hall of Chiefs entries.
"""

import json
import os
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import streamlit as st

# Constants
HALL_OF_CHIEFS_DATA_FILE = "data/hall_of_chiefs_data.json"
CONSTRUCTION_CATEGORY = "construction"
RESEARCH_CATEGORY = "research"
TRAINING_CATEGORY = "training"

# Data structure for entries
ENTRY_SCHEMA = {
    CONSTRUCTION_CATEGORY: {
        "description": str,
        "power": float,
        "speedup_minutes": float,
        "points_per_power": int
    },
    RESEARCH_CATEGORY: {
        "description": str,
        "power": float,
        "speedup_minutes": float,
        "points_per_power": int
    },
    TRAINING_CATEGORY: {
        "description": str,
        "days": int,
        "hours": int,
        "minutes": int,
        "seconds": int,
        "troops_per_batch": int,
        "points_per_troop": float
    }
}


class HallOfChiefsDataManager:
    """Manages Hall of Chiefs data persistence and CRUD operations."""
    
    def __init__(self, data_file: str = HALL_OF_CHIEFS_DATA_FILE):
        """
        Initialize the data manager.
        
        Args:
            data_file (str): Path to the JSON data file
        """
        self.data_file = data_file
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self) -> None:
        """Ensure the data file exists with proper structure."""
        if not os.path.exists(self.data_file):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Initialize with empty structure
            initial_data = {
                CONSTRUCTION_CATEGORY: [],
                RESEARCH_CATEGORY: [],
                TRAINING_CATEGORY: [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
            self._write_data(initial_data)
    
    def _read_data(self) -> Dict[str, Any]:
        """
        Read data from JSON file.
        
        Returns:
            Dict[str, Any]: Data from file
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            json.JSONDecodeError: If JSON is malformed
        """
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Recreate file if it doesn't exist
            self._ensure_data_file_exists()
            return self._read_data()
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in data file: {e}")
    
    def _write_data(self, data: Dict[str, Any]) -> None:
        """
        Write data to JSON file.
        
        Args:
            data (Dict[str, Any]): Data to write
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _validate_entry(self, category: str, entry: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate an entry against the schema.
        
        Args:
            category (str): Entry category
            entry (Dict[str, Any]): Entry data
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if category not in ENTRY_SCHEMA:
            return False, f"Invalid category: {category}"
        
        schema = ENTRY_SCHEMA[category]
        
        # Check required fields
        for field, expected_type in schema.items():
            if field not in entry:
                return False, f"Missing required field: {field}"
            
            if not isinstance(entry[field], expected_type):
                return False, f"Invalid type for {field}: expected {expected_type.__name__}, got {type(entry[field]).__name__}"
        
        # Additional validation
        if category in [CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY]:
            if entry['power'] <= 0:
                return False, "Power must be greater than 0"
            if entry['speedup_minutes'] < 0:
                return False, "Speed-up minutes cannot be negative"
            if entry['points_per_power'] not in [30, 45]:
                return False, "Points per power must be 30 or 45"
        
        elif category == TRAINING_CATEGORY:
            if entry['troops_per_batch'] <= 0:
                return False, "Troops per batch must be greater than 0"
            if entry['points_per_troop'] <= 0:
                return False, "Points per troop must be greater than 0"
            if entry['days'] < 0 or entry['hours'] < 0 or entry['minutes'] < 0 or entry['seconds'] < 0:
                return False, "Time values cannot be negative"
        
        return True, ""
    
    def get_all_entries(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all entries from all categories.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: All entries organized by category
        """
        data = self._read_data()
        return {
            CONSTRUCTION_CATEGORY: data.get(CONSTRUCTION_CATEGORY, []),
            RESEARCH_CATEGORY: data.get(RESEARCH_CATEGORY, []),
            TRAINING_CATEGORY: data.get(TRAINING_CATEGORY, [])
        }
    
    def get_entries(self, category: str) -> List[Dict[str, Any]]:
        """
        Get entries for a specific category.
        
        Args:
            category (str): Category to retrieve entries for
            
        Returns:
            List[Dict[str, Any]]: List of entries for the category
        """
        if category not in [CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY]:
            raise ValueError(f"Invalid category: {category}")
        
        data = self._read_data()
        return data.get(category, [])
    
    def add_entry(self, category: str, entry: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Add a new entry to a category.
        
        Args:
            category (str): Category to add entry to
            entry (Dict[str, Any]): Entry data
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Validate entry
        is_valid, error_message = self._validate_entry(category, entry)
        if not is_valid:
            return False, error_message
        
        # Add timestamp
        entry_with_timestamp = entry.copy()
        entry_with_timestamp['created_at'] = datetime.now().isoformat()
        entry_with_timestamp['id'] = self._generate_entry_id(category)
        
        # Read current data
        data = self._read_data()
        
        # Add entry
        if category not in data:
            data[category] = []
        data[category].append(entry_with_timestamp)
        
        # Write back to file
        try:
            self._write_data(data)
            return True, f"Entry added successfully to {category}"
        except Exception as e:
            return False, f"Failed to save entry: {str(e)}"
    
    def update_entry(self, category: str, entry_id: str, updated_entry: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Update an existing entry.
        
        Args:
            category (str): Category of the entry
            entry_id (str): ID of the entry to update
            updated_entry (Dict[str, Any]): Updated entry data
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Validate entry
        is_valid, error_message = self._validate_entry(category, updated_entry)
        if not is_valid:
            return False, error_message
        
        # Read current data
        data = self._read_data()
        
        if category not in data:
            return False, f"Category {category} not found"
        
        # Find and update entry
        for i, entry in enumerate(data[category]):
            if entry.get('id') == entry_id:
                # Preserve timestamp and ID
                updated_entry_with_metadata = updated_entry.copy()
                updated_entry_with_metadata['created_at'] = entry.get('created_at')
                updated_entry_with_metadata['id'] = entry_id
                updated_entry_with_metadata['updated_at'] = datetime.now().isoformat()
                
                data[category][i] = updated_entry_with_metadata
                
                try:
                    self._write_data(data)
                    return True, "Entry updated successfully"
                except Exception as e:
                    return False, f"Failed to save updated entry: {str(e)}"
        
        return False, f"Entry with ID {entry_id} not found"
    
    def delete_entry(self, category: str, entry_id: str) -> Tuple[bool, str]:
        """
        Delete an entry.
        
        Args:
            category (str): Category of the entry
            entry_id (str): ID of the entry to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Read current data
        data = self._read_data()
        
        if category not in data:
            return False, f"Category {category} not found"
        
        # Find and remove entry
        for i, entry in enumerate(data[category]):
            if entry.get('id') == entry_id:
                del data[category][i]
                
                try:
                    self._write_data(data)
                    return True, "Entry deleted successfully"
                except Exception as e:
                    return False, f"Failed to delete entry: {str(e)}"
        
        return False, f"Entry with ID {entry_id} not found"
    
    def delete_all_entries(self, category: Optional[str] = None) -> Tuple[bool, str]:
        """
        Delete all entries from a category or all categories.
        
        Args:
            category (Optional[str]): Category to clear, or None for all categories
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        data = self._read_data()
        
        if category:
            if category not in [CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY]:
                return False, f"Invalid category: {category}"
            data[category] = []
            message = f"All entries from {category} deleted"
        else:
            data[CONSTRUCTION_CATEGORY] = []
            data[RESEARCH_CATEGORY] = []
            data[TRAINING_CATEGORY] = []
            message = "All entries from all categories deleted"
        
        try:
            self._write_data(data)
            return True, message
        except Exception as e:
            return False, f"Failed to delete entries: {str(e)}"
    
    def _generate_entry_id(self, category: str) -> str:
        """
        Generate a unique ID for an entry.
        
        Args:
            category (str): Category of the entry
            
        Returns:
            str: Unique entry ID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        return f"{category}_{timestamp}"
    
    def get_entry_count(self, category: Optional[str] = None) -> Dict[str, int]:
        """
        Get entry counts by category.
        
        Args:
            category (Optional[str]): Specific category, or None for all
            
        Returns:
            Dict[str, int]: Entry counts by category
        """
        data = self._read_data()
        
        if category:
            if category not in [CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY]:
                raise ValueError(f"Invalid category: {category}")
            return {category: len(data.get(category, []))}
        
        return {
            CONSTRUCTION_CATEGORY: len(data.get(CONSTRUCTION_CATEGORY, [])),
            RESEARCH_CATEGORY: len(data.get(RESEARCH_CATEGORY, [])),
            TRAINING_CATEGORY: len(data.get(TRAINING_CATEGORY, []))
        }
    
    def backup_data(self, backup_path: str) -> Tuple[bool, str]:
        """
        Create a backup of the data file.
        
        Args:
            backup_path (str): Path for the backup file
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            data = self._read_data()
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True, f"Backup created successfully at {backup_path}"
        except Exception as e:
            return False, f"Failed to create backup: {str(e)}"
    
    def persist_speedup_inventory(self, inventory: Dict[str, float]) -> None:
        """
        Persist the speedup inventory to the JSON file under the 'metadata' section.
        Args:
            inventory (Dict[str, float]): The speedup inventory to persist
        """
        data = self._read_data()
        if 'metadata' not in data:
            data['metadata'] = {}
        data['metadata']['speedup_inventory'] = inventory
        self._write_data(data)


# Global instance for easy access
_data_manager = None

def get_data_manager() -> HallOfChiefsDataManager:
    """
    Get the global data manager instance.
    
    Returns:
        HallOfChiefsDataManager: Global data manager instance
    """
    global _data_manager
    if _data_manager is None:
        _data_manager = HallOfChiefsDataManager()
    return _data_manager 