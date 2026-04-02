"""OntapS3Policy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.s3.services.policies.model import (
    OntapS3Policy,
    OntapS3PolicyStatement,
)


def _transform_statements(record: dict[str, Any]) -> list[OntapS3PolicyStatement]:
    """Transform statements into OntapS3PolicyStatement list."""
    return [OntapS3PolicyStatement(**item) for item in record.get("statements", [])]


ONTAPS3POLICY_MAPPING = TypeMapping(
    name="OntapS3Policy",
    model_class=OntapS3Policy,
    api_endpoint="/protocols/s3/services/{svm.uuid}/policies?fields=*",
    api_type="ontap",
    parent_mapping="OntapS3Service",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="read_only",
            api_path="read-only",
            default=False,
        ),
        FieldMapping(
            cache_attr="statements",
            api_path="statements",
            transform=_transform_statements,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapS3Policy", ONTAPS3POLICY_MAPPING)
