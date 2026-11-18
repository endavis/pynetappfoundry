"""Tests for the OCCM cloud working environment to ``CloudMetadata`` adapter (#1086, ADR-0033)."""

from __future__ import annotations

import ast
import json
import types
import typing
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import pytest
from pydantic import BaseModel

import pynetappfoundry.cache.occm_cloud_metadata as adapter_module
from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster_resolver import OccmData, OccmLocation
from pynetappfoundry.cache.occm_cloud_metadata import (
    CLOUD_MAPPING_PROVIDER,
    CLOUD_METADATA_SOURCES,
    console_links,
    occm_cloud_metadata,
    pick_occm_data,
)
from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata
from pynetappfoundry.utils.cloud import get_node_number

AWS_HA = "OccmAwsHaWorkingEnvironment"
AWS = "OccmAwsWorkingEnvironment"
AZURE_HA = "OccmAzureHaWorkingEnvironment"
AZURE = "OccmAzureWorkingEnvironment"
CVO_ID = "VsaWorkingEnvironment-AAAA"
ONPREM_ID = "OnPremWorkingEnvironment-BBBB"

_FIXTURE = (
    Path(__file__).resolve().parents[2]
    / "fixtures"
    / "console_models"
    / "cvo_working_environment_shapes.json"
)
_LISTS: dict[str, dict[str, Any]] = json.loads(_FIXTURE.read_text(encoding="utf-8"))["lists"]
_FIXTURE_KEY = {AWS_HA: "aws-ha", AZURE_HA: "azure-ha", AZURE: "azure-vsa"}


def _aws_record(*, ha: bool = True) -> dict[str, Any]:
    instances = [
        {
            "id": "i-node1",
            "isVsaInstance": True,
            "isOCCMInstance": False,
            "instanceType": "m5.xlarge",
            "imageId": "ami-1",
            "privateIpAddress": "192.0.2.1",
            "availabilityZone": "us-east-1a",
        },
        {
            "id": "i-node2",
            "isVsaInstance": True,
            "isOCCMInstance": False,
            "instanceType": "m5.2xlarge",
            "imageId": "ami-2",
            "privateIpAddress": "192.0.2.2",
            "availabilityZone": "us-east-1b",
        },
        {"id": "i-mediator", "isVsaInstance": False, "isOCCMInstance": False},
        {"id": "i-agent", "isVsaInstance": False, "isOCCMInstance": True},
    ]
    nodes = [{"name": "lab1-01", "cloudProviderId": "i-node1"}]
    if ha:
        nodes.append({"name": "lab1-02", "cloudProviderId": "i-node2"})
    return {
        "isHA": ha,
        "publicId": CVO_ID,
        "awsProperties": {
            "accountId": "111122223333",
            "regionName": "us-east-1",
            "instances": instances,
        },
        "ontapClusterProperties": {"nodes": nodes},
        "clusterProperties": {"instanceType": "m5.xlarge"},
    }


def _azure_record(*, ha: bool = True) -> dict[str, Any]:
    def info(n: int) -> dict[str, Any]:
        return {
            "instanceName": f"vm-{n}",
            "primaryIp": f"192.0.2.{n}",
            "availabilitySet": {"faultDomain": n, "updateDomain": n + 10},
            "availabilityZone": None,
        }

    nodes = [{"name": "lab1-01", "cloudProviderId": "az-id-1"}]
    if ha:
        nodes.append({"name": "lab1-02", "cloudProviderId": "az-id-2"})
    return {
        "isHA": ha,
        "publicId": CVO_ID,
        "providerProperties": {
            "subscriptionId": "sub-1",
            "regionName": "eastus",
            "instanceType": "Standard_DS4",
            "resourceGroup": {"name": "rg-1", "location": "eastus"},
        },
        "clusterProperties": {"instanceType": "Standard_DS3"},
        "haProperties": {"node1Info": info(1), "node2Info": info(2)},
        "ontapClusterProperties": {"nodes": nodes},
    }


def _run(
    record: dict[str, Any],
    mapping: str,
    names: list[str] | None = None,
    sso: dict[str, str | dict[str, str]] | None = None,
) -> list[CloudMetadata] | None:
    return occm_cloud_metadata(
        record,
        mapping,
        cluster_name="lab1",
        ontap_node_names=names if names is not None else ["lab1-01", "lab1-02"],
        aws_sso_config=sso,
    )


