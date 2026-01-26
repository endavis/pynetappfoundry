"""Base database utilities."""

from __future__ import annotations

import sqlite3
from datetime import datetime


def adapt_datetime(dt: datetime) -> str:
    """Adapter to convert datetime to ISO format string.

    Args:
        dt: Datetime object to convert.

    Returns:
        ISO format string.
    """
    return dt.isoformat()


def convert_datetime(s: bytes) -> datetime:
    """Converter to convert ISO format string to datetime.

    Args:
        s: Bytes containing ISO format date string.

    Returns:
        Datetime object.
    """
    return datetime.fromisoformat(s.decode())


# Register the default adapter and converter
sqlite3.register_adapter(datetime, adapt_datetime)
