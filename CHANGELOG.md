# Changelog
## [Unreleased]

## [v0.4.0] - 2025-06-22

### Added
- FEAT: Improved sidebar persistence and behavior for Research and Construction entries:
  - Added explicit "Add Entry" buttons for Research and Construction sections in sidebar
  - Users now fill input fields (power, points per power, description, speedup minutes) and click "Add Entry" to persist entries
  - Entries are saved in session state and displayed in Hall of Chiefs tab tables
  - Sidebar inputs reset/clear after adding an entry
  - Sidebar only shows input fields for adding new entries, not existing entries
  - Existing entries remain visible and editable only in main tables within the tab
  - Full persistence across sessions so entries stay in tables after reload
  - Input validation with clear error messages for required fields and numeric checks
  - Success feedback messages on successful entry addition
  - Reactive UI updates reflecting changes immediately
- FEAT: Enhanced Hall of Chiefs Points Efficiency tab with improved functionality:
  - Added Power field to Construction and Research entries for accurate points calculation (Points = Power × Points per Power)
  - Added Description field to Construction entries for better organization and identification
  - Split main summary table into three separate category tables: Construction, Research, and Training
  - Added overall summary table showing average efficiency and total metrics per category
  - Added "Remove All Entries" button with confirmation dialog for bulk clearing
  - Updated Remove button styling to web-friendly red color (#DC3545)
  - Improved session state persistence for all sidebar sections
  - Enhanced UI with category-specific metrics and better data organization
  - Added data editor for inline editing of entries
  - Added export functionality for efficiency data
- FEAT: Implemented Speed-up Minutes Inventory system with centralized speed-up management:
  - New sidebar section "Speed-up Minutes Inventory" with inputs for four categories: General, Construction, Training, and Research
  - General speed-ups usable for any category, category-specific speed-ups for their respective activities
  - Speed-up allocation logic: uses category-specific speed-ups first, then general speed-ups
  - Session state persistence for all speed-up inventory values
  - Enhanced training analysis with speed-up allocation breakdown display
  - JSON file persistence for speed-up inventory data
- FEAT: Implemented Pack Value Comparison tab:
  - Add, compare, and export pack purchase data
  - Calculate cost per speed-up minute from 60min and 5min speedups
  - Sortable, persistent history table with inline editing
  - Remove individual or all entries with confirmation dialogs
  - Export to CSV functionality
  - Input validation and user feedback messages
  - JSON file persistence for pack comparison data
- FEAT: Enhanced Pack Purchases tab with comprehensive functionality:
  - Manual purchase entry with CSV persistence
  - Automatic purchase history loading from CSV file
  - Combined purchase statistics: total spent, average daily spending, daily spending bar chart
  - Date range filtering for purchase tables and statistics
  - Export combined purchase history to CSV
  - Row-level delete functionality for manual purchases with confirmation
  - Speed-up tracking integration
  - Improved UI consistency and error handling

### Changed
- REFACTOR: Updated research points calculation to use direct power input instead of speedup-based estimation
- REFACTOR: Improved Hall of Chiefs data structure to include Power column for better transparency
- REFACTOR: Enhanced session state management for better persistence across all sidebar sections
- REFACTOR: Removed speed-up inputs from Training Parameters section to centralize all speed-up management in the new Speed-up Minutes Inventory
- REFACTOR: Updated training calculations to use the new speed-up inventory system with proper category allocation
- REFACTOR: Updated Hall of Chiefs calculations to use the new speed-up inventory system
- REFACTOR: Updated session state structure to separate training parameters from speed-up inventory
- REFACTOR: Improved app architecture with three main tabs: Pack Purchases, Pack Value Comparison, and Hall of Chiefs
- REFACTOR: Enhanced data persistence with JSON files for speed-up inventory and pack comparison data

### Fixed
- FIX: Resolved session state persistence issues across tab switches
- FIX: Improved error handling for invalid training time inputs
- FIX: Enhanced data validation for all input fields
- FIX: Fixed CSV file operation safety improvements
- FIX: Resolved purchase deletion confirmation handling
- FIX: Improved input validation edge cases
- FIX: Enhanced data persistence reliability

### Tested
- Added comprehensive unit tests for speed-up inventory functionality
- Added integration tests for speed-up allocation logic and training calculations
- Updated existing tests to work with new session state structure
- All tests passing with proper speed-up category allocation and calculation logic
- Comprehensive unit and integration tests added for new modules
- Improved error handling and type hints in modular components
- Current test coverage: 72% (below 80% target - needs improvement)
- All critical paths verified and tested

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

## [v0.1.0] - 2025-06-15

### Added
- Initial release of the application

### Changed
- Initial release of the application

### Fixed
- Initial release of the application

### Tested
- Initial release of the application

## Technical
- TEST: Added comprehensive validation tests for new sidebar input functionality
- TEST: Added integration tests for Add Entry button behavior and input persistence
- TEST: Enhanced test coverage for session state persistence and UI interactions
- TEST: Added comprehensive integration tests for new Hall of Chiefs functionality
- TEST: Updated unit tests to reflect new power-based calculations and data structures
- TEST: Enhanced test coverage for session state persistence and UI interactions
- Comprehensive unit and integration tests added for new modules
- Improved error handling and type hints in modular components
