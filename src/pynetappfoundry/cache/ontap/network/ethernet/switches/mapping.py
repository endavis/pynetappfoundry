"""OntapSwitch type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ethernet.switches.model import OntapSwitch

ONTAPSWITCH_MAPPING = TypeMapping(
    name="OntapSwitch",
    model_class=OntapSwitch,
    api_endpoint="/network/ethernet/switches?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="address",
        ),
        FieldMapping(
            cache_attr="discovered",
            default=False,
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="monitoring.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="monitoring.monitored",
            default=False,
        ),
        FieldMapping(
            cache_attr="monitoring.reason",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="network",
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="snmp.user",
        ),
        FieldMapping(
            cache_attr="snmp.version",
        ),
        FieldMapping(
            cache_attr="version",
        ),
    ),
)

model_registry.register_mapping("OntapSwitch", ONTAPSWITCH_MAPPING)
