"""Tests for CLI utility functions."""

from __future__ import annotations

import pytest

from pynetappfoundry.cli.utils import format_value_markup


class TestFormatValueMarkup:
    """Tests for format_value_markup shared formatter."""

    def test_none_value(self) -> None:
        """Test None formats as yellow null."""
        assert format_value_markup(None) == "[yellow]null[/yellow]"

    def test_bool_true(self) -> None:
        """Test True formats as yellow true."""
        assert format_value_markup(True) == "[yellow]true[/yellow]"

    def test_bool_false(self) -> None:
        """Test False formats as yellow false."""
        assert format_value_markup(False) == "[yellow]false[/yellow]"

    def test_integer(self) -> None:
        """Test integer formats as magenta."""
        assert format_value_markup(42) == "[magenta]42[/magenta]"

    def test_float(self) -> None:
        """Test float formats as magenta."""
        assert format_value_markup(3.14) == "[magenta]3.14[/magenta]"

    def test_string(self) -> None:
        """Test non-empty string formats as green."""
        assert format_value_markup("hello") == "[green]hello[/green]"

    def test_empty_string(self) -> None:
        """Test empty string formats as dim (empty)."""
        assert format_value_markup("") == "[dim](empty)[/dim]"

    def test_list_returns_none(self) -> None:
        """Test list returns None for caller-specific handling."""
        assert format_value_markup([1, 2, 3]) is None

    def test_dict_returns_none(self) -> None:
        """Test dict returns None for caller-specific handling."""
        assert format_value_markup({"key": "value"}) is None

    @pytest.mark.parametrize(
        "value",
        [set(), frozenset(), (1, 2), object()],
    )
    def test_other_types_return_none(self, value: object) -> None:
        """Test unsupported types return None."""
        assert format_value_markup(value) is None

    def test_bool_before_int(self) -> None:
        """Test that bool is checked before int (bool is subclass of int)."""
        # This ensures True doesn't get formatted as magenta 1
        result = format_value_markup(True)
        assert "yellow" in result  # type: ignore[operator]
        assert "magenta" not in result  # type: ignore[operator]
