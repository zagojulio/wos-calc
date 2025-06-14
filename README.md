# Whiteout Survival Calculator

A web-based tool for optimizing resource investments and training strategies in the Whiteout Survival game.

## 🔧 Features

### Training Calculator
- Calculate effective training times with reduction bonuses
- Optimize speed-up usage for maximum points
- Cost analysis and level-based point returns
- Support for multiple speed-up categories
- Scenario comparison tools

### Pack Purchases
- Track purchases with date, pack name, cost, and speed-ups included
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

3. Navigate between the available tabs:
   - Training Analysis
   - Pack Purchases

## 📊 Visualizations

- Speed-up Utilization Charts
- Points Efficiency Overview
- Purchase Table View

## 🧱 Architecture

- Modular layout: `features/`, `pages/`, `utils/`, `styles/`, `config/`
- Type hints and docstrings throughout
- Session-based state for dynamic data
- Dark-themed UI with custom CSS

## 🛠️ Development

- Git workflow with `main`, `dev`, and feature branches
- Commit convention: `[TYPE]: description` (e.g., `FEAT: Add pack purchase tracker`)
- `.cursorrules` defines coding and branching standards

## 🧪 Next Steps

- Unit and integration test coverage (`tests/`)
- Add CI/CD pipeline
- Remote GitHub integration
- Enhanced data persistence and export features

## 🤝 Contributing

Feel free to open issues and submit pull requests with improvements or features.
