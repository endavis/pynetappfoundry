"""OntapSnapmirrorPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.snapmirror.policies.model import (
    OntapSnapmirrorPolicy,
    OntapSnapmirrorPolicyRetention,
)


def _transform_retention(record: dict[str, Any]) -> list[OntapSnapmirrorPolicyRetention]:
    """Transform retention into OntapSnapmirrorPolicyRetention list."""
    return [OntapSnapmirrorPolicyRetention(**item) for item in record.get("retention", [])]


ONTAPSNAPMIRRORPOLICY_MAPPING = TypeMapping(
    name="OntapSnapmirrorPolicy",
    model_class=OntapSnapmirrorPolicy,
    api_endpoint="/snapmirror/policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="copy_all_source_snapshots",
            default=False,
        ),
        FieldMapping(
            cache_attr="copy_latest_source_snapshot",
            default=False,
        ),
        FieldMapping(
            cache_attr="create_snapshot_on_source",
            default=False,
        ),
        FieldMapping(
            cache_attr="identity_preservation",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="network_compression_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="retention",
            transform=_transform_retention,
            default=[],
        ),
        FieldMapping(
            cache_attr="rpo",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="sync_common_snapshot_schedule.name",
        ),
        FieldMapping(
            cache_attr="sync_common_snapshot_schedule.uuid",
        ),
        FieldMapping(
            cache_attr="sync_type",
        ),
        FieldMapping(
            cache_attr="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="transfer_schedule.name",
        ),
        FieldMapping(
            cache_attr="transfer_schedule.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapmirrorPolicy", ONTAPSNAPMIRRORPOLICY_MAPPING)
