"""
Core calculation module for Whiteout Survival investment/return calculator.
Contains functions for calculating training times, points, and efficiency metrics.
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
        time_reduction_bonus (float): Training time reduction bonus as a decimal (e.g., 0.2 for 20%)
    
    Returns:
        float: Effective training time in minutes
    """
    if base_time < 0:
        raise ValueError("Base training time cannot be negative.")
    if not (0 <= time_reduction_bonus <= 1):
        raise ValueError("Time reduction bonus must be between 0 and 1.")
    if base_time == float('inf') or time_reduction_bonus == float('inf'):
        raise ValueError("Infinite values are not allowed.")
    return max(0, base_time * (1 - time_reduction_bonus))

def calculate_batches_and_points(
    total_speedups: float,
    effective_training_time: float,
    points_per_batch: float,
    current_points: float
) -> Tuple[int, float]:
    """
    Calculate the number of batches that can be trained and total points earned.
    
    Args:
        total_speedups (float): Total speed-up minutes available
        effective_training_time (float): Training time per batch after bonuses
        points_per_batch (float): Points earned per batch
        current_points (float): Current points earned
    
    Returns:
        Tuple[int, float]: Number of batches and total points earned
    """
    if any(x == float('inf') for x in [total_speedups, effective_training_time, points_per_batch, current_points]):
        raise ValueError("Infinite values are not allowed.")
    if total_speedups < 0 or effective_training_time <= 0 or points_per_batch < 0 or current_points < 0:
        raise ValueError("Inputs must be non-negative and effective_training_time > 0.")
    num_batches = int(total_speedups // effective_training_time)
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

def calculate_speedups_needed(
    target_points: float,
    points_per_batch: float,
    current_points: float,
    effective_training_time: float
) -> float:
    """
    Calculate the number of speed-up minutes needed to reach target points.
    
    Args:
        target_points (float): Desired total points
        points_per_batch (float): Points earned per batch
        current_points (float): Current points earned
        effective_training_time (float): Training time per batch after bonuses
    
    Returns:
        float: Required speed-up minutes
    """
    if any(x < 0 for x in [target_points, points_per_batch, current_points, effective_training_time]):
        raise ValueError("Inputs must be non-negative.")
    if points_per_batch == 0 or effective_training_time <= 0:
        raise ZeroDivisionError("points_per_batch and effective_training_time must be > 0.")
    if current_points >= target_points:
        return 0
    batches_needed = (target_points - current_points) / points_per_batch
    return max(0, batches_needed * effective_training_time) 