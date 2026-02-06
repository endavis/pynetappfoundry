"""Tests for the volume type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
    parse_cli_record,
    parse_cli_records,
)
from pynetappfoundry.cache.mappings.volume import (
    VOLUME_MAPPING,
    _api_aggregates_list,
    _cli_aggregates_list,
)
from pynetappfoundry.cache.models import VolumeInfo

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API volume record with all fields."""
    return {
        "uuid": "09d308eb-1234-5678-9abc-def012345678",
        "name": "PRODVOL1",
        "svm": {"name": "svm_PRODCL1"},
        "state": "online",
        "type": "rw",
        "style": "flexvol",
        "size": 9064378368,
        "autosize": {
            "mode": "grow_shrink",
            "grow_threshold": 90,
            "shrink_threshold": 50,
            "maximum": 18128756736,
            "minimum": 4532189184,
        },
        "files": {"maximum": 31122, "used": 100},
        "tiering": {"policy": "none", "min_cooling_days": 2},
        "aggregates": [
            {"name": "PRODAGGR1", "uuid": "aaa"},
            {"name": "PRODAGGR2", "uuid": "bbb"},
        ],
        "snapshot_policy": {"name": "none"},
        "nas": {
            "export_policy": {"name": "default"},
            "path": "/PRODVOL1",
            "security_style": "ntfs",
        },
    }


@pytest.fixture
def full_cli_record() -> dict[str, Any]:
    """Full CLI volume record with all fields."""
    return {
        "instance-uuid": "09d308eb-1234-5678-9abc-def012345678",
        "volume": "PRODVOL1",
        "vserver": "svm_PRODCL1",
        "state": "online",
        "type": "RW",
        "volume-style-extended": "flexvol",
        "size": "9064378368",
        "autosize-mode": "grow_shrink",
        "autosize-grow-threshold-percent": "90%",
        "autosize-shrink-threshold-percent": "50%",
        "max-autosize": "18128756736",
        "min-autosize": "4532189184",
        "files": "31122",
        "tiering-policy": "none",
        "tiering-minimum-cooling-days": "2",
        "aggregate": "PRODAGGR1",
        "aggr-list": "PRODAGGR1,PRODAGGR2",
        "snapshot-policy": "none",
        "policy": "default",
        "junction-path": "/PRODVOL1",
        "security-style": "ntfs",
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestVolumeMappingDefinition:
    """Tests for VOLUME_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid VolumeInfo field."""
        model_fields = set(VolumeInfo.model_fields.keys())
        for field in VOLUME_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on VolumeInfo"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in VOLUME_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_endpoint(self) -> None:
        """API endpoint includes expensive fields."""
        assert "autosize" in VOLUME_MAPPING.api_endpoint
        assert "files" in VOLUME_MAPPING.api_endpoint
        assert "nas.path" in VOLUME_MAPPING.api_endpoint
        assert "nas.security_style" in VOLUME_MAPPING.api_endpoint

    def test_cli_command(self) -> None:
        """CLI command is volume show."""
        assert VOLUME_MAPPING.cli_command == "volume show"

    def test_model_class(self) -> None:
        """Model class is VolumeInfo."""
        assert VOLUME_MAPPING.model_class is VolumeInfo

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = VOLUME_MAPPING.api_expected_fields()
        assert expected == [
            "aggregates",
            "autosize",
            "files",
            "name",
            "nas",
            "size",
            "snapshot_policy",
            "state",
            "style",
            "svm",
            "tiering",
            "type",
            "uuid",
        ]


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestVolumeApiParsing:
    """Tests for parsing API volume records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record parses to complete VolumeInfo."""
        vol = parse_api_record(VOLUME_MAPPING, full_api_record, "[test]")
        assert isinstance(vol, VolumeInfo)
        assert vol.uuid == "09d308eb-1234-5678-9abc-def012345678"
        assert vol.name == "PRODVOL1"
        assert vol.svm == "svm_PRODCL1"
        assert vol.state == "online"
        assert vol.type == "rw"
        assert vol.style == "flexvol"
        assert vol.size == 9064378368
        assert vol.autosize_mode == "grow_shrink"
        assert vol.autosize_grow_threshold == 90
        assert vol.autosize_shrink_threshold == 50
        assert vol.autosize_maximum == 18128756736
        assert vol.autosize_minimum == 4532189184
        assert vol.files_maximum == 31122
        assert vol.tiering_policy == "none"
        assert vol.tiering_minimum_cooling_days == 2
        assert vol.aggregate == "PRODAGGR1"
        assert vol.aggregates == ["PRODAGGR1", "PRODAGGR2"]
        assert vol.snapshot_policy == "none"
        assert vol.export_policy == "default"
        assert vol.junction_path == "/PRODVOL1"
        assert vol.nas_security_style == "ntfs"

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "minvol", "uuid": "abc"}
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert isinstance(vol, VolumeInfo)
        assert vol.name == "minvol"
        assert vol.uuid == "abc"
        assert vol.svm == ""
        assert vol.size == 0
        assert vol.autosize_mode == ""
        assert vol.aggregate == ""
        assert vol.aggregates == []

    def test_nested_svm_extraction(self) -> None:
        """svm.name dot-path works."""
        record: dict[str, Any] = {"svm": {"name": "test_svm"}}
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert vol.svm == "test_svm"

    def test_autosize_fields(self) -> None:
        """autosize.* fields extracted correctly."""
        record: dict[str, Any] = {
            "autosize": {"mode": "grow", "grow_threshold": 85},
        }
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert vol.autosize_mode == "grow"
        assert vol.autosize_grow_threshold == 85

    def test_aggregate_first_of_list(self) -> None:
        """aggregates[0].name extracted for single aggregate field."""
        record: dict[str, Any] = {
            "aggregates": [{"name": "aggr1"}, {"name": "aggr2"}],
        }
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert vol.aggregate == "aggr1"

    def test_aggregate_empty_list(self) -> None:
        """Empty aggregates list gives default for aggregate."""
        record: dict[str, Any] = {"aggregates": []}
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert vol.aggregate == ""
        assert vol.aggregates == []

    def test_nas_fields(self) -> None:
        """nas.* nested fields extracted correctly."""
        record: dict[str, Any] = {
            "nas": {
                "export_policy": {"name": "pol1"},
                "path": "/vol1",
                "security_style": "unix",
            },
        }
        vol = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert vol.export_policy == "pol1"
        assert vol.junction_path == "/vol1"
        assert vol.nas_security_style == "unix"

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {"name": "vol1", "uuid": "a"},
                {"name": "vol2", "uuid": "b"},
            ],
        }
        results = parse_api_response(VOLUME_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "vol1"
        assert results[1].name == "vol2"


# ---------------------------------------------------------------------------
# CLI parsing tests
# ---------------------------------------------------------------------------


class TestVolumeCliParsing:
    """Tests for parsing CLI volume records."""

    def test_full_record(self, full_cli_record: dict[str, Any]) -> None:
        """Full CLI record parses to complete VolumeInfo."""
        vol = parse_cli_record(VOLUME_MAPPING, full_cli_record, "[test]")
        assert isinstance(vol, VolumeInfo)
        assert vol.uuid == "09d308eb-1234-5678-9abc-def012345678"
        assert vol.name == "PRODVOL1"
        assert vol.svm == "svm_PRODCL1"
        assert vol.state == "online"
        assert vol.type == "RW"
        assert vol.style == "flexvol"
        assert vol.size == 9064378368
        assert vol.autosize_mode == "grow_shrink"
        assert vol.autosize_grow_threshold == 90
        assert vol.autosize_shrink_threshold == 50
        assert vol.autosize_maximum == 18128756736
        assert vol.autosize_minimum == 4532189184
        assert vol.files_maximum == 31122
        assert vol.tiering_policy == "none"
        assert vol.tiering_minimum_cooling_days == 2
        assert vol.aggregate == "PRODAGGR1"
        assert vol.aggregates == ["PRODAGGR1", "PRODAGGR2"]
        assert vol.snapshot_policy == "none"
        assert vol.export_policy == "default"
        assert vol.junction_path == "/PRODVOL1"
        assert vol.nas_security_style == "ntfs"

    def test_int_coercion_with_percent(self) -> None:
        """CLI percentage values have % stripped before int conversion."""
        record = {
            "autosize-grow-threshold-percent": "85%",
            "autosize-shrink-threshold-percent": "45%",
        }
        vol = parse_cli_record(VOLUME_MAPPING, record, "[test]")
        assert vol.autosize_grow_threshold == 85
        assert vol.autosize_shrink_threshold == 45

    def test_dash_values_use_defaults(self) -> None:
        """CLI dash values coerce to default."""
        record = {
            "tiering-minimum-cooling-days": "-",
            "junction-path": "-",
        }
        vol = parse_cli_record(VOLUME_MAPPING, record, "[test]")
        assert vol.tiering_minimum_cooling_days == 0
        assert vol.junction_path == ""

    def test_cli_aggregates_transform(self) -> None:
        """CLI aggr-list parsed into list."""
        record = {"aggr-list": "aggr1, aggr2, aggr3"}
        vol = parse_cli_record(VOLUME_MAPPING, record, "[test]")
        assert vol.aggregates == ["aggr1", "aggr2", "aggr3"]

    def test_cli_aggregates_empty(self) -> None:
        """Empty aggr-list returns empty list."""
        record: dict[str, Any] = {"aggr-list": "-"}
        vol = parse_cli_record(VOLUME_MAPPING, record, "[test]")
        assert vol.aggregates == []

    def test_parse_cli_records_multiple(self) -> None:
        """parse_cli_records handles multiple records."""
        records = [
            {"volume": "vol1", "instance-uuid": "a"},
            {"volume": "vol2", "instance-uuid": "b"},
        ]
        results = parse_cli_records(VOLUME_MAPPING, records, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "vol1"
        assert results[1].name == "vol2"


# ---------------------------------------------------------------------------
# Transform unit tests
# ---------------------------------------------------------------------------


class TestTransformFunctions:
    """Tests for volume transform functions."""

    def test_api_aggregates_list_normal(self) -> None:
        """Normal aggregate list extraction."""
        record = {
            "aggregates": [
                {"name": "aggr1", "uuid": "a"},
                {"name": "aggr2", "uuid": "b"},
            ]
        }
        assert _api_aggregates_list(record) == ["aggr1", "aggr2"]

    def test_api_aggregates_list_empty(self) -> None:
        """Empty aggregates list."""
        assert _api_aggregates_list({"aggregates": []}) == []
        assert _api_aggregates_list({}) == []

    def test_api_aggregates_list_filters_non_dict(self) -> None:
        """Non-dict items in aggregates are filtered out."""
        record: dict[str, Any] = {"aggregates": [{"name": "a"}, "bad", None]}
        assert _api_aggregates_list(record) == ["a"]

    def test_api_aggregates_list_filters_empty_names(self) -> None:
        """Aggregates with empty/missing names are filtered."""
        record = {"aggregates": [{"name": ""}, {"name": "a"}, {"uuid": "b"}]}
        assert _api_aggregates_list(record) == ["a"]

    def test_cli_aggregates_list_comma_separated(self) -> None:
        """Comma-separated aggr-list."""
        record = {"aggr-list": "aggr1,aggr2,aggr3"}
        assert _cli_aggregates_list(record) == ["aggr1", "aggr2", "aggr3"]

    def test_cli_aggregates_list_space_separated(self) -> None:
        """Space-separated aggr-list."""
        record = {"aggr-list": "aggr1 aggr2"}
        assert _cli_aggregates_list(record) == ["aggr1", "aggr2"]

    def test_cli_aggregates_list_dash(self) -> None:
        """Dash means no aggregates."""
        assert _cli_aggregates_list({"aggr-list": "-"}) == []

    def test_cli_aggregates_list_empty(self) -> None:
        """Empty string means no aggregates."""
        assert _cli_aggregates_list({"aggr-list": ""}) == []
        assert _cli_aggregates_list({}) == []


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written parser."""

    @staticmethod
    def _old_parse_volume(record: dict[str, Any]) -> VolumeInfo:
        """Reproduce old _parse_volumes_response logic for one record."""
        autosize = record.get("autosize", {})
        tiering = record.get("tiering", {})
        nas = record.get("nas", {})
        aggr = record.get("aggregates", [])
        return VolumeInfo(
            uuid=record.get("uuid", ""),
            name=record.get("name", ""),
            svm=(record.get("svm", {}).get("name", "") if record.get("svm") else ""),
            state=record.get("state", ""),
            type=record.get("type", ""),
            style=record.get("style", ""),
            size=record.get("size", 0),
            autosize_mode=autosize.get("mode", ""),
            autosize_grow_threshold=autosize.get("grow_threshold", 0),
            autosize_shrink_threshold=autosize.get("shrink_threshold", 0),
            autosize_maximum=autosize.get("maximum", 0),
            autosize_minimum=autosize.get("minimum", 0),
            files_maximum=record.get("files", {}).get("maximum", 0),
            tiering_policy=tiering.get("policy", ""),
            tiering_minimum_cooling_days=tiering.get("min_cooling_days", 0),
            aggregate=(record.get("aggregates", [{}])[0].get("name", "") if aggr else ""),
            aggregates=[a.get("name", "") for a in aggr if a.get("name")],
            snapshot_policy=(record.get("snapshot_policy", {}).get("name", "")),
            export_policy=nas.get("export_policy", {}).get("name", ""),
            junction_path=nas.get("path", ""),
            nas_security_style=nas.get("security_style", ""),
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical VolumeInfo."""
        old = self._old_parse_volume(full_api_record)
        new = parse_api_record(VOLUME_MAPPING, full_api_record, "[test]")
        assert isinstance(new, VolumeInfo)
        for field_name in VolumeInfo.model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"name": "testvol", "uuid": "xyz"}
        old = self._old_parse_volume(record)
        new = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert isinstance(new, VolumeInfo)
        for field_name in VolumeInfo.model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_missing_nested(self) -> None:
        """Framework and old parser match with missing nested objects."""
        record: dict[str, Any] = {
            "name": "vol1",
            "svm": None,
            "autosize": {},
            "nas": {},
        }
        old = self._old_parse_volume(record)
        new = parse_api_record(VOLUME_MAPPING, record, "[test]")
        assert isinstance(new, VolumeInfo)
        for field_name in VolumeInfo.model_fields:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
