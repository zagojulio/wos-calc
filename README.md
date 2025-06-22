# Whiteout Survival Calculator

A web-based tool for optimizing resource investments and training strategies in the Whiteout Survival game.

## 🔧 Features

### 🛡️ Hall of Chiefs Points Efficiency
- Compare points gained from Construction, Research, and Training activities
- Power-based points calculation (Points = Power × Points per Power)
- Category-specific efficiency analysis with detailed metrics
- Session state persistence for all entries across sessions
- Data editor for inline editing of entries
- Export functionality for efficiency data
- Remove individual or all entries with confirmation dialogs
- Speed-up inventory integration and real-time display

### 💰 Pack Purchases
- Track purchases with date, pack name, cost, and speed-ups included
- Automatic purchase history from CSV file
- Manual purchase entry with CSV persistence
- Combined purchase statistics and analysis
- Daily spending visualization with interactive charts
- Date range filtering for purchase tables and statistics
- Export combined purchase history to CSV
- Row-level delete functionality for manual purchases
- Summarized spending and inventory insights

### 📦 Pack Value Comparison
- Add, compare, and export pack purchase data
- Calculate cost per speed-up minute from 60min and 5min speedups
- Sortable, persistent history table with inline editing
- Remove individual or all entries with confirmation dialogs
- Export to CSV functionality
- Input validation and user feedback messages
- JSON file persistence for pack comparison data

### ⚡ Speed-up Inventory Management
- Centralized speed-up inventory system with four categories
- General speed-ups usable for any category
- Category-specific speed-ups for Construction, Training, and Research
- Smart allocation logic: uses category-specific speed-ups first, then general
- Session state persistence and JSON file storage
- Visual progress indicators and real-time updates
- Integration with all calculation modules

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

3. Navigate between three main tools:
   - **Pack Purchases**: Track and analyze purchase history
   - **Pack Value Comparison**: Compare pack costs and efficiency
   - **Hall of Chiefs**: Analyze points efficiency across activities

4. Speed-up Inventory (Sidebar):
   - Set your available speed-ups by category
   - General speed-ups work for any activity
   - Category-specific speed-ups are used first
   - Click "Update Speedup Inventory" to save changes

5. Hall of Chiefs Usage:
   - Add Construction entries: Power, Points per Power (30/45), Description, Speed-up Minutes
   - Add Research entries: Power, Points per Power (30/45), Description, Speed-up Minutes
   - Add Training entries: Time parameters, Troops per Batch, Points per Troop
   - View efficiency metrics and category summaries
   - Export data for external analysis

6. Pack Purchases Usage:
   - View automatic purchases from CSV
   - Add manual purchases with form
   - Filter by date range
   - View combined spending statistics
   - Export combined purchase history
   - Delete manual purchases with confirmation

7. Pack Value Comparison Usage:
   - Add packs with name, price, and speed-up quantities
   - View cost per minute calculations
   - Sort and filter pack data
   - Remove individual or all entries
   - Export comparison data to CSV

## 📊 Visualizations

- Speed-up Utilization Chart
- Points Progression Overview
- Scenario Comparison Chart
- Daily Spending Bar Chart
- Speed-up Inventory Progress Visualization
- Hall of Chiefs Efficiency Metrics
- Pack Purchase Tables

## 🧱 Architecture

- Modular layout with separation of concerns:
  - `features/`: core features (purchase_manager, pack_value_comparison, hall_of_chiefs, speedup_inventory)
  - `utils/`, `config/`, `styles/`: helper modules and UI config
  - `calculations.py`: computational logic
  - `visualizations.py`: plotting and chart functions
  - `app.py`: main Streamlit app with three-tab navigation
- Uses Plotly for interactive charts
- Session-based state for dynamic data flow
- Dark-themed UI with custom CSS
- CSV and JSON-based data persistence
- Type hints and docstrings throughout

## 🛠️ Development

- Git workflow with main, dev, and feature branches
- Commit convention: `[TYPE]: description` (e.g., `FEAT: Add pack purchase tracker`)
- Comprehensive test suite with 72% coverage (target: 80%)
- Modular architecture for maintainability

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Current test coverage: 72% (needs improvement to reach 80% target)

## 📁 Data Files

- `data/purchase_history.csv`: Automatic purchase history
- `data/manual_purchases.csv`: Manual purchase entries
- `data/pack_value_comparison.json`: Pack comparison data
- `data/hall_of_chiefs_data.json`: Hall of Chiefs entries
- `data/speedup_inventory.json`: Speed-up inventory data
- `data/pack_items.json`: Pack contents data (not currently integrated)

## 🤝 Contributing

Contributions are welcome! Feel free to open issues and submit pull requests.

### Current Priorities
1. Improve test coverage to 80%
2. Fix failing integration tests
3. Integrate pack contents summary feature
4. Enhance error handling and validation