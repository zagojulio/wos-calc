# Whiteout Survival Calculator - Feature Tracker

## Implemented Features

### Core Functionality
- ✅ Basic calculation of training times and points
- ✅ Speed-up utilization calculations
- ✅ Points efficiency metrics
- ✅ Multiple scenario comparison
- ✅ Speed-up inventory management with category allocation
- ✅ Hall of Chiefs points efficiency analysis

### User Interface
- ✅ Dark theme implementation
- ✅ Responsive layout
- ✅ Interactive input controls
- ✅ Clear results display
- ✅ Scenario comparison visualization
- ✅ Three-tab navigation: Pack Purchases, Pack Value Comparison, Hall of Chiefs
- ✅ Centralized speed-up inventory sidebar

### Visualizations
- ✅ Speed-up utilization pie chart
- ✅ Points progression line chart
- ✅ Efficiency comparison bar chart
- ✅ Daily spending bar chart
- ✅ Speed-up inventory progress visualization

### Pack Purchases
- ✅ Manual pack entry with cost and speed-ups
- ✅ Automatic purchase history loading from CSV file
- ✅ Persistence of manual purchase entries to CSV
- ✅ Combined purchase statistics: total spent, average daily spending, daily spending bar chart
- ✅ Date range filtering for purchase tables and statistics
- ✅ Export combined purchase history to CSV
- ✅ Tracking of speed-ups included in purchases and relation to training usage
- ✅ Improved UI consistency and error handling for purchases
- ✅ Row-level delete functionality for manual purchases with confirmation

### Pack Value Comparison
- ✅ Add, compare, and export pack purchase data
- ✅ Calculate cost per speed-up minute from 60min and 5min speedups
- ✅ Sortable, persistent history table with inline editing
- ✅ Remove individual or all entries with confirmation dialogs
- ✅ Export to CSV functionality
- ✅ Input validation and user feedback messages
- ✅ JSON file persistence for pack comparison data

### Hall of Chiefs Points Efficiency
- ✅ Compare points gained from Construction, Research, and Training activities
- ✅ Power-based points calculation (Points = Power × Points per Power)
- ✅ Category-specific efficiency analysis
- ✅ Session state persistence for all entries
- ✅ Data editor for inline editing of entries
- ✅ Export functionality for efficiency data
- ✅ Remove individual or all entries with confirmation
- ✅ Speed-up inventory integration and display
- ✅ Overall summary metrics and category breakdowns

### Speed-up Inventory Management
- ✅ Centralized speed-up inventory system
- ✅ Four categories: General, Construction, Training, and Research
- ✅ Category-specific speed-up allocation logic
- ✅ Session state persistence
- ✅ JSON file persistence
- ✅ Visual progress indicators
- ✅ Integration with all calculation modules

### Data Persistence
- ✅ CSV-based purchase history
- ✅ JSON-based speed-up inventory
- ✅ JSON-based pack value comparison data
- ✅ JSON-based Hall of Chiefs entries
- ✅ Session state management across tabs
- ✅ Export functionality for all data types

## Planned Features

### Core Functionality
- [ ] Save/load scenarios
- [ ] Export calculations to CSV
- [ ] Advanced optimization algorithms
- [ ] Resource cost calculations
- [ ] Training queue management

### User Interface
- [ ] Custom theme options
- [ ] Mobile-optimized layout
- [ ] Tutorial/help section
- [ ] Input validation improvements
- [ ] Keyboard shortcuts

### Visualizations
- [ ] 3D efficiency surface plots
- [ ] Interactive scenario comparison
- [ ] Resource usage heatmaps
- [ ] Historical data tracking
- [ ] Custom chart configurations

### Pack Purchases
- [ ] Auto-sum by pack type
- [ ] Visualize purchase trends
- [ ] Export pack logs
- [ ] Pack contents summary integration

### Hall of Chiefs
- [ ] Advanced filtering and sorting options
- [ ] Historical efficiency tracking
- [ ] Performance benchmarking
- [ ] Goal setting and progress tracking

### Speed-up Inventory
- [ ] Usage history tracking
- [ ] Predictive allocation suggestions
- [ ] Cost optimization recommendations
- [ ] Integration with external data sources

## Future Roadmap

### Phase 1 (Current - Q2 2025)
- Focus on core calculation accuracy
- Basic visualization implementation
- User interface refinement
- Speed-up inventory optimization

### Phase 2 (Planned - Q3 2025)
- Advanced optimization features
- Enhanced data persistence
- Improved visualizations
- Mobile optimization
- Pack contents summary integration

### Phase 3 (Future - Q4 2025+)
- Machine learning optimization
- Real-time data integration
- Community features
- API integration
- Advanced analytics dashboard

## Known Issues
- Test coverage currently at 72% (below 80% target)
- Some integration tests failing due to data structure changes
- Pack contents summary feature exists but not integrated into main app

## Contributing
Feel free to contribute to this project by:
1. Reporting bugs
2. Suggesting new features
3. Improving documentation
4. Submitting pull requests
5. Improving test coverage