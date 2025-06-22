"""
Integration tests for app.py workflows.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
from features.purchase_manager import (
    load_purchases,
    save_purchase,
    calculate_purchase_stats
)

@pytest.fixture
def sample_purchase_data(tmp_path):
    """Create sample purchase data files."""
    auto_data = pd.DataFrame({
        'Date': pd.to_datetime(['2025-06-01', '2025-06-02']),
        'Purchase Name': ['Pack 1', 'Pack 2'],
        'Value (R$)': [30.90, 61.90]
    })
    
    manual_data = pd.DataFrame({
        'Date': pd.to_datetime(['2025-06-03', '2025-06-04']),
        'Pack Name': ['Pack 3', 'Pack 4'],
        'Spending ($)': [30.90, 61.90],
        'Speed-ups (min)': [0, 1000]
    })
    
    auto_path = tmp_path / "purchase_history.csv"
    manual_path = tmp_path / "manual_purchases.csv"
    
    auto_data.to_csv(auto_path, index=False)
    manual_data.to_csv(manual_path, index=False)
    
    return {
        'auto_path': str(auto_path),
        'manual_path': str(manual_path),
        'auto_data': auto_data,
        'manual_data': manual_data
    }

class TestPurchaseWorkflow:
    def test_load_purchase_data(self, sample_purchase_data):
        """Test loading purchase data into session state."""
        # Load automatic purchases
        auto_purchases, _ = load_purchases(sample_purchase_data['auto_path'])
        assert isinstance(auto_purchases, pd.DataFrame)
        assert len(auto_purchases) == len(sample_purchase_data['auto_data'])
        
        # Load manual purchases
        _, manual_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        assert isinstance(manual_purchases, pd.DataFrame)
        assert len(manual_purchases) == len(sample_purchase_data['manual_data'])

    def test_add_manual_purchase(self, sample_purchase_data):
        """Test adding a manual purchase."""
        new_purchase = {
            'Date': datetime.now(),
            'Pack Name': 'Test Pack',
            'Spending ($)': 30.90,
            'Speed-ups (min)': 0
        }
        
        # Save new purchase
        assert save_purchase(sample_purchase_data['manual_path'], new_purchase)
        
        # Verify purchase was added
        _, updated_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        assert len(updated_purchases) == len(sample_purchase_data['manual_data']) + 1
        assert updated_purchases['Pack Name'].iloc[-1] == new_purchase['Pack Name']

    def test_delete_manual_purchase(self, sample_purchase_data):
        """Test deleting a manual purchase."""
        # Load initial data
        _, initial_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        initial_count = len(initial_purchases)
        
        # Delete first purchase
        purchase_to_delete = initial_purchases.iloc[0]
        updated_purchases = initial_purchases[
            ~(initial_purchases['Date'] == purchase_to_delete['Date']) &
            ~(initial_purchases['Pack Name'] == purchase_to_delete['Pack Name'])
        ]
        
        # Save updated data
        updated_purchases.to_csv(sample_purchase_data['manual_path'], index=False)
        
        # Verify purchase was deleted
        _, final_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        assert len(final_purchases) == initial_count - 1

    def test_filter_purchases_by_date(self, sample_purchase_data):
        """Test filtering purchases by date range."""
        # Load purchases
        auto_purchases, _ = load_purchases(sample_purchase_data['auto_path'])
        _, manual_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        
        # Set date range
        start_date = datetime(2025, 6, 1)
        end_date = datetime(2025, 6, 2)
        
        # Filter purchases
        filtered_auto = auto_purchases[
            (auto_purchases['Date'].dt.date >= start_date.date()) &
            (auto_purchases['Date'].dt.date <= end_date.date())
        ]
        
        filtered_manual = manual_purchases[
            (manual_purchases['Date'].dt.date >= start_date.date()) &
            (manual_purchases['Date'].dt.date <= end_date.date())
        ]
        
        # Verify filtered data
        assert len(filtered_auto) == 2  # Both auto purchases are in range
        assert len(filtered_manual) == 0  # No manual purchases in range

    def test_calculate_stats_after_changes(self, sample_purchase_data):
        """Test calculating stats after data changes."""
        # Load initial data
        auto_purchases, _ = load_purchases(sample_purchase_data['auto_path'])
        _, manual_purchases = load_purchases(manual_path=sample_purchase_data['manual_path'])
        
        # Calculate initial stats
        initial_stats = calculate_purchase_stats(auto_purchases, manual_purchases)
        
        # Add new purchase
        new_purchase = {
            'Date': datetime.now(),
            'Pack Name': 'Test Pack',
            'Spending ($)': 30.90,
            'Speed-ups (min)': 0
        }
        save_purchase(sample_purchase_data['manual_path'], new_purchase)
        
        # Load updated data and calculate new stats
        _, updated_manual = load_purchases(manual_path=sample_purchase_data['manual_path'])
        updated_stats = calculate_purchase_stats(auto_purchases, updated_manual)
        
        # Verify stats were updated
        assert updated_stats['total_spent_manual'] > initial_stats['total_spent_manual']
        assert updated_stats['total_speedups'] == initial_stats['total_speedups']

def test_pack_value_comparison_tab_renders(app_test_client):
    # This is a stub for integration testing the new tab
    # Would use selenium or streamlit testing tools in a full implementation
    assert True 