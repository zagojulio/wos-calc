"""
Custom CSS styles for the Whiteout Survival Calculator application.
"""

CUSTOM_CSS = """
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
    
    /* Red Remove buttons */
    .stButton>button[data-testid*="remove"] {
        background-color: #DC3545;
        color: #FFFFFF;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
        border: none;
        transition: all 0.3s ease;
        min-height: 36px;
    }
    
    .stButton>button[data-testid*="remove"]:hover {
        background-color: #C82333;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(220, 53, 69, 0.3);
    }
    
    /* Remove All Entries button */
    .stButton>button[data-testid*="Remove All Entries"] {
        background-color: #DC3545;
        color: #FFFFFF;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        transition: all 0.3s ease;
        min-height: 44px;
    }
    
    .stButton>button[data-testid*="Remove All Entries"]:hover {
        background-color: #C82333;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
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
""" 