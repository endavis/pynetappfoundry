"""Convert values between compatible units within the same dimension.

Example:
    >>> from pynetappfoundry.units.dimensions import BYTES, GIB
    >>> from pynetappfoundry.units.conversion import convert
    >>> convert(1073741824, BYTES, GIB)
    1.0
    >>> convert(2, GIB, MIB)
    2048.0
"""

from __future__ import annotations

from pynetappfoundry.units.dimensions import Unit


class IncompatibleUnitsError(ValueError):
    """Raised when attempting to convert between units of different dimensions."""

    def __init__(self, from_unit: Unit, to_unit: Unit) -> None:
        self.from_unit = from_unit
        self.to_unit = to_unit
        super().__init__(
            f"Cannot convert from {from_unit.name} ({from_unit.dimension.value}) "
            f"to {to_unit.name} ({to_unit.dimension.value}): different dimensions"
        )


def convert(value: int | float, from_unit: Unit, to_unit: Unit) -> float:
    """Convert a numeric value from one unit to another.

    Both units must belong to the same dimension.

    Args:
        value: The numeric value to convert.
        from_unit: The unit the value is currently in.
        to_unit: The unit to convert to.

    Returns:
        The converted value as a float.

    Raises:
        IncompatibleUnitsError: If the units belong to different dimensions.

    Examples:
        >>> convert(1073741824, BYTES, GIB)
        1.0
        >>> convert(90, PERCENT, PERCENT)
        90.0
        >>> convert(2, DAYS, HOURS)
        48.0
    """
    if from_unit.dimension != to_unit.dimension:
        raise IncompatibleUnitsError(from_unit, to_unit)

    if from_unit is to_unit:
        return float(value)

    return float(value) * from_unit.factor / to_unit.factor


def format_value(
    value: int | float,
    unit: Unit,
    precision: int = 2,
) -> str:
    """Format a value with its unit symbol for display.

    Args:
        value: The numeric value.
        unit: The unit for the suffix.
        precision: Decimal places (default 2).

    Returns:
        Formatted string like ``"1.00 GiB"`` or ``"90.00%"``.

    Examples:
        >>> format_value(1.5, GIB)
        '1.50 GiB'
        >>> format_value(90, PERCENT)
        '90.00%'
    """
    formatted = f"{value:.{precision}f}"
    if unit.dimension.value == "percentage":
        return f"{formatted}{unit.symbol}"
    return f"{formatted} {unit.symbol}"
