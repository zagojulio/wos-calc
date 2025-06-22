"""
Unit tests for calculations.py module.
"""

import pytest
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)

class TestCalculateBatchesAndPoints:
    def test_normal_case(self):
        speedups = 1000
        base_time = 60
        points_per_batch = 1000
        current_points = 0
        batches, points = calculate_batches_and_points(
            speedups, base_time, points_per_batch, current_points
        )
        expected_batches = 16  # 1000 / 60
        expected_points = expected_batches * points_per_batch
        assert batches == expected_batches
        assert points == expected_points

    def test_zero_speedups(self):
        speedups = 0
        base_time = 60
        points_per_batch = 1000
        current_points = 0
        batches, points = calculate_batches_and_points(
            speedups, base_time, points_per_batch, current_points
        )
        assert batches == 0
        assert points == 0

    def test_existing_points(self):
        speedups = 1000
        base_time = 60
        points_per_batch = 1000
        current_points = 5000
        batches, points = calculate_batches_and_points(
            speedups, base_time, points_per_batch, current_points
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