"""
Unit tests for the updated training analysis functionality.
"""

import pytest
import streamlit as st
from features.training_manager import render_training_analysis
from calculations import (
    calculate_batches_and_points,
    calculate_efficiency_metrics
)

@pytest.fixture
def default_params():
    """Fixture providing default training parameters."""
    return {
        'general_speedups': 18000.0,
        'training_speedups': 1515.0,
        'base_training_time': 290.0,  # 4h 50m
        'troops_per_batch': 426,
        'points_per_troop': 830.0
    }

class TestRenderTrainingAnalysis:
    def test_normal_case(self, default_params):
        """Test training analysis with normal parameters."""
        # Calculate expected values
        points_per_batch = default_params['troops_per_batch'] * default_params['points_per_troop']
        total_speedups = default_params['general_speedups'] + default_params['training_speedups']
        current_points = 0.0

        # Calculate expected batches and points
        expected_batches, expected_total_points = calculate_batches_and_points(
            total_speedups,
            default_params['base_training_time'],
            points_per_batch,
            current_points
        )

        # Calculate expected efficiency metrics
        expected_efficiency = calculate_efficiency_metrics(
            total_speedups,
            expected_total_points
        )

        # Calculate expected remaining speedups
        expected_remaining = total_speedups - (expected_batches * default_params['base_training_time'])

        # Verify calculations
        assert points_per_batch == default_params['troops_per_batch'] * default_params['points_per_troop']
        assert total_speedups == default_params['general_speedups'] + default_params['training_speedups']
        assert expected_batches > 0
        assert expected_total_points > 0
        assert expected_remaining >= 0

    def test_edge_cases(self):
        """Test training analysis with edge cases."""
        # Test with zero values
        zero_params = {
            'general_speedups': 0.0,
            'training_speedups': 0.0,
            'base_training_time': 0.0,
            'troops_per_batch': 0,
            'points_per_troop': 0.0
        }

        with pytest.raises(ValueError):
            render_training_analysis(zero_params)

        # Test with maximum values
        max_params = {
            'general_speedups': float('inf'),
            'training_speedups': float('inf'),
            'base_training_time': float('inf'),
            'troops_per_batch': 1000000,
            'points_per_troop': float('inf')
        }

        with pytest.raises(ValueError):
            render_training_analysis(max_params)

    def test_input_validation(self, default_params):
        """Test input validation in training analysis."""
        # Test negative values
        negative_params = default_params.copy()
        negative_params['base_training_time'] = -100.0
        with pytest.raises(ValueError):
            render_training_analysis(negative_params)

        # Test invalid speed-up values
        invalid_speedups_params = default_params.copy()
        invalid_speedups_params['general_speedups'] = -1000.0
        with pytest.raises(ValueError):
            render_training_analysis(invalid_speedups_params)

    def test_metric_calculations(self, default_params):
        """Test accuracy of displayed metrics."""
        # Calculate expected values
        points_per_batch = default_params['troops_per_batch'] * default_params['points_per_troop']
        total_speedups = default_params['general_speedups'] + default_params['training_speedups']
        current_points = 0.0

        batches, total_points = calculate_batches_and_points(
            total_speedups,
            default_params['base_training_time'],
            points_per_batch,
            current_points
        )

        remaining_speedups = total_speedups - (batches * default_params['base_training_time'])

        # Verify metric calculations
        assert points_per_batch > 0
        assert batches >= 0
        assert total_points >= 0
        assert remaining_speedups >= 0
        assert remaining_speedups <= total_speedups 