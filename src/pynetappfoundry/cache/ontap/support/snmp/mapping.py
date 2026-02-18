"""OntapSnmp type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.snmp.model import OntapSnmp

ONTAPSNMP_MAPPING = TypeMapping(
    name="OntapSnmp",
    model_class=OntapSnmp,
    api_endpoint="/support/snmp?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="auth_traps_enabled",
            api_path="auth_traps_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="contact",
            api_path="contact",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
            api_path="location",
        ),
        FieldMapping(
            cache_attr="traps_enabled",
            api_path="traps_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="trigger_test_trap",
            api_path="trigger_test_trap",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSnmp", ONTAPSNMP_MAPPING)
