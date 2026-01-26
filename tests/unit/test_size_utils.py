"""Tests for size utility functions."""

from __future__ import annotations

import pytest

from pynetappfoundry.utils.size import (
    approximate_size,
    approximate_size_specific,
    convert_size,
)


class TestApproximateSize:
    """Tests for approximate_size function."""

    def test_kilobytes_binary(self) -> None:
        """Test conversion to binary kilobytes."""
        result = approximate_size(1024 * 1024)
        assert result == "1.00 MiB"

    def test_kilobytes_decimal(self) -> None:
        """Test conversion to decimal kilobytes."""
        result = approximate_size(1000 * 1000, a_kilobyte_is_1024_bytes=False)
        assert result == "1.00 MB"

    def test_gigabytes(self) -> None:
        """Test conversion to gigabytes."""
        result = approximate_size(1024**3)
        assert result == "1.00 GiB"

    def test_terabytes(self) -> None:
        """Test conversion to terabytes."""
        result = approximate_size(1024**4)
        assert result == "1.00 TiB"

    def test_negative_raises(self) -> None:
        """Test that negative values raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            approximate_size(-1)

    def test_without_suffix(self) -> None:
        """Test getting numeric value without suffix."""
        result = approximate_size(1024 * 1024, withsuffix=False)
        assert isinstance(result, float)
        assert abs(result - 1.0) < 0.01


class TestApproximateSizeSpecific:
    """Tests for approximate_size_specific function."""

    def test_to_gb(self) -> None:
        """Test conversion to specific GB suffix."""
        result = approximate_size_specific(1000**3, "GB")
        assert result == "1.00 GB"

    def test_to_tib(self) -> None:
        """Test conversion to specific TiB suffix."""
        result = approximate_size_specific(1024**4, "TiB")
        assert result == "1.00 TiB"

    def test_invalid_suffix(self) -> None:
        """Test with invalid suffix returns -1."""
        result = approximate_size_specific(1000, "INVALID")
        assert result == -1


class TestConvertSize:
    """Tests for convert_size function."""

    def test_tb_to_gb(self) -> None:
        """Test conversion from TB to GB."""
        result = convert_size("1 TB", "GB")
        assert "1000.00 GB" in str(result)

    def test_gib_to_mib(self) -> None:
        """Test conversion from GiB to MiB."""
        result = convert_size("1 GiB", "MiB")
        assert "1024.00 MiB" in str(result)
