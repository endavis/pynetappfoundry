"""OntapApplicationComponentSnapshot type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.application.applications.components.snapshots.model import (
    OntapApplicationComponentSnapshot,
)

ONTAPAPPLICATIONCOMPONENTSNAPSHOT_MAPPING = TypeMapping(
    name="OntapApplicationComponentSnapshot",
    model_class=OntapApplicationComponentSnapshot,
    api_endpoint="/application/applications/{application.uuid}/components/{component.uuid}/snapshots?fields=*",
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
            cache_attr="component.name",
        ),
        FieldMapping(
            cache_attr="component.uuid",
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

model_registry.register_mapping(
    "OntapApplicationComponentSnapshot", ONTAPAPPLICATIONCOMPONENTSNAPSHOT_MAPPING
)
