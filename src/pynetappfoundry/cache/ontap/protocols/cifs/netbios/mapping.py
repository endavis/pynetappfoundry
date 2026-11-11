"""OntapNetbios type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.netbios.model import (
    OntapNetbios,
    OntapNetbiosWinsServer,
)

ONTAPNETBIOS_MAPPING = TypeMapping(
    name="OntapNetbios",
    model_class=OntapNetbios,
    api_endpoint="/protocols/cifs/netbios?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="interfaces",
            default=[],
        ),
        FieldMapping(
            cache_attr="mode",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="name_registration_type",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="suffix",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="time_left",
            default=0,
        ),
        FieldMapping(
            cache_attr="wins_servers",
            item_model=OntapNetbiosWinsServer,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapNetbios", ONTAPNETBIOS_MAPPING)
