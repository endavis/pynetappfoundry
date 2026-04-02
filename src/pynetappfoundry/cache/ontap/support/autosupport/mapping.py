"""OntapAutosupport type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.autosupport.model import OntapAutosupport

ONTAPAUTOSUPPORT_MAPPING = TypeMapping(
    name="OntapAutosupport",
    model_class=OntapAutosupport,
    api_endpoint="/support/autosupport?fields=*",
    api_type="ontap",
    records_path="issues",
    fields=(
        FieldMapping(
            cache_attr="component",
            api_path="component",
        ),
        FieldMapping(
            cache_attr="corrective_action.code",
            api_path="corrective_action.code",
        ),
        FieldMapping(
            cache_attr="corrective_action.message",
            api_path="corrective_action.message",
        ),
        FieldMapping(
            cache_attr="destination",
            api_path="destination",
        ),
        FieldMapping(
            cache_attr="issue.code",
            api_path="issue.code",
        ),
        FieldMapping(
            cache_attr="issue.message",
            api_path="issue.message",
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapAutosupport", ONTAPAUTOSUPPORT_MAPPING)
