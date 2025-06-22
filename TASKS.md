# Whiteout Survival - To-Do List

## Done
- [x] Refactor collapsible sidebar to be specific to the Training tab only:
      - Show training parameter controls in sidebar only when Training tab is active
      - Clear or hide sidebar content on other tabs (e.g., Pack Purchases)
      - Ensure sidebar inputs persist with session state across tab switches
      - Consider moving sidebar controls into an in-page collapsible expander as an alternative
- [x] Merge manual and automatic purchase histories into a single unified table:
      - Fill missing speed-up minutes with 0
- [x] Add row-level delete/remove functionality in the purchase history table:
      - Confirm deletion before removing
      - Update CSV and session state accordingly
- [x] Modularize `app.py` to improve maintainability and scalability:
      - Split large app.py into `purchase_manager.py`, `training_manager.py`
      - Simplified app.py to handle layout/routing only
      - Verified session state and UI integrity
- [x] Pack Contents Summary feature (aggregate, convert, and display all pack rewards in Pack Purchases tab)

## UI Improvements
- [ ] Implement persistent configuration saving and loading:
      - Save current training parameters and app configurations to a local JSON file
      - Load saved configuration on app startup to pre-populate defaults
      - Provide a UI control (e.g., save button) to trigger saving
      - Sync configurations with st.session_state for reactive UI
- [x] Restore the "Total Points" calculation and display in the Training Analysis Results section:
      - Recalculate total points correctly based on batches and points per batch
      - Add a metric display for "Total Points" in the UI alongside other training metrics
      - Ensure the value updates reactively with parameter changes
      - Add corresponding test scenarios to verify correct calculation and display
- [ ] Replace all deprecated `st.experimental_rerun` calls with `st.rerun` in the codebase to ensure future compatibility with Streamlit updates

## Next Features / Enhancements
- [x] Plan and prioritize next feature implementation after sidebar refactor
- [ ] Review existing tabs and identify UI/UX refinements
- [ ] Implement Pack Contents Summary in Pack Purchases tab:
      - Aggregate and display total quantities of all pack items purchased
      - Calculate total speed-up minutes converting all speed-up types to minutes
      - Show sortable table/grid with item names and totals
      - Add reactive updates on purchase changes
      - Ensure consistent UI styling and responsive layout

## Pack Purchases Tab Improvements
- [ ] Consider adding:
      - Editable rows for manual purchases
      - Search, filter, and sorting capabilities
      - Pagination or virtualization for large data sets
      - Undo feature for recent deletions
      - Enhanced visual summaries (sparklines, trend indicators)


## Test Scenarios

### UI Improvements

#### Refactor collapsible sidebar to be training-tab specific
- Load app, select Training tab → sidebar shows training parameter controls
- Switch to Pack Purchases tab → sidebar hides training controls
- Enter values in sidebar inputs, switch tabs, then return to Training tab → inputs persist
- Verify sidebar is empty or shows appropriate message on non-training tabs
- (Optional) Move sidebar controls to in-page expander → test expand/collapse, input persistence

#### Persistent configuration saving and loading
- Modify training parameters, click "Save" → config file created or updated correctly
- Reload app → saved config loaded and inputs pre-populated accordingly
- Corrupt or delete config file, reload app → fallback to defaults without crash
- Change config, reload app multiple times → values remain consistent
- UI triggers save correctly and shows confirmation or error messages

### Pack Purchases Tab Improvements

#### Merge manual and automatic purchase histories into a single table
- Load app with both manual and automatic purchases → all appear in one table
- Records missing speed-up minutes show 0 in that column
- Sorting and filtering (if implemented) work correctly on combined table
- Table refresh (via reload button) keeps merged state consistent

#### Add row-level delete/remove functionality
- Click delete on a manual purchase row → confirmation appears → confirm → row removed and persisted
- Attempt deletion cancellation → row remains
- Delete an automatic purchase (if allowed) → verify removal and persistence
- Delete last remaining row → table shows empty state gracefully
- Verify error handling on delete failure (e.g., file write error)

#### Additional UX enhancements (optional)
- Edit manual purchase entries inline → changes persist correctly
- Search bar filters results dynamically
- Date range filter updates table and stats correctly
- Pagination loads correct rows per page
- Undo recent deletion restores row
- Visual summary elements display accurate data


## Pack Contents Summary Feature

### Purpose
- Provide aggregated totals of all items obtained from pack purchases, including a detailed breakdown of speed-up minutes.

### Layout
- Scrollable table or grid with item names and total quantities.
- Sortable columns.
- Summary row showing total speed-up minutes.
- Toggle or collapsible panel to show/hide summary.

### Functionalities
- Aggregate rewards data from all packs.
- Convert speed-ups to total minutes.
- Reactive updates on purchase history changes.
- Dark theme, responsive design.

### Test Scenarios
- Validate aggregation and conversion accuracy.
- UI responsiveness and error handling.

# Pack Value Comparison Tab

### Purpose
- Compare cost efficiency of packs by price per speed-up minute

### Layout
- Header: "Pack Value Comparison"
- Input fields: Pack Name, Price (currency), Speed-up Minutes
- Add Button: "Add Pack"
- Price History Table:
    - Columns: Pack Name, Price, Speed-up Minutes, Cost per Minute
    - Sortable columns, default sorted by Cost per Minute ascending
- Actions: Remove entry, Clear all entries, Export CSV
- Optional: Search/filter bar, highlight best value pack

### Functionalities
- Add new packs to session state and persist to CSV
- Calculate and display cost per minute on add
- Sort and filter the price history table
- Remove individual entries and clear all with confirmation
- Export full pack price history CSV

### Test Scenarios
- Add valid packs → appear with correct calculations
- Add invalid data → validation error, no addition
- Sorting by cost/min and other columns works
- Remove pack entries with confirm/cancel flow
- Clear all packs with confirmation clears storage and UI
- Packs persist across app reloads
- Export CSV matches current price history
- UI handles empty state and resets inputs after add
- Responsive layout on desktop and mobile


## Parking Lot — Minor Improvements (Future Integration)

- Fix font sizes in the app UI that are currently too small; ensure readability and accessibility  
- Review and standardize spacing and padding for UI elements  
- Optimize button sizes and clickable areas for better user experience  
- Refine color contrast to meet accessibility guidelines  
- Improve loading indicators and feedback messages  
- Add consistent tooltip descriptions for all inputs and buttons  
- Review and update any outdated or inconsistent text labels  