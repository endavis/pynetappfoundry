"""OntapSnapshotPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snapshot_policies.model import (
    OntapSnapshotPolicy,
    OntapSnapshotPolicyCopy,
)


def _transform_copies(record: dict[str, Any]) -> list[OntapSnapshotPolicyCopy]:
    """Transform copies into OntapSnapshotPolicyCopy list."""
    return [OntapSnapshotPolicyCopy(**item) for item in record.get("copies", [])]


ONTAPSNAPSHOTPOLICY_MAPPING = TypeMapping(
    name="OntapSnapshotPolicy",
    model_class=OntapSnapshotPolicy,
    api_endpoint="/storage/snapshot-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="copies",
            api_path="copies",
            transform=_transform_copies,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapshotPolicy", ONTAPSNAPSHOTPOLICY_MAPPING)
