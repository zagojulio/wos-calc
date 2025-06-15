## Bug #1 - TypeError: Cannot compare Timestamp with datetime.date in purchase statistics calculation

- **Date:** 2025-06-15
- **Status:** Open
- **Reported by:** User
- **Description:**  
  When calculating purchase statistics in `purchase_manager.py`, a TypeError occurs due to a comparison between pandas Timestamp and python datetime.date objects. The error suggests using `ts == pd.Timestamp(date)` or `ts.date() == date` instead.

- **Traceback:**  
  ```
  File "/Users/jaz/opt/anaconda3/lib/python3.8/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 542, in _run_script
      exec(code, module.__dict__)
  File "/Users/jaz/Library/Mobile Documents/com~apple~CloudDocs/Estudos/05. Projects/02. Whiteout Survival/app.py", line 333, in <module>
      stats = calculate_purchase_stats(
  File "/Users/jaz/Library/Mobile Documents/com~apple~CloudDocs/Estudos/05. Projects/02. Whiteout Survival/features/purchase_manager.py", line 95, in calculate_purchase_stats
      manual_daily = manual_purchases.groupby('Date')["Spending ($)"].sum().reset_index()
  ...
  TypeError: Cannot compare Timestamp with datetime.date. Use ts == pd.Timestamp(date) or ts.date() == date instead.
  ```

- **Environment:**  
  Python 3.8, Pandas, Streamlit

- **Steps to Reproduce:**  
  1. Load purchase data with mixed date types in the 'Date' column.  
  2. Run purchase statistics calculation that groups by date.  
  3. Observe the TypeError.

- **Expected Behavior:**  
  Grouping by dates should work without type comparison errors.

- **Actual Behavior:**  
  TypeError raised during groupby aggregation due to timestamp/date comparison incompatibility.

- **Workaround:**  
  None known yet.

- **Fix:**  
  Pending — update date comparison in purchase statistics calculation to ensure consistent datetime types.

## Bug #2 - KeyError: "['Pack Name'] not in index" when appending purchase DataFrames

- **Date:** 2025-06-15
- **Status:** Closed
- **Reported by:** User
- **Description:**  
  While appending DataFrames during purchase data processing, a KeyError is raised indicating the column 'Pack Name' is missing from one of the DataFrames.

- **Traceback:**  
  ```
  Traceback (most recent call last):
    File "/Users/jaz/opt/anaconda3/lib/python3.8/site-packages/streamlit/runtime/scriptrunner/script_runner.py", line 542, in _run_script
      exec(code, module.__dict__)
    File "/Users/jaz/Library/Mobile Documents/com~apple~CloudDocs/Estudos/05. Projects/02. Whiteout Survival/app.py", line 459, in <module>
      dfs.append(auto_df[['Date', 'Pack Name', 'Amount', 'Source']])
    File "/Users/jaz/opt/anaconda3/lib/python3.8/site-packages/pandas/core/frame.py", line 3767, in __getitem__
      indexer = self.columns._get_indexer_strict(key, "columns")[1]
    File "/Users/jaz/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexes/base.py", line 5877, in _get_indexer_strict
      self._raise_if_missing(keyarr, indexer, axis_name)
    File "/Users/jaz/opt/anaconda3/lib/python3.8/site-packages/pandas/core/indexes/base.py", line 5941, in _raise_if_missing
      raise KeyError(f"{not_found} not in index")
  KeyError: "['Pack Name'] not in index"
  ```

- **Environment:**  
  Python 3.8, Pandas, Streamlit

- **Steps to Reproduce:**  
  1. Load purchase data CSVs and attempt to combine them into a single DataFrame.  
  2. The code attempts to select columns ['Date', 'Pack Name', 'Amount', 'Source'] from the automatic purchase DataFrame.  
  3. KeyError occurs indicating 'Pack Name' is not found.

- **Expected Behavior:**  
  The column selection should succeed without error, assuming consistent column naming across DataFrames.

- **Actual Behavior:**  
  KeyError raised due to missing 'Pack Name' column in one of the DataFrames.

- **Workaround:**  
  None known yet.

- **Fix:**  
  Investigate column names in CSV files and ensure consistent naming conventions or add column renaming/mapping before combining DataFrames.


## Bug #3 - AttributeError: 'Series' object has no attribute 'strftime' in purchase deletion selectbox

- **Date:** 2025-06-15
- **Status:** Closed
- **Reported by:** User
- **Description:**  
  When rendering the selectbox for deleting purchases, the code attempts to call `.strftime('%Y-%m-%d')` on a pandas Series instead of a scalar datetime object. This causes an AttributeError.

- **Traceback:**  
  ```
  File "/Users/jaz/Library/Mobile Documents/com~apple~CloudDocs/Estudos/05. Projects/02. Whiteout Survival/app.py", line 497, in <lambda>
      format_func=lambda x: f"{combined_df.loc[x, 'Date'].strftime('%Y-%m-%d')} - {combined_df.loc[x, 'Pack Name']} - R${combined_df.loc[x, 'Amount']:,.2f}"
  AttributeError: 'Series' object has no attribute 'strftime'
  ```

- **Environment:**  
  Python 3.8, Pandas, Streamlit

- **Steps to Reproduce:**  
  1. Open the Pack Purchases tab.  
  2. Attempt to delete a purchase using the selectbox that lists purchases by formatted string.  
  3. Observe the AttributeError due to `.strftime()` called on a Series.

- **Expected Behavior:**  
  The selectbox should show a list of purchase strings formatted with date, pack name, and amount without errors.

- **Actual Behavior:**  
  The app raises an AttributeError because `.strftime()` is called on a Series.

- **Workaround:**  
  None known.

- **Fix Suggestion:**  
  Pre-format the display strings for the selectbox outside the widget call, ensuring `.strftime()` is called on scalar datetime objects. Map the selected option back to the DataFrame index for deletion.