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
        ),
        FieldMapping(
            cache_attr="copies",
            transform=_transform_copies,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
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
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapshotPolicy", ONTAPSNAPSHOTPOLICY_MAPPING)
