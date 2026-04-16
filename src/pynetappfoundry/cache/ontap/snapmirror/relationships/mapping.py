# ruff: noqa: E501
"""OntapSnapmirrorRelationship type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.snapmirror.relationships.model import (
    OntapSnapmirrorRelationship,
    OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument,
    OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume,
    OntapSnapmirrorRelationshipSourceConsistencyGroupVolume,
    OntapSnapmirrorRelationshipSvmdrVolume,
    OntapSnapmirrorRelationshipUnhealthyReason,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_consistency_group_failover_error_arguments(
    record: dict[str, Any],
) -> list[OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument]:
    """Transform consistency_group_failover.error.arguments into OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument list."""
    try:
        items = get_nested_value(record, "consistency_group_failover.error.arguments")
    except Exception:
        items = []
    return [
        OntapSnapmirrorRelationshipConsistencyGroupFailoverErrorArgument(**item) for item in items
    ]


def _transform_destination_consistency_group_volumes(
    record: dict[str, Any],
) -> list[OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume]:
    """Transform destination.consistency_group_volumes into OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume list."""
    try:
        items = get_nested_value(record, "destination.consistency_group_volumes")
    except Exception:
        items = []
    return [OntapSnapmirrorRelationshipDestinationConsistencyGroupVolume(**item) for item in items]


def _transform_source_consistency_group_volumes(
    record: dict[str, Any],
) -> list[OntapSnapmirrorRelationshipSourceConsistencyGroupVolume]:
    """Transform source.consistency_group_volumes into OntapSnapmirrorRelationshipSourceConsistencyGroupVolume list."""
    try:
        items = get_nested_value(record, "source.consistency_group_volumes")
    except Exception:
        items = []
    return [OntapSnapmirrorRelationshipSourceConsistencyGroupVolume(**item) for item in items]


def _transform_svmdr_volumes(
    record: dict[str, Any],
) -> list[OntapSnapmirrorRelationshipSvmdrVolume]:
    """Transform svmdr_volumes into OntapSnapmirrorRelationshipSvmdrVolume list."""
    return [
        OntapSnapmirrorRelationshipSvmdrVolume(**item) for item in record.get("svmdr_volumes", [])
    ]


def _transform_unhealthy_reason(
    record: dict[str, Any],
) -> list[OntapSnapmirrorRelationshipUnhealthyReason]:
    """Transform unhealthy_reason into OntapSnapmirrorRelationshipUnhealthyReason list."""
    return [
        OntapSnapmirrorRelationshipUnhealthyReason(**item)
        for item in record.get("unhealthy_reason", [])
    ]


ONTAPSNAPMIRRORRELATIONSHIP_MAPPING = TypeMapping(
    name="OntapSnapmirrorRelationship",
    model_class=OntapSnapmirrorRelationship,
    api_endpoint="/snapmirror/relationships?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="backoff_level",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.error.arguments",
            transform=_transform_consistency_group_failover_error_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.error.code",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.error.message",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.state",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.status.code",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.status.message",
        ),
        FieldMapping(
            cache_attr="consistency_group_failover.type_",
            api_path="consistency_group_failover.type",
        ),
        FieldMapping(
            cache_attr="create_destination.bucket_retention.default_period",
        ),
        FieldMapping(
            cache_attr="create_destination.bucket_retention.mode",
        ),
        FieldMapping(
            cache_attr="create_destination.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_destination.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="create_destination.snapshot_locking_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_destination.storage_service.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_destination.storage_service.enforce_performance",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_destination.storage_service.name",
        ),
        FieldMapping(
            cache_attr="create_destination.tiering.policy",
        ),
        FieldMapping(
            cache_attr="create_destination.tiering.supported",
            default=False,
        ),
        FieldMapping(
            cache_attr="destination.cluster.name",
        ),
        FieldMapping(
            cache_attr="destination.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="destination.consistency_group_volumes",
            transform=_transform_destination_consistency_group_volumes,
            default=[],
        ),
        FieldMapping(
            cache_attr="destination.ipspace",
        ),
        FieldMapping(
            cache_attr="destination.luns.name",
        ),
        FieldMapping(
            cache_attr="destination.luns.uuid",
        ),
        FieldMapping(
            cache_attr="destination.path",
        ),
        FieldMapping(
            cache_attr="destination.svm.name",
        ),
        FieldMapping(
            cache_attr="destination.svm.uuid",
        ),
        FieldMapping(
            cache_attr="exported_snapshot",
        ),
        FieldMapping(
            cache_attr="group_type",
        ),
        FieldMapping(
            cache_attr="healthy",
            default=False,
        ),
        FieldMapping(
            cache_attr="identity_preservation",
        ),
        FieldMapping(
            cache_attr="io_serving_copy",
        ),
        FieldMapping(
            cache_attr="lag_time",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="last_transfer_network_compression_ratio",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="last_transfer_type",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="master_bias_activated_site",
        ),
        FieldMapping(
            cache_attr="policy.name",
        ),
        FieldMapping(
            cache_attr="policy.type_",
            api_path="policy.type",
        ),
        FieldMapping(
            cache_attr="policy.uuid",
        ),
        FieldMapping(
            cache_attr="preferred_site",
        ),
        FieldMapping(
            cache_attr="preserve",
            default=False,
        ),
        FieldMapping(
            cache_attr="quick_resync",
            default=False,
        ),
        FieldMapping(
            cache_attr="recover_after_break",
            default=False,
        ),
        FieldMapping(
            cache_attr="restore",
            default=False,
        ),
        FieldMapping(
            cache_attr="restore_to_snapshot",
        ),
        FieldMapping(
            cache_attr="source.cluster.name",
        ),
        FieldMapping(
            cache_attr="source.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="source.consistency_group_volumes",
            transform=_transform_source_consistency_group_volumes,
            default=[],
        ),
        FieldMapping(
            cache_attr="source.luns.name",
        ),
        FieldMapping(
            cache_attr="source.luns.uuid",
        ),
        FieldMapping(
            cache_attr="source.path",
        ),
        FieldMapping(
            cache_attr="source.svm.name",
        ),
        FieldMapping(
            cache_attr="source.svm.uuid",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svmdr_volumes",
            transform=_transform_svmdr_volumes,
            default=[],
        ),
        FieldMapping(
            cache_attr="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="total_transfer_bytes",
            default=0,
        ),
        FieldMapping(
            cache_attr="total_transfer_duration",
        ),
        FieldMapping(
            cache_attr="transfer.bytes_transferred",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="transfer.end_time",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="transfer.last_updated_time",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="transfer.state",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="transfer.total_duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="transfer.type_",
            api_path="transfer.type",
        ),
        FieldMapping(
            cache_attr="transfer.uuid",
        ),
        FieldMapping(
            cache_attr="transfer_schedule.name",
        ),
        FieldMapping(
            cache_attr="transfer_schedule.uuid",
        ),
        FieldMapping(
            cache_attr="unhealthy_reason",
            transform=_transform_unhealthy_reason,
            default=[],
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapmirrorRelationship", ONTAPSNAPMIRRORRELATIONSHIP_MAPPING)
