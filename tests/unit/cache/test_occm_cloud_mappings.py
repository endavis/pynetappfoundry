"""Cloud working-environment mappings on the OCCM backend (#1074, ADR-0027, ADR-0030).

Fixtures use synthetic placeholder values shaped like the live measurements (#1074).
"""

from __future__ import annotations

import importlib
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
import requests
from pydantic import BaseModel, ValidationError

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import TypeMapping
from pynetappfoundry.cache.occm._working_environments import DEFAULT_FIELDS
from pynetappfoundry.cache.occm_collector import (
    OCCM_LIST_OPS,
    OCCM_WORKING_ENVIRONMENT_MAPPINGS,
    OccmAgentSnapshot,
    OccmCollector,
    OccmSnapshot,
    refresh_occm_cache,
)
from pynetappfoundry.cache.occm_db import OccmCacheDB
from pynetappfoundry.clients.console.generated import ConsoleAgentOps
from pynetappfoundry.console.discovery import AccountInventory, ConsoleInventory
from pynetappfoundry.data._routing import RoutingDecision
from pynetappfoundry.data.occm_backend import _OPS, OccmBackend
from pynetappfoundry.data.source import DataSource
from pynetappfoundry.models.console_types import ConsoleAgentInfo

_CLIENT_PATH = "pynetappfoundry.clients.console.agent.ConsoleAgentClient"
_LIVE = RoutingDecision(cache_fields=(), live_fields=("name", "publicId"))


@dataclass(frozen=True)
class Cloud:
    name: str
    package: str
    module: str
    endpoint: str
    op: str
    aws: bool
    measured: bool
    filter_path: str
    filter_value: str

    @property
    def model(self) -> type[BaseModel]:
        mod = importlib.import_module(f"pynetappfoundry.models.console.cvo.{self.module}")
        model: type[BaseModel] = mod.ResponseBody
        return model

    @property
    def mapping(self) -> TypeMapping:
        importlib.import_module(f"pynetappfoundry.cache.occm.{self.package}.mapping")
        mapping = model_registry.get_mapping(self.name)
        assert mapping is not None
        return mapping

    def item(self, public_id: str = "p1", **extra: Any) -> dict[str, Any]:
        """A measured-shape record with synthetic values."""
        data: dict[str, Any] = {"publicId": public_id, "name": f"n-{public_id}", **extra}
        if self.aws:
            data["awsProperties"] = {
                "regionName": "region-placeholder",
                "instances": [{"tags": {"tag-key": "tag-value"}}],
                "vpc": {"tags": [{"key": "tag-key", "value": "tag-value"}]},
            }
            data["cloudSyncProperties"] = {"isSynced": False}
        else:
            data["providerProperties"] = {
                "regionName": "region-placeholder",
                "subscriptionId": "subscription-placeholder",
                "availabilityZone": None,
            }
        return data


CLOUDS = [
    Cloud(
        "OccmAwsWorkingEnvironment",
        "aws_working_environments",
        "get_vsa_working_environments",
        "/occm/api/vsa/working-environments",
        "list_vsa_working_environments",
        True,
        False,
        "awsProperties.regionName",
        "region-placeholder",
    ),
    Cloud(
        "OccmAwsHaWorkingEnvironment",
        "aws_ha_working_environments",
        "get_aws_ha_working_environments",
        "/occm/api/aws/ha/working-environments",
        "list_aws_ha_working_environments",
        True,
        True,
        "awsProperties.regionName",
        "region-placeholder",
    ),
    Cloud(
        "OccmAzureWorkingEnvironment",
        "azure_working_environments",
        "get_azure_vsa_working_environments",
        "/occm/api/azure/vsa/working-environments",
        "list_azure_vsa_working_environments",
        False,
        True,
        "providerProperties.subscriptionId",
        "subscription-placeholder",
    ),
    Cloud(
        "OccmAzureHaWorkingEnvironment",
        "azure_ha_working_environments",
        "get_azure_ha_working_environments",
        "/occm/api/azure/ha/working-environments",
        "list_azure_ha_working_environments",
        False,
        True,
        "providerProperties.subscriptionId",
        "subscription-placeholder",
    ),
    Cloud(
        "OccmGcpWorkingEnvironment",
        "gcp_working_environments",
        "get_gcp_vsa_working_environments",
        "/occm/api/gcp/vsa/working-environments",
        "list_gcp_vsa_working_environments",
        False,
        False,
        "providerProperties.regionName",
        "region-placeholder",
    ),
    Cloud(
        "OccmGcpHaWorkingEnvironment",
        "gcp_ha_working_environments",
        "get_gcp_ha_working_environments",
        "/occm/api/gcp/ha/working-environments",
        "list_gcp_ha_working_environments",
        False,
        False,
        "providerProperties.regionName",
        "region-placeholder",
    ),
]
_IDS = [c.name for c in CLOUDS]
_AZURE_HA = CLOUDS[3]


def _gcp_fixup(cloud: Cloud, data: dict[str, Any]) -> dict[str, Any]:
    """GCP provider properties carry no subscription id; keep the region only."""
    if cloud.name.startswith("OccmGcp"):
        data["providerProperties"] = {"regionName": "region-placeholder"}
    return data


def _record(cloud: Cloud, public_id: str = "p1", **extra: Any) -> dict[str, Any]:
    return _gcp_fixup(cloud, cloud.item(public_id, **extra))


def _config() -> MagicMock:
    config = MagicMock()
    config.data = {"connectors": {"c1": {"agent_id": "agent-1"}}}
    return config


@pytest.fixture
def client_cls() -> Iterator[MagicMock]:
    with patch(_CLIENT_PATH) as cls:
        yield cls


@pytest.fixture
def empty_cache(tmp_path: Path) -> Iterator[OccmCacheDB]:
    with (
        OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db,
        patch.object(OccmBackend, "_cache_db", db),
    ):
        yield db


# --- mappings --------------------------------------------------------------------


def test_default_fields_are_the_eight_measured_keys() -> None:
    assert len(DEFAULT_FIELDS) == 8
    assert "publicId" in DEFAULT_FIELDS


def test_seven_working_environment_mappings() -> None:
    assert len(OCCM_WORKING_ENVIRONMENT_MAPPINGS) == 7
    assert {c.name for c in CLOUDS} <= set(OCCM_WORKING_ENVIRONMENT_MAPPINGS)


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_mapping_matches_model_and_defaults(cloud: Cloud) -> None:
    mapping = cloud.mapping
    model = cloud.model
    assert [f.cache_attr for f in mapping.fields] == list(model.model_fields)
    assert set(mapping.explicit_fetch_fields()) == set(model.model_fields) - DEFAULT_FIELDS
    assert set(model.model_fields) >= DEFAULT_FIELDS
    assert mapping.api_endpoint == cloud.endpoint
    assert mapping.api_type == "occm"
    assert mapping.records_path == ""
    assert mapping.identifier_field == "publicId"
    assert mapping.model_class is model
    assert model_registry.get_mapping_by_model_class(model) is mapping


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_endpoint_has_a_list_op_on_agent_ops(cloud: Cloud) -> None:
    assert OCCM_LIST_OPS[cloud.endpoint] == cloud.op
    assert _OPS[cloud.endpoint] == cloud.op
    assert callable(getattr(ConsoleAgentOps, cloud.op))


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_provider_properties_by_cloud(cloud: Cloud) -> None:
    fields = set(cloud.model.model_fields)
    if cloud.aws:
        assert {"awsProperties", "cloudSyncProperties"} <= fields
        assert "providerProperties" not in fields
    else:
        assert "providerProperties" in fields
        assert "awsProperties" not in fields


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_op_sends_fields_star_and_returns_response_bodies(cloud: Cloud) -> None:
    dispatch = MagicMock(return_value=[_record(cloud)])
    result = getattr(ConsoleAgentOps(dispatch), cloud.op)(fields="*")
    assert dispatch.call_args.kwargs["method"] == "GET"
    assert dispatch.call_args.kwargs["path_template"] == cloud.endpoint
    assert dispatch.call_args.kwargs["query_params"] == {"fields": "*"}
    assert isinstance(result[0], cloud.model)


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_measured_shape_validates_against_current_models(cloud: Cloud) -> None:
    extra: dict[str, Any] = {}
    if cloud.name == "OccmAwsHaWorkingEnvironment":
        extra["haProperties"] = {"mediatorStatus": {"statusCode": 0, "statusMessage": "ok"}}
    if cloud is _AZURE_HA:
        extra["haProperties"] = {
            "node1Info": {
                "instanceName": "node-placeholder",
                "availabilityZone": None,
                "availabilitySet": {"faultDomain": 0, "updateDomain": 0},
            }
        }
    model = cloud.model.model_validate(_record(cloud, **extra))
    assert model.model_dump()["publicId"] == "p1"


# --- backend ---------------------------------------------------------------------


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_backend_default_query_passes_no_fields(cloud: Cloud, client_cls: MagicMock) -> None:
    op = getattr(client_cls.return_value.ops, cloud.op)
    items = [cloud.model.model_validate(_record(cloud))]
    op.return_value = items
    result = OccmBackend(_config()).query(cloud.model, cloud.mapping, _LIVE, "a1", {})
    assert result == items
    op.assert_called_once_with()


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_backend_fields_csv(cloud: Cloud, client_cls: MagicMock) -> None:
    op = getattr(client_cls.return_value.ops, cloud.op)
    op.return_value = []
    prop = "awsProperties" if cloud.aws else "providerProperties"
    decision = RoutingDecision(cache_fields=(), live_fields=("name", prop))
    OccmBackend(_config()).query(cloud.model, cloud.mapping, decision, "a1", {})
    op.assert_called_once_with(fields=prop)


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_backend_dotted_filter_filters_in_memory(cloud: Cloud, client_cls: MagicMock) -> None:
    op = getattr(client_cls.return_value.ops, cloud.op)
    other_extra = _record(cloud, "p2")
    group = "awsProperties" if cloud.aws else "providerProperties"
    other_extra[group]["regionName"] = "other-region-placeholder"
    if "subscriptionId" in cloud.filter_path:
        other_extra[group]["subscriptionId"] = "other-subscription-placeholder"
    match = cloud.model.model_validate(_record(cloud, "p1"))
    other = cloud.model.model_validate(other_extra)
    op.return_value = [match, other]
    result = OccmBackend(_config()).query(
        cloud.model, cloud.mapping, _LIVE, "a1", {cloud.filter_path: cloud.filter_value}
    )
    assert result == [match]
    op.assert_called_once_with(fields=group)


def test_backend_azure_ha_node_filter(client_cls: MagicMock) -> None:
    cloud = _AZURE_HA
    op = getattr(client_cls.return_value.ops, cloud.op)
    ha = {"node1Info": {"instanceName": "node-placeholder"}}
    match = cloud.model.model_validate(_record(cloud, "p1", haProperties=ha))
    other = cloud.model.model_validate(
        _record(cloud, "p2", haProperties={"node1Info": {"instanceName": "other-placeholder"}})
    )
    op.return_value = [match, other]
    result = OccmBackend(_config()).query(
        cloud.model,
        cloud.mapping,
        _LIVE,
        "a1",
        {"haProperties.node1Info.instanceName": "node-placeholder"},
    )
    assert result == [match]
    op.assert_called_once_with(fields="haProperties")


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_backend_wrong_item_class_raises(cloud: Cloud, client_cls: MagicMock) -> None:
    getattr(client_cls.return_value.ops, cloud.op).return_value = [{"publicId": "p1"}]
    with pytest.raises(TypeError, match="expected ResponseBody"):
        OccmBackend(_config()).query(cloud.model, cloud.mapping, _LIVE, "a1", {})


# --- DataSource ------------------------------------------------------------------


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_datasource_resolves_to_occm_and_gets_by_public_id(
    cloud: Cloud, client_cls: MagicMock, empty_cache: OccmCacheDB
) -> None:
    assert DataSource._resolve_mapping(cloud.model).api_type == "occm"
    op = getattr(client_cls.return_value.ops, cloud.op)
    op.return_value = [
        cloud.model.model_validate(_record(cloud, "pub-1")),
        cloud.model.model_validate(_record(cloud, "pub-2")),
    ]
    found = DataSource(_config()).get(cloud.model, cluster="c1", id="pub-2")
    assert found is not None
    assert found.model_dump()["publicId"] == "pub-2"


