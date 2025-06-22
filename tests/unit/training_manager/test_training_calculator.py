"""
Unit tests for training_calculator.py module.
"""

import pytest
from features.training_calculator import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)

class TestCalculateBatchesAndPoints:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        total_speedups = 1000
        base_training_time = 60
        points_per_batch = 1000
        current_points = 0
        batches, points = calculate_batches_and_points(
            total_speedups,
            base_training_time,
            points_per_batch,
            current_points
        )
        expected_batches = int(total_speedups // base_training_time)
        expected_points = expected_batches * points_per_batch
        assert batches == expected_batches
        assert points == expected_points

    def test_with_existing_points(self):
        """Test with existing points."""
        total_speedups = 1000
        base_training_time = 60
        points_per_batch = 1000
        current_points = 500
        batches, points = calculate_batches_and_points(
            total_speedups,
            base_training_time,
            points_per_batch,
            current_points
        )
        expected_batches = int(total_speedups // base_training_time)
        expected_points = (expected_batches * points_per_batch) + current_points
        assert batches == expected_batches
        assert points == expected_points

    def test_negative_speedups(self):
        """Test with negative speedups."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(-100, 60, 1000, 0)

    def test_negative_base_time(self):
        """Test with negative base training time."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(100, -60, 1000, 0)

    def test_negative_points_per_batch(self):
        """Test with negative points per batch."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(100, 60, -1000, 0)

    def test_negative_current_points(self):
        """Test with negative current points."""
        with pytest.raises(ValueError):
            calculate_batches_and_points(100, 60, 1000, -100)

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