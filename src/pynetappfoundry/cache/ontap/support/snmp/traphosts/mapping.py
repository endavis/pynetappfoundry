"""OntapSnmpTraphost type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.snmp.traphosts.model import OntapSnmpTraphost

ONTAPSNMPTRAPHOST_MAPPING = TypeMapping(
    name="OntapSnmpTraphost",
    model_class=OntapSnmpTraphost,
    api_endpoint="/support/snmp/traphosts?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="host",
        ),
        FieldMapping(
            cache_attr="ip_address",
        ),
        FieldMapping(
            cache_attr="user.name",
        ),
    ),
)

model_registry.register_mapping("OntapSnmpTraphost", ONTAPSNMPTRAPHOST_MAPPING)
