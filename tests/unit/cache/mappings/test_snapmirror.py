"""Tests for the SnapMirror type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)
from pynetappfoundry.cache.mappings.snapmirror import SNAPMIRROR_MAPPING
from pynetappfoundry.cache.models import SnapMirrorRelationship

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API SnapMirror relationship record with all fields."""
    return {
        "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "source": {"path": "svm1:vol_src"},
        "destination": {"path": "svm2:vol_dst"},
        "policy": {"type": "async", "uuid": "pol-uuid-1"},
        "throttle": 1024,
        "group_type": "none",
        "transfer_schedule": {"uuid": "sched-uuid-1"},
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestSnapMirrorMappingDefinition:
    """Tests for SNAPMIRROR_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid SnapMirrorRelationship field."""
        model_fields = set(SnapMirrorRelationship.model_fields.keys())
        for field in SNAPMIRROR_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on SnapMirrorRelationship"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in SNAPMIRROR_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (8)."""
        assert len(SNAPMIRROR_MAPPING.fields) == 8

    def test_model_class(self) -> None:
        """Model class is SnapMirrorRelationship."""
        assert SNAPMIRROR_MAPPING.model_class is SnapMirrorRelationship

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert "/snapmirror/relationships" in SNAPMIRROR_MAPPING.api_endpoint
        assert "fields=" in SNAPMIRROR_MAPPING.api_endpoint

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert SNAPMIRROR_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = SNAPMIRROR_MAPPING.api_expected_fields()
        assert expected == [
            "destination",
            "group_type",
            "policy",
            "source",
            "throttle",
            "transfer_schedule",
            "uuid",
        ]

    def test_id_field(self) -> None:
        """id_field is uuid."""
        assert SNAPMIRROR_MAPPING.id_field == "uuid"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestSnapMirrorApiParsing:
    """Tests for parsing API SnapMirror records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses correctly."""
        result = parse_api_record(SNAPMIRROR_MAPPING, full_api_record, "[test]")
        assert isinstance(result, SnapMirrorRelationship)
        assert result.uuid == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        assert result.source_path == "svm1:vol_src"
        assert result.destination_path == "svm2:vol_dst"
        assert result.relationship_type == "async"
        assert result.policy_uuid == "pol-uuid-1"
        assert result.throttle == 1024
        assert result.group_type == "none"
        assert result.transfer_schedule_uuid == "sched-uuid-1"

    def test_minimal_record(self) -> None:
        """Minimal record (only uuid) uses defaults for missing fields."""
        record: dict[str, Any] = {"uuid": "abc-123"}
        result = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(result, SnapMirrorRelationship)
        assert result.uuid == "abc-123"
        assert result.source_path == ""
        assert result.destination_path == ""
        assert result.relationship_type == ""
        assert result.policy_uuid == ""
        assert result.throttle == 0
        assert result.group_type == ""
        assert result.transfer_schedule_uuid == ""

    def test_missing_policy(self) -> None:
        """Missing policy defaults relationship_type and policy_uuid to empty."""
        record: dict[str, Any] = {
            "uuid": "abc-123",
            "source": {"path": "svm1:vol1"},
            "destination": {"path": "svm2:vol1_dp"},
        }
        result = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(result, SnapMirrorRelationship)
        assert result.relationship_type == ""
        assert result.policy_uuid == ""

    def test_missing_transfer_schedule(self) -> None:
        """Missing transfer_schedule defaults transfer_schedule_uuid to empty."""
        record: dict[str, Any] = {
            "uuid": "abc-123",
            "source": {"path": "svm1:vol1"},
        }
        result = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(result, SnapMirrorRelationship)
        assert result.transfer_schedule_uuid == ""

    def test_throttle_defaults_to_zero(self) -> None:
        """Throttle defaults to 0 when absent."""
        record: dict[str, Any] = {"uuid": "abc-123"}
        result = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(result, SnapMirrorRelationship)
        assert result.throttle == 0

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "uuid": "sm-1",
                    "source": {"path": "svm1:vol1"},
                    "destination": {"path": "svm2:vol1_dp"},
                    "policy": {"type": "async", "uuid": "pol-1"},
                    "throttle": 512,
                    "group_type": "none",
                    "transfer_schedule": {"uuid": "sched-1"},
                },
                {
                    "uuid": "sm-2",
                    "source": {"path": "svm1:vol2"},
                    "destination": {"path": "svm2:vol2_dp"},
                    "policy": {"type": "sync", "uuid": "pol-2"},
                    "throttle": 0,
                    "group_type": "svm_dr",
                },
            ],
        }
        results = parse_api_response(SNAPMIRROR_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].uuid == "sm-1"  # type: ignore[union-attr]
        assert results[1].uuid == "sm-2"  # type: ignore[union-attr]

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(SNAPMIRROR_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(SNAPMIRROR_MAPPING, {}, "[test]", MagicMock()) == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original 4 fields only (uuid, source_path,
    destination_path, relationship_type). The old parser also had ``state``
    which has been removed, and the new fields (policy_uuid, throttle,
    group_type, transfer_schedule_uuid) were not in the old parser.

    Note: The old parser used ``source.svm.name`` + ``source.path`` to build
    the path string, but the new mapping reads ``source.path`` directly which
    already contains the ``"svm:volume"`` string per the ONTAP REST API.
    Parity records use the new API response format.
    """

    _ORIGINAL_FIELDS = (
        "uuid",
        "source_path",
        "destination_path",
        "relationship_type",
    )

    @staticmethod
    def _old_parse_snapmirror(record: dict[str, Any]) -> SnapMirrorRelationship:
        """Reproduce old inline SnapMirror parsing logic from collector.

        This is a static copy of the code that was in
        ``_collect_relationships_via_api`` before migration, adapted to use
        the ``source.path`` format (the API returns full ``svm:volume`` paths).
        """
        source = record.get("source")
        source_path = source.get("path", "") if isinstance(source, dict) else ""

        destination = record.get("destination")
        dest_path = destination.get("path", "") if isinstance(destination, dict) else ""

        return SnapMirrorRelationship(
            uuid=record.get("uuid", ""),
            source_path=source_path,
            destination_path=dest_path,
            relationship_type=record.get("policy", {}).get("type", ""),
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical SnapMirrorRelationship."""
        old = self._old_parse_snapmirror(full_api_record)
        new = parse_api_record(SNAPMIRROR_MAPPING, full_api_record, "[test]")
        assert isinstance(new, SnapMirrorRelationship)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"uuid": "abc-123"}
        old = self._old_parse_snapmirror(record)
        new = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(new, SnapMirrorRelationship)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_missing_policy(self) -> None:
        """Framework and old parser match when policy is missing."""
        record: dict[str, Any] = {
            "uuid": "abc-123",
            "source": {"path": "svm1:vol1"},
            "destination": {"path": "svm2:vol1_dp"},
        }
        old = self._old_parse_snapmirror(record)
        new = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(new, SnapMirrorRelationship)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_empty_source_destination(self) -> None:
        """Framework and old parser match with empty source/destination."""
        record: dict[str, Any] = {
            "uuid": "abc-123",
            "source": {},
            "destination": {},
            "policy": {"type": "async"},
        }
        old = self._old_parse_snapmirror(record)
        new = parse_api_record(SNAPMIRROR_MAPPING, record, "[test]")
        assert isinstance(new, SnapMirrorRelationship)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
