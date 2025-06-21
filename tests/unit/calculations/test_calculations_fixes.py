"""
Tests for calculation fixes and improvements.
"""

import pytest
from calculations import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)

class TestCalculateEffectiveTrainingTimeFixes:
    """Test fixes for effective training time calculation."""
    
    def test_negative_base_time_raises_error(self):
        """Test that negative base time raises ValueError."""
        with pytest.raises(ValueError, match="Base training time cannot be negative"):
            calculate_effective_training_time(-100.0, 0.2)
    
    def test_negative_reduction_raises_error(self):
        """Test that negative reduction bonus raises ValueError."""
        with pytest.raises(ValueError, match="Time reduction bonus must be between 0 and 1"):
            calculate_effective_training_time(100.0, -0.2)
    
    def test_reduction_greater_than_one_raises_error(self):
        """Test that reduction bonus > 1 raises ValueError."""
        with pytest.raises(ValueError, match="Time reduction bonus must be between 0 and 1"):
            calculate_effective_training_time(100.0, 1.5)
    
    def test_infinite_values_raise_error(self):
        """Test that infinite values raise ValueError."""
        with pytest.raises(ValueError, match="Infinite values are not allowed"):
            calculate_effective_training_time(float('inf'), 0.2)
        
        with pytest.raises(ValueError, match="Time reduction bonus must be between 0 and 1"):
            calculate_effective_training_time(100.0, float('inf'))
    
    def test_max_reduction_returns_zero(self):
        """Test that 100% reduction returns 0."""
        result = calculate_effective_training_time(100.0, 1.0)
        assert result == 0.0

class TestCalculateBatchesAndPointsFixes:
    """Test fixes for batches and points calculation."""
    
    def test_negative_speedups_raises_error(self):
        """Test that negative speedups raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_batches_and_points(-100.0, 60.0, 1000.0, 0.0)
    
    def test_zero_effective_time_raises_error(self):
        """Test that zero effective time raises ValueError."""
        with pytest.raises(ValueError, match="effective_training_time > 0"):
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
        effective_time = 60.0   # 1 hour per batch
        points_per_batch = 1000.0
        current_points = 500.0
        
        batches, total_points = calculate_batches_and_points(
            total_speedups, effective_time, points_per_batch, current_points
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

class TestCalculateSpeedupsNeededFixes:
    """Test fixes for speedups needed calculation."""
    
    def test_negative_target_points_raises_error(self):
        """Test that negative target points raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_speedups_needed(-1000.0, 100.0, 0.0, 60.0)
    
    def test_negative_points_per_batch_raises_error(self):
        """Test that negative points per batch raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_speedups_needed(1000.0, -100.0, 0.0, 60.0)
    
    def test_negative_current_points_raises_error(self):
        """Test that negative current points raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_speedups_needed(1000.0, 100.0, -500.0, 60.0)
    
    def test_negative_effective_time_raises_error(self):
        """Test that negative effective time raises ValueError."""
        with pytest.raises(ValueError, match="Inputs must be non-negative"):
            calculate_speedups_needed(1000.0, 100.0, 0.0, -60.0)
    
    def test_zero_points_per_batch_raises_error(self):
        """Test that zero points per batch raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="points_per_batch and effective_training_time must be > 0"):
            calculate_speedups_needed(1000.0, 0.0, 0.0, 60.0)
    
    def test_zero_effective_time_raises_error(self):
        """Test that zero effective time raises ZeroDivisionError."""
        with pytest.raises(ZeroDivisionError, match="points_per_batch and effective_training_time must be > 0"):
            calculate_speedups_needed(1000.0, 100.0, 0.0, 0.0)
    
    def test_already_achieved_target_returns_zero(self):
        """Test that already achieved target returns 0."""
        result = calculate_speedups_needed(1000.0, 100.0, 1200.0, 60.0)
        assert result == 0.0
    
    def test_correct_speedups_calculation(self):
        """Test that speedups calculation is correct."""
        target_points = 1000.0
        points_per_batch = 100.0
        current_points = 200.0
        effective_time = 60.0
        
        result = calculate_speedups_needed(target_points, points_per_batch, current_points, effective_time)
        
        # Need 800 more points (1000 - 200)
        # Need 8 more batches (800 / 100)
        # Need 480 minutes (8 * 60)
        expected = 480.0
        assert result == expected 