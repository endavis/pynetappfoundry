"""OntapIgroup type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.san.igroups.model import (
    OntapIgroup,
    OntapIgroupAlert,
    OntapIgroupArgument,
    OntapIgroupIgroup,
    OntapIgroupInitiator,
    OntapIgroupLunMap,
    OntapIgroupParentIgroup,
    OntapIgroupRequiredNode,
)


def _transform_connectivity_tracking_alerts(record: dict[str, Any]) -> list[OntapIgroupAlert]:
    """Transform connectivity_tracking.alerts into OntapIgroupAlert list."""
    return [OntapIgroupAlert(**item) for item in record.get("connectivity_tracking.alerts", [])]


def _transform_connectivity_tracking_required_nodes(
    record: dict[str, Any],
) -> list[OntapIgroupRequiredNode]:
    """Transform connectivity_tracking.required_nodes into OntapIgroupRequiredNode list."""
    return [
        OntapIgroupRequiredNode(**item)
        for item in record.get("connectivity_tracking.required_nodes", [])
    ]


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
) -> list[OntapIgroupArgument]:
    """Transform replication.error.summary.arguments into OntapIgroupArgument list."""
    return [
        OntapIgroupArgument(**item)
        for item in record.get("replication.error.summary.arguments", [])
    ]


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
            cache_attr="connectivity_tracking_alerts",
            transform=_transform_connectivity_tracking_alerts,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking_connection_state",
            api_path="connectivity_tracking.connection_state",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="connectivity_tracking_required_nodes",
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
            transform=_transform_igroups,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="initiators",
            transform=_transform_initiators,
            default=[],
        ),
        FieldMapping(
            cache_attr="lun_maps",
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
            transform=_transform_parent_igroups,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="portset_name",
            api_path="portset.name",
        ),
        FieldMapping(
            cache_attr="portset_uuid",
            api_path="portset.uuid",
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="replication_error_igroup_local_svm",
            api_path="replication.error.igroup.local_svm",
            default=False,
        ),
        FieldMapping(
            cache_attr="replication_error_igroup_name",
            api_path="replication.error.igroup.name",
        ),
        FieldMapping(
            cache_attr="replication_error_igroup_uuid",
            api_path="replication.error.igroup.uuid",
        ),
        FieldMapping(
            cache_attr="replication_error_summary_arguments",
            transform=_transform_replication_error_summary_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="replication_error_summary_code",
            api_path="replication.error.summary.code",
        ),
        FieldMapping(
            cache_attr="replication_error_summary_message",
            api_path="replication.error.summary.message",
        ),
        FieldMapping(
            cache_attr="replication_peer_svm_name",
            api_path="replication.peer_svm.name",
        ),
        FieldMapping(
            cache_attr="replication_peer_svm_uuid",
            api_path="replication.peer_svm.uuid",
        ),
        FieldMapping(
            cache_attr="replication_state",
            api_path="replication.state",
        ),
        FieldMapping(
            cache_attr="supports_igroups",
            api_path="supports_igroups",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target_firmware_revision",
            api_path="target.firmware_revision",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="target_product_id",
            api_path="target.product_id",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="target_vendor_id",
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
