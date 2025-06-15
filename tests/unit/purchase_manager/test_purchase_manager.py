"""
Unit tests for purchase_manager.py module.
"""

import pytest
import pandas as pd
import os
from datetime import datetime
from features.purchase_manager import (
    load_purchases,
    save_purchase,
    calculate_purchase_stats,
    export_combined_purchases
)

@pytest.fixture
def temp_csv_dir(tmp_path):
    """Create a temporary directory for test CSV files."""
    return tmp_path

@pytest.fixture
def sample_auto_purchases():
    """Create sample automatic purchase data."""
    return pd.DataFrame({
        'Date': pd.to_datetime(['2025-06-01', '2025-06-02']),
        'Purchase Name': ['Pack 1', 'Pack 2'],
        'Value (R$)': [30.90, 61.90]
    })

@pytest.fixture
def sample_manual_purchases():
    """Create sample manual purchase data."""
    return pd.DataFrame({
        'Date': pd.to_datetime(['2025-06-03', '2025-06-04']),
        'Pack Name': ['Pack 3', 'Pack 4'],
        'Spending ($)': [30.90, 61.90],
        'Speed-ups (min)': [0, 1000]
    })

class TestLoadPurchases:
    def test_load_valid_csv(self, temp_csv_dir, sample_auto_purchases):
        """Test loading a valid CSV file."""
        csv_path = temp_csv_dir / "test_purchases.csv"
        sample_auto_purchases.to_csv(csv_path, index=False)
        
        loaded_df = load_purchases(str(csv_path))
        assert isinstance(loaded_df, pd.DataFrame)
        assert len(loaded_df) == len(sample_auto_purchases)
        assert all(col in loaded_df.columns for col in sample_auto_purchases.columns)

    def test_load_nonexistent_file(self):
        """Test loading a nonexistent file."""
        with pytest.raises(Exception):
            load_purchases("nonexistent.csv")

    def test_load_invalid_csv(self, temp_csv_dir):
        """Test loading an invalid CSV file."""
        csv_path = temp_csv_dir / "invalid.csv"
        with open(csv_path, 'w') as f:
            f.write("invalid,csv,data\n")
        
        with pytest.raises(Exception):
            load_purchases(str(csv_path))

class TestSavePurchase:
    def test_save_new_purchase(self, temp_csv_dir):
        """Test saving a new purchase to a new file."""
        csv_path = temp_csv_dir / "new_purchases.csv"
        purchase = {
            'Date': datetime.now(),
            'Pack Name': 'Test Pack',
            'Spending ($)': 30.90,
            'Speed-ups (min)': 0
        }
        
        assert save_purchase(str(csv_path), purchase)
        assert os.path.exists(csv_path)
        
        loaded_df = pd.read_csv(csv_path)
        assert len(loaded_df) == 1
        assert loaded_df['Pack Name'].iloc[0] == purchase['Pack Name']

    def test_append_existing_purchase(self, temp_csv_dir, sample_manual_purchases):
        """Test appending a purchase to an existing file."""
        csv_path = temp_csv_dir / "existing_purchases.csv"
        sample_manual_purchases.to_csv(csv_path, index=False)
        
        new_purchase = {
            'Date': datetime.now(),
            'Pack Name': 'New Pack',
            'Spending ($)': 30.90,
            'Speed-ups (min)': 0
        }
        
        assert save_purchase(str(csv_path), new_purchase)
        loaded_df = pd.read_csv(csv_path)
        assert len(loaded_df) == len(sample_manual_purchases) + 1

class TestCalculatePurchaseStats:
    def test_calculate_stats_with_data(self, sample_auto_purchases, sample_manual_purchases):
        """Test calculating stats with both auto and manual purchases."""
        stats = calculate_purchase_stats(sample_auto_purchases, sample_manual_purchases)
        
        assert stats['total_spent_auto'] == sample_auto_purchases['Value (R$)'].sum()
        assert stats['total_spent_manual'] == sample_manual_purchases['Spending ($)'].sum()
        assert stats['total_speedups'] == sample_manual_purchases['Speed-ups (min)'].sum()
        assert isinstance(stats['spending_by_day'], pd.DataFrame)

    def test_calculate_stats_empty_data(self):
        """Test calculating stats with empty data."""
        stats = calculate_purchase_stats(None, None)
        
        assert stats['total_spent_auto'] == 0
        assert stats['total_spent_manual'] == 0
        assert stats['total_speedups'] == 0
        assert stats['spending_by_day'].empty

class TestExportCombinedPurchases:
    def test_export_combined_data(self, temp_csv_dir, sample_auto_purchases, sample_manual_purchases):
        """Test exporting combined purchase data."""
        output_path = temp_csv_dir / "combined_purchases.csv"
        
        assert export_combined_purchases(
            sample_auto_purchases,
            sample_manual_purchases,
            str(output_path)
        )
        
        assert os.path.exists(output_path)
        loaded_df = pd.read_csv(output_path)
        assert len(loaded_df) == len(sample_auto_purchases) + len(sample_manual_purchases)

    def test_export_empty_data(self, temp_csv_dir):
        """Test exporting with empty data."""
        output_path = temp_csv_dir / "empty_combined.csv"
        
        assert not export_combined_purchases(None, None, str(output_path))
        assert not os.path.exists(output_path) 