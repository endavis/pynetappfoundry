"""OntapSnaplockLitigation type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.litigations.model import (
    OntapSnaplockLitigation,
    OntapSnaplockLitigationOperation,
)


def _transform_operations(record: dict[str, Any]) -> list[OntapSnaplockLitigationOperation]:
    """Transform operations into OntapSnaplockLitigationOperation list."""
    return [OntapSnaplockLitigationOperation(**item) for item in record.get("operations", [])]


ONTAPSNAPLOCKLITIGATION_MAPPING = TypeMapping(
    name="OntapSnaplockLitigation",
    model_class=OntapSnaplockLitigation,
    api_endpoint="/storage/snaplock/litigations?fields=*",
    api_type="ontap",
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="operations",
            transform=_transform_operations,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnaplockLitigation", ONTAPSNAPLOCKLITIGATION_MAPPING)
