"""Map one OCCM AWS working environment record to ``CloudMetadata`` (#1086, ADR-0033).

The reports read AWS cloud details from the OCCM cache first.  This module is the cache-layer
adapter: pure functions from one working environment record (the dict of
``OccmData.record.model_dump()``, camelCase keys) to one :class:`CloudMetadata` per ONTAP node.
It reads no database and imports nothing from ``pynetappfoundry.data`` or
``pynetappfoundry.clients``, so it cannot make a live call.

Every field-to-path mapping lives in one table, :data:`CLOUD_METADATA_SOURCES`: a measurement
result changes that table only (the :data:`LINK_RULES` pattern of ``cluster_resolver``).  Path
syntax: dotted record keys; ``name[]`` selects the element of that list the adapter joined to the
ONTAP node (``ontapClusterProperties.nodes``, ``awsProperties.instances``).

The adapter answers a cluster completely or not at all: it returns ``None`` when any ONTAP node
cannot be joined to the record, or the account, region or an instance id is missing, and the caller
then uses the CLI-parsed metadata for the whole cluster.

Only AWS is answered.  Measured: Azure Console records never carry the VM instance id (the node
``cloudProviderId`` and the HA ``instanceId`` are empty) nor the offer and sku (the product code
and platform license fields are empty while the CLI has them), so an Azure cluster could never be
answered completely.  Azure, GCP and on-prem always use the CLI path.

The System Manager link (#1105) is not a cloud field: :func:`system_manager_link` reads
``ontapClusterProperties.systemManagerUrl`` of any single record, whatever its mapping.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal
from urllib.parse import urlsplit

from pynetappfoundry.utils.cloud import (
    build_aws_instance_link,
    build_cloud_instance_sso_link,
    build_vm_name,
)
from pynetappfoundry.utils.console_links import (
    build_console_aggregates_link,
    build_console_volumes_link,
    build_console_working_environment_link,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from pynetappfoundry.cache.cluster_resolver import OccmData, OccmLocation
    from pynetappfoundry.models.ontap.cloud.metadata.model import CloudMetadata

_NODES = "ontapClusterProperties.nodes"
_INSTANCES = "awsProperties.instances"
# Measured: ``clusterProperties.systemManagerUrl`` is always empty, so it is never used.
SYSTEM_MANAGER_URL_PATH = "ontapClusterProperties.systemManagerUrl"


@dataclass(frozen=True)
class CloudFieldSource:
    """Where one ``CloudMetadata`` field comes from in an OCCM working environment record.

    Attributes:
        aws: Paths tried in order; the first non-empty value wins.  Empty means the OCCM
            record does not carry the field (a gap: the field stays ``""``).
        scope: ``"we"`` for a working environment level value, ``"node"`` for a per-node value.
        note: Why the field has no path, or how it is derived.
    """

    aws: tuple[str, ...] = ()
    scope: Literal["we", "node"] = "we"
    note: str = ""


#: One row per ``CloudMetadata`` data field (the computed ``node``, ``vm_name`` and link fields
#: are not in the table).  The documented mapping of ``docs/usage/report-cloud-details.md``.
CLOUD_METADATA_SOURCES: Mapping[str, CloudFieldSource] = {
    "instance_id": CloudFieldSource(aws=(f"{_NODES}[].cloudProviderId",), scope="node"),
    "account_id": CloudFieldSource(aws=("awsProperties.accountId",)),
    "image_id": CloudFieldSource(aws=(f"{_INSTANCES}[].imageId",), scope="node"),
    "instance_type": CloudFieldSource(aws=(f"{_INSTANCES}[].instanceType",), scope="node"),
    "cpu_platform": CloudFieldSource(note="gap: no OCCM field"),
    "region": CloudFieldSource(aws=("awsProperties.regionName",)),
    "provider": CloudFieldSource(
        note='derived from CLOUD_MAPPING_PROVIDER ("AWS"); cloudProviderName is spelled '
        'differently from the CLI value, which is exactly "AWS"'
    ),
    "consumer": CloudFieldSource(note="gap: no OCCM field"),
    "primary_ip": CloudFieldSource(aws=(f"{_INSTANCES}[].privateIpAddress",), scope="node"),
    "metadata_version": CloudFieldSource(note="gap: no OCCM field"),
    "availability_zone": CloudFieldSource(aws=(f"{_INSTANCES}[].availabilityZone",), scope="node"),
    "availability_zone_id": CloudFieldSource(note="gap: no OCCM field"),
    "fault_domain": CloudFieldSource(note="not applicable: Azure only"),
    "update_domain": CloudFieldSource(note="not applicable: Azure only"),
    "resource_group_name": CloudFieldSource(note="not applicable: Azure only"),
    "offer": CloudFieldSource(note="gap: empty in both OCCM and the CLI for AWS (measured)"),
    "sku": CloudFieldSource(note="gap: empty in both OCCM and the CLI for AWS (measured)"),
    "sku_version": CloudFieldSource(note="gap: no OCCM field"),
}

#: The mappings the adapter answers, with the provider name ``CloudMetadata.provider`` carries.
#: Azure and GCP have no entry and always use the CLI path (Azure: measured, the Console record
#: has no VM instance id, offer or sku; GCP: unmeasured).
CLOUD_MAPPING_PROVIDER: Mapping[str, str] = {
    "OccmAwsWorkingEnvironment": "AWS",
    "OccmAwsHaWorkingEnvironment": "AWS",
}


def _lookup(
    record: Mapping[str, Any],
    path: str,
    elements: Mapping[str, Mapping[str, Any]],
) -> Any:
    """Return the value at *path* of *record*, or ``None`` when any step is absent."""
    current: Any = record
    walked: list[str] = []
    for segment in path.split("."):
        is_list = segment.endswith("[]")
        name = segment[:-2] if is_list else segment
        if not isinstance(current, dict):
            return None
        current = current.get(name)
        walked.append(name)
        if is_list:
            current = elements.get(".".join(walked))
    return current


def _text(value: Any) -> str:
    """Return *value* as a string; ``None`` and non-scalar values are ``""``."""
    if isinstance(value, str):
        return value
    if isinstance(value, bool | int | float):
        return str(value)
    return ""


def _fields(
    record: Mapping[str, Any],
    elements: Mapping[str, Mapping[str, Any]],
) -> dict[str, str]:
    """Return every table field for one node: the first non-empty value of its paths."""
    values: dict[str, str] = {}
    for name, source in CLOUD_METADATA_SOURCES.items():
        value = ""
        for path in source.aws:
            value = _text(_lookup(record, path, elements))
            if value:
                break
        values[name] = value
    return values


def _named_node(record: Mapping[str, Any], name: str) -> Mapping[str, Any] | None:
    """Return the ``ontapClusterProperties.nodes`` entry called *name*, else ``None``."""
    nodes = _lookup(record, _NODES, {})
    if not isinstance(nodes, list):
        return None
    for node in nodes:
        if isinstance(node, dict) and node.get("name") == name:
            return node
    return None


def _vsa_instance(record: Mapping[str, Any], instance_id: str) -> Mapping[str, Any] | None:
    """Return the AWS VSA instance with *instance_id* (never the mediator or the agent)."""
    instances = _lookup(record, _INSTANCES, {})
    if not isinstance(instances, list) or not instance_id:
        return None
    for instance in instances:
        if (
            isinstance(instance, dict)
            and instance.get("id") == instance_id
            and instance.get("isVsaInstance") is True
        ):
            return instance
    return None


def occm_cloud_metadata(
    record: Mapping[str, Any],
    mapping: str,
    *,
    ontap_node_names: Sequence[str],
    aws_sso_config: dict[str, str | dict[str, str]] | None = None,
) -> list[CloudMetadata] | None:
    """Return one :class:`CloudMetadata` per ONTAP node from an OCCM record, or ``None``.

    ``None`` means OCCM cannot answer this cluster completely: an unsupported mapping (Azure,
    GCP, on-prem), no ONTAP nodes, a missing account or region, or an ONTAP node with no joined
    record or no instance id.  Gap fields (``CLOUD_METADATA_SOURCES`` rows without a path) are
    ``""``.

    Args:
        record: ``OccmData.record.model_dump()`` of the working environment.
        mapping: The working-environment mapping name of the record.
        ontap_node_names: The ONTAP node names, in report order.
        aws_sso_config: Optional AWS SSO settings for ``instance_sso_link``.
    """
    provider = CLOUD_MAPPING_PROVIDER.get(mapping)
    if provider is None or not ontap_node_names:
        return None
    # Imported here so ``nf --help`` loads no ``models.ontap`` module (#960).
    from pynetappfoundry.models.ontap.cloud.metadata.model import (
        CloudMetadata,
    )

    result: list[CloudMetadata] = []
    for node_name in ontap_node_names:
        ontap_node = _named_node(record, node_name)
        if ontap_node is None:
            return None
        instance = _vsa_instance(record, _text(ontap_node.get("cloudProviderId")))
        if instance is None:
            return None
        values = _fields(record, {_NODES: ontap_node, _INSTANCES: instance})
        if not values["account_id"] or not values["region"] or not values["instance_id"]:
            return None
        values["provider"] = provider
        values["node"] = node_name
        _apply_links(values, aws_sso_config)
        result.append(CloudMetadata(**values))
    return result


def _apply_links(
    values: dict[str, str],
    aws_sso_config: dict[str, str | dict[str, str]] | None,
) -> None:
    """Add ``vm_name`` and the link fields to *values* in place (``utils.cloud`` builders)."""
    instance_id = values["instance_id"]
    values["vm_name"] = build_vm_name("aws", instance_id=instance_id)
    values["instance_link"] = build_aws_instance_link(values["region"], instance_id)
    values["instance_sso_link"] = build_cloud_instance_sso_link(
        "AWS", values["instance_link"], values["account_id"], aws_sso_config
    )


def pick_occm_data(occm: Sequence[OccmData]) -> OccmData | None:
    """Return the one OCCM record to use for a cluster, or ``None`` when there is none to use.

    Several distinct working environment ``publicId`` values are ambiguous: ``None``.  One
    ``publicId`` under several agents gives one record: a UUID match before a name match, then a
    non-stale agent, then the lowest agent id.
    """
    if len({d.location.public_id for d in occm}) != 1:
        return None
    return min(
        occm,
        key=lambda d: (d.location.matched_by != "uuid", d.is_stale, d.location.agent_id),
    )


def system_manager_link(record: Mapping[str, Any]) -> str:
    """Return the System Manager URL of *record*, or ``""`` when absent or unsafe.

    The value is used only when it is a ``str`` with an ``http`` or ``https`` scheme, a host, and
    no whitespace or control characters; it is never rewritten.  The scheme check blocks
    ``javascript:`` and ``data:`` hrefs.
    """
    value = _lookup(record, SYSTEM_MANAGER_URL_PATH, {})
    if not isinstance(value, str) or not value:
        return ""
    if any(ch.isspace() or not ch.isprintable() for ch in value):
        return ""
    try:
        parts = urlsplit(value)
        hostname = parts.hostname
    except ValueError:
        return ""
    if parts.scheme not in {"http", "https"} or not hostname:
        return ""
    return value


@dataclass(frozen=True)
class ConsoleWorkingEnvironmentLinks:
    """The NetApp Console links and agent context of one working environment.

    Computed, not cached (ADR-0033): ``""`` means no link.

    Attributes:
        public_id: The working environment ``publicId``.
        agent_id: The Console agent id.
        agent_name: The agent name, or ``None``.
        scopes: The Console account scopes the agent was discovered in (``None`` is the root).
        working_environment: Link to the working environment page.
        volumes: Link to its Volumes tab.
        aggregates: Link to its Aggregates view; CVO only.
        system_manager: The System Manager URL from the record
            (``ontapClusterProperties.systemManagerUrl``), or ``""`` when absent or unsafe.
    """

    public_id: str
    agent_id: str
    agent_name: str | None
    scopes: tuple[str | None, ...]
    working_environment: str
    volumes: str
    aggregates: str
    system_manager: str = ""


def console_links(
    location: OccmLocation,
    *,
    base_url: str,
    record: Mapping[str, Any] | None = None,
) -> ConsoleWorkingEnvironmentLinks:
    """Return the Console links of *location*; a builder that rejects the id gives ``""``.

    *record* (the dumped working environment record) supplies the System Manager link.
    """
    public_id = location.public_id
    try:
        working_environment = build_console_working_environment_link(public_id, base_url=base_url)
        volumes = build_console_volumes_link(public_id, base_url=base_url)
    except ValueError:
        working_environment = volumes = ""
    try:
        aggregates = build_console_aggregates_link(public_id, base_url=base_url)
    except ValueError:
        aggregates = ""
    return ConsoleWorkingEnvironmentLinks(
        public_id=public_id,
        agent_id=location.agent_id,
        agent_name=location.agent_name,
        scopes=location.scopes,
        working_environment=working_environment,
        volumes=volumes,
        aggregates=aggregates,
        system_manager=system_manager_link(record) if record is not None else "",
    )
