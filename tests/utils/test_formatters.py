"""
Unit tests for utils/formatters.py
"""
import pytest
from utils.formatters import format_currency, format_duration, format_number

def test_format_currency_typical():
    assert format_currency(1234.56) == "$1,234.56"
    assert format_currency(0) == "$0.00"
    assert format_currency(-99.99) == "$-99.99"

def test_format_currency_large():
    assert format_currency(123456789.987) == "$123,456,789.99"

def test_format_duration_typical():
    assert format_duration(60) == "1h"
    assert format_duration(90) == "1h 30m"
    assert format_duration(1440) == "1d"
    assert format_duration(1500) == "1d 1h"
    assert format_duration(0) == "0m"
    assert format_duration(59) == "59m"
    assert format_duration(61) == "1h 1m"
    assert format_duration(2881) == "2d 1m"

def test_format_duration_negative():
    # Negative durations should still format, but as negative minutes
    assert format_duration(-5) == "-5m"

def test_format_number_typical():
    assert format_number(1000) == "1,000"
    assert format_number(1234567.89) == "1,234,568"
    assert format_number(0) == "0"
    assert format_number(-1234) == "-1,234" 