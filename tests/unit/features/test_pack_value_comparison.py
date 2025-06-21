import os
import json
import pytest
from features import pack_value_comparison

def test_add_and_load_pack(tmp_path):
    # Setup temp file
    test_file = tmp_path / "pack_value_comparison.json"
    data = [
        {"Pack Name": "Test Pack", "Price": 10.0, "Speed-up Minutes": 100, "Cost per Minute": 0.1}
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
    new_data = data + [{"Pack Name": "Another", "Price": 20.0, "Speed-up Minutes": 200, "Cost per Minute": 0.1}]
    pack_value_comparison.save_pack_history(new_data)
    with open(test_file) as f:
        saved = json.load(f)
    assert saved == new_data
    # Cleanup
    pack_value_comparison.PACKS_JSON_PATH = orig_path

def test_cost_per_minute_calculation():
    price = 15.0
    minutes = 30
    cost = round(price / minutes, 4)
    assert cost == 0.5 