class TestAws:
    def test_ha_nodes_join_instances_and_skip_mediator(self) -> None:
        result = _run(_aws_record(), AWS_HA)
        assert result is not None
        assert [m.node for m in result] == ["lab1-01", "lab1-02"]
        first, second = result
        assert (first.instance_id, first.instance_type) == ("i-node1", "m5.xlarge")
        assert (second.instance_id, second.instance_type) == ("i-node2", "m5.2xlarge")
        assert first.image_id == "ami-1"
        assert first.primary_ip == "192.0.2.1"
        assert first.availability_zone == "us-east-1a"
        assert {m.account_id for m in result} == {"111122223333"}
        assert {m.region for m in result} == {"us-east-1"}
        assert {m.provider for m in result} == {"AWS"}
        assert first.vm_name == "i-node1"
        assert "i-node1" in first.instance_link
        assert urlparse(first.instance_link).hostname == "us-east-1.console.aws.amazon.com"

    def test_sso_link_needs_config(self) -> None:
        sso: dict[str, str | dict[str, str]] = {
            "subdomain": "corp",
            "account_roles": {"111122223333": "Admin"},
        }
        with_sso = _run(_aws_record(), AWS_HA, sso=sso)
        without = _run(_aws_record(), AWS_HA)
        assert with_sso is not None
        assert without is not None
        assert urlparse(with_sso[0].instance_sso_link).hostname == "corp.awsapps.com"
        assert without[0].instance_sso_link == ""

    def test_single_node_uses_aws_rows(self) -> None:
        result = _run(_aws_record(ha=False), AWS, ["lab1-01"])
        assert result is not None
        assert [m.instance_id for m in result] == ["i-node1"]

    def test_unmatched_node_returns_none(self) -> None:
        assert _run(_aws_record(), AWS_HA, ["lab1-01", "lab1-09"]) is None

    def test_non_vsa_instance_never_joins(self) -> None:
        record = _aws_record()
        record["ontapClusterProperties"]["nodes"][1]["cloudProviderId"] = "i-mediator"
        assert _run(record, AWS_HA) is None
        record["ontapClusterProperties"]["nodes"][1]["cloudProviderId"] = "i-agent"
        assert _run(record, AWS_HA) is None

    def test_gap_fields_are_empty(self) -> None:
        result = _run(_aws_record(), AWS_HA)
        assert result is not None
        first = result[0]
        for gap in (
            "cpu_platform",
            "consumer",
            "availability_zone_id",
            "sku_version",
            "metadata_version",
            "fault_domain",
            "update_domain",
            "offer",
            "sku",
            "resource_group_name",
            "resource_group_link",
        ):
            assert getattr(first, gap) == "", gap


class TestAzure:
    def test_ha_nodes_use_node_info_by_number(self) -> None:
        result = _run(_azure_record(), AZURE_HA)
        assert result is not None
        first, second = result
        assert (first.vm_name, second.vm_name) == ("vm-1", "vm-2")
        assert (first.instance_id, second.instance_id) == ("az-id-1", "az-id-2")
        assert (first.primary_ip, second.primary_ip) == ("192.0.2.1", "192.0.2.2")
        assert (first.fault_domain, second.fault_domain) == ("1", "2")
        assert (first.update_domain, second.update_domain) == ("11", "12")
        assert first.provider == "Azure"
        assert first.account_id == "sub-1"
        assert first.region == "eastus"
        assert first.resource_group_name == "rg-1"
        assert first.instance_type == "Standard_DS4"
        assert first.instance_link.endswith(
            "/rg-1/providers/Microsoft.Compute/virtualMachines/vm-1"
        )
        assert first.resource_group_link.endswith("/subscriptions/sub-1/resourceGroups/rg-1")
        assert first.availability_zone == ""

    def test_null_provider_instance_type_falls_to_cluster_properties(self) -> None:
        record = _azure_record()
        record["providerProperties"]["instanceType"] = None
        result = _run(record, AZURE_HA)
        assert result is not None
        assert result[0].instance_type == "Standard_DS3"

    def test_null_instance_type_everywhere_stays_empty_and_answers(self) -> None:
        record = _azure_record()
        record["providerProperties"]["instanceType"] = None
        record["clusterProperties"]["instanceType"] = None
        result = _run(record, AZURE_HA)
        assert result is not None
        assert result[0].instance_type == ""

    def test_single_node_uses_node1_only(self) -> None:
        result = _run(_azure_record(ha=False), AZURE, ["lab1-01"])
        assert result is not None
        assert len(result) == 1
        assert result[0].vm_name == "vm-1"
        assert result[0].primary_ip == "192.0.2.1"

    def test_ha_node_without_number_returns_none(self) -> None:
        assert _run(_azure_record(), AZURE_HA, ["lab1-a", "lab1-b"]) is None

    def test_empty_instance_name_falls_back_to_derived_vm_name(self) -> None:
        record = _azure_record()
        record["haProperties"]["node2Info"]["instanceName"] = ""
        result = _run(record, AZURE_HA)
        assert result is not None
        assert result[1].vm_name == "lab1-vm2"
        assert result[0].vm_name == "vm-1"

    def test_missing_resource_group_gives_no_links(self) -> None:
        record = _azure_record()
        record["providerProperties"]["resourceGroup"] = None
        result = _run(record, AZURE_HA)
        assert result is not None
        assert result[0].resource_group_name == ""
        assert result[0].instance_link == ""
        assert result[0].resource_group_link == ""


class TestIncomplete:
    @pytest.mark.parametrize(
        ("record", "mapping", "path"),
        [
            (_aws_record(), AWS_HA, ("awsProperties", "accountId")),
            (_aws_record(), AWS_HA, ("awsProperties", "regionName")),
            (_azure_record(), AZURE_HA, ("providerProperties", "subscriptionId")),
            (_azure_record(), AZURE_HA, ("providerProperties", "regionName")),
        ],
    )
    def test_missing_account_or_region(
        self, record: dict[str, Any], mapping: str, path: tuple[str, str]
    ) -> None:
        record[path[0]][path[1]] = ""
        assert _run(record, mapping) is None

    def test_azure_empty_instance_id(self) -> None:
        record = _azure_record()
        record["ontapClusterProperties"]["nodes"][0]["cloudProviderId"] = ""
        assert _run(record, AZURE_HA) is None

    def test_ontap_node_absent_from_record(self) -> None:
        assert _run(_azure_record(), AZURE_HA, ["lab1-01", "lab1-03"]) is None

    @pytest.mark.parametrize(
        "mapping",
        [
            "OccmGcpWorkingEnvironment",
            "OccmGcpHaWorkingEnvironment",
            "OccmOnpremWorkingEnvironment",
        ],
    )
    def test_unsupported_mappings(self, mapping: str) -> None:
        assert _run(_aws_record(), mapping) is None

    def test_no_ontap_nodes(self) -> None:
        assert _run(_aws_record(), AWS_HA, []) is None


def _field_models(annotation: Any) -> list[type[BaseModel]]:
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return [annotation]
    if typing.get_origin(annotation) in (typing.Union, types.UnionType, list):
        return [m for arg in typing.get_args(annotation) for m in _field_models(arg)]
    return []


def _resolves(model: type[BaseModel], parts: list[str]) -> bool:
    field = model.model_fields.get(parts[0])
    if field is None:
        return False
    if len(parts) == 1:
        return True
    return any(_resolves(m, parts[1:]) for m in _field_models(field.annotation))


def _concrete_paths() -> list[tuple[str, str, str]]:
    """Return ``(field, mapping, concrete path)`` for every table path of the measured types."""
    rows: list[tuple[str, str, str]] = []
    for field, source in CLOUD_METADATA_SOURCES.items():
        for mapping, paths in ((AWS_HA, source.aws), (AZURE_HA, source.azure)):
            for path in paths:
                rows.append((field, mapping, path))
    return rows


@pytest.mark.parametrize(("field", "mapping", "path"), _concrete_paths())
def test_table_paths_resolve_against_the_models(field: str, mapping: str, path: str) -> None:
    models = [mapping] + ([AWS] if mapping == AWS_HA else [AZURE])
    for name in models:
        mp = model_registry.get_mapping(name)
        assert mp is not None
        for n in (1, 2):
            concrete = path.replace("{N}", str(n)).replace("[]", "")
            assert _resolves(mp.model_class, concrete.split(".")), (field, name, concrete)


@pytest.mark.parametrize(("field", "mapping", "path"), _concrete_paths())
def test_table_paths_appear_in_the_measured_shapes(field: str, mapping: str, path: str) -> None:
    keys = [_FIXTURE_KEY[mapping]] + (["azure-vsa"] if mapping == AZURE_HA else [])
    for key in keys:
        paths = _LISTS[key]["paths"]
        for n in (1, 2):
            concrete = path.replace("{N}", str(n))
            assert concrete in paths, (field, key, concrete)


def test_table_has_one_row_per_data_field() -> None:
    computed = {
        "node",
        "instance_link",
        "instance_sso_link",
        "resource_group_link",
        "vm_name",
    }
    assert set(CLOUD_METADATA_SOURCES) == set(CloudMetadata.model_fields) - computed


