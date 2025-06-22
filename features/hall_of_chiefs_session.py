"""
Hall of Chiefs Session State Abstraction Layer
Manages all session state interactions for Hall of Chiefs data.
"""

import streamlit as st
from typing import Dict, List, Any, Optional, Tuple
from features.hall_of_chiefs_data import get_data_manager, CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY


class HallOfChiefsSessionManager:
    """Manages session state for Hall of Chiefs data with persistence sync."""
    
    def __init__(self):
        """Initialize the session manager."""
        self.data_manager = get_data_manager()
        self._init_session_state()
    
    def _init_session_state(self) -> None:
        """Initialize session state variables."""
        # Main data storage
        if 'hall_of_chiefs_data' not in st.session_state:
            st.session_state['hall_of_chiefs_data'] = {
                CONSTRUCTION_CATEGORY: [],
                RESEARCH_CATEGORY: [],
                TRAINING_CATEGORY: []
            }
        
        # UI state flags
        if 'hall_of_chiefs_clear_inputs' not in st.session_state:
            st.session_state['hall_of_chiefs_clear_inputs'] = {
                CONSTRUCTION_CATEGORY: False,
                RESEARCH_CATEGORY: False,
                TRAINING_CATEGORY: False
            }
        
        # Confirmation states
        if 'hall_of_chiefs_delete_confirm' not in st.session_state:
            st.session_state['hall_of_chiefs_delete_confirm'] = {
                'entry_id': None,
                'category': None
            }
        
        if 'hall_of_chiefs_clear_all_confirm' not in st.session_state:
            st.session_state['hall_of_chiefs_clear_all_confirm'] = False
        
        # Load data from persistence on first init
        if 'hall_of_chiefs_data_loaded' not in st.session_state:
            self._load_data_from_persistence()
            st.session_state['hall_of_chiefs_data_loaded'] = True
    
    def _load_data_from_persistence(self) -> None:
        """Load data from persistence layer into session state."""
        try:
            all_entries = self.data_manager.get_all_entries()
            st.session_state['hall_of_chiefs_data'] = all_entries
        except Exception as e:
            st.error(f"Failed to load data from persistence: {str(e)}")
            # Initialize with empty data if loading fails
            st.session_state['hall_of_chiefs_data'] = {
                CONSTRUCTION_CATEGORY: [],
                RESEARCH_CATEGORY: [],
                TRAINING_CATEGORY: []
            }
    
    def get_entries(self, category: str) -> List[Dict[str, Any]]:
        """
        Get entries for a specific category from session state.
        
        Args:
            category (str): Category to retrieve entries for
            
        Returns:
            List[Dict[str, Any]]: List of entries for the category
        """
        if category not in [CONSTRUCTION_CATEGORY, RESEARCH_CATEGORY, TRAINING_CATEGORY]:
            raise ValueError(f"Invalid category: {category}")
        
        return st.session_state['hall_of_chiefs_data'].get(category, [])
    
    def get_all_entries(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Get all entries from all categories.
        
        Returns:
            Dict[str, List[Dict[str, Any]]]: All entries organized by category
        """
        return st.session_state['hall_of_chiefs_data'].copy()
    
    def add_entry(self, category: str, entry: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Add a new entry to a category.
        
        Args:
            category (str): Category to add entry to
            entry (Dict[str, Any]): Entry data
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Add to persistence
        success, message = self.data_manager.add_entry(category, entry)
        
        if success:
            # Reload data from persistence to get the new entry with ID and timestamp
            self._load_data_from_persistence()
            # Set flag to clear inputs
            st.session_state['hall_of_chiefs_clear_inputs'][category] = True
        
        return success, message
    
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
        # Update in persistence
        success, message = self.data_manager.update_entry(category, entry_id, updated_entry)
        
        if success:
            # Reload data from persistence
            self._load_data_from_persistence()
        
        return success, message
    
    def delete_entry(self, category: str, entry_id: str) -> Tuple[bool, str]:
        """
        Delete an entry.
        
        Args:
            category (str): Category of the entry
            entry_id (str): ID of the entry to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Delete from persistence
        success, message = self.data_manager.delete_entry(category, entry_id)
        
        if success:
            # Reload data from persistence
            self._load_data_from_persistence()
        
        return success, message
    
    def delete_all_entries(self, category: Optional[str] = None) -> Tuple[bool, str]:
        """
        Delete all entries from a category or all categories.
        
        Args:
            category (Optional[str]): Category to clear, or None for all categories
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        # Delete from persistence
        success, message = self.data_manager.delete_all_entries(category)
        
        if success:
            # Reload data from persistence
            self._load_data_from_persistence()
        
        return success, message
    
    def get_entry_count(self, category: Optional[str] = None) -> Dict[str, int]:
        """
        Get entry counts by category.
        
        Args:
            category (Optional[str]): Specific category, or None for all
            
        Returns:
            Dict[str, int]: Entry counts by category
        """
        if category:
            entries = self.get_entries(category)
            return {category: len(entries)}
        
        all_entries = self.get_all_entries()
        return {cat: len(entries) for cat, entries in all_entries.items()}
    
    def should_clear_inputs(self, category: str) -> bool:
        """
        Check if inputs should be cleared for a category.
        
        Args:
            category (str): Category to check
            
        Returns:
            bool: True if inputs should be cleared
        """
        return st.session_state['hall_of_chiefs_clear_inputs'].get(category, False)
    
    def reset_clear_inputs_flag(self, category: str) -> None:
        """
        Reset the clear inputs flag for a category.
        
        Args:
            category (str): Category to reset flag for
        """
        st.session_state['hall_of_chiefs_clear_inputs'][category] = False
    
    def set_delete_confirmation(self, entry_id: str, category: str) -> None:
        """
        Set delete confirmation state for an entry.
        
        Args:
            entry_id (str): ID of entry to delete
            category (str): Category of the entry
        """
        st.session_state['hall_of_chiefs_delete_confirm'] = {
            'entry_id': entry_id,
            'category': category
        }
    
    def get_delete_confirmation(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get current delete confirmation state.
        
        Returns:
            Tuple[Optional[str], Optional[str]]: (entry_id, category) or (None, None)
        """
        confirm = st.session_state['hall_of_chiefs_delete_confirm']
        return confirm.get('entry_id'), confirm.get('category')
    
    def clear_delete_confirmation(self) -> None:
        """Clear delete confirmation state."""
        st.session_state['hall_of_chiefs_delete_confirm'] = {
            'entry_id': None,
            'category': None
        }
    
    def set_clear_all_confirmation(self, confirmed: bool) -> None:
        """
        Set clear all confirmation state.
        
        Args:
            confirmed (bool): Whether to show confirmation dialog
        """
        st.session_state['hall_of_chiefs_clear_all_confirm'] = confirmed
    
    def get_clear_all_confirmation(self) -> bool:
        """
        Get clear all confirmation state.
        
        Returns:
            bool: True if confirmation dialog should be shown
        """
        return st.session_state['hall_of_chiefs_clear_all_confirm']
    
    def refresh_data(self) -> None:
        """Refresh data from persistence layer."""
        self._load_data_from_persistence()
    
    def validate_construction_entry(self, description: str, power: float, speedup_minutes: float, points_per_power: int) -> Tuple[bool, str]:
        """
        Validate construction entry inputs.
        
        Args:
            description (str): Entry description
            power (float): Power value
            speedup_minutes (float): Speed-up minutes
            points_per_power (int): Points per power
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not description.strip():
            return False, "Description is required"
        
        if power <= 0:
            return False, "Power must be greater than 0"
        
        if speedup_minutes < 0:
            return False, "Speed-up minutes cannot be negative"
        
        if points_per_power not in [30, 45]:
            return False, "Points per power must be 30 or 45"
        
        return True, ""
    
    def validate_research_entry(self, description: str, power: float, speedup_minutes: float, points_per_power: int) -> Tuple[bool, str]:
        """
        Validate research entry inputs.
        
        Args:
            description (str): Entry description
            power (float): Power value
            speedup_minutes (float): Speed-up minutes
            points_per_power (int): Points per power
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not description.strip():
            return False, "Description is required"
        
        if power <= 0:
            return False, "Power must be greater than 0"
        
        if speedup_minutes < 0:
            return False, "Speed-up minutes cannot be negative"
        
        if points_per_power not in [30, 45]:
            return False, "Points per power must be 30 or 45"
        
        return True, ""
    
    def validate_training_entry(self, description: str, days: int, hours: int, minutes: int, seconds: int, 
                               troops_per_batch: int, points_per_troop: float) -> Tuple[bool, str]:
        """
        Validate training entry inputs.
        
        Args:
            description (str): Entry description
            days (int): Days
            hours (int): Hours
            minutes (int): Minutes
            seconds (int): Seconds
            troops_per_batch (int): Troops per batch
            points_per_troop (float): Points per troop
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not description.strip():
            return False, "Description is required"
        
        if troops_per_batch <= 0:
            return False, "Troops per batch must be greater than 0"
        
        if points_per_troop <= 0:
            return False, "Points per troop must be greater than 0"
        
        if days < 0 or hours < 0 or minutes < 0 or seconds < 0:
            return False, "Time values cannot be negative"
        
        # Check if at least some time is specified
        total_time = (days * 24 * 60) + (hours * 60) + minutes + (seconds / 60)
        if total_time <= 0:
            return False, "At least some time must be specified"
        
        return True, ""


# Global instance for easy access
_session_manager = None

def get_session_manager() -> HallOfChiefsSessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        HallOfChiefsSessionManager: Global session manager instance
    """
    global _session_manager
    if _session_manager is None:
        _session_manager = HallOfChiefsSessionManager()
    return _session_manager 