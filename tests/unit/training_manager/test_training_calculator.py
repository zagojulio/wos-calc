"""
Unit tests for training_calculator.py module.
"""

import pytest
from features.training_calculator import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)

class TestCalculateEffectiveTrainingTime:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        base_time = 120  # 2 hours
        reduction = 0.2  # 20% reduction
        expected = 96  # 120 * (1 - 0.2)
        assert calculate_effective_training_time(base_time, reduction) == expected

    def test_zero_reduction(self):
        """Test with zero reduction bonus."""
        base_time = 120
        reduction = 0
        assert calculate_effective_training_time(base_time, reduction) == base_time

    def test_max_reduction(self):
        """Test with maximum reduction bonus."""
        base_time = 120
        reduction = 1
        assert calculate_effective_training_time(base_time, reduction) == 0

    def test_negative_reduction(self):
        """Test with negative reduction bonus."""
        base_time = 120
        reduction = -0.2
        with pytest.raises(ValueError):
            calculate_effective_training_time(base_time, reduction)

    def test_negative_base_time(self):
        """Test with negative base time."""
        base_time = -120
        reduction = 0.2
        with pytest.raises(ValueError):
            calculate_effective_training_time(base_time, reduction)

class TestCalculateBatchesAndPoints:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        troops_per_batch = 100
        points_per_troop = 10
        points_per_batch = None  # Should be calculated
        current_points = 0
        batches, points = calculate_batches_and_points(
            troops_per_batch,
            points_per_troop,
            points_per_batch,
            current_points
        )
        assert batches == 1  # Default to 1 batch
        assert points == troops_per_batch * points_per_troop

    def test_with_existing_points(self):
        """Test with existing points."""
        troops_per_batch = 100
        points_per_troop = 10
        points_per_batch = 1000
        current_points = 500
        batches, points = calculate_batches_and_points(
            troops_per_batch,
            points_per_troop,
            points_per_batch,
            current_points
        )
        assert batches == 1
        assert points == points_per_batch + current_points

    def test_negative_troops(self):
        """Test with negative troops per batch."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(-100, 10, None, 0)

    def test_negative_points(self):
        """Test with negative points per troop."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(100, -10, None, 0)

    def test_negative_current_points(self):
        """Test with negative current points."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(100, 10, None, -100)

class TestCalculateEfficiencyMetrics:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        speedup_minutes = 1000
        total_points = 10000
        metrics = calculate_efficiency_metrics(speedup_minutes, total_points)
        expected_points_per_minute = total_points / speedup_minutes
        assert metrics['points_per_minute'] == expected_points_per_minute
        assert metrics['efficiency_score'] == expected_points_per_minute * 100

    def test_zero_speedups(self):
        """Test with zero speedup minutes."""
        speedup_minutes = 0
        total_points = 10000
        metrics = calculate_efficiency_metrics(speedup_minutes, total_points)
        assert metrics['points_per_minute'] == 0
        assert metrics['efficiency_score'] == 0

    def test_zero_points(self):
        """Test with zero total points."""
        speedup_minutes = 1000
        total_points = 0
        metrics = calculate_efficiency_metrics(speedup_minutes, total_points)
        assert metrics['points_per_minute'] == 0
        assert metrics['efficiency_score'] == 0

class TestCalculateSpeedupsNeeded:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        target_points = 10000
        points_per_batch = 1000
        current_points = 0
        effective_time = 60
        speedups = calculate_speedups_needed(
            target_points,
            points_per_batch,
            current_points,
            effective_time
        )
        expected_batches = target_points / points_per_batch
        expected_speedups = expected_batches * effective_time
        assert speedups == expected_speedups

    def test_already_achieved_target(self):
        """Test when target points are already achieved."""
        target_points = 10000
        points_per_batch = 1000
        current_points = 12000
        effective_time = 60
        speedups = calculate_speedups_needed(
            target_points,
            points_per_batch,
            current_points,
            effective_time
        )
        assert speedups == 0

    def test_zero_points_per_batch(self):
        """Test with zero points per batch."""
        target_points = 10000
        points_per_batch = 0
        current_points = 0
        effective_time = 60
        with pytest.raises(ZeroDivisionError):
            calculate_speedups_needed(
                target_points,
                points_per_batch,
                current_points,
                effective_time
            ) 