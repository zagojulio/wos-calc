import os
import json
import pytest
from features import pack_value_comparison

def test_add_and_load_pack(tmp_path):
    # Setup temp file
    test_file = tmp_path / "pack_value_comparison.json"
    data = [
        {"Pack Name": "Test Pack", "Price": 10.0, "60min Speedups": 1, "5min Speedups": 10, "Total Speedup Minutes": 70, "Cost per Minute": 0.1429}
    ]
    with open(test_file, "w") as f:
        json.dump(data, f)
    # Patch path
    orig_path = pack_value_comparison.PACKS_JSON_PATH
    pack_value_comparison.PACKS_JSON_PATH = str(test_file)
    # Load
    loaded = pack_value_comparison.load_pack_history()
    assert loaded == data
    # Save
    new_data = data + [{"Pack Name": "Another", "Price": 20.0, "60min Speedups": 2, "5min Speedups": 20, "Total Speedup Minutes": 140, "Cost per Minute": 0.1429}]
    pack_value_comparison.save_pack_history(new_data)
    with open(test_file) as f:
        saved = json.load(f)
    assert saved == new_data
    # Cleanup
    pack_value_comparison.PACKS_JSON_PATH = orig_path

def test_cost_per_minute_calculation():
    price = 15.0
    minutes = 30
    cost = pack_value_comparison.calculate_cost_per_minute(price, minutes)
    assert cost == 0.5

def test_cost_per_minute_zero_minutes():
    price = 15.0
    minutes = 0
    cost = pack_value_comparison.calculate_cost_per_minute(price, minutes)
    assert cost == 0.0

def test_cost_per_minute_negative_minutes():
    price = 15.0
    minutes = -10
    cost = pack_value_comparison.calculate_cost_per_minute(price, minutes)
    assert cost == 0.0

def test_calculate_total_minutes():
    # Test with only 60min speedups
    total = pack_value_comparison.calculate_total_minutes(2, 0)
    assert total == 120
    
    # Test with only 5min speedups
    total = pack_value_comparison.calculate_total_minutes(0, 10)
    assert total == 50
    
    # Test with both types
    total = pack_value_comparison.calculate_total_minutes(1, 5)
    assert total == 85
    
    # Test with zero speedups
    total = pack_value_comparison.calculate_total_minutes(0, 0)
    assert total == 0

def test_calculate_total_minutes_edge_cases():
    # Test with large numbers
    total = pack_value_comparison.calculate_total_minutes(100, 1000)
    assert total == 11000  # (100 * 60) + (1000 * 5) = 6000 + 5000 = 11000
    
    # Test with negative inputs (should still calculate correctly)
    total = pack_value_comparison.calculate_total_minutes(-1, -5)
    assert total == -85 