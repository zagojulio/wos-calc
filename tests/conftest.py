"""
Pytest configuration and fixtures for Whiteout Survival tests.
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import os
import shutil
from pathlib import Path

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory for test data files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def sample_auto_purchases(test_data_dir):
    """Create sample automatic purchase data."""
    data = {
        'Date': [datetime.now() - timedelta(days=i) for i in range(5)],
        'Purchase Name': [f'Pack {i}' for i in range(5)],
        'Value (R$)': [10.0 * (i + 1) for i in range(5)],
        'Speed-ups (min)': [100 * (i + 1) for i in range(5)]
    }
    df = pd.DataFrame(data)
    file_path = test_data_dir / "purchase_history.csv"
    df.to_csv(file_path, index=False)
    return df, file_path

@pytest.fixture
def sample_manual_purchases(test_data_dir):
    """Create sample manual purchase data."""
    data = {
        'Date': [datetime.now() - timedelta(days=i) for i in range(5)],
        'Pack Name': [f'Manual Pack {i}' for i in range(5)],
        'Spending ($)': [20.0 * (i + 1) for i in range(5)],
        'Speed-ups (min)': [200 * (i + 1) for i in range(5)]
    }
    df = pd.DataFrame(data)
    file_path = test_data_dir / "manual_purchases.csv"
    df.to_csv(file_path, index=False)
    return df, file_path

@pytest.fixture
def mock_session_state():
    """Create a mock Streamlit session state."""
    class MockSessionState:
        """Mock Streamlit session state for testing."""
        def __init__(self):
            self._state = {}
            self.training_params = {
                'days': 0,
                'hours': 4,  # Safe default: 4 hours
                'minutes': 50,  # Safe default: 50 minutes
                'seconds': 0,
                'base_training_time': 290.0,  # 4h 50m in minutes
                'troops_per_batch': 426,  # Safe default: 426 troops
                'points_per_troop': 830.0  # Safe default: 830 points per troop
            }
            self.speedup_inventory = {
                'general': 18000.0,  # Safe default: 18k general speedups
                'construction': 0.0,
                'training': 1515.0,  # Safe default: 1515 training speedups
                'research': 0.0
            }
        
        def __getitem__(self, key):
            return self._state[key]
        
        def __setitem__(self, key, value):
            self._state[key] = value
        
        def __contains__(self, key):
            return key in self._state
        
        def get(self, key, default=None):
            return self._state.get(key, default)
    return MockSessionState()

@pytest.fixture(autouse=True)
def mock_streamlit(monkeypatch, mock_session_state):
    """Mock Streamlit functions and session state."""
    def mock_session_state_getter():
        return mock_session_state
    
    monkeypatch.setattr("streamlit.session_state", mock_session_state_getter())
    monkeypatch.setattr("streamlit.set_page_config", lambda **kwargs: None)
    monkeypatch.setattr("streamlit.title", lambda text: None)
    monkeypatch.setattr("streamlit.markdown", lambda text, **kwargs: None)
    monkeypatch.setattr("streamlit.sidebar", type("Sidebar", (), {"expander": lambda *args, **kwargs: type("Expander", (), {"__enter__": lambda self: self, "__exit__": lambda self, *args: None})()}))
    monkeypatch.setattr("streamlit.columns", lambda n: [type("Column", (), {"__enter__": lambda self: self, "__exit__": lambda self, *args: None})() for _ in range(n)])
    monkeypatch.setattr(
        "streamlit.number_input",
        lambda *args, **kwargs: mock_session_state.get(kwargs.get("key"), kwargs.get("value", 0))
    )
    monkeypatch.setattr("streamlit.text_input", lambda *args, **kwargs: kwargs.get("value", ""))
    monkeypatch.setattr("streamlit.date_input", lambda *args, **kwargs: kwargs.get("value", datetime.now()))
    monkeypatch.setattr("streamlit.button", lambda *args, **kwargs: False)
    monkeypatch.setattr("streamlit.form", lambda *args, **kwargs: type("Form", (), {"__enter__": lambda self: self, "__exit__": lambda self, *args: None})())
    monkeypatch.setattr("streamlit.form_submit_button", lambda *args, **kwargs: False)
    monkeypatch.setattr("streamlit.dataframe", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.error", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.success", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.warning", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.info", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.metric", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.plotly_chart", lambda *args, **kwargs: None)
    monkeypatch.setattr("streamlit.experimental_rerun", lambda: None) 