# Changelog

## [Unreleased] - 2025-06-14

### Added
- Manual purchase entries are now persisted to CSV (`data/manual_purchases.csv`).
- Automatic purchase history loaded from CSV (`data/purchase_history.csv`).
- Combined purchase statistics including total spent, average spending per day, and daily spending bar chart.
- Date range filtering for all purchase tables and statistics.
- Export functionality to download combined purchase history as CSV.
- Tracking of speed-ups included in purchases related to training usage.
- New UI improvements: consistent styling between manual and automatic purchase tables, clear section separation, and combined summary area.
- Enhanced error handling with user-friendly messages for CSV load/save operations.

### Changed
- Refactored Pack Purchases tab to unify manual and automatic purchase data display and interaction.
- Improved UI organization and layout for better user experience.
- Maintained consistent dark theme styling across all new features.

### Fixed
- Safe file operations to prevent CSV corruption during manual purchase persistence.
- Graceful handling of missing or malformed CSV files.
