"""
UI Manager for Whiteout Survival Calculator
Handles common UI components and styling.
"""

import streamlit as st

def apply_custom_styling():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown("""
        <style>
        /* Main container */
        .stApp {
            background-color: #1E1E1E;
            color: #FFFFFF;
        }
        
        /* Headers */
        h1, h2, h3 {
            color: #FFFFFF;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        /* Cards and metrics */
        .stMetric {
            background-color: #2D2D2D;
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .stMetric label {
            color: #A0A0A0;
            font-size: 0.9rem;
        }
        
        .stMetric div[data-testid="stMetricValue"] {
            color: #FFFFFF;
            font-size: 1.5rem;
            font-weight: 600;
        }
        
        /* Input fields */
        .stNumberInput>div>div>input {
            background-color: #2D2D2D;
            color: white;
            border: 1px solid #404040;
            border-radius: 4px;
        }
        
        .stNumberInput>div>div>input:focus {
            border-color: #4CAF50;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            border: none;
            transition: background-color 0.3s;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #252525;
        }
        
        /* Table styling */
        .stDataFrame {
            background-color: #2D2D2D;
            border-radius: 8px;
            padding: 1rem;
        }
        
        /* Form styling */
        .stForm {
            background-color: #2D2D2D;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .stMetric {
                margin-bottom: 0.5rem;
            }
        }
        </style>
        """, unsafe_allow_html=True)

def setup_page_config():
    """Configure the Streamlit page settings."""
    st.set_page_config(
        page_title="Whiteout Survival Calculator",
        page_icon="❄️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def render_header():
    """Render the app header and description."""
    st.title("❄️ Whiteout Survival Investment Calculator")
    st.markdown("""
        Optimize your training strategy with precise calculations and visual insights.
        Input your parameters in the sidebar to analyze your training efficiency.
    """) 