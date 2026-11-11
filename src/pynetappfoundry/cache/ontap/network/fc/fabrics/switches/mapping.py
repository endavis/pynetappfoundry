"""OntapFcSwitch type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.fabrics.switches.model import (
    OntapFcSwitch,
    OntapFcSwitchPort,
)

ONTAPFCSWITCH_MAPPING = TypeMapping(
    name="OntapFcSwitch",
    model_class=OntapFcSwitch,
    api_endpoint="/network/fc/fabrics/{fabric.name}/switches?fields=*",
    api_type="ontap",
    parent_mapping="OntapFabric",
    parent_id_field="name",
    fields=(
        FieldMapping(
            cache_attr="cache.age",
        ),
        FieldMapping(
            cache_attr="cache.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="cache.update_time",
        ),
        FieldMapping(
            cache_attr="domain_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="fabric.name",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="ports",
            item_model=OntapFcSwitchPort,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="release",
        ),
        FieldMapping(
            cache_attr="vendor",
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
    ),
)

model_registry.register_mapping("OntapFcSwitch", ONTAPFCSWITCH_MAPPING)
