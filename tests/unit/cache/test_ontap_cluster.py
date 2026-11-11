"""Tests for the generated ``OntapCluster`` model and mapping (#967, ADR-0024)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

from pynetappfoundry.cache._base import METADATA_SCHEMA_MIN_COMPATIBLE, METADATA_SCHEMA_VERSION
from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.db import ClusterMetadataDB, _model_to_row, realtime_attrs
from pynetappfoundry.cache.fetchers import fetch
from pynetappfoundry.cache.ontap.cluster.mapping import ONTAPCLUSTER_MAPPING
from pynetappfoundry.models.ontap.cluster.model import OntapCluster, OntapClusterVersion

_UUID = "00000000-0000-0000-0000-000000000001"


def test_password_fields_are_realtime() -> None:
    passwords = [f for f in ONTAPCLUSTER_MAPPING.fields if f.cache_attr.endswith("password")]
    assert {f.cache_attr for f in passwords} == {
        "password",
        "active_directory.password",
        "configuration_backup.password",
    }
    assert all(f.cache_strategy == "realtime" for f in passwords)


def test_metric_and_statistics_fields_are_realtime() -> None:
    volatile = [
        f
        for f in ONTAPCLUSTER_MAPPING.fields
        if f.cache_attr.startswith(("metric.", "statistics."))
    ]
    assert volatile
    assert all(f.cache_strategy == "realtime" for f in volatile)
    assert "password" in realtime_attrs(OntapCluster)


def test_fetch_leaves_password_defaults_and_row_stores_none() -> None:
    client = MagicMock()
    client.call_endpoint.return_value = {
        "name": "c1",
        "uuid": _UUID,
        "password": "top-secret",
        "active_directory": {"password": "nested-secret", "fqdn": "ad.example.com"},
        "configuration_backup": {"password": "backup-secret", "url": "https://b"},
    }
    result = fetch(OntapCluster, cluster="c1", config=None, api_client=client)

    assert isinstance(result, OntapCluster)
    assert result.password == ""
    assert result.active_directory.password == ""
    assert result.configuration_backup.password == ""
    assert result.active_directory.fqdn == "ad.example.com"
    row = _model_to_row(result, OntapCluster, realtime_attrs(OntapCluster))
    assert "secret" not in json.dumps(row, default=str)


def test_mapping_shape() -> None:
    assert ONTAPCLUSTER_MAPPING.response_shape == "singleton"
    assert ONTAPCLUSTER_MAPPING.name == "OntapCluster"


def test_to_flat_dict_reads_nested_cluster_values() -> None:
    metadata = CachedClusterMetadata(
        cluster_name="c1",
        cluster=OntapCluster(
            name="c1", uuid=_UUID, version=OntapClusterVersion(full="9.15.1", generation=9)
        ),
    )
    flat: dict[str, Any] = dict(metadata.to_flat_dict())
    assert flat["cluster_uuid"] == _UUID
    assert flat["ontap_version"] == "9.15.1"
    assert flat["version_generation"] == "9"


def test_snapshot_schema_is_3_0_clean_break() -> None:
    assert METADATA_SCHEMA_VERSION == "3.0"
    assert METADATA_SCHEMA_MIN_COMPATIBLE == "3.0"


def _cluster_with_passwords() -> OntapCluster:
    return OntapCluster.model_validate(
        {
            "name": "c1",
            "uuid": _UUID,
            "password": "top-secret",
            "active_directory": {"password": "ad-secret", "fqdn": "ad.example.com"},
            "configuration_backup": {"password": "backup-secret", "url": "https://b"},
        }
    )


def test_model_to_row_strips_top_level_and_nested_passwords() -> None:
    row = _model_to_row(_cluster_with_passwords(), OntapCluster, realtime_attrs(OntapCluster))

    assert "secret" not in json.dumps(row, default=str)
    assert "password" not in row
    assert json.loads(row["active_directory"])["fqdn"] == "ad.example.com"
    assert json.loads(row["configuration_backup"])["url"] == "https://b"


def test_directly_built_cluster_round_trips_without_passwords(tmp_path: Path) -> None:
    db = ClusterMetadataDB(db_path=tmp_path / "pw.db")
    db.set("c1", CachedClusterMetadata(cluster_name="c1", cluster=_cluster_with_passwords()))
    stored = " ".join(
        str(v) for r in db.conn.execute("SELECT * FROM ontapcluster").fetchall() for v in tuple(r)
    )
    loaded = db.get("c1")
    db.close()

    assert "secret" not in stored
    assert loaded is not None
    assert loaded.cluster.password == ""
    assert loaded.cluster.active_directory.password == ""
    assert loaded.cluster.configuration_backup.password == ""
    assert loaded.cluster.active_directory.fqdn == "ad.example.com"


def test_model_to_row_without_exclude_keeps_nested_values() -> None:
    row = _model_to_row(_cluster_with_passwords(), OntapCluster)
    assert json.loads(row["active_directory"])["password"] == "ad-secret"
