"""
Tests for calculation fixes and improvements.
"""

import pytest
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)

class TestCalculateBatchesAndPointsFixes:
    """Test fixes for batches and points calculation."""
    
    def test_negative_speedups_raises_error(self):
        """Test that negative speedups raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_batches_and_points(-100.0, 60.0, 1000.0, 0.0)
    
    def test_zero_base_time_raises_error(self):
        """Test that zero base time raises ValueError."""
        with pytest.raises(ValueError, match="base_training_time > 0"):
            calculate_batches_and_points(100.0, 0.0, 1000.0, 0.0)
    
    def test_negative_points_per_batch_raises_error(self):
        """Test that negative points per batch raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_batches_and_points(100.0, 60.0, -1000.0, 0.0)
    
    def test_negative_current_points_raises_error(self):
        """Test that negative current points raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_batches_and_points(100.0, 60.0, 1000.0, -100.0)
    
    def test_infinite_values_raise_error(self):
        """Test that infinite values raise ValueError."""
        with pytest.raises(ValueError, match="Infinite values are not allowed"):
            calculate_batches_and_points(float('inf'), 60.0, 1000.0, 0.0)
    
    def test_correct_batch_calculation(self):
        """Test that batch calculation is correct."""
        total_speedups = 120.0  # 2 hours
        base_time = 60.0   # 1 hour per batch
        points_per_batch = 1000.0
        current_points = 500.0
        
        batches, total_points = calculate_batches_and_points(
            total_speedups, base_time, points_per_batch, current_points
        )
        
        assert batches == 2  # 120 / 60 = 2 batches
        assert total_points == 2500.0  # (2 * 1000) + 500

class TestCalculateEfficiencyMetricsFixes:
    """Test fixes for efficiency metrics calculation."""
    
    def test_negative_speedups_raises_error(self):
        """Test that negative speedups raises ValueError."""
        with pytest.raises(ValueError, match="Total speedups cannot be negative"):
            calculate_efficiency_metrics(-100.0, 1000.0)
    
    def test_zero_speedups_returns_zero_metrics(self):
        """Test that zero speedups returns zero metrics."""
        metrics = calculate_efficiency_metrics(0.0, 1000.0)
        assert metrics['points_per_minute'] == 0.0
        assert metrics['time_per_point'] == 0.0
        assert metrics['efficiency_score'] == 0.0
    
    def test_zero_points_returns_zero_metrics(self):
        """Test that zero points returns zero metrics."""
        metrics = calculate_efficiency_metrics(1000.0, 0.0)
        assert metrics['points_per_minute'] == 0.0
        assert metrics['time_per_point'] == 0.0
        assert metrics['efficiency_score'] == 0.0
    
    def test_correct_efficiency_calculation(self):
        """Test that efficiency calculation is correct."""
        speedups = 100.0
        points = 1000.0
        
        metrics = calculate_efficiency_metrics(speedups, points)
        
        expected_points_per_minute = points / speedups
        expected_time_per_point = speedups / points
        
        assert metrics['points_per_minute'] == expected_points_per_minute
        assert metrics['time_per_point'] == expected_time_per_point
        assert metrics['efficiency_score'] == expected_points_per_minute * 100 