"""OntapS3BucketSvm type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.buckets.model import (
    OntapS3BucketSvm,
    OntapS3BucketSvmAggregate,
    OntapS3BucketSvmCorsRule,
    OntapS3BucketSvmLifecycleManagementRule,
    OntapS3BucketSvmPolicyStatement,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_aggregates(record: dict[str, Any]) -> list[OntapS3BucketSvmAggregate]:
    """Transform aggregates into OntapS3BucketSvmAggregate list."""
    return [OntapS3BucketSvmAggregate(**item) for item in record.get("aggregates", [])]


def _transform_cors_rules(record: dict[str, Any]) -> list[OntapS3BucketSvmCorsRule]:
    """Transform cors.rules into OntapS3BucketSvmCorsRule list."""
    try:
        items = get_nested_value(record, "cors.rules")
    except Exception:
        items = []
    return [OntapS3BucketSvmCorsRule(**item) for item in items]


def _transform_lifecycle_management_rules(
    record: dict[str, Any],
) -> list[OntapS3BucketSvmLifecycleManagementRule]:
    """Transform lifecycle_management.rules into OntapS3BucketSvmLifecycleManagementRule list."""
    try:
        items = get_nested_value(record, "lifecycle_management.rules")
    except Exception:
        items = []
    return [OntapS3BucketSvmLifecycleManagementRule(**item) for item in items]


def _transform_policy_statements(record: dict[str, Any]) -> list[OntapS3BucketSvmPolicyStatement]:
    """Transform policy.statements into OntapS3BucketSvmPolicyStatement list."""
    try:
        items = get_nested_value(record, "policy.statements")
    except Exception:
        items = []
    return [OntapS3BucketSvmPolicyStatement(**item) for item in items]


ONTAPS3BUCKETSVM_MAPPING = TypeMapping(
    name="OntapS3BucketSvm",
    model_class=OntapS3BucketSvm,
    api_endpoint="/protocols/s3/services/{svm.uuid}/buckets?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="aggregates",
            transform=_transform_aggregates,
            default=[],
        ),
        FieldMapping(
            cache_attr="audit_event_selector.access",
        ),
        FieldMapping(
            cache_attr="audit_event_selector.permission",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="constituents_per_aggregate",
            default=0,
        ),
        FieldMapping(
            cache_attr="cors.rules",
            transform=_transform_cors_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="lifecycle_management.rules",
            transform=_transform_lifecycle_management_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="logical_used_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="nas_path",
        ),
        FieldMapping(
            cache_attr="policy.statements",
            transform=_transform_policy_statements,
            default=[],
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_external_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.destination.is_ontap",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status.is_protected",
            default=False,
        ),
        FieldMapping(
            cache_attr="qos_policy.max_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.max_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.min_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.min_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="retention.default_period",
        ),
        FieldMapping(
            cache_attr="retention.mode",
        ),
        FieldMapping(
            cache_attr="role",
        ),
        FieldMapping(
            cache_attr="size",
            default=0,
        ),
        FieldMapping(
            cache_attr="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="storage_service_level",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="versioning_state",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3BucketSvm", ONTAPS3BUCKETSVM_MAPPING)
