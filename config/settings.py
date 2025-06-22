"""
Global settings and configuration for the Whiteout Survival Calculator.
"""

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