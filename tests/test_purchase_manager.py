"""
Tests for the purchase manager module.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from features.purchase_manager import (
    load_purchases,
    save_purchase,
    calculate_purchase_stats,
    export_combined_purchases
)

def test_load_purchases(sample_auto_purchases, sample_manual_purchases, monkeypatch):
    """Test loading purchase data."""
    auto_df, auto_path = sample_auto_purchases
    manual_df, manual_path = sample_manual_purchases
    
    # Mock the file paths
    monkeypatch.setattr("features.purchase_manager.AUTO_PURCHASES_PATH", str(auto_path))
    monkeypatch.setattr("features.purchase_manager.MANUAL_PURCHASES_PATH", str(manual_path))
    
    loaded_auto, loaded_manual = load_purchases(str(auto_path), str(manual_path))
    assert loaded_auto.equals(auto_df)
    assert loaded_manual.equals(manual_df)

def test_save_purchase(test_data_dir):
    """Test saving a new purchase."""
    file_path = test_data_dir / "test_purchases.csv"
    purchase = {
        "Date": datetime.now(),
        "Pack Name": "Test Pack",
        "Spending ($)": 100.0,
        "Speed-ups (min)": 1000
    }
    
    # Test saving to new file
    assert save_purchase(str(file_path), purchase)
    saved_df = pd.read_csv(file_path, parse_dates=['Date'])
    assert len(saved_df) == 1
    assert saved_df.iloc[0]['Pack Name'] == "Test Pack"
    
    # Test appending to existing file
    new_purchase = {
        "Date": datetime.now(),
        "Pack Name": "Test Pack 2",
        "Spending ($)": 200.0,
        "Speed-ups (min)": 2000
    }
    assert save_purchase(str(file_path), new_purchase)
    saved_df = pd.read_csv(file_path, parse_dates=['Date'])
    assert len(saved_df) == 2
    assert saved_df.iloc[1]['Pack Name'] == "Test Pack 2"

def test_calculate_purchase_stats(sample_auto_purchases, sample_manual_purchases):
    """Test purchase statistics calculation."""
    auto_df, _ = sample_auto_purchases
    manual_df, _ = sample_manual_purchases
    
    stats = calculate_purchase_stats(auto_df, manual_df)
    
    # Verify totals
    assert stats["total_spent_auto"] == auto_df["Value (R$)"].sum()
    assert stats["total_spent_manual"] == manual_df["Spending ($)"].sum()
    assert stats["total_speedups"] == manual_df["Speed-ups (min)"].sum()
    
    # Verify daily stats
    assert not stats["spending_by_day"].empty
    assert "Date" in stats["spending_by_day"].columns
    assert "Amount" in stats["spending_by_day"].columns
    assert stats["avg_spending_per_day"] > 0

def test_export_combined_purchases(sample_auto_purchases, sample_manual_purchases, test_data_dir):
    """Test exporting combined purchase history."""
    auto_df, _ = sample_auto_purchases
    manual_df, _ = sample_manual_purchases
    output_path = test_data_dir / "combined_purchases.csv"
    
    # Test export with both dataframes
    assert export_combined_purchases(auto_df, manual_df, str(output_path))
    exported_df = pd.read_csv(output_path, parse_dates=['Date'])
    assert len(exported_df) == len(auto_df) + len(manual_df)
    assert all(col in exported_df.columns for col in ['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source'])
    
    # Test export with only auto purchases
    assert export_combined_purchases(auto_df, None, str(output_path))
    exported_df = pd.read_csv(output_path, parse_dates=['Date'])
    assert len(exported_df) == len(auto_df)
    assert all(exported_df['Source'] == 'Automatic')
    
    # Test export with only manual purchases
    assert export_combined_purchases(None, manual_df, str(output_path))
    exported_df = pd.read_csv(output_path, parse_dates=['Date'])
    assert len(exported_df) == len(manual_df)
    assert all(exported_df['Source'] == 'Manual')
    
    # Test export with no data
    assert not export_combined_purchases(None, None, str(output_path))

def test_error_handling(test_data_dir):
    """Test error handling in purchase manager functions."""
    # Test loading non-existent files
    with pytest.raises(Exception):
        load_purchases("nonexistent_auto.csv", "nonexistent_manual.csv")
    
    # Test saving to invalid path
    with pytest.raises(Exception):
        save_purchase("/invalid/path/purchases.csv", {"Date": datetime.now()})
    
    # Test exporting to invalid path with non-empty DataFrames
    auto_df = pd.DataFrame({
        'Date': [datetime.now()],
        'Pack Name': ['Test Pack'],
        'Value (R$)': [100.0]
    })
    manual_df = pd.DataFrame({
        'Date': [datetime.now()],
        'Pack Name': ['Test Pack'],
        'Spending ($)': [100.0],
        'Speed-ups (min)': [1000]
    })
    with pytest.raises(Exception):
        export_combined_purchases(auto_df, manual_df, "/invalid/path/export.csv") 