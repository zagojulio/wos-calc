"""
Utility functions for formatting display values.
"""

def format_currency(amount: float) -> str:
    """
    Format a number as currency.
    
    Args:
        amount (float): Amount to format
    
    Returns:
        str: Formatted currency string
    """
    return f"${amount:,.2f}"

def format_duration(minutes: float) -> str:
    """
    Format minutes into a human-readable duration.
    
    Args:
        minutes (float): Duration in minutes
    
    Returns:
        str: Formatted duration string
    """
    if minutes < 0:
        return f"{int(minutes)}m"
    days = int(minutes // (24 * 60))
    hours = int((minutes % (24 * 60)) // 60)
    mins = int(minutes % 60)
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if mins > 0 or not parts:
        parts.append(f"{mins}m")
    
    return " ".join(parts)

def format_number(number: float) -> str:
    """
    Format a number with commas for thousands.
    
    Args:
        number (float): Number to format
    
    Returns:
        str: Formatted number string
    """
    return f"{number:,.0f}" 