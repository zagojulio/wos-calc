"""
Unit tests for pack contents summary functionality.
"""

import pytest
import pandas as pd
from unittest.mock import patch, mock_open
import json
from features.pack_contents_summary import (
    load_pack_data,
    aggregate_pack_rewards,
    format_item_name,
    create_pack_summary_dataframe,
    SPEEDUP_CONVERSIONS
)


class TestLoadPackData:
    """Test pack data loading functionality."""
    
    def test_load_pack_data_success(self):
        """Test successful loading of pack data."""
        mock_data = [
            {
                "name": "Test Pack",
                "datetime": "2025-01-01T00:00:00",
                "rewards": {"diamonds": 100, "meat_10k": 50}
            }
        ]
        
        with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
            result = load_pack_data("test_path.json")
            assert result == mock_data
    
    def test_load_pack_data_file_not_found(self):
        """Test handling of missing file."""
        with patch("builtins.open", side_effect=FileNotFoundError("File not found")):
            result = load_pack_data("nonexistent.json")
            assert result == []
    
    def test_load_pack_data_json_error(self):
        """Test handling of invalid JSON."""
        with patch("builtins.open", mock_open(read_data="invalid json")):
            result = load_pack_data("test_path.json")
            assert result == []
    
    def test_load_pack_data_empty_list(self):
        """Test loading empty data."""
        with patch("builtins.open", mock_open(read_data=json.dumps([]))):
            result = load_pack_data("test_path.json")
            assert result == []


class TestAggregatePackRewards:
    """Test pack rewards aggregation functionality."""
    
    def test_aggregate_pack_rewards_basic(self):
        """Test basic aggregation of pack rewards."""
        pack_data = [
            {
                "name": "Pack 1",
                "rewards": {"diamonds": 100, "meat_10k": 50}
            },
            {
                "name": "Pack 2", 
                "rewards": {"diamonds": 200, "wood_10k": 75}
            }
        ]
        
        aggregated, total_speedup = aggregate_pack_rewards(pack_data)
        
        assert aggregated["diamonds"] == 300
        assert aggregated["meat_10k"] == 50
        assert aggregated["wood_10k"] == 75
        assert total_speedup == 0
    
    def test_aggregate_pack_rewards_with_speedups(self):
        """Test aggregation with speed-up conversions."""
        pack_data = [
            {
                "name": "Speed Pack",
                "rewards": {
                    "1h_speedups": 2,
                    "5m_speedups": 10,
                    "1h_speedups_training": 1,
                    "5m_speedups_training": 5
                }
            }
        ]
        
        aggregated, total_speedup = aggregate_pack_rewards(pack_data)
        
        expected_minutes = (2 * 60) + (10 * 5) + (1 * 60) + (5 * 5)  # 120 + 50 + 60 + 25 = 255
        assert aggregated["speedup_minutes"] == expected_minutes
        assert total_speedup == expected_minutes
    
    def test_aggregate_pack_rewards_missing_rewards(self):
        """Test handling of packs without rewards."""
        pack_data = [
            {"name": "Pack 1", "rewards": {"diamonds": 100}},
            {"name": "Pack 2"},  # No rewards
            {"name": "Pack 3", "rewards": {"wood_10k": 50}}
        ]
        
        aggregated, total_speedup = aggregate_pack_rewards(pack_data)
        
        assert aggregated["diamonds"] == 100
        assert aggregated["wood_10k"] == 50
        assert total_speedup == 0
    
    def test_aggregate_pack_rewards_empty_data(self):
        """Test aggregation with empty data."""
        aggregated, total_speedup = aggregate_pack_rewards([])
        
        assert aggregated == {}
        assert total_speedup == 0


class TestFormatItemName:
    """Test item name formatting functionality."""
    
    def test_format_item_name_basic(self):
        """Test basic item name formatting."""
        assert format_item_name("diamonds") == "Diamonds"
        assert format_item_name("meat_10k") == "Meat (10K)"
        assert format_item_name("wood_100k") == "Wood (100K)"
    
    def test_format_item_name_speedup_minutes(self):
        """Test speed-up minutes formatting."""
        assert format_item_name("speedup_minutes") == "Speed-up Minutes"
    
    def test_format_item_name_with_numbers(self):
        """Test formatting with various number suffixes."""
        assert format_item_name("stone_1k") == "Stone (1K)"
        assert format_item_name("exp_books_5k") == "Exp Books (5K)"
    
    def test_format_item_name_complex(self):
        """Test complex item name formatting."""
        assert format_item_name("hero_shards") == "Hero Shards"
        assert format_item_name("combat_books") == "Combat Books"


class TestCreatePackSummaryDataframe:
    """Test DataFrame creation functionality."""
    
    def test_create_pack_summary_dataframe_basic(self):
        """Test basic DataFrame creation."""
        aggregated_rewards = {
            "diamonds": 1000,
            "meat_10k": 500,
            "wood_10k": 300
        }
        
        df = create_pack_summary_dataframe(aggregated_rewards)
        
        assert len(df) == 3
        assert "Item" in df.columns
        assert "Total Quantity" in df.columns
        assert df[df["Item"] == "Diamonds"]["Total Quantity"].iloc[0] == 1000
    
    def test_create_pack_summary_dataframe_with_speedups(self):
        """Test DataFrame creation with speed-ups."""
        aggregated_rewards = {
            "diamonds": 1000,
            "speedup_minutes": 500,
            "meat_10k": 300
        }
        
        df = create_pack_summary_dataframe(aggregated_rewards)
        
        # Speed-up minutes should be first
        assert df.iloc[0]["Item"] == "Speed-up Minutes"
        assert df.iloc[0]["Total Quantity"] == 500
    
    def test_create_pack_summary_dataframe_empty(self):
        """Test DataFrame creation with empty data."""
        df = create_pack_summary_dataframe({})
        
        assert df.empty
    
    def test_create_pack_summary_dataframe_sorting(self):
        """Test DataFrame sorting functionality."""
        aggregated_rewards = {
            "diamonds": 100,
            "speedup_minutes": 500,
            "meat_10k": 1000,
            "wood_10k": 50
        }
        
        df = create_pack_summary_dataframe(aggregated_rewards)
        
        # Speed-up minutes should be first, then sorted by quantity descending
        assert df.iloc[0]["Item"] == "Speed-up Minutes"
        assert df.iloc[1]["Item"] == "Meat (10K)"  # 1000
        assert df.iloc[2]["Item"] == "Diamonds"    # 100
        assert df.iloc[3]["Item"] == "Wood (10K)"  # 50


class TestSpeedupConversions:
    """Test speed-up conversion constants."""
    
    def test_speedup_conversion_constants(self):
        """Test speed-up conversion values."""
        assert SPEEDUP_CONVERSIONS["1h_speedups"] == 60
        assert SPEEDUP_CONVERSIONS["1h_speedups_training"] == 60
        assert SPEEDUP_CONVERSIONS["5m_speedups"] == 5
        assert SPEEDUP_CONVERSIONS["5m_speedups_training"] == 5
    
    def test_speedup_conversion_calculation(self):
        """Test speed-up conversion calculations."""
        pack_data = [
            {
                "name": "Test Pack",
                "rewards": {
                    "1h_speedups": 2,
                    "5m_speedups": 10
                }
            }
        ]
        
        aggregated, total_speedup = aggregate_pack_rewards(pack_data)
        
        expected_minutes = (2 * 60) + (10 * 5)  # 120 + 50 = 170
        assert total_speedup == expected_minutes
        assert aggregated["speedup_minutes"] == expected_minutes


if __name__ == "__main__":
    pytest.main([__file__]) 