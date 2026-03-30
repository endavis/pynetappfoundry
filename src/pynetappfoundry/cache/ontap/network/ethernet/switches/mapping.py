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
            api_path="address",
        ),
        FieldMapping(
            cache_attr="discovered",
            api_path="discovered",
            default=False,
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="monitoring_enabled",
            api_path="monitoring.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="monitoring_monitored",
            api_path="monitoring.monitored",
            default=False,
        ),
        FieldMapping(
            cache_attr="monitoring_reason",
            api_path="monitoring.reason",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="network",
            api_path="network",
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="snmp_user",
            api_path="snmp.user",
        ),
        FieldMapping(
            cache_attr="snmp_version",
            api_path="snmp.version",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapSwitch", ONTAPSWITCH_MAPPING)
