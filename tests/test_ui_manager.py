"""
Tests for the UI manager module.
"""

import pytest
from features.ui_manager import (
    apply_custom_styling,
    setup_page_config,
    render_header
)

def test_apply_custom_styling():
    """Test custom styling application."""
    # This is mostly a smoke test since we can't easily verify CSS
    apply_custom_styling()
    # No assertions needed as we're just verifying no exceptions

def test_setup_page_config():
    """Test page configuration setup."""
    # This is mostly a smoke test since we can't easily verify Streamlit config
    setup_page_config()
    # No assertions needed as we're just verifying no exceptions

def test_render_header():
    """Test header rendering."""
    # This is mostly a smoke test since we can't easily verify Streamlit UI
    render_header()
    # No assertions needed as we're just verifying no exceptions

def test_ui_consistency():
    """Test UI consistency across different screen sizes."""
    # This would typically be an integration test with a UI testing framework
    # For now, we'll just verify the functions don't raise exceptions
    apply_custom_styling()
    setup_page_config()
    render_header()
    # No assertions needed as we're just verifying no exceptions 