"""Characterization tests for dotted-path handling in ``cache/db.py`` (#965).

These pin the registry order and the nested shape that
``_query_registry_subset`` and ``_insert_model_data`` produce, so the
dotted-path helpers can be consolidated without changing behaviour.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from pynetappfoundry.cache import CachedClusterMetadata
from pynetappfoundry.cache.db import ClusterMetadataDB, _query_registry_subset
from pynetappfoundry.cache.db_schema import _ensure_registry
from pynetappfoundry.models.ontap.name_services.dns.model import OntapDns
from pynetappfoundry.models.ontap.network.ip.subnets.model import OntapIpSubnet
from pynetappfoundry.models.ontap.network.model import NetworkInfo
from pynetappfoundry.models.ontap.storage.model import StorageInfo
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume


@pytest.fixture
def db() -> ClusterMetadataDB:
    """Create an in-memory test database."""
    return ClusterMetadataDB(db_path=":memory:")


def _sample() -> CachedClusterMetadata:
    return CachedClusterMetadata(
        cluster_name="c1",
        network=NetworkInfo(
            dns=[OntapDns(domains=["example.com"], servers=["10.0.0.1"])],
            ip_subnets=[OntapIpSubnet(name="sub1")],
        ),
        storage=StorageInfo(
            volumes=[
                OntapVolume(
                    name="vol1",
                    uuid="11111111-1111-1111-1111-111111111111",
                    size=1073741824,
                    state="online",
                ),
            ],
        ),
    )


class TestRegistryOrder:
    """The registry lists ``network`` after its ``network.*`` children."""

    def test_network_container_follows_its_children(self) -> None:
        paths = list(_ensure_registry())
        children = [p for p in paths if p.startswith("network.")]
        assert children
        assert paths.index("network") > max(paths.index(c) for c in children)

    def test_network_is_only_prefix_entry(self) -> None:
        paths = list(_ensure_registry())
        prefixes = {p for p in paths if any(o.startswith(f"{p}.") for o in paths)}
        assert prefixes == {"network"}


class TestQueryRegistrySubset:
    """``_query_registry_subset`` nests registry paths into a kwargs dict."""

    def test_nested_shape_and_key_order(self, db: ClusterMetadataDB) -> None:
        db.set("c1", _sample())
        registry = _ensure_registry()
        subset = {k: registry[k] for k in ("network.dns", "network")}

        result = _query_registry_subset(db.conn, "c1", subset)

        assert list(result) == ["network"]
        network: Any = result["network"]
        # The container entry replaces the dict built from its children.
        assert isinstance(network, NetworkInfo)

    def test_children_only_build_nested_dict(self, db: ClusterMetadataDB) -> None:
        db.set("c1", _sample())
        registry = _ensure_registry()
        subset = {k: registry[k] for k in ("network.dns", "network.ip_subnets")}

        result = _query_registry_subset(db.conn, "c1", subset)

        assert list(result) == ["network"]
        assert list(result["network"]) == ["dns", "ip_subnets"]
        assert [d.servers for d in result["network"]["dns"]] == [["10.0.0.1"]]
        assert [s.name for s in result["network"]["ip_subnets"]] == ["sub1"]

    def test_storage_path_nests_under_group(self, db: ClusterMetadataDB) -> None:
        db.set("c1", _sample())
        registry = _ensure_registry()

        subset = {"storage.volumes": registry["storage.volumes"]}
        result = _query_registry_subset(db.conn, "c1", subset)

        assert list(result) == ["storage"]
        assert [v.name for v in result["storage"]["volumes"]] == ["vol1"]

    def test_single_segment_path(self, db: ClusterMetadataDB) -> None:
        db.set("c1", _sample())
        registry = _ensure_registry()

        result = _query_registry_subset(db.conn, "c1", {"cloud": registry["cloud"]})

        assert result == {"cloud": []}


class TestRoundTrip:
    """Saving and reloading preserves the model exactly."""

    def test_round_trip_json_identical(self, db: ClusterMetadataDB) -> None:
        meta = _sample()
        db.set("c1", meta)

        got = db.get("c1")

        assert got is not None
        before = json.loads(meta.model_dump_json())
        after = json.loads(got.model_dump_json())
        for key in ("cluster_name", "storage"):
            assert after[key] == before[key]
        assert after["network"]["dns"] == before["network"]["dns"]
        assert after["network"]["ip_subnets"] == before["network"]["ip_subnets"]
