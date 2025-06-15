"""
Core calculation module for training times, points, and efficiency metrics.
"""

from typing import Dict, Tuple
import numpy as np

def calculate_effective_training_time(
    base_time: float,
    time_reduction_bonus: float
) -> float:
    """
    Calculate the effective training time after applying reduction bonuses.
    
    Args:
        base_time (float): Base training time in minutes
        time_reduction_bonus (float): Training time reduction bonus as a decimal
    
    Returns:
        float: Effective training time in minutes
    """
    return base_time * (1 - time_reduction_bonus)

def calculate_batches_and_points(
    troops_per_batch: int,
    points_per_troop: float,
    points_per_batch: float = None,
    current_points: float = 0.0
) -> Tuple[int, float]:
    """
    Calculate number of batches and total points.
    
    Args:
        troops_per_batch (int): Number of troops per batch
        points_per_troop (float): Points per troop
        points_per_batch (float, optional): Points per batch. If None, calculated from troops_per_batch
        current_points (float, optional): Current points. Defaults to 0.0
    
    Returns:
        Tuple[int, float]: Number of batches and total points
    """
    if troops_per_batch < 0:
        raise ValueError("Troops per batch cannot be negative")
    if points_per_troop < 0:
        raise ValueError("Points per troop cannot be negative")
    if current_points < 0:
        raise ValueError("Current points cannot be negative")
    
    if points_per_batch is None:
        points_per_batch = troops_per_batch * points_per_troop
    
    batches = 1  # Default to 1 batch
    total_points = points_per_batch + current_points
    
    return batches, total_points

def calculate_efficiency_metrics(
    speedup_minutes: float,
    total_points: float
) -> Dict[str, float]:
    """
    Calculate efficiency metrics for the investment.
    
    Args:
        speedup_minutes (float): Total speed-up minutes used
        total_points (float): Total points earned
    
    Returns:
        Dict[str, float]: Dictionary containing efficiency metrics
    """
    points_per_minute = total_points / speedup_minutes if speedup_minutes > 0 else 0
    return {
        "points_per_minute": points_per_minute,
        "efficiency_score": points_per_minute * 100  # Normalized score
    }

def calculate_speedups_needed(
    target_points: float,
    points_per_batch: float,
    _: float,  # Removed points_bonus parameter
    effective_training_time: float
) -> float:
    """
    Calculate the number of speed-up minutes needed to reach target points.
    
    Args:
        target_points (float): Desired total points
        points_per_batch (float): Points earned per batch
        _ (float): Unused parameter (kept for backward compatibility)
        effective_training_time (float): Training time per batch after bonuses
    
    Returns:
        float: Required speed-up minutes
    """
    batches_needed = target_points / points_per_batch
    return batches_needed * effective_training_time 