# Whiteout Survival Calculator

A web-based tool for optimizing resource investments and training strategies in the Whiteout Survival game.

## 🔧 Features

### 🛡️ Training Calculator
- Calculate effective training times with reduction bonuses
- Optimize speed-up usage for maximum points
- Cost analysis and level-based point returns
- Support for multiple speed-up categories
- Scenario comparison tools
- Batch training calculations
- Detailed time input (days, hours, minutes, seconds)

### 💰 Pack Purchases
- Track purchases with date, pack name, cost, and speed-ups included
- Automatic purchase history from CSV file
- Manual purchase entry with CSV persistence
- Combined purchase statistics and analysis
- Daily spending visualization
- Date range filtering
- Export combined purchase history
- Summarized spending and inventory insights

## 📦 Setup

1. Install Python 3.8 or higher  
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

1. Launch the app:
```bash
streamlit run app.py
```

2. Access the web interface at `http://localhost:8501`

3. Navigate between available tools:
   - Training Analysis
   - Pack Purchases

4. Input Parameters (Training):
   - Total Speed-up Minutes Available
   - Base Training Time (days/hours/minutes/seconds)
   - Troops per Batch
   - Training Time Reduction Bonus (%)
   - Points per Troop
   - Target Points (optional)

5. View Results:
   - Effective Training Time
   - Number of Batches
   - Total Points
   - Points per Minute
   - Required Speed-ups for Target

6. Pack Purchases Features:
   - View automatic purchases from CSV
   - Add manual purchases with CSV persistence
   - Filter purchases by date range
   - View combined spending statistics
   - Export combined purchase history
   - Track speed-ups included in purchases

## 📊 Visualizations

- Speed-up Utilization Chart
- Points Progression Overview
- Scenario Comparison Chart
- Daily Spending Bar Chart
- Pack Purchase Tables

## 🧱 Architecture

- Modular layout with separation of concerns:
  - `features/`: core features like training and packs
  - `utils/`, `config/`, `styles/`: helper modules and UI config
  - `calculations.py`: computational logic
  - `visualizations.py`: plotting and chart functions
  - `app.py`: main Streamlit app
- Uses Plotly for interactive charts
- Session-based state for dynamic data flow
- Dark-themed UI with custom CSS
- CSV-based data persistence
- Type hints and docstrings throughout

## 🛠️ Development

- Git workflow with main, dev, and feature branches. Project recently restructured to move all files from `wos-calc/` to root directory for better modular access and simplicity.
- Commit convention: `[TYPE]: description` (e.g., `FEAT: Add pack purchase tracker`)
- `.cursorrules` defines coding and branching standards

## 🧪 Next Steps

- Unit and integration test coverage (`tests/`)
- Add CI/CD pipeline
- Remote GitHub integration
- Enhanced data persistence and export features

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and submit pull requests.