"""
Unit tests for calculations.py module.
"""

import pytest
from calculations import (
    calculate_effective_training_time,
    calculate_batches_and_points,
    calculate_efficiency_metrics,
    calculate_speedups_needed
)

class TestCalculateEffectiveTrainingTime:
    def test_normal_case(self):
        base_time = 120  # 2 hours
        reduction = 0.2  # 20% reduction
        expected = 96  # 120 * (1 - 0.2)
        assert calculate_effective_training_time(base_time, reduction) == expected

    def test_zero_reduction(self):
        base_time = 120
        reduction = 0
        assert calculate_effective_training_time(base_time, reduction) == base_time

    def test_max_reduction(self):
        base_time = 120
        reduction = 1
        assert calculate_effective_training_time(base_time, reduction) == 0

    def test_negative_reduction(self):
        base_time = 120
        reduction = -0.2
        with pytest.raises(ValueError):
            calculate_effective_training_time(base_time, reduction)

    def test_negative_base_time(self):
        base_time = -120
        reduction = 0.2
        with pytest.raises(ValueError):
            calculate_effective_training_time(base_time, reduction)

class TestCalculateBatchesAndPoints:
    def test_normal_case(self):
        speedups = 1000
        effective_time = 60
        points_per_batch = 1000
        current_points = 0
        batches, points = calculate_batches_and_points(
            speedups, effective_time, points_per_batch, current_points
        )
        expected_batches = 16  # 1000 / 60
        expected_points = expected_batches * points_per_batch
        assert batches == expected_batches
        assert points == expected_points

    def test_zero_speedups(self):
        speedups = 0
        effective_time = 60
        points_per_batch = 1000
        current_points = 0
        batches, points = calculate_batches_and_points(
            speedups, effective_time, points_per_batch, current_points
        )
        assert batches == 0
        assert points == 0

    def test_existing_points(self):
        speedups = 1000
        effective_time = 60
        points_per_batch = 1000
        current_points = 5000
        batches, points = calculate_batches_and_points(
            speedups, effective_time, points_per_batch, current_points
        )
        expected_batches = 16
        expected_points = (expected_batches * points_per_batch) + current_points
        assert batches == expected_batches
        assert points == expected_points

class TestCalculateEfficiencyMetrics:
    def test_normal_case(self):
        speedups = 1000
        total_points = 10000
        metrics = calculate_efficiency_metrics(speedups, total_points)
        expected_points_per_minute = total_points / speedups
        assert metrics['points_per_minute'] == expected_points_per_minute

    def test_zero_speedups(self):
        speedups = 0
        total_points = 10000
        metrics = calculate_efficiency_metrics(speedups, total_points)
        assert metrics['points_per_minute'] == 0

    def test_zero_points(self):
        speedups = 1000
        total_points = 0
        metrics = calculate_efficiency_metrics(speedups, total_points)
        assert metrics['points_per_minute'] == 0

class TestCalculateSpeedupsNeeded:
    def test_normal_case(self):
        target_points = 10000
        points_per_batch = 1000
        current_points = 0
        effective_time = 60
        speedups = calculate_speedups_needed(
            target_points, points_per_batch, current_points, effective_time
        )
        expected_batches = 10  # (10000 - 0) / 1000
        expected_speedups = expected_batches * effective_time
        assert speedups == expected_speedups

    def test_already_achieved_target(self):
        target_points = 10000
        points_per_batch = 1000
        current_points = 12000
        effective_time = 60
        speedups = calculate_speedups_needed(
            target_points, points_per_batch, current_points, effective_time
        )
        assert speedups == 0

    def test_zero_points_per_batch(self):
        target_points = 10000
        points_per_batch = 0
        current_points = 0
        effective_time = 60
        with pytest.raises(ZeroDivisionError):
            calculate_speedups_needed(
                target_points, points_per_batch, current_points, effective_time
            ) 