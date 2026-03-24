"""OntapS3Bucket type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.s3.buckets.model import (
    OntapS3Bucket,
    OntapS3BucketAggregate,
    OntapS3BucketRule,
    OntapS3BucketRule2,
    OntapS3BucketStatement,
)


def _transform_aggregates(record: dict[str, Any]) -> list[OntapS3BucketAggregate]:
    """Transform aggregates into OntapS3BucketAggregate list."""
    return [OntapS3BucketAggregate(**item) for item in record.get("aggregates", [])]


def _transform_cors_rules(record: dict[str, Any]) -> list[OntapS3BucketRule]:
    """Transform cors.rules into OntapS3BucketRule list."""
    return [OntapS3BucketRule(**item) for item in record.get("cors.rules", [])]


def _transform_lifecycle_management_rules(record: dict[str, Any]) -> list[OntapS3BucketRule2]:
    """Transform lifecycle_management.rules into OntapS3BucketRule2 list."""
    return [OntapS3BucketRule2(**item) for item in record.get("lifecycle_management.rules", [])]


def _transform_policy_statements(record: dict[str, Any]) -> list[OntapS3BucketStatement]:
    """Transform policy.statements into OntapS3BucketStatement list."""
    return [OntapS3BucketStatement(**item) for item in record.get("policy.statements", [])]


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
            cache_attr="audit_event_selector_access",
            api_path="audit_event_selector.access",
        ),
        FieldMapping(
            cache_attr="audit_event_selector_permission",
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
            cache_attr="cors_rules",
            api_path="cors.rules",
            transform=_transform_cors_rules,
            default=[],
        ),
        FieldMapping(
            cache_attr="encryption_enabled",
            api_path="encryption.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="lifecycle_management_rules",
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
            cache_attr="policy_statements",
            api_path="policy.statements",
            transform=_transform_policy_statements,
            default=[],
        ),
        FieldMapping(
            cache_attr="protection_status_destination_is_cloud",
            api_path="protection_status.destination.is_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status_destination_is_external_cloud",
            api_path="protection_status.destination.is_external_cloud",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status_destination_is_ontap",
            api_path="protection_status.destination.is_ontap",
            default=False,
        ),
        FieldMapping(
            cache_attr="protection_status_is_protected",
            api_path="protection_status.is_protected",
            default=False,
        ),
        FieldMapping(
            cache_attr="qos_policy_max_throughput_iops",
            api_path="qos_policy.max_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy_max_throughput_mbps",
            api_path="qos_policy.max_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy_min_throughput_iops",
            api_path="qos_policy.min_throughput_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy_min_throughput_mbps",
            api_path="qos_policy.min_throughput_mbps",
            default=0,
        ),
        FieldMapping(
            cache_attr="qos_policy_name",
            api_path="qos_policy.name",
        ),
        FieldMapping(
            cache_attr="qos_policy_uuid",
            api_path="qos_policy.uuid",
        ),
        FieldMapping(
            cache_attr="retention_default_period",
            api_path="retention.default_period",
        ),
        FieldMapping(
            cache_attr="retention_mode",
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
            cache_attr="snapshot_policy_name",
            api_path="snapshot_policy.name",
        ),
        FieldMapping(
            cache_attr="snapshot_policy_uuid",
            api_path="snapshot_policy.uuid",
        ),
        FieldMapping(
            cache_attr="storage_service_level",
            api_path="storage_service_level",
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
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3Bucket", ONTAPS3BUCKET_MAPPING)
