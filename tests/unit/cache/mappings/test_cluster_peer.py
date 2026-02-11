"""Tests for the cluster peer type mapping definition."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from pynetappfoundry.cache import ClusterPeer
from pynetappfoundry.cache.cluster.peers.mapping import (
    CLUSTER_PEER_MAPPING,
    _api_authentication_in_use,
    _api_authentication_state,
    _api_encryption_state,
    _api_peer_addresses,
    _api_remote_cluster_name,
)
from pynetappfoundry.cache.field_mapping import (
    parse_api_record,
    parse_api_response,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def full_api_record() -> dict[str, Any]:
    """Full API cluster peer record with dict remote and authentication."""
    return {
        "name": "DRCL1",
        "uuid": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "remote": {
            "name": "DRCL1",
            "ip_addresses": ["10.0.1.10", "10.0.1.11"],
        },
        "authentication": {
            "state": "ok",
            "in_use": "pre_shared_key",
        },
        "encryption": {
            "state": "tls_psk",
        },
    }


# ---------------------------------------------------------------------------
# Mapping definition tests
# ---------------------------------------------------------------------------


class TestClusterPeerMappingDefinition:
    """Tests for CLUSTER_PEER_MAPPING structure."""

    def test_all_cache_attrs_exist_on_model(self) -> None:
        """Every cache_attr in the mapping is a valid ClusterPeer field."""
        model_fields = set(ClusterPeer.model_fields.keys())
        for field in CLUSTER_PEER_MAPPING.fields:
            assert field.cache_attr in model_fields, (
                f"cache_attr '{field.cache_attr}' not on ClusterPeer"
            )

    def test_no_duplicate_cache_attrs(self) -> None:
        """No duplicate cache_attr values."""
        attrs = [f.cache_attr for f in CLUSTER_PEER_MAPPING.fields]
        assert len(attrs) == len(set(attrs))

    def test_field_count(self) -> None:
        """Mapping has expected number of fields (7)."""
        assert len(CLUSTER_PEER_MAPPING.fields) == 7

    def test_model_class(self) -> None:
        """Model class is ClusterPeer."""
        assert CLUSTER_PEER_MAPPING.model_class is ClusterPeer

    def test_endpoint(self) -> None:
        """API endpoint is correct."""
        assert CLUSTER_PEER_MAPPING.api_endpoint == "/cluster/peers?fields=*"

    def test_cli_command_empty(self) -> None:
        """CLI command is empty (API-only type)."""
        assert CLUSTER_PEER_MAPPING.cli_command == ""

    def test_api_expected_fields(self) -> None:
        """api_expected_fields returns correct top-level keys."""
        expected = CLUSTER_PEER_MAPPING.api_expected_fields()
        assert expected == ["name", "uuid"]

    def test_id_field(self) -> None:
        """id_field is name (default)."""
        assert CLUSTER_PEER_MAPPING.id_field == "name"


# ---------------------------------------------------------------------------
# API parsing tests
# ---------------------------------------------------------------------------


class TestClusterPeerApiParsing:
    """Tests for parsing API cluster peer records."""

    def test_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Full API record with dict remote/auth parses correctly."""
        result = parse_api_record(CLUSTER_PEER_MAPPING, full_api_record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.name == "DRCL1"
        assert result.uuid == "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        assert result.remote_cluster_name == "DRCL1"
        assert result.peer_addresses == ["10.0.1.10", "10.0.1.11"]
        assert result.authentication_state == "ok"
        assert result.authentication_in_use == "pre_shared_key"
        assert result.encryption_state == "tls_psk"

    def test_minimal_record(self) -> None:
        """Minimal record uses defaults for missing fields."""
        record: dict[str, Any] = {"name": "PEER1", "uuid": "abc"}
        result = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.name == "PEER1"
        assert result.uuid == "abc"
        assert result.remote_cluster_name == ""
        assert result.peer_addresses == []
        assert result.authentication_state == ""
        assert result.authentication_in_use == ""
        assert result.encryption_state == ""

    def test_remote_as_string(self) -> None:
        """When remote is a string, remote_cluster_name gets the string value."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": "REMOTECL1",
            "authentication": {"state": "ok"},
        }
        result = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.remote_cluster_name == "REMOTECL1"
        assert result.peer_addresses == []

    def test_authentication_as_string(self) -> None:
        """When authentication is a string, authentication_state gets the string value."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": {"name": "REMOTECL1", "ip_addresses": ["10.0.1.1"]},
            "authentication": "pending",
        }
        result = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.authentication_state == "pending"

    def test_missing_fields(self) -> None:
        """Record with no remote or authentication fields."""
        record: dict[str, Any] = {"name": "PEER1"}
        result = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.name == "PEER1"
        assert result.uuid == ""
        assert result.remote_cluster_name == ""
        assert result.peer_addresses == []
        assert result.authentication_state == ""
        assert result.authentication_in_use == ""
        assert result.encryption_state == ""

    def test_address_filtering(self) -> None:
        """Empty/falsy addresses are filtered out."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": {
                "name": "REMOTECL1",
                "ip_addresses": ["10.0.1.1", "", None, "10.0.1.2"],
            },
        }
        result = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(result, ClusterPeer)
        assert result.peer_addresses == ["10.0.1.1", "10.0.1.2"]

    def test_parse_api_response_multiple(self) -> None:
        """parse_api_response handles multiple records."""
        response = {
            "records": [
                {
                    "name": "PEER1",
                    "uuid": "a",
                    "remote": {"name": "CL1", "ip_addresses": ["10.0.1.1"]},
                    "authentication": {"state": "ok"},
                },
                {
                    "name": "PEER2",
                    "uuid": "b",
                    "remote": {"name": "CL2", "ip_addresses": ["10.0.2.1"]},
                    "authentication": {"state": "ok"},
                },
            ],
        }
        results = parse_api_response(CLUSTER_PEER_MAPPING, response, "[test]", MagicMock())
        assert len(results) == 2
        assert results[0].name == "PEER1"
        assert results[1].name == "PEER2"

    def test_parse_api_response_empty(self) -> None:
        """parse_api_response handles empty/None response."""
        assert parse_api_response(CLUSTER_PEER_MAPPING, None, "[test]", MagicMock()) == []
        assert parse_api_response(CLUSTER_PEER_MAPPING, {}, "[test]", MagicMock()) == []


# ---------------------------------------------------------------------------
# Transform unit tests
# ---------------------------------------------------------------------------


class TestTransformFunctions:
    """Tests for cluster peer transform functions."""

    # -- _api_remote_cluster_name --

    def test_remote_cluster_name_dict(self) -> None:
        """Dict remote returns name."""
        assert _api_remote_cluster_name({"remote": {"name": "CL1"}}) == "CL1"

    def test_remote_cluster_name_dict_missing_name(self) -> None:
        """Dict remote without name key returns empty string."""
        assert _api_remote_cluster_name({"remote": {"ip_addresses": []}}) == ""

    def test_remote_cluster_name_string(self) -> None:
        """String remote returns the string."""
        assert _api_remote_cluster_name({"remote": "CL1"}) == "CL1"

    def test_remote_cluster_name_none(self) -> None:
        """None remote returns empty string."""
        assert _api_remote_cluster_name({"remote": None}) == ""

    def test_remote_cluster_name_missing(self) -> None:
        """Missing remote key returns empty string."""
        assert _api_remote_cluster_name({}) == ""

    # -- _api_peer_addresses --

    def test_peer_addresses_dict(self) -> None:
        """Dict remote extracts ip_addresses."""
        record = {"remote": {"name": "CL1", "ip_addresses": ["10.0.1.1", "10.0.1.2"]}}
        assert _api_peer_addresses(record) == ["10.0.1.1", "10.0.1.2"]

    def test_peer_addresses_dict_empty(self) -> None:
        """Dict remote with empty ip_addresses."""
        assert _api_peer_addresses({"remote": {"ip_addresses": []}}) == []

    def test_peer_addresses_dict_no_key(self) -> None:
        """Dict remote without ip_addresses key."""
        assert _api_peer_addresses({"remote": {"name": "CL1"}}) == []

    def test_peer_addresses_filters_falsy(self) -> None:
        """Falsy addresses are filtered out."""
        record = {"remote": {"ip_addresses": ["10.0.1.1", "", None, "10.0.1.2"]}}
        assert _api_peer_addresses(record) == ["10.0.1.1", "10.0.1.2"]

    def test_peer_addresses_string(self) -> None:
        """String remote returns empty list."""
        assert _api_peer_addresses({"remote": "CL1"}) == []

    def test_peer_addresses_none(self) -> None:
        """None remote returns empty list."""
        assert _api_peer_addresses({"remote": None}) == []

    def test_peer_addresses_missing(self) -> None:
        """Missing remote key returns empty list."""
        assert _api_peer_addresses({}) == []

    # -- _api_authentication_state --

    def test_authentication_state_dict(self) -> None:
        """Dict authentication returns state."""
        assert _api_authentication_state({"authentication": {"state": "ok"}}) == "ok"

    def test_authentication_state_dict_missing_state(self) -> None:
        """Dict authentication without state key returns empty string."""
        assert _api_authentication_state({"authentication": {"in_use": "ok"}}) == ""

    def test_authentication_state_string(self) -> None:
        """String authentication returns the string."""
        assert _api_authentication_state({"authentication": "pending"}) == "pending"

    def test_authentication_state_none(self) -> None:
        """None authentication returns empty string."""
        assert _api_authentication_state({"authentication": None}) == ""

    def test_authentication_state_missing(self) -> None:
        """Missing authentication key returns empty string."""
        assert _api_authentication_state({}) == ""

    # -- _api_authentication_in_use --

    def test_authentication_in_use_dict(self) -> None:
        """Dict authentication returns in_use."""
        assert (
            _api_authentication_in_use({"authentication": {"in_use": "pre_shared_key"}})
            == "pre_shared_key"
        )

    def test_authentication_in_use_dict_missing_key(self) -> None:
        """Dict authentication without in_use key returns empty string."""
        assert _api_authentication_in_use({"authentication": {"state": "ok"}}) == ""

    def test_authentication_in_use_string(self) -> None:
        """String authentication returns empty string."""
        assert _api_authentication_in_use({"authentication": "pending"}) == ""

    def test_authentication_in_use_none(self) -> None:
        """None authentication returns empty string."""
        assert _api_authentication_in_use({"authentication": None}) == ""

    def test_authentication_in_use_missing(self) -> None:
        """Missing authentication key returns empty string."""
        assert _api_authentication_in_use({}) == ""

    # -- _api_encryption_state --

    def test_encryption_state_dict(self) -> None:
        """Dict encryption returns state."""
        assert _api_encryption_state({"encryption": {"state": "tls_psk"}}) == "tls_psk"

    def test_encryption_state_dict_missing_key(self) -> None:
        """Dict encryption without state key returns empty string."""
        assert _api_encryption_state({"encryption": {"protocol": "tls"}}) == ""

    def test_encryption_state_string(self) -> None:
        """String encryption returns the string."""
        assert _api_encryption_state({"encryption": "none"}) == "none"

    def test_encryption_state_none(self) -> None:
        """None encryption returns empty string."""
        assert _api_encryption_state({"encryption": None}) == ""

    def test_encryption_state_missing(self) -> None:
        """Missing encryption key returns empty string."""
        assert _api_encryption_state({}) == ""


# ---------------------------------------------------------------------------
# Parity test: old parser vs new framework
# ---------------------------------------------------------------------------


class TestParityWithOldParser:
    """Verify framework produces same output as old hand-written inline parser.

    Parity is checked for the original 5 fields only. The new fields
    (authentication_in_use, encryption_state) were not in the old parser.
    """

    _ORIGINAL_FIELDS = (
        "name",
        "uuid",
        "remote_cluster_name",
        "peer_addresses",
        "authentication_state",
    )

    @staticmethod
    def _old_parse_cluster_peer(record: dict[str, Any]) -> ClusterPeer:
        """Reproduce old inline ClusterPeer parsing logic from collector.

        This is a static copy of the code that was in
        ``_collect_relationships_via_api`` before migration.
        """
        remote = record.get("remote")
        remote_name = remote.get("name", "") if isinstance(remote, dict) else str(remote or "")
        auth = record.get("authentication")
        auth_state = auth.get("state", "") if isinstance(auth, dict) else str(auth or "")
        peer_addresses = remote.get("ip_addresses", []) if isinstance(remote, dict) else []
        return ClusterPeer(
            name=record.get("name", ""),
            uuid=record.get("uuid", ""),
            remote_cluster_name=remote_name,
            peer_addresses=[addr for addr in peer_addresses if addr],
            authentication_state=auth_state,
        )

    def test_parity_full_record(self, full_api_record: dict[str, Any]) -> None:
        """Framework and old parser produce identical ClusterPeer."""
        old = self._old_parse_cluster_peer(full_api_record)
        new = parse_api_record(CLUSTER_PEER_MAPPING, full_api_record, "[test]")
        assert isinstance(new, ClusterPeer)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_minimal_record(self) -> None:
        """Framework and old parser match on minimal record."""
        record: dict[str, Any] = {"name": "PEER1", "uuid": "xyz"}
        old = self._old_parse_cluster_peer(record)
        new = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterPeer)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_remote_as_string(self) -> None:
        """Framework and old parser match when remote is a string."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": "REMOTECL1",
            "authentication": {"state": "ok"},
        }
        old = self._old_parse_cluster_peer(record)
        new = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterPeer)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_auth_as_string(self) -> None:
        """Framework and old parser match when authentication is a string."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": {"name": "CL1", "ip_addresses": ["10.0.1.1"]},
            "authentication": "pending",
        }
        old = self._old_parse_cluster_peer(record)
        new = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterPeer)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )

    def test_parity_address_filtering(self) -> None:
        """Framework and old parser match on address filtering."""
        record: dict[str, Any] = {
            "name": "PEER1",
            "uuid": "abc",
            "remote": {
                "name": "CL1",
                "ip_addresses": ["10.0.1.1", "", None, "10.0.1.2"],
            },
            "authentication": {"state": "ok"},
        }
        old = self._old_parse_cluster_peer(record)
        new = parse_api_record(CLUSTER_PEER_MAPPING, record, "[test]")
        assert isinstance(new, ClusterPeer)
        for field_name in self._ORIGINAL_FIELDS:
            old_val = getattr(old, field_name)
            new_val = getattr(new, field_name)
            assert old_val == new_val, (
                f"Field '{field_name}' differs: old={old_val!r}, new={new_val!r}"
            )
