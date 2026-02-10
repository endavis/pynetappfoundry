"""Dimension and unit definitions for ONTAP field measurements.

Provides enums and frozen dataclasses for type-safe unit metadata.

Example:
    >>> from pynetappfoundry.units.dimensions import Dimension, BYTES, GIB
    >>> BYTES.dimension
    <Dimension.STORAGE: 'storage'>
    >>> GIB.factor
    1073741824.0
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from enum import Enum


class Dimension(Enum):
    """Measurement dimension grouping compatible units.

    Units within the same dimension can be converted to each other.
    """

    STORAGE = "storage"
    PERCENTAGE = "percentage"
    DURATION = "duration"
    RATE = "rate"


@dataclass(frozen=True)
class Unit:
    """A unit of measurement within a dimension.

    Attributes:
        name: Machine-readable identifier (e.g., ``"bytes"``, ``"gib"``).
        symbol: Human-readable suffix for display (e.g., ``"B"``, ``"GiB"``, ``"%"``).
        dimension: The dimension this unit belongs to.
        factor: Multiplication factor relative to the base unit of the dimension.
            For storage, base is bytes, so GiB has factor ``1073741824.0``
            (``1024**3``).  To convert a value in this unit to the base unit:
            ``value * factor``.  To convert from base to this unit:
            ``value / factor``.
    """

    name: str
    symbol: str
    dimension: Dimension
    factor: float


# --- Storage units (base: bytes) ---
BYTES = Unit(name="bytes", symbol="B", dimension=Dimension.STORAGE, factor=1.0)

# Binary prefixes (powers of 1024)
KIB = Unit(name="kib", symbol="KiB", dimension=Dimension.STORAGE, factor=1024.0)
MIB = Unit(name="mib", symbol="MiB", dimension=Dimension.STORAGE, factor=1024.0**2)
GIB = Unit(name="gib", symbol="GiB", dimension=Dimension.STORAGE, factor=1024.0**3)
TIB = Unit(name="tib", symbol="TiB", dimension=Dimension.STORAGE, factor=1024.0**4)
PIB = Unit(name="pib", symbol="PiB", dimension=Dimension.STORAGE, factor=1024.0**5)

# Decimal prefixes (powers of 1000)
KB = Unit(name="kb", symbol="KB", dimension=Dimension.STORAGE, factor=1000.0)
MB = Unit(name="mb", symbol="MB", dimension=Dimension.STORAGE, factor=1000.0**2)
GB = Unit(name="gb", symbol="GB", dimension=Dimension.STORAGE, factor=1000.0**3)
TB = Unit(name="tb", symbol="TB", dimension=Dimension.STORAGE, factor=1000.0**4)
PB = Unit(name="pb", symbol="PB", dimension=Dimension.STORAGE, factor=1000.0**5)

# --- Percentage units (base: percent, 0-100 scale) ---
PERCENT = Unit(name="percent", symbol="%", dimension=Dimension.PERCENTAGE, factor=1.0)

# --- Duration units (base: seconds) ---
SECONDS = Unit(name="seconds", symbol="s", dimension=Dimension.DURATION, factor=1.0)
MINUTES = Unit(name="minutes", symbol="min", dimension=Dimension.DURATION, factor=60.0)
HOURS = Unit(name="hours", symbol="h", dimension=Dimension.DURATION, factor=3600.0)
DAYS = Unit(name="days", symbol="d", dimension=Dimension.DURATION, factor=86400.0)

# --- Rate units (base: bytes_per_second) ---
BYTES_PER_SEC = Unit(name="bytes_per_sec", symbol="B/s", dimension=Dimension.RATE, factor=1.0)
KB_PER_SEC = Unit(name="kb_per_sec", symbol="KB/s", dimension=Dimension.RATE, factor=1000.0)
MB_PER_SEC = Unit(name="mb_per_sec", symbol="MB/s", dimension=Dimension.RATE, factor=1000.0**2)

# Lookup table: name -> Unit (populated at module level for fast access)
ALL_UNITS: dict[str, Unit] = {}


def _register_module_units() -> None:
    """Populate ALL_UNITS from module-level Unit constants."""
    module = sys.modules[__name__]
    for attr_name in dir(module):
        obj = getattr(module, attr_name)
        if isinstance(obj, Unit):
            ALL_UNITS[obj.name] = obj


_register_module_units()


def get_unit(name: str) -> Unit:
    """Look up a Unit by its name.

    Args:
        name: The unit name (e.g., ``"bytes"``, ``"gib"``, ``"percent"``).

    Returns:
        The matching Unit instance.

    Raises:
        KeyError: If no unit with the given name exists.
    """
    try:
        return ALL_UNITS[name]
    except KeyError:
        raise KeyError(f"Unknown unit '{name}'. Available: {sorted(ALL_UNITS.keys())}") from None
