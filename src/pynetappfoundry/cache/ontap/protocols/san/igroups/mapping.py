# ruff: noqa: E501
"""OntapIgroup type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.san.igroups.model import (
    OntapIgroup,
    OntapIgroupConnectivityTrackingRequiredNode,
    OntapIgroupIgroup,
    OntapIgroupInitiator,
    OntapIgroupLunMap,
    OntapIgroupParentIgroup,
    OntapIgroupReplicationErrorSummaryArgument,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_connectivity_tracking_required_nodes(
    record: dict[str, Any],
) -> list[OntapIgroupConnectivityTrackingRequiredNode]:
    """Transform connectivity_tracking.required_nodes into OntapIgroupConnectivityTrackingRequiredNode list."""
    try:
        items = get_nested_value(record, "connectivity_tracking.required_nodes")
    except Exception:
        items = []
    return [OntapIgroupConnectivityTrackingRequiredNode(**item) for item in items]


def _transform_igroups(record: dict[str, Any]) -> list[OntapIgroupIgroup]:
    """Transform igroups into OntapIgroupIgroup list."""
    return [OntapIgroupIgroup(**item) for item in record.get("igroups", [])]


def _transform_initiators(record: dict[str, Any]) -> list[OntapIgroupInitiator]:
    """Transform initiators into OntapIgroupInitiator list."""
    return [OntapIgroupInitiator(**item) for item in record.get("initiators", [])]


def _transform_lun_maps(record: dict[str, Any]) -> list[OntapIgroupLunMap]:
    """Transform lun_maps into OntapIgroupLunMap list."""
    return [OntapIgroupLunMap(**item) for item in record.get("lun_maps", [])]


def _transform_parent_igroups(record: dict[str, Any]) -> list[OntapIgroupParentIgroup]:
    """Transform parent_igroups into OntapIgroupParentIgroup list."""
    return [OntapIgroupParentIgroup(**item) for item in record.get("parent_igroups", [])]


def _transform_replication_error_summary_arguments(
    record: dict[str, Any],
) -> list[OntapIgroupReplicationErrorSummaryArgument]:
    """Transform replication.error.summary.arguments into OntapIgroupReplicationErrorSummaryArgument list."""
    try:
        items = get_nested_value(record, "replication.error.summary.arguments")
    except Exception:
        items = []
    return [OntapIgroupReplicationErrorSummaryArgument(**item) for item in items]


ONTAPIGROUP_MAPPING = TypeMapping(
    name="OntapIgroup",
    model_class=OntapIgroup,
    api_endpoint="/protocols/san/igroups?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.alerts",
            api_path="connectivity_tracking.alerts",
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.connection_state",
            api_path="connectivity_tracking.connection_state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking.required_nodes",
            api_path="connectivity_tracking.required_nodes",
            transform=_transform_connectivity_tracking_required_nodes,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="delete_on_unmap",
            api_path="delete_on_unmap",
            default=False,
        ),
        FieldMapping(
            cache_attr="igroups",
            api_path="igroups",
            transform=_transform_igroups,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="initiators",
            api_path="initiators",
            transform=_transform_initiators,
            default=[],
        ),
        FieldMapping(
            cache_attr="lun_maps",
            api_path="lun_maps",
            transform=_transform_lun_maps,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="os_type",
            api_path="os_type",
        ),
        FieldMapping(
            cache_attr="parent_igroups",
            api_path="parent_igroups",
            transform=_transform_parent_igroups,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="portset.name",
            api_path="portset.name",
        ),
        FieldMapping(
            cache_attr="portset.uuid",
            api_path="portset.uuid",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="replication.error.igroup.local_svm",
            api_path="replication.error.igroup.local_svm",
            default=False,
        ),
        FieldMapping(
            cache_attr="replication.error.igroup.name",
            api_path="replication.error.igroup.name",
        ),
        FieldMapping(
            cache_attr="replication.error.igroup.uuid",
            api_path="replication.error.igroup.uuid",
        ),
        FieldMapping(
            cache_attr="replication.error.summary.arguments",
            api_path="replication.error.summary.arguments",
            transform=_transform_replication_error_summary_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="replication.error.summary.code",
            api_path="replication.error.summary.code",
        ),
        FieldMapping(
            cache_attr="replication.error.summary.message",
            api_path="replication.error.summary.message",
        ),
        FieldMapping(
            cache_attr="replication.peer_svm.name",
            api_path="replication.peer_svm.name",
        ),
        FieldMapping(
            cache_attr="replication.peer_svm.uuid",
            api_path="replication.peer_svm.uuid",
        ),
        FieldMapping(
            cache_attr="replication.state",
            api_path="replication.state",
        ),
        FieldMapping(
            cache_attr="supports_igroups",
            api_path="supports_igroups",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target.firmware_revision",
            api_path="target.firmware_revision",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="target.product_id",
            api_path="target.product_id",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="target.vendor_id",
            api_path="target.vendor_id",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIgroup", ONTAPIGROUP_MAPPING)
