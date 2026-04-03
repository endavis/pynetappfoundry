"""OntapSnmp type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.snmp.model import OntapSnmp

ONTAPSNMP_MAPPING = TypeMapping(
    name="OntapSnmp",
    model_class=OntapSnmp,
    api_endpoint="/support/snmp?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="auth_traps_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="contact",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="location",
        ),
        FieldMapping(
            cache_attr="traps_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="trigger_test_trap",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapSnmp", ONTAPSNMP_MAPPING)
