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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        /* Headers - Improved font sizes and spacing */
        h1 {
            color: #FFFFFF;
            font-weight: 700;
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }
        
        h2 {
            color: #FFFFFF;
            font-weight: 600;
            font-size: 1.8rem;
            margin-bottom: 1.25rem;
            line-height: 1.3;
        }
        
        h3 {
            color: #FFFFFF;
            font-weight: 600;
            font-size: 1.4rem;
            margin-bottom: 1rem;
            line-height: 1.4;
        }
        
        /* Cards and metrics - Improved spacing and contrast */
        .stMetric {
            background-color: #2D2D2D;
            padding: 1.5rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid #404040;
        }
        
        .stMetric label {
            color: #E0E0E0;
            font-size: 1.1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        .stMetric div[data-testid="stMetricValue"] {
            color: #FFFFFF;
            font-size: 1.8rem;
            font-weight: 700;
            line-height: 1.2;
        }
        
        /* Input fields - Improved sizing and contrast */
        .stNumberInput>div>div>input {
            background-color: #2D2D2D;
            color: #FFFFFF;
            border: 2px solid #404040;
            border-radius: 8px;
            padding: 0.75rem;
            font-size: 1rem;
            font-weight: 500;
        }
        
        .stNumberInput>div>div>input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        
        .stNumberInput label {
            color: #E0E0E0;
            font-size: 1rem;
            font-weight: 500;
            margin-bottom: 0.5rem;
        }
        
        /* Buttons - Improved sizing and spacing */
        .stButton>button {
            background-color: #4CAF50;
            color: #FFFFFF;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            transition: all 0.3s ease;
            min-height: 44px;
        }
        
        .stButton>button:hover {
            background-color: #45a049;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar - Improved contrast and spacing */
        .css-1d391kg {
            background-color: #252525;
        }
        
        .css-1d391kg .stExpander {
            background-color: #2D2D2D;
            border-radius: 8px;
            margin-bottom: 1rem;
            border: 1px solid #404040;
        }
        
        .css-1d391kg .stExpander .streamlit-expanderHeader {
            background-color: #2D2D2D;
            color: #E0E0E0;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 1rem;
        }
        
        /* Table styling - Improved readability */
        .stDataFrame {
            background-color: #2D2D2D;
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #404040;
        }
        
        /* Form styling - Consistent spacing */
        .stForm {
            background-color: #2D2D2D;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            border: 1px solid #404040;
        }
        
        /* Warning and info boxes - Improved contrast */
        .stAlert {
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            border: 1px solid;
        }
        
        /* Tabs - Improved styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #2D2D2D;
            border-radius: 8px;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #404040;
            border-radius: 6px;
            color: #E0E0E0;
            font-weight: 500;
            padding: 0.75rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #4CAF50;
            color: #FFFFFF;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            h1 { font-size: 2rem; }
            h2 { font-size: 1.5rem; }
            h3 { font-size: 1.2rem; }
            
            .stMetric {
                margin-bottom: 1rem;
                padding: 1rem;
            }
            
            .stMetric div[data-testid="stMetricValue"] {
                font-size: 1.5rem;
            }
        }
        
        /* Focus indicators for accessibility */
        *:focus {
            outline: 2px solid #4CAF50;
            outline-offset: 2px;
        }
        
        /* High contrast mode support */
        @media (prefers-contrast: high) {
            .stMetric {
                border: 2px solid #FFFFFF;
            }
            
            .stNumberInput>div>div>input {
                border: 2px solid #FFFFFF;
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
        <div style="font-size: 1.1rem; line-height: 1.6; color: #E0E0E0; margin-bottom: 2rem;">
            Optimize your training strategy with precise calculations and visual insights.
            Input your parameters in the sidebar to analyze your training efficiency.
        </div>
    """, unsafe_allow_html=True) 