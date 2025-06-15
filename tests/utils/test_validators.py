"""
Unit tests for utils/validators.py
"""
import pytest
from utils.validators import validate_speedup_inputs, validate_pack_purchase

def test_validate_speedup_inputs_valid():
    speedup_categories = {"1m": {"cost": 1, "points": 1}}
    valid, msg = validate_speedup_inputs(1, 2, 0, 100, speedup_categories)
    assert valid
    assert msg == ""

def test_validate_speedup_inputs_negative_levels():
    speedup_categories = {"1m": {"cost": 1, "points": 1}}
    valid, msg = validate_speedup_inputs(-1, 2, 0, 100, speedup_categories)
    assert not valid
    assert "negative" in msg

def test_validate_speedup_inputs_level_order():
    speedup_categories = {"1m": {"cost": 1, "points": 1}}
    valid, msg = validate_speedup_inputs(5, 2, 0, 100, speedup_categories)
    assert not valid
    assert "higher" in msg

def test_validate_speedup_inputs_negative_points():
    speedup_categories = {"1m": {"cost": 1, "points": 1}}
    valid, msg = validate_speedup_inputs(1, 2, -10, 100, speedup_categories)
    assert not valid
    assert "negative" in msg

def test_validate_speedup_inputs_points_order():
    speedup_categories = {"1m": {"cost": 1, "points": 1}}
    valid, msg = validate_speedup_inputs(1, 2, 200, 100, speedup_categories)
    assert not valid
    assert "higher" in msg

def test_validate_speedup_inputs_negative_cost():
    speedup_categories = {"1m": {"cost": -1, "points": 1}}
    valid, msg = validate_speedup_inputs(1, 2, 0, 100, speedup_categories)
    assert not valid
    assert "negative" in msg

def test_validate_speedup_inputs_negative_points_in_category():
    speedup_categories = {"1m": {"cost": 1, "points": -1}}
    valid, msg = validate_speedup_inputs(1, 2, 0, 100, speedup_categories)
    assert not valid
    assert "negative" in msg

def test_validate_pack_purchase_valid():
    speedups = {"1m": 10, "5m": 5}
    valid, msg = validate_pack_purchase("2024-01-01", "Starter Pack", 10.0, speedups)
    assert valid
    assert msg == ""

def test_validate_pack_purchase_missing_date():
    speedups = {"1m": 10}
    valid, msg = validate_pack_purchase("", "Pack", 10.0, speedups)
    assert not valid
    assert "Date" in msg

def test_validate_pack_purchase_missing_pack_name():
    speedups = {"1m": 10}
    valid, msg = validate_pack_purchase("2024-01-01", "", 10.0, speedups)
    assert not valid
    assert "Pack name" in msg

def test_validate_pack_purchase_nonpositive_spending():
    speedups = {"1m": 10}
    valid, msg = validate_pack_purchase("2024-01-01", "Pack", 0.0, speedups)
    assert not valid
    assert "greater than 0" in msg

def test_validate_pack_purchase_negative_speedup():
    speedups = {"1m": -5}
    valid, msg = validate_pack_purchase("2024-01-01", "Pack", 10.0, speedups)
    assert not valid
    assert "negative" in msg 