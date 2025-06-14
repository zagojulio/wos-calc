"""
Global settings and configuration for the Whiteout Survival Calculator.
"""

# Default values
DEFAULT_TRAINING_TIME = {
    "days": 0,
    "hours": 4,
    "minutes": 57,
    "seconds": 0
}

DEFAULT_TROOPS_PER_BATCH = 426
DEFAULT_POINTS_PER_TROOP = 830
DEFAULT_TIME_REDUCTION_BONUS = 20.0
DEFAULT_SPEEDUPS = {
    "general": 5000.0,
    "training": 5000.0
}

# UI Configuration
PAGE_CONFIG = {
    "page_title": "Whiteout Survival Calculator",
    "page_icon": "❄️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Input Constraints
INPUT_CONSTRAINTS = {
    "speedups": {
        "min_value": 0.0,
        "step": 100.0
    },
    "time_reduction": {
        "min_value": 0.0,
        "max_value": 100.0,
        "step": 1.0
    },
    "troops_per_batch": {
        "min_value": 1,
        "step": 1
    },
    "points_per_troop": {
        "min_value": 1.0,
        "step": 1.0
    }
}

# File Paths
DATA_DIR = "data"
SAMPLE_PACKS_FILE = "sample_packs.csv" 