"""Time-related utility functions."""

from __future__ import annotations

from datetime import datetime


def to_epoch_ms(dt: datetime) -> int:
    """Convert a datetime to epoch milliseconds.

    Args:
        dt: The datetime to convert.

    Returns:
        Epoch time in milliseconds.
    """
    return int(dt.timestamp() * 1000)
