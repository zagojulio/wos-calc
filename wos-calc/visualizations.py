"""
Visualization module for Whiteout Survival calculator.
Contains functions for creating interactive charts and graphs.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Tuple

def create_efficiency_chart(
    scenarios: List[Dict[str, float]],
    metric: str = "points_per_minute"
) -> go.Figure:
    """
    Create a bar chart comparing efficiency metrics across different scenarios.
    
    Args:
        scenarios (List[Dict[str, float]]): List of scenario results
        metric (str): Metric to plot (default: points_per_minute)
    
    Returns:
        go.Figure: Plotly figure object
    """
    df = pd.DataFrame(scenarios)
    
    fig = px.bar(
        df,
        x="scenario_name",
        y=metric,
        title=f"Efficiency Comparison - {metric.replace('_', ' ').title()}",
        labels={
            "scenario_name": "Scenario",
            metric: metric.replace("_", " ").title()
        }
    )
    
    fig.update_layout(
        template="plotly_dark",
        showlegend=False,
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_speedup_utilization_chart(
    speedup_minutes: float,
    effective_training_time: float,
    num_batches: int
) -> go.Figure:
    """
    Create a pie chart showing speed-up utilization.
    
    Args:
        speedup_minutes (float): Total speed-up minutes available
        effective_training_time (float): Training time per batch
        num_batches (int): Number of batches that can be trained
    
    Returns:
        go.Figure: Plotly figure object
    """
    used_minutes = num_batches * effective_training_time
    remaining_minutes = speedup_minutes - used_minutes
    
    fig = go.Figure(data=[go.Pie(
        labels=["Used Speed-ups", "Remaining Speed-ups"],
        values=[used_minutes, remaining_minutes],
        hole=.3
    )])
    
    fig.update_layout(
        title="Speed-up Utilization",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig

def create_points_progression_chart(
    batches: List[int],
    points_per_batch: float
) -> go.Figure:
    """
    Create a line chart showing points progression over batches.
    
    Args:
        batches (List[int]): List of batch numbers
        points_per_batch (float): Points earned per batch
    
    Returns:
        go.Figure: Plotly figure object
    """
    points = [batch * points_per_batch for batch in batches]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=batches,
        y=points,
        mode='lines+markers',
        name='Points Progression'
    ))
    
    fig.update_layout(
        title="Points Progression Over Batches",
        xaxis_title="Number of Batches",
        yaxis_title="Total Points",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    
    return fig 