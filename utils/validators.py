"""
Utility functions for input validation.
"""

from typing import Dict, Any, Tuple

def validate_speedup_inputs(
    current_level: int,
    target_level: int,
    current_points: float,
    speedup_categories: Dict[str, Dict[str, Any]]
) -> Tuple[bool, str]:
    """
    Validate speedup calculation inputs.
    
    Args:
        current_level (int): Current training level
        target_level (int): Target training level
        current_points (float): Current training points
        speedup_categories (Dict): Speedup category configurations
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if current_level < 0 or target_level < 0:
        return False, "Levels cannot be negative"
    
    if current_level > target_level:
        return False, "Current level cannot be higher than target level"
    
    if current_points < 0:
        return False, "Points cannot be negative"
    
    for category, config in speedup_categories.items():
        if config['cost'] < 0:
            return False, f"Cost for {category} cannot be negative"
        if config['points'] < 0:
            return False, f"Points for {category} cannot be negative"
    
    return True, ""

def validate_pack_purchase(
    date: str,
    pack_name: str,
    spending: float,
    speedups: Dict[str, int]
) -> Tuple[bool, str]:
    """
    Validate pack purchase inputs.
    
    Args:
        date (str): Purchase date
        pack_name (str): Name of the pack
        spending (float): Amount spent
        speedups (Dict): Speedups included in pack
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if not date:
        return False, "Date is required"
    
    if not pack_name:
        return False, "Pack name is required"
    
    if spending <= 0:
        return False, "Spending must be greater than 0"
    
    for category, amount in speedups.items():
        if amount < 0:
            return False, f"Speedup amount for {category} cannot be negative"
    
    return True, "" 