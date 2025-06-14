"""
Constants used throughout the application.
"""

# Training level points requirements
LEVEL_POINTS = {
    1: 0,
    2: 100,
    3: 300,
    4: 600,
    5: 1000,
    6: 1500,
    7: 2100,
    8: 2800,
    9: 3600,
    10: 4500,
    11: 5500,
    12: 6600,
    13: 7800,
    14: 9100,
    15: 10500,
    16: 12000,
    17: 13600,
    18: 15300,
    19: 17100,
    20: 19000
}

# Default speedup categories
DEFAULT_SPEEDUP_CATEGORIES = {
    "1m": {"cost": 1, "points": 1},
    "5m": {"cost": 4, "points": 5},
    "15m": {"cost": 10, "points": 15},
    "30m": {"cost": 18, "points": 30},
    "1h": {"cost": 30, "points": 60},
    "3h": {"cost": 80, "points": 180},
    "8h": {"cost": 180, "points": 480},
    "24h": {"cost": 450, "points": 1440}
}

# UI Constants
MAX_LEVEL = 20
MIN_LEVEL = 1
MAX_POINTS = 19000
MIN_POINTS = 0 