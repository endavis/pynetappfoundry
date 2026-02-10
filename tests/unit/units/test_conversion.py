"""Tests for unit conversion utilities."""

from __future__ import annotations

import pytest

from pynetappfoundry.units.conversion import (
    IncompatibleUnitsError,
    convert,
    format_value,
)
from pynetappfoundry.units.dimensions import (
    BYTES,
    BYTES_PER_SEC,
    DAYS,
    GB,
    GIB,
    HOURS,
    KB_PER_SEC,
    MB,
    MB_PER_SEC,
    MIB,
    PERCENT,
    SECONDS,
    TIB,
)


class TestConvert:
    """Tests for the convert function."""

    def test_same_unit_identity(self) -> None:
        assert convert(100, BYTES, BYTES) == 100.0

    def test_bytes_to_gib(self) -> None:
        assert convert(1024**3, BYTES, GIB) == 1.0

    def test_gib_to_bytes(self) -> None:
        assert convert(1, GIB, BYTES) == 1073741824.0

    def test_gib_to_mib(self) -> None:
        assert convert(1, GIB, MIB) == 1024.0

    def test_mib_to_gib(self) -> None:
        assert convert(1024, MIB, GIB) == 1.0

    def test_tib_to_gib(self) -> None:
        assert convert(1, TIB, GIB) == 1024.0

    def test_decimal_gb_to_mb(self) -> None:
        assert convert(1, GB, MB) == 1000.0

    def test_cross_binary_decimal_gib_to_gb(self) -> None:
        result = convert(1, GIB, GB)
        assert result == pytest.approx(1.073741824)

    def test_percent_identity(self) -> None:
        assert convert(90, PERCENT, PERCENT) == 90.0

    def test_days_to_hours(self) -> None:
        assert convert(2, DAYS, HOURS) == 48.0

    def test_hours_to_seconds(self) -> None:
        assert convert(1, HOURS, SECONDS) == 3600.0

    def test_kb_per_sec_to_mb_per_sec(self) -> None:
        assert convert(1000, KB_PER_SEC, MB_PER_SEC) == 1.0

    def test_bytes_per_sec_to_kb_per_sec(self) -> None:
        assert convert(1000, BYTES_PER_SEC, KB_PER_SEC) == 1.0

    def test_integer_input_returns_float(self) -> None:
        result = convert(100, BYTES, BYTES)
        assert isinstance(result, float)

    def test_zero_value(self) -> None:
        assert convert(0, GIB, BYTES) == 0.0


class TestIncompatibleUnits:
    """Tests for IncompatibleUnitsError."""

    def test_bytes_to_percent_raises(self) -> None:
        with pytest.raises(IncompatibleUnitsError):
            convert(100, BYTES, PERCENT)

    def test_percent_to_days_raises(self) -> None:
        with pytest.raises(IncompatibleUnitsError):
            convert(100, PERCENT, DAYS)

    def test_storage_to_rate_raises(self) -> None:
        with pytest.raises(IncompatibleUnitsError):
            convert(100, BYTES, BYTES_PER_SEC)

    def test_error_message_includes_unit_names(self) -> None:
        with pytest.raises(
            IncompatibleUnitsError,
            match=r"Cannot convert from bytes.*to percent.*different dimensions",
        ):
            convert(100, BYTES, PERCENT)

    def test_error_attributes(self) -> None:
        try:
            convert(100, BYTES, PERCENT)
        except IncompatibleUnitsError as exc:
            assert exc.from_unit is BYTES
            assert exc.to_unit is PERCENT


class TestFormatValue:
    """Tests for the format_value function."""

    def test_storage_with_space(self) -> None:
        assert format_value(1.5, GIB) == "1.50 GiB"

    def test_bytes_large_value(self) -> None:
        assert format_value(1073741824, BYTES) == "1073741824.00 B"

    def test_percent_no_space(self) -> None:
        assert format_value(90, PERCENT) == "90.00%"

    def test_custom_precision_zero(self) -> None:
        assert format_value(2, GIB, precision=0) == "2 GiB"

    def test_custom_precision_four(self) -> None:
        assert format_value(1.23456, GIB, precision=4) == "1.2346 GiB"

    def test_duration_with_space(self) -> None:
        assert format_value(48, HOURS) == "48.00 h"

    def test_rate_with_space(self) -> None:
        assert format_value(100, KB_PER_SEC) == "100.00 KB/s"
