"""OntapEmsMessageResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.ems.messages.model import OntapEmsMessageResponse

ONTAPEMSMESSAGERESPONSE_MAPPING = TypeMapping(
    name="OntapEmsMessageResponse",
    model_class=OntapEmsMessageResponse,
    api_endpoint="/support/ems/messages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="corrective_action",
            api_path="corrective_action",
        ),
        FieldMapping(
            cache_attr="deprecated",
            api_path="deprecated",
            default=False,
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="severity",
            api_path="severity",
        ),
        FieldMapping(
            cache_attr="snmp_trap_type",
            api_path="snmp_trap_type",
        ),
    ),
)

model_registry.register_mapping("OntapEmsMessageResponse", ONTAPEMSMESSAGERESPONSE_MAPPING)
