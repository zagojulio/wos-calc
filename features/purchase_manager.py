"""
Module for managing purchase data persistence and calculations.
"""

import pandas as pd
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple

def load_purchases(csv_path: str) -> Optional[pd.DataFrame]:
    """
    Load purchases from CSV file.
    Raises an exception if the file does not exist.
    
    Args:
        csv_path (str): Path to CSV file
    
    Returns:
        Optional[pd.DataFrame]: Loaded data or None if error
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file {csv_path} does not exist.")
    try:
        df = pd.read_csv(csv_path, parse_dates=['Date'])
        return df
    except Exception as e:
        raise Exception(f"Error loading CSV file {csv_path}: {str(e)}")

def save_purchase(csv_path: str, purchase: Dict) -> bool:
    """
    Append a new purchase to CSV file.
    
    Args:
        csv_path (str): Path to CSV file
        purchase (Dict): Purchase data to save
    
    Returns:
        bool: Success status
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Convert purchase to DataFrame
        df_new = pd.DataFrame([purchase])
        
        # Append to existing file or create new
        if os.path.exists(csv_path):
            df_new.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            df_new.to_csv(csv_path, index=False)
        
        return True
    except Exception as e:
        raise Exception(f"Error saving purchase to {csv_path}: {str(e)}")

def calculate_purchase_stats(
    auto_purchases: Optional[pd.DataFrame],
    manual_purchases: Optional[pd.DataFrame]
) -> Dict:
    """
    Calculate combined purchase statistics.
    
    Args:
        auto_purchases (Optional[pd.DataFrame]): Automatic purchases
        manual_purchases (Optional[pd.DataFrame]): Manual purchases
    
    Returns:
        Dict: Statistics including totals and averages
    """
    stats = {
        "total_spent_auto": 0.0,
        "total_spent_manual": 0.0,
        "total_speedups": 0,
        "avg_spending_per_day": 0.0,
        "spending_by_day": pd.DataFrame()
    }
    
    # Process automatic purchases
    if auto_purchases is not None and not auto_purchases.empty:
        stats["total_spent_auto"] = auto_purchases["Value (R$)"].sum()
    
    # Process manual purchases
    if manual_purchases is not None and not manual_purchases.empty:
        stats["total_spent_manual"] = manual_purchases["Spending ($)"].sum()
        stats["total_speedups"] = manual_purchases["Speed-ups (min)"].sum()
    
    # Combine purchases for daily stats
    dfs = []
    if auto_purchases is not None and not auto_purchases.empty:
        auto_daily = auto_purchases.groupby('Date')["Value (R$)"].sum().reset_index()
        auto_daily.columns = ['Date', 'Amount']
        dfs.append(auto_daily)
    
    if manual_purchases is not None and not manual_purchases.empty:
        manual_daily = manual_purchases.groupby('Date')["Spending ($)"].sum().reset_index()
        manual_daily.columns = ['Date', 'Amount']
        dfs.append(manual_daily)
    
    if dfs:
        combined_daily = pd.concat(dfs).groupby('Date')['Amount'].sum().reset_index()
        stats["spending_by_day"] = combined_daily
        stats["avg_spending_per_day"] = combined_daily['Amount'].mean()
    
    return stats

def export_combined_purchases(
    auto_purchases: Optional[pd.DataFrame],
    manual_purchases: Optional[pd.DataFrame],
    output_path: str
) -> bool:
    """
    Export combined purchase history to CSV, handling missing columns gracefully.
    
    Args:
        auto_purchases (Optional[pd.DataFrame]): Automatic purchases
        manual_purchases (Optional[pd.DataFrame]): Manual purchases
        output_path (str): Path to save combined CSV
    
    Returns:
        bool: Success status
    """
    try:
        dfs = []
        
        if auto_purchases is not None and not auto_purchases.empty:
            auto_df = auto_purchases.copy()
            # Standardize columns
            if 'Pack Name' not in auto_df.columns:
                if 'Purchase Name' in auto_df.columns:
                    auto_df['Pack Name'] = auto_df['Purchase Name']
                else:
                    auto_df['Pack Name'] = ''
            if 'Value (R$)' in auto_df.columns:
                auto_df['Amount'] = auto_df['Value (R$)']
            elif 'Spending ($)' in auto_df.columns:
                auto_df['Amount'] = auto_df['Spending ($)']
            else:
                auto_df['Amount'] = 0.0
            if 'Speed-ups (min)' not in auto_df.columns:
                auto_df['Speed-ups (min)'] = 0
            auto_df['Source'] = 'Automatic'
            dfs.append(auto_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])
        
        if manual_purchases is not None and not manual_purchases.empty:
            manual_df = manual_purchases.copy()
            if 'Amount' not in manual_df.columns:
                if 'Spending ($)' in manual_df.columns:
                    manual_df['Amount'] = manual_df['Spending ($)']
                else:
                    manual_df['Amount'] = 0.0
            if 'Speed-ups (min)' not in manual_df.columns:
                manual_df['Speed-ups (min)'] = 0
            manual_df['Source'] = 'Manual'
            if 'Pack Name' not in manual_df.columns:
                manual_df['Pack Name'] = ''
            dfs.append(manual_df[['Date', 'Pack Name', 'Amount', 'Speed-ups (min)', 'Source']])
        
        if dfs:
            combined_df = pd.concat(dfs).sort_values('Date')
            combined_df.to_csv(output_path, index=False)
            return True
        
        return False
    except Exception as e:
        raise Exception(f"Error exporting combined purchases: {str(e)}") 