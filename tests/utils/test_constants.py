"""
Unit tests for utils/constants.py
"""
import pytest
import utils.constants as constants

def test_level_points_keys_and_values():
    # Check all expected levels are present
    expected_levels = list(range(1, 21))
    assert list(constants.LEVEL_POINTS.keys()) == expected_levels
    # Check values are non-negative and increasing
    last = -1
    for lvl in expected_levels:
        val = constants.LEVEL_POINTS[lvl]
        assert val >= 0
        assert val > last
        last = val

def test_default_speedup_categories():
    expected = {
        "1m": {"cost": 1, "points": 1},
        "5m": {"cost": 4, "points": 5},
        "15m": {"cost": 10, "points": 15},
        "30m": {"cost": 18, "points": 30},
        "1h": {"cost": 30, "points": 60},
        "3h": {"cost": 80, "points": 180},
        "8h": {"cost": 180, "points": 480},
        "24h": {"cost": 450, "points": 1440}
    }
    assert constants.DEFAULT_SPEEDUP_CATEGORIES == expected
    # Check all costs and points are positive
    for cat, conf in constants.DEFAULT_SPEEDUP_CATEGORIES.items():
        assert conf["cost"] > 0
        assert conf["points"] > 0

def test_ui_constants():
    assert constants.MAX_LEVEL == 20
    assert constants.MIN_LEVEL == 1
    assert constants.MAX_POINTS == 19000
    assert constants.MIN_POINTS == 0 