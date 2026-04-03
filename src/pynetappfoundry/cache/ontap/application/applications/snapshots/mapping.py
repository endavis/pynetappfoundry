"""OntapApplicationSnapshot type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.applications.snapshots.model import (
    OntapApplicationSnapshot,
    OntapApplicationSnapshotComponent,
)


def _transform_components(record: dict[str, Any]) -> list[OntapApplicationSnapshotComponent]:
    """Transform components into OntapApplicationSnapshotComponent list."""
    return [OntapApplicationSnapshotComponent(**item) for item in record.get("components", [])]


ONTAPAPPLICATIONSNAPSHOT_MAPPING = TypeMapping(
    name="OntapApplicationSnapshot",
    model_class=OntapApplicationSnapshot,
    api_endpoint="/application/applications/{application.uuid}/snapshots?fields=*",
    api_type="ontap",
    parent_mapping="OntapApplication",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="application.name",
        ),
        FieldMapping(
            cache_attr="application.uuid",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="components",
            transform=_transform_components,
            default=[],
        ),
        FieldMapping(
            cache_attr="consistency_type",
        ),
        FieldMapping(
            cache_attr="create_time",
        ),
        FieldMapping(
            cache_attr="is_partial",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
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

model_registry.register_mapping("OntapApplicationSnapshot", ONTAPAPPLICATIONSNAPSHOT_MAPPING)
