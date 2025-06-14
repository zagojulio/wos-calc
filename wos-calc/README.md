# Whiteout Survival Calculator

A web-based calculator for optimizing training times and points in Whiteout Survival game.

## Features

- Calculate effective training times with reduction bonuses
- Optimize speed-up usage for maximum points
- Compare multiple training scenarios
- Interactive visualizations of training efficiency
- Batch training calculations
- Detailed time input (days, hours, minutes, seconds)

## Setup

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Launch the app:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

3. Input Parameters:
   - Total Speed-up Minutes Available
   - Base Training Time (days/hours/minutes/seconds)
   - Troops per Batch
   - Training Time Reduction Bonus (%)
   - Points per Troop
   - Target Points (optional)

4. View Results:
   - Effective Training Time
   - Number of Batches
   - Total Points
   - Points per Minute
   - Required Speed-ups for Target

## Visualizations

- Speed-up Utilization Chart
- Points Progression Chart
- Scenario Comparison Chart

## Technical Details

- Built with Streamlit
- Uses Plotly for interactive visualizations
- Modular architecture with separate calculation and visualization modules

## Contributing

Feel free to submit issues and enhancement requests.