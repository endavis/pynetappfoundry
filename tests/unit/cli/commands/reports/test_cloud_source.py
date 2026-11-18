"""Tests for the report cloud source: OCCM cache first, ONTAP CLI path as the fallback (#1086)."""

from __future__ import annotations

import logging
from collections.abc import Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, PropertyMock, patch

import pytest

from pynetappfoundry.cache._metadata import CachedClusterMetadata
from pynetappfoundry.cache.cluster_resolver import ClusterResolver
from pynetappfoundry.cache.db import ClusterMetadataDB
from pynetappfoundry.cache.occm_collector import OccmAgentSnapshot, OccmSnapshot
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.cli.commands.reports._cloud_source import ReportCloudSource
from pynetappfoundry.console.discovery import ConsoleInventory
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.models.ontap.cluster.model import OntapCluster

UUID = "11111111-1111-1111-1111-111111111111"
AWS_HA = "OccmAwsHaWorkingEnvironment"
GCP = "OccmGcpWorkingEnvironment"
ON_PREM = "OccmOnpremWorkingEnvironment"
CVO_ID = "VsaWorkingEnvironment-AAAA"
ONPREM_ID = "OnPremWorkingEnvironment-BBBB"
NODES = ["lab1-01", "lab1-02"]


def _aws_we(public_id: str = CVO_ID, uuid: str = UUID, name: str = "lab1") -> dict[str, Any]:
    return {
        "publicId": public_id,
        "name": name,
        "isHA": True,
        "awsProperties": {
            "accountId": "111122223333",
            "regionName": "us-east-1",
            "instances": [
                {"id": "i-1", "isVsaInstance": True, "instanceType": "m5.xlarge"},
                {"id": "i-2", "isVsaInstance": True, "instanceType": "m5.xlarge"},
            ],
        },
        "ontapClusterProperties": {
            "clusterUuid": uuid,
            "clusterName": name,
            "nodes": [
                {"name": "lab1-01", "cloudProviderId": "i-1"},
                {"name": "lab1-02", "cloudProviderId": "i-2"},
            ],
        },
    }


def _on_prem_we() -> dict[str, Any]:
    return {
        "publicId": ONPREM_ID,
        "name": "lab1",
        "ontapClusterProperties": {"clusterUuid": UUID, "clusterName": "lab1"},
    }


def _snapshot(agents: dict[str, dict[str, list[dict[str, Any]]]]) -> OccmSnapshot:
    when = datetime.now(UTC)
    return OccmSnapshot(
        cached_at=when,
        inventory=ConsoleInventory(),
        agents=tuple(
            OccmAgentSnapshot(
                agent_id=a, scope=None, organization_id="org", cached_at=when, records=r
            )
            for a, r in agents.items()
        ),
        failed_agents=(),
        skipped_agents=(),
    )


@pytest.fixture
def ontap_db() -> Iterator[ClusterMetadataDB]:
    with ClusterMetadataDB(db_path=":memory:") as db:
        db.set(
            "lab1",
            CachedClusterMetadata(
                cluster_name="lab1", cluster=OntapCluster(name="lab1", uuid=UUID)
            ),
        )
        yield db


@pytest.fixture
def occm_db(tmp_path: Path) -> Iterator[OccmCacheDB]:
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        yield db


def _source(ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB) -> ReportCloudSource:
    resolver = ClusterResolver(ontap_db=ontap_db, aiqum_db=None, occm_db=occm_db)
    return ReportCloudSource(resolver, ui_base_url="https://ui.example.test")


def _entry(cloud: list[CloudMetadata] | None = None, *, raises: bool = False) -> MagicMock:
    entry = MagicMock()
    ontap = MagicMock()
    if raises:
        type(ontap).cloud = PropertyMock(side_effect=AssertionError("ontap.cloud was read"))
    else:
        ontap.cloud = cloud or []
    entry.ontap = ontap
    return entry


CLI_META = [CloudMetadata(node="lab1-01", provider="AWS", instance_id="cli-1")]


def test_occm_hit_never_touches_the_cli_path(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    occm_db.set(_snapshot({"agent-1": {AWS_HA: [_aws_we()]}}))
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(raises=True)
    )
    assert details.source == "occm"
    assert [m.instance_id for m in details.metadata] == ["i-1", "i-2"]
    assert details.console is not None
    assert details.console.working_environment.endswith(CVO_ID)
    assert details.console.aggregates.endswith("/aggregates")


def test_miss_uses_the_cli_path(ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB) -> None:
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META)
    )
    assert details.source == "cli"
    assert details.metadata == CLI_META
    assert details.console is None


def test_incomplete_record_uses_cli_but_keeps_console_links(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    occm_db.set(_snapshot({"agent-1": {AWS_HA: [_aws_we()]}}))
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=[*NODES, "lab1-03"], entry=_entry(CLI_META)
    )
    assert details.source == "cli"
    assert details.metadata == CLI_META
    assert details.console is not None