def test_table_scope_matches_path_markers() -> None:
    for field, source in CLOUD_METADATA_SOURCES.items():
        marked = any("[]" in p or "{N}" in p for p in (*source.aws, *source.azure))
        assert (source.scope == "node") == marked, field


def test_provider_mapping_covers_aws_and_azure_only() -> None:
    assert set(CLOUD_MAPPING_PROVIDER.values()) == {"AWS", "Azure"}
    assert all("Gcp" not in m and "Onprem" not in m for m in CLOUD_MAPPING_PROVIDER)


def test_get_node_number_agrees_with_node_info_slots() -> None:
    assert get_node_number("lab1-01") == 1
    assert get_node_number("lab1-02") == 2


class _Empty(BaseModel):
    pass


def _data(
    public_id: str = CVO_ID,
    agent: str = "agent-a",
    matched_by: typing.Literal["uuid", "name"] = "uuid",
    stale: bool = False,
    mapping: str = AWS_HA,
) -> OccmData:
    loc = OccmLocation(agent, f"name-{agent}", (None, "org1"), mapping, public_id, matched_by)
    return OccmData(cached_at=datetime.now(UTC), is_stale=stale, location=loc, record=_Empty())


class TestPickOccmData:
    def test_empty_is_none(self) -> None:
        assert pick_occm_data([]) is None

    def test_two_public_ids_is_none(self) -> None:
        assert pick_occm_data([_data(CVO_ID), _data(ONPREM_ID)]) is None

    def test_uuid_beats_name(self) -> None:
        picked = pick_occm_data([_data(agent="a", matched_by="name"), _data(agent="b")])
        assert picked is not None
        assert picked.location.agent_id == "b"

    def test_non_stale_beats_stale(self) -> None:
        picked = pick_occm_data([_data(agent="a", stale=True), _data(agent="b")])
        assert picked is not None
        assert picked.location.agent_id == "b"

    def test_same_public_id_under_two_agents_gives_the_first_agent(self) -> None:
        picked = pick_occm_data([_data(agent="b"), _data(agent="a")])
        assert picked is not None
        assert picked.location.agent_id == "a"


class TestConsoleLinks:
    def test_cvo_has_three_links(self) -> None:
        links = console_links(_data().location, base_url="https://ui.example.test/")
        assert (
            links.working_environment
            == f"https://ui.example.test/storage/cloud-volumes-ontap/{CVO_ID}"
        )
        assert links.volumes == f"{links.working_environment}/volumes"
        assert links.aggregates == f"{links.working_environment}/aggregates"
        assert (links.agent_id, links.agent_name, links.scopes) == (
            "agent-a",
            "name-agent-a",
            (None, "org1"),
        )

    def test_on_prem_has_no_aggregates(self) -> None:
        links = console_links(_data(ONPREM_ID).location, base_url="https://ui.example.test")
        assert links.working_environment
        assert links.volumes
        assert links.aggregates == ""

    def test_unknown_prefix_is_all_empty(self) -> None:
        links = console_links(_data("Other-1").location, base_url="https://ui.example.test")
        assert (links.working_environment, links.volumes, links.aggregates) == ("", "", "")


def test_module_imports_no_data_or_client_layer() -> None:
    tree = ast.parse(Path(adapter_module.__file__ or "").read_text(encoding="utf-8"))
    imported = [n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)] + [
        a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names
    ]
    assert not [
        m for m in imported if m.startswith(("pynetappfoundry.data", "pynetappfoundry.clients"))
    ]


def test_usage_page_table_equals_the_path_table() -> None:
    """The documented mapping is ``CLOUD_METADATA_SOURCES`` (docs/usage/report-cloud-details.md)."""
    page = Path(__file__).resolve().parents[3] / "docs" / "usage" / "report-cloud-details.md"
    rows: dict[str, tuple[list[str], list[str], str]] = {}
    for line in page.read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 5 and cells[0].startswith("`") and cells[0].endswith("`"):

            def paths(cell: str) -> list[str]:
                return [p.strip("` ") for p in cell.split(", ") if p]

            rows[cells[0].strip("`")] = (paths(cells[1]), paths(cells[2]), cells[3])
    assert set(rows) == set(CLOUD_METADATA_SOURCES)
    for name, source in CLOUD_METADATA_SOURCES.items():
        assert rows[name] == (list(source.aws), list(source.azure), source.scope), name
