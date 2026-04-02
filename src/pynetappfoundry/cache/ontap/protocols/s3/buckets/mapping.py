"""OntapS3Bucket type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.buckets.model import (
    OntapS3Bucket,
    OntapS3BucketAggregate,
    OntapS3BucketCorsRule,
    OntapS3BucketLifecycleManagementRule,
    OntapS3BucketPolicyStatement,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_aggregates(record: dict[str, Any]) -> list[OntapS3BucketAggregate]:
    """Transform aggregates into OntapS3BucketAggregate list."""
    return [OntapS3BucketAggregate(**item) for item in record.get("aggregates", [])]


def _transform_cors_rules(record: dict[str, Any]) -> list[OntapS3BucketCorsRule]:
    """Transform cors.rules into OntapS3BucketCorsRule list."""
    try:
        items = get_nested_value(record, "cors.rules")
    except Exception:
        items = []
    return [OntapS3BucketCorsRule(**item) for item in items]


def _transform_lifecycle_management_rules(
    record: dict[str, Any],
) -> list[OntapS3BucketLifecycleManagementRule]:
    """Transform lifecycle_management.rules into OntapS3BucketLifecycleManagementRule list."""
    try:
        items = get_nested_value(record, "lifecycle_management.rules")
    except Exception:
        items = []
    return [OntapS3BucketLifecycleManagementRule(**item) for item in items]


def _transform_policy_statements(record: dict[str, Any]) -> list[OntapS3BucketPolicyStatement]:
    """Transform policy.statements into OntapS3BucketPolicyStatement list."""
    try:
        items = get_nested_value(record, "policy.statements")
    except Exception:
        items = []
    return [OntapS3BucketPolicyStatement(**item) for item in items]


ONTAPS3BUCKET_MAPPING = TypeMapping(
    name="OntapS3Bucket",
    model_class=OntapS3Bucket,
    api_endpoint="/protocols/s3/buckets?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="aggregates",
            api_path="aggregates",
            transform=_transform_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="allowed",
            api_path="allowed",
            default=False,
        ),
        FieldMapping(
            cache_attr="audit_event_selector.access",
            api_path="audit_event_selector.access",
        ),
        FieldMapping(
            cache_attr="audit_event_selector.permission",
            api_path="audit_event_selector.permission",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="constituents_per_aggregate",
            api_path="constituents_per_aggregate",
            default=0,
        ),
        FieldMapping(
            cache_attr="cors.rules",
            api_path="cors.rules",
            transform=_transform_cors_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption.enabled",
            api_path="encryption.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="lifecycle_management.rules",
            api_path="lifecycle_management.rules",
            transform=_transform_lifecycle_management_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="logical_used_size",
            api_path="logical_used_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="nas_path",
            api_path="nas_path",
        ),
        FieldMapping(
            cache_attr="policy.statements",
            api_path="policy.statements",
            transform=_transform_policy_statements,
            default=[],
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_cloud",
            api_path="protection_status.destination.is_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_external_cloud",
            api_path="protection_status.destination.is_external_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_ontap",
            api_path="protection_status.destination.is_ontap",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.is_protected",
            api_path="protection_status.is_protected",
            default=False,
        ),
        FieldMapping(
            cache_attr="qos_policy.max_throughput_iops",
            api_path="qos_policy.max_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.max_throughput_mbps",
            api_path="qos_policy.max_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.min_throughput_iops",
            api_path="qos_policy.min_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.min_throughput_mbps",
            api_path="qos_policy.min_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.name",
            api_path="qos_policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy.uuid",
            api_path="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="retention.default_period",
            api_path="retention.default_period",
        ),
        FieldMapping(
            cache_attr="retention.mode",
            api_path="retention.mode",
        ),
        FieldMapping(
            cache_attr="role",
            api_path="role",
        ),
        FieldMapping(
            cache_attr="size",
            api_path="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="snapshot_policy.name",
            api_path="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.uuid",
            api_path="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="storage_service_level",
            api_path="storage_service_level",
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
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="use_mirrored_aggregates",
            api_path="use_mirrored_aggregates",
            default=False,
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="versioning_state",
            api_path="versioning_state",
        ),
        FieldMapping(
            cache_attr="volume.name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3Bucket", ONTAPS3BUCKET_MAPPING)
