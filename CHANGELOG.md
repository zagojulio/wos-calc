# Changelog
## [Unreleased]

### Added
- FEAT: Implemented Speed-up Minutes Inventory system with centralized speed-up management:
  - New sidebar section "Speed-up Minutes Inventory" with inputs for four categories: General, Construction, Training, and Research
  - General speed-ups usable for any category, category-specific speed-ups for their respective activities
  - Speed-up allocation logic: uses category-specific speed-ups first, then general speed-ups
  - Session state persistence for all speed-up inventory values
  - Enhanced training analysis with speed-up allocation breakdown display
- FEAT: Implemented Pack Contents Summary feature in Pack Purchases tab. Aggregates all pack rewards, converts speed-ups to total minutes, and displays a sortable, searchable summary table with a summary row. Includes error handling and is fully reactive to data changes.
- FEAT: Implemented Pack Value Comparison tab. Allows adding/removing packs with price and speed-up minutes, calculates cost per minute, displays a sortable and persistent table, includes export to CSV, confirmation modals, and user feedback messages.

### Changed
- REFACTOR: Removed speed-up inputs from Training Parameters section to centralize all speed-up management in the new Speed-up Minutes Inventory
- REFACTOR: Updated training calculations to use the new speed-up inventory system with proper category allocation
- REFACTOR: Updated Hall of Chiefs calculations to use the new speed-up inventory system
- REFACTOR: Updated session state structure to separate training parameters from speed-up inventory

### Fixed

### Tested
- Added comprehensive unit tests for speed-up inventory functionality
- Added integration tests for speed-up allocation logic and training calculations
- Updated existing tests to work with new session state structure
- All tests passing with proper speed-up category allocation and calculation logic

## [v0.2.2] - 2025-06-15

### Added
- Restored "Total Points" metric calculation and display in the Training Analysis Results section.
  - Total Points calculated as batches * points_per_batch + current_points.
  - Display updates reactively with parameter changes.
  - Metric formatted with thousands separators for readability.
- Removed redundant "Batches to Target" metric to simplify UI.

## [v0.2.1] - 2025-06-15

### Added
- Core calculation engine for training times and points
- Speed-up utilization tracking and optimization
- Points efficiency metrics and target calculations
- Multiple scenario comparison functionality
- Dark theme UI with responsive layout
- Interactive visualizations:
  - Speed-up utilization pie chart
  - Points progression line chart
  - Efficiency comparison bar chart
- Pack purchase management:
  - Manual entry with CSV persistence
  - Automatic history loading
  - Combined statistics and filtering
  - Export functionality
  - Speed-up tracking integration
- Modularized codebase by splitting `app.py` into feature-specific modules:
  - `features/ui_manager.py` for UI components and styling
  - `features/training_manager.py` for training tab logic and UI
  - `utils/session_manager.py` for Streamlit session state management
- Comprehensive unit and integration tests added for new modules
- Improved error handling and type hints in modular components

### Changed
- Unified purchase data display and interaction
- Improved UI organization and layout
- Enhanced error handling and data validation
- Optimized calculation performance
- Refactored app architecture to improve maintainability and scalability
- Updated session state management across modules for consistency
- Enhanced test coverage to 62% with focus on core calculation and purchase management logic

### Fixed
- CSV file operation safety improvements
- Purchase deletion confirmation handling
- Input validation edge cases
- Data persistence reliability

### Tested
- Core calculation unit tests
- Purchase management integration tests
- UI component tests
- Error handling validation
- Current test coverage: 62%
- All critical paths verified
- Verified all modular components run without regression and maintain UI/UX consistency

## [v0.2.0] - 2025-06-15

### Added
- Manual purchase entries are now persisted to CSV (`data/manual_purchases.csv`).
- Automatic purchase history loaded from CSV (`data/purchase_history.csv`).
- Combined purchase statistics including total spent, average spending per day, and daily spending bar chart.
- Date range filtering for all purchase tables and statistics.
- Export functionality to download combined purchase history as CSV.
- Tracking of speed-ups included in purchases related to training usage.
- New UI improvements: consistent styling between manual and automatic purchase tables, clear section separation, and combined summary area.
- Row-level delete functionality for manual purchases with confirmation dialogs.

### Changed
- Refactored Pack Purchases tab to unify manual and automatic purchase data display and interaction.
- Improved UI organization and layout for better user experience.
- Maintained consistent dark theme styling across all new features.

### Fixed
- Safe file operations to prevent CSV corruption during manual purchase persistence.
- Graceful handling of missing or malformed CSV files.
- Fixed bug causing errors when deleting purchases due to improper selectbox formatting.

### Tested
- Implemented comprehensive unit and integration test suites covering core calculation and purchase management functions.
- Added error handling tests for invalid inputs and file operations.
- Achieved 62% test coverage with all tests passing and no regressions.
- Verified robustness against missing data and edge cases.
- Planned next steps for UI/end-to-end testing and visualization coverage.
