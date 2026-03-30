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
            cache_attr="application_name",
            api_path="application.name",
        ),
        FieldMapping(
            cache_attr="application_uuid",
            api_path="application.uuid",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="component_name",
            api_path="component.name",
        ),
        FieldMapping(
            cache_attr="component_uuid",
            api_path="component.uuid",
        ),
        FieldMapping(
            cache_attr="consistency_type",
            api_path="consistency_type",
        ),
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="is_partial",
            api_path="is_partial",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapApplicationComponentSnapshot", ONTAPAPPLICATIONCOMPONENTSNAPSHOT_MAPPING
)