def test_unsupported_cloud_mapping_uses_cli(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    occm_db.set(_snapshot({"agent-1": {GCP: [_aws_we()]}}))
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META)
    )
    assert details.source == "cli"
    assert details.console is not None


@pytest.mark.parametrize(
    "mapping", ["OccmAzureWorkingEnvironment", "OccmAzureHaWorkingEnvironment"]
)
def test_azure_uses_cli_but_keeps_console_links(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB, mapping: str
) -> None:
    occm_db.set(_snapshot({"agent-1": {mapping: [_aws_we()]}}))
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META)
    )
    assert details.source == "cli"
    assert details.metadata == CLI_META
    assert details.console is not None
    assert details.console.working_environment


def test_ambiguous_match_uses_cli_without_console(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    occm_db.set(
        _snapshot({"agent-1": {AWS_HA: [_aws_we(), _aws_we("VsaWorkingEnvironment-CCCC")]}})
    )
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META)
    )
    assert details.source == "cli"
    assert details.console is None


def test_not_cloud_gives_none_with_on_prem_links_and_no_cli_access(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB
) -> None:
    occm_db.set(_snapshot({"agent-1": {ON_PREM: [_on_prem_we()]}}))
    details = _source(ontap_db, occm_db).details(
        "lab1", is_cloud=False, node_names=NODES, entry=_entry(raises=True)
    )
    assert details.source == "none"
    assert details.metadata == []
    assert details.console is not None
    assert details.console.working_environment
    assert details.console.volumes
    assert details.console.aggregates == ""


def test_resolver_error_falls_back_with_a_warning_without_values(
    ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB, caplog: pytest.LogCaptureFixture
) -> None:
    source = _source(ontap_db, occm_db)
    with (
        patch.object(ClusterResolver, "read", side_effect=LookupError("secret-record-value-xyz")),
        caplog.at_level(logging.WARNING),
    ):
        details = source.details("lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META))
    assert details.source == "cli"
    assert details.metadata == CLI_META
    assert details.console is None
    assert "lab1" in caplog.text
    assert "LookupError" in caplog.text
    assert "secret-record-value-xyz" not in caplog.text


def test_no_resolver_uses_cli() -> None:
    details = ReportCloudSource(None).details(
        "lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META)
    )
    assert (details.source, details.metadata, details.console) == ("cli", CLI_META, None)


def test_occm_path_makes_no_live_call(ontap_db: ClusterMetadataDB, occm_db: OccmCacheDB) -> None:
    occm_db.set(_snapshot({"agent-1": {AWS_HA: [_aws_we()]}}))
    boom = RuntimeError("live call")
    with (
        patch("pynetappfoundry.data.source.DataSource", side_effect=boom) as ds,
        patch("pynetappfoundry.clients.console.agent.ConsoleAgentClient", side_effect=boom) as c,
        patch("socket.socket.connect", side_effect=boom) as connect,
    ):
        details = _source(ontap_db, occm_db).details(
            "lab1", is_cloud=True, node_names=NODES, entry=_entry(raises=True)
        )
    assert details.source == "occm"
    for mock in (ds, c, connect):
        mock.assert_not_called()


def test_from_config_with_no_files_creates_nothing(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    config.settings = {}
    config.get_setting.return_value = "https://ui.example.test"
    with ReportCloudSource.from_config(config) as source:
        details = source.details("lab1", is_cloud=True, node_names=NODES, entry=_entry(CLI_META))
    assert details.source == "cli"
    assert list(tmp_path.iterdir()) == []


def test_from_config_opens_existing_files_then_closes_them(tmp_path: Path) -> None:
    config = MagicMock()
    config.config_dir = tmp_path
    config.settings = {"aws": {"sso": {"subdomain": "corp"}}}
    config.get_setting.return_value = "https://ui.example.test"
    cache = tmp_path / ".cache"
    cache.mkdir()
    with ClusterMetadataDB(db_path=cache / "cluster_metadata.db") as ontap:
        ontap.set(
            "lab1",
            CachedClusterMetadata(
                cluster_name="lab1", cluster=OntapCluster(name="lab1", uuid=UUID)
            ),
        )
    with OccmCacheDB(db_path=cache / "occm_cache.db") as occm:
        occm.set(_snapshot({"agent-1": {AWS_HA: [_aws_we()]}}))
    with ReportCloudSource.from_config(config) as source:
        details = source.details("lab1", is_cloud=True, node_names=NODES, entry=_entry(raises=True))
        opened = list(source._owned)
    assert details.source == "occm"
    assert len(opened) == 2
    for opened_db in opened:
        with pytest.raises(Exception, match="closed"):
            opened_db.conn.execute("SELECT 1")