@pytest.mark.parametrize("cloud", CLOUDS, ids=_IDS)
def test_cache_source_round_trips_and_filters(
    cloud: Cloud, client_cls: MagicMock, empty_cache: OccmCacheDB
) -> None:
    group = "awsProperties" if cloud.aws else "providerProperties"
    other = _record(cloud, "p2")
    other[group]["regionName"] = "other-region-placeholder"
    empty_cache.set(
        OccmSnapshot(
            cached_at=datetime.now(UTC),
            inventory=ConsoleInventory(),
            agents=(
                OccmAgentSnapshot(
                    agent_id="agent-1",
                    scope=None,
                    organization_id=None,
                    cached_at=datetime.now(UTC),
                    records={
                        cloud.name: [
                            cloud.model.model_validate(r).model_dump(mode="json")
                            for r in (_record(cloud, "p1"), other)
                        ]
                    },
                ),
            ),
        )
    )
    ds = DataSource(_config())
    assert len(list(ds.query(cloud.model, cluster="c1", source="cache"))) == 2
    region = list(
        ds.query(cloud.model, cluster="c1", source="cache").filter(
            {f"{group}.regionName": "region-placeholder"}
        )
    )
    assert [r.model_dump()["publicId"] for r in region] == ["p1"]
    client_cls.assert_not_called()


# --- collector -------------------------------------------------------------------


def _inventory(*agent_ids: str) -> ConsoleInventory:
    return ConsoleInventory(
        accounts=[
            AccountInventory(
                scope=None,
                agents=[
                    ConsoleAgentInfo(agentId=a, scope=None, organization_id="org-1", status=None)
                    for a in agent_ids
                ],
            )
        ]
    )


def _discovery(*agent_ids: str) -> MagicMock:
    discovery = MagicMock()
    discovery.discover.return_value = _inventory(*agent_ids)
    return discovery


