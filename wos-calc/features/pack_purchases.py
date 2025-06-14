"""
Module for managing pack purchase tracking and calculations.
"""

from typing import Dict, List
import pandas as pd
from datetime import datetime

def add_purchase(
    purchases: List[Dict],
    date: datetime,
    pack_name: str,
    spending: float,
    speedups: int
) -> List[Dict]:
    """
    Add a new purchase to the purchase history.
    
    Args:
        purchases (List[Dict]): Current list of purchases
        date (datetime): Date of purchase
        pack_name (str): Name of the pack
        spending (float): Amount spent
        speedups (int): Number of speed-ups included
    
    Returns:
        List[Dict]: Updated list of purchases
    """
    new_purchase = {
        "Date": date,
        "Pack Name": pack_name,
        "Spending ($)": spending,
        "Speed-ups (min)": speedups
    }
    return purchases + [new_purchase]

def get_purchase_summary(purchases: List[Dict]) -> Dict[str, float]:
    """
    Calculate summary metrics for purchases.
    
    Args:
        purchases (List[Dict]): List of purchases
    
    Returns:
        Dict[str, float]: Summary metrics
    """
    if not purchases:
        return {"total_spent": 0.0, "total_speedups": 0}
    
    df = pd.DataFrame(purchases)
    return {
        "total_spent": df["Spending ($)"].sum(),
        "total_speedups": df["Speed-ups (min)"].sum()
    }

def clear_purchases() -> List[Dict]:
    """
    Clear all purchases.
    
    Returns:
        List[Dict]: Empty list
    """
    return [] 