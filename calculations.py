"""
Core calculation module for Whiteout Survival investment/return calculator.
Contains functions for calculating training times, points, and efficiency metrics.
"""

from typing import Dict, Tuple
import numpy as np

def calculate_batches_and_points(
    total_speedups: float,
    base_training_time: float,
    points_per_batch: float,
    current_points: float
) -> Tuple[int, float]:
    """
    Calculate the number of batches that can be trained and total points earned.
    
    Args:
        total_speedups (float): Total speed-up minutes available
        base_training_time (float): Base training time per batch
        points_per_batch (float): Points earned per batch
        current_points (float): Current points earned
    
    Returns:
        Tuple[int, float]: Number of batches and total points earned
    """
    if any(x == float('inf') for x in [total_speedups, base_training_time, points_per_batch, current_points]):
        raise ValueError("Infinite values are not allowed.")
    if total_speedups < 0 or base_training_time <= 0 or points_per_batch < 0 or current_points < 0:
        raise ValueError("Inputs must be non-negative and base_training_time > 0.")
    num_batches = int(total_speedups // base_training_time)
    total_points = (num_batches * points_per_batch) + current_points
    return num_batches, total_points

def calculate_efficiency_metrics(
    total_speedups: float,
    total_points: float
) -> Dict[str, float]:
    """
    Calculate efficiency metrics for the investment.
    
    Args:
        total_speedups (float): Total speed-up minutes used
        total_points (float): Total points earned
    
    Returns:
        Dict[str, float]: Dictionary containing efficiency metrics
    """
    if total_speedups < 0:
        raise ValueError("Total speedups cannot be negative.")
    if total_speedups == 0 or total_points == 0:
        return {
            "points_per_minute": 0.0,
            "time_per_point": 0.0,
            "efficiency_score": 0.0
        }
    points_per_minute = total_points / total_speedups
    time_per_point = total_speedups / total_points
    return {
        "points_per_minute": points_per_minute,
        "time_per_point": time_per_point,
        "efficiency_score": points_per_minute * 100  # Normalized score
    } 