"""
Unit tests for training_visualizer.py module.
"""

import pytest
import pandas as pd
import numpy as np
from features.training_visualizer import (
    create_training_chart,
    create_efficiency_chart,
    create_speedup_chart
)

class TestCreateTrainingChart:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        data = {
            'batch': [1, 2, 3],
            'points': [1000, 2000, 3000],
            'time': [60, 120, 180]
        }
        df = pd.DataFrame(data)
        chart = create_training_chart(df)
        assert chart is not None
        assert chart.data[0].x == list(df['batch'])
        assert chart.data[0].y == list(df['points'])

    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame(columns=['batch', 'points', 'time'])
        chart = create_training_chart(df)
        assert chart is not None
        assert len(chart.data[0].x) == 0
        assert len(chart.data[0].y) == 0

    def test_missing_columns(self):
        """Test with missing required columns."""
        df = pd.DataFrame({'batch': [1, 2, 3]})
        with pytest.raises(KeyError):
            create_training_chart(df)

class TestCreateEfficiencyChart:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        data = {
            'batch': [1, 2, 3],
            'efficiency': [0.8, 0.9, 1.0],
            'points_per_minute': [10, 12, 15]
        }
        df = pd.DataFrame(data)
        chart = create_efficiency_chart(df)
        assert chart is not None
        assert chart.data[0].x == list(df['batch'])
        assert chart.data[0].y == list(df['efficiency'])

    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame(columns=['batch', 'efficiency', 'points_per_minute'])
        chart = create_efficiency_chart(df)
        assert chart is not None
        assert len(chart.data[0].x) == 0
        assert len(chart.data[0].y) == 0

    def test_missing_columns(self):
        """Test with missing required columns."""
        df = pd.DataFrame({'batch': [1, 2, 3]})
        with pytest.raises(KeyError):
            create_efficiency_chart(df)

class TestCreateSpeedupChart:
    def test_normal_case(self):
        """Test normal case with valid inputs."""
        data = {
            'batch': [1, 2, 3],
            'speedups': [100, 200, 300],
            'cumulative_speedups': [100, 300, 600]
        }
        df = pd.DataFrame(data)
        chart = create_speedup_chart(df)
        assert chart is not None
        assert chart.data[0].x == list(df['batch'])
        assert chart.data[0].y == list(df['speedups'])

    def test_empty_dataframe(self):
        """Test with empty dataframe."""
        df = pd.DataFrame(columns=['batch', 'speedups', 'cumulative_speedups'])
        chart = create_speedup_chart(df)
        assert chart is not None
        assert len(chart.data[0].x) == 0
        assert len(chart.data[0].y) == 0

    def test_missing_columns(self):
        """Test with missing required columns."""
        df = pd.DataFrame({'batch': [1, 2, 3]})
        with pytest.raises(KeyError):
            create_speedup_chart(df)

    def test_negative_speedups(self):
        """Test with negative speedup values."""
        data = {
            'batch': [1, 2, 3],
            'speedups': [-100, -200, -300],
            'cumulative_speedups': [-100, -300, -600]
        }
        df = pd.DataFrame(data)
        chart = create_speedup_chart(df)
        assert chart is not None
        assert chart.data[0].x == list(df['batch'])
        assert chart.data[0].y == list(df['speedups']) 