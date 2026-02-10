"""Tests for dimension and unit definitions."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from pynetappfoundry.units.dimensions import (
    ALL_UNITS,
    BYTES,
    BYTES_PER_SEC,
    DAYS,
    GB,
    GIB,
    HOURS,
    KB,
    KB_PER_SEC,
    KIB,
    MB,
    MB_PER_SEC,
    MIB,
    MINUTES,
    PB,
    PERCENT,
    PIB,
    SECONDS,
    TB,
    TIB,
    Dimension,
    Unit,
    get_unit,
)


class TestDimension:
    """Tests for the Dimension enum."""

    def test_storage_value(self) -> None:
        assert Dimension.STORAGE.value == "storage"

    def test_percentage_value(self) -> None:
        assert Dimension.PERCENTAGE.value == "percentage"

    def test_duration_value(self) -> None:
        assert Dimension.DURATION.value == "duration"

    def test_rate_value(self) -> None:
        assert Dimension.RATE.value == "rate"

    def test_four_dimensions_exist(self) -> None:
        assert len(Dimension) == 4


class TestUnit:
    """Tests for the Unit frozen dataclass."""

    def test_unit_is_frozen(self) -> None:
        with pytest.raises(FrozenInstanceError):
            BYTES.name = "changed"  # type: ignore[misc]

    def test_unit_equality(self) -> None:
        same = Unit(name="bytes", symbol="B", dimension=Dimension.STORAGE, factor=1.0)
        assert same == BYTES

    def test_unit_hashing(self) -> None:
        same = Unit(name="bytes", symbol="B", dimension=Dimension.STORAGE, factor=1.0)
        assert hash(BYTES) == hash(same)
        assert len({BYTES, same}) == 1

    def test_unit_inequality(self) -> None:
        assert BYTES != GIB


class TestStorageUnits:
    """Tests for storage unit constants."""

    def test_bytes_is_base(self) -> None:
        assert BYTES.factor == 1.0
        assert BYTES.dimension == Dimension.STORAGE
        assert BYTES.symbol == "B"

    def test_binary_factors_are_powers_of_1024(self) -> None:
        assert KIB.factor == 1024.0
        assert MIB.factor == 1024.0**2
        assert GIB.factor == 1024.0**3
        assert TIB.factor == 1024.0**4
        assert PIB.factor == 1024.0**5

    def test_decimal_factors_are_powers_of_1000(self) -> None:
        assert KB.factor == 1000.0
        assert MB.factor == 1000.0**2
        assert GB.factor == 1000.0**3
        assert TB.factor == 1000.0**4
        assert PB.factor == 1000.0**5

    def test_all_storage_units_share_dimension(self) -> None:
        storage_units = [BYTES, KIB, MIB, GIB, TIB, PIB, KB, MB, GB, TB, PB]
        for unit in storage_units:
            assert unit.dimension == Dimension.STORAGE

    def test_binary_symbols(self) -> None:
        assert KIB.symbol == "KiB"
        assert MIB.symbol == "MiB"
        assert GIB.symbol == "GiB"
        assert TIB.symbol == "TiB"
        assert PIB.symbol == "PiB"

    def test_decimal_symbols(self) -> None:
        assert KB.symbol == "KB"
        assert MB.symbol == "MB"
        assert GB.symbol == "GB"
        assert TB.symbol == "TB"
        assert PB.symbol == "PB"


class TestPercentageUnits:
    """Tests for percentage unit constants."""

    def test_percent_is_base(self) -> None:
        assert PERCENT.factor == 1.0
        assert PERCENT.dimension == Dimension.PERCENTAGE
        assert PERCENT.symbol == "%"
        assert PERCENT.name == "percent"


class TestDurationUnits:
    """Tests for duration unit constants."""

    def test_seconds_is_base(self) -> None:
        assert SECONDS.factor == 1.0
        assert SECONDS.dimension == Dimension.DURATION

    def test_duration_factors(self) -> None:
        assert MINUTES.factor == 60.0
        assert HOURS.factor == 3600.0
        assert DAYS.factor == 86400.0

    def test_all_duration_units_share_dimension(self) -> None:
        for unit in [SECONDS, MINUTES, HOURS, DAYS]:
            assert unit.dimension == Dimension.DURATION


class TestRateUnits:
    """Tests for rate unit constants."""

    def test_bytes_per_sec_is_base(self) -> None:
        assert BYTES_PER_SEC.factor == 1.0
        assert BYTES_PER_SEC.dimension == Dimension.RATE

    def test_rate_factors(self) -> None:
        assert KB_PER_SEC.factor == 1000.0
        assert MB_PER_SEC.factor == 1000.0**2

    def test_all_rate_units_share_dimension(self) -> None:
        for unit in [BYTES_PER_SEC, KB_PER_SEC, MB_PER_SEC]:
            assert unit.dimension == Dimension.RATE


class TestAllUnits:
    """Tests for the ALL_UNITS lookup table."""

    def test_all_units_populated(self) -> None:
        assert len(ALL_UNITS) > 0

    def test_contains_all_module_constants(self) -> None:
        expected_names = {
            "bytes",
            "kib",
            "mib",
            "gib",
            "tib",
            "pib",
            "kb",
            "mb",
            "gb",
            "tb",
            "pb",
            "percent",
            "seconds",
            "minutes",
            "hours",
            "days",
            "bytes_per_sec",
            "kb_per_sec",
            "mb_per_sec",
        }
        assert set(ALL_UNITS.keys()) == expected_names

    def test_values_are_unit_instances(self) -> None:
        for unit in ALL_UNITS.values():
            assert isinstance(unit, Unit)


class TestGetUnit:
    """Tests for the get_unit lookup function."""

    def test_lookup_known_unit(self) -> None:
        assert get_unit("bytes") is BYTES
        assert get_unit("gib") is GIB
        assert get_unit("percent") is PERCENT

    def test_lookup_unknown_raises_key_error(self) -> None:
        with pytest.raises(KeyError, match="Unknown unit 'nonexistent'"):
            get_unit("nonexistent")
