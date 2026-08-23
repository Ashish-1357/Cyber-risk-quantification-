"""Utility formatters for the platform"""


def format_currency(value: float) -> str:
    """Format a number as currency with appropriate suffix"""
    if value >= 1e9:
        return f"${value / 1e9:.1f}B"
    if value >= 1e6:
        return f"${value / 1e6:.1f}M"
    if value >= 1e3:
        return f"${value / 1e3:.1f}K"
    return f"${value:.0f}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format a decimal as percentage"""
    return f"{value * 100:.{decimals}f}%"


def risk_score_color(score: float) -> str:
    """Get color for risk score"""
    if score < 25:
        return "#10b981"  # Green
    elif score < 50:
        return "#f59e0b"  # Yellow
    elif score < 75:
        return "#ef4444"  # Red
    else:
        return "#7f1d1d"  # Dark Red
