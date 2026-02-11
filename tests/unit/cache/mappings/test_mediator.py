"""Tests for the mediator type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.cluster.mediators.mapping import MEDIATOR_MAPPING
from pynetappfoundry.cache.cluster.mediators.model import MediatorInfo
from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API mediator record with all fields."""
    return {
        "uuid": "med-uuid-1234-5678-abcd",
        "ip_address": "10.0.0.100",
        "port": 31784,
        "reachable": True,
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestMediatorMappingDefinition:
    """Tests for MEDIATOR_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid MediatorInfo field."""
        model_fields = set(MediatorInfo.model_fields.keys())
        for field in MEDIATOR_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on MediatorInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in MEDIATOR_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (3)."""
        assert len(MEDIATOR_MAPPING.fields) == 3

    def test_model_class(self) -> None:
        """Model class is MediatorInfo."""
        assert MEDIATOR_MAPPING.model_class is MediatorInfo

    def test_endpoint(self) -> None:
        """API endpoint is /cluster/mediators?fields=*."""
        assert MEDIATOR_MAPPING.api_endpoint == "/cluster/mediators?fields=*"

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only)."""
        assert MEDIATOR_MAPPING.cli_command == ""

    def test_id_field(self) -> None:
        """ID field is uuid."""
        assert MEDIATOR_MAPPING.id_field == "uuid"

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = MEDIATOR_MAPPING.api_expected_fields()
        assert expected == ["ip_address", "port", "uuid"]


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestMediatorApiParsing:
    """Tests for parsing API mediator records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete MediatorInfo."""
        result = parse_api_record(MEDIATOR_MAPPING, full_api_record, "[test]")
        assert isinstance(result, MediatorInfo)
        assert result.mediator_address == "10.0.0.100"
        assert result.mediator_uuid == "med-uuid-1234-5678-abcd"
        assert result.mediator_port == 31784

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "abc"}
        result = parse_api_record(MEDIATOR_MAPPING, record, "[test]")
        assert isinstance(result, MediatorInfo)
        assert result.mediator_uuid == "abc"
        assert result.mediator_address == ""
        assert result.mediator_port == 0

    def test_empty_record(self) -> None:
        """Empty record uses all defaults."""
        record: dict[str, Any] = {}
        result = parse_api_record(MEDIATOR_MAPPING, record, "[test]")
        assert isinstance(result, MediatorInfo)
        assert result.mediator_address == ""
        assert result.mediator_uuid == ""
        assert result.mediator_port == 0

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {"uuid": "med1", "ip_address": "10.0.0.1", "port": 31784},
                {"uuid": "med2", "ip_address": "10.0.0.2", "port": 31785},
            ],
        }
        results = parse_api_response(MEDIATOR_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].mediator_uuid == "med1"  # type: ignore[union-attr]
        assert results[1].mediator_uuid == "med2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty records list."""
        response: dict[str, Any] = {"records": []}
        results = parse_api_response(MEDIATOR_MAPPING, response, "[test]", MagicMock())
        assert results == []

    def test_parse_api_response_no_records(self) -> None:
        """parse_api_response handles None response."""
        results = parse_api_response(MEDIATOR_MAPPING, None, "[test]", MagicMock())
        assert results == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser.

    Reproduces the manual .get() logic from the collector to confirm the
    declarative mapping produces identical results.
    """

    @staticmethod
    def _old_parse_mediator(record: dict[str, Any]) -> MediatorInfo:
        """Reproduce old inline mediator parsing logic."""
        return MediatorInfo(
            mediator_address=record.get("ip_address", ""),
            mediator_uuid=record.get("uuid", ""),
            mediator_port=record.get("port", 0),
        )

    _MEDIATOR_FIELDS = (
        "mediator_address",
        "mediator_uuid",
        "mediator_port",
    )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical MediatorInfo for full record."""
        old = self._old_parse_mediator(full_api_record)
        new = parse_api_record(MEDIATOR_MAPPING, full_api_record, "[test]")
        assert isinstance(new, MediatorInfo)
        for field_name in self._MEDIATOR_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "xyz"}
        old = self._old_parse_mediator(record)
        new = parse_api_record(MEDIATOR_MAPPING, record, "[test]")
        assert isinstance(new, MediatorInfo)
        for field_name in self._MEDIATOR_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_empty_record(self) -> None:
        """Framework and old parser match on empty record."""
        record: dict[str, Any] = {}
        old = self._old_parse_mediator(record)
        new = parse_api_record(MEDIATOR_MAPPING, record, "[test]")
        assert isinstance(new, MediatorInfo)
        for field_name in self._MEDIATOR_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