def _factory(
    items: dict[str, list[dict[str, Any]]] | None = None,
    raising: dict[str, Exception] | None = None,
) -> MagicMock:
    """Client factory: each op returns the ``items`` of its name, or raises."""
    items = items or {}
    raising = raising or {}

    def build(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
        client = MagicMock(name=f"client-{agent_id}")
        for cloud in CLOUDS:
            op = getattr(client.ops, cloud.op)
            if cloud.op in raising:
                op.side_effect = raising[cloud.op]
            else:
                op.return_value = [cloud.model.model_validate(r) for r in items.get(cloud.op, [])]
        client.ops.list_onprem_working_environments.return_value = []
        return client

    return MagicMock(side_effect=build)


def _validation_error() -> ValidationError:
    try:
        _AZURE_HA.model.model_validate({"isHA": "not-a-bool"})
    except ValidationError as exc:
        return exc
    raise AssertionError("expected a ValidationError")


def test_collect_calls_all_seven_ops_with_fields_star() -> None:
    factory = _factory({c.op: [_record(c, f"id-{c.op}")] for c in CLOUDS})
    snapshot = OccmCollector(
        MagicMock(), discovery=_discovery("a1"), agent_client_factory=factory
    ).collect()
    (agent,) = snapshot.agents
    for cloud in CLOUDS:
        assert [r["publicId"] for r in agent.records[cloud.name]] == [f"id-{cloud.op}"]
    assert agent.records["OccmOnpremWorkingEnvironment"] == []
    assert set(agent.records) == set(OCCM_WORKING_ENVIRONMENT_MAPPINGS)
    assert snapshot.failed_mappings == ()


def test_each_op_is_called_with_fields_star() -> None:
    created: list[MagicMock] = []
    base = _factory()

    def build(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
        client: MagicMock = base.side_effect(config, agent_id, **kwargs)
        created.append(client)
        return client

    OccmCollector(
        MagicMock(), discovery=_discovery("a1"), agent_client_factory=MagicMock(side_effect=build)
    ).collect()
    for op_name in OCCM_LIST_OPS.values():
        getattr(created[0].ops, op_name).assert_called_once_with(fields="*")


@pytest.mark.parametrize(
    "error",
    [_validation_error(), ValueError("bad"), TypeError("bad")],
    ids=lambda e: type(e).__name__,
)
def test_one_failing_mapping_is_recorded_and_the_rest_collected(error: Exception) -> None:
    cloud = _AZURE_HA
    factory = _factory(
        {"list_aws_ha_working_environments": [_record(CLOUDS[1], "p-aws")]},
        raising={cloud.op: error},
    )
    snapshot = OccmCollector(
        MagicMock(), discovery=_discovery("a1"), agent_client_factory=factory
    ).collect()
    assert snapshot.failed_agents == ()
    assert snapshot.failed_mappings == (("a1", cloud.name),)
    (agent,) = snapshot.agents
    assert cloud.name not in agent.records
    assert [r["publicId"] for r in agent.records["OccmAwsHaWorkingEnvironment"]] == ["p-aws"]


def test_transport_error_fails_the_agent() -> None:
    factory = _factory(raising={_AZURE_HA.op: requests.ConnectionError("down")})
    snapshot = OccmCollector(
        MagicMock(), discovery=_discovery("a1"), agent_client_factory=factory
    ).collect()
    assert snapshot.failed_agents == ("a1",)
    assert snapshot.failed_mappings == ()
    assert snapshot.agents == ()


def test_every_mapping_failing_fails_the_agent() -> None:
    factory = _factory(raising={op: ValueError("bad") for op in OCCM_LIST_OPS.values()})
    base_factory = factory.side_effect

    def build(config: Any, agent_id: str, **kwargs: Any) -> MagicMock:
        client: MagicMock = base_factory(config, agent_id, **kwargs)
        client.ops.list_onprem_working_environments.side_effect = ValueError("bad")
        return client

    snapshot = OccmCollector(
        MagicMock(), discovery=_discovery("a1"), agent_client_factory=MagicMock(side_effect=build)
    ).collect()
    assert snapshot.failed_agents == ("a1",)
    assert snapshot.failed_mappings == ()
    assert snapshot.agents == ()


def test_failed_mapping_keeps_earlier_rows_and_cached_at(tmp_path: Path) -> None:
    cloud = _AZURE_HA
    good = _factory({cloud.op: [_record(cloud, "p-azure")]})
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        refresh_occm_cache(
            MagicMock(), db=db, discovery=_discovery("a1"), agent_client_factory=good
        )
        first = db.conn.execute(
            "SELECT cached_at FROM occm_collections WHERE agent_id = ? AND mapping = ?",
            ("a1", cloud.name),
        ).fetchone()["cached_at"]
        assert db.agents_for_working_environment("p-azure") == ["a1"]

        bad = _factory(raising={cloud.op: ValueError("bad")})
        snapshot = refresh_occm_cache(
            MagicMock(), db=db, discovery=_discovery("a1"), agent_client_factory=bad
        )
        assert snapshot.failed_mappings == (("a1", cloud.name),)
        second = db.conn.execute(
            "SELECT cached_at FROM occm_collections WHERE agent_id = ? AND mapping = ?",
            ("a1", cloud.name),
        ).fetchone()["cached_at"]
        assert second == first
        assert db.agents_for_working_environment("p-azure") == ["a1"]


# --- database --------------------------------------------------------------------


def _agent(agent_id: str, records: dict[str, list[dict[str, Any]]]) -> OccmAgentSnapshot:
    return OccmAgentSnapshot(
        agent_id=agent_id,
        scope=None,
        organization_id=None,
        cached_at=datetime.now(UTC),
        records=records,
    )


def test_cloud_working_environments_map_to_agents(tmp_path: Path) -> None:
    with OccmCacheDB(db_path=tmp_path / "occm_cache.db") as db:
        db.set(
            OccmSnapshot(
                cached_at=datetime.now(UTC),
                inventory=ConsoleInventory(),
                agents=(
                    _agent(
                        "a1",
                        {
                            "OccmOnpremWorkingEnvironment": [{"publicId": "p-onprem", "name": "n"}],
                            "OccmAzureHaWorkingEnvironment": [
                                {"publicId": "p-azure", "name": "n"},
                                {"publicId": "p-azure", "name": "n"},
                            ],
                        },
                    ),
                    _agent("a2", {"OccmAwsHaWorkingEnvironment": [{"publicId": "p-azure"}]}),
                ),
            )
        )
        assert db.agents_for_working_environment("p-azure") == ["a1", "a2"]
        assert db.agents_for_working_environment("p-onprem") == ["a1"]
        assert db.working_environment_agents() == {
            "p-azure": ["a1", "a2"],
            "p-onprem": ["a1"],
        }
