"""OntapSnmpUser type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.support.snmp.users.model import OntapSnmpUser

ONTAPSNMPUSER_MAPPING = TypeMapping(
    name="OntapSnmpUser",
    model_class=OntapSnmpUser,
    api_endpoint="/support/snmp/users?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_method",
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="engine_id",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner.name",
        ),
        FieldMapping(
            cache_attr="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="snmpv3.authentication_password",
        ),
        FieldMapping(
            cache_attr="snmpv3.authentication_protocol",
        ),
        FieldMapping(
            cache_attr="snmpv3.privacy_password",
        ),
        FieldMapping(
            cache_attr="snmpv3.privacy_protocol",
        ),
        FieldMapping(
            cache_attr="switch_address",
        ),
    ),
)

model_registry.register_mapping("OntapSnmpUser", ONTAPSNMPUSER_MAPPING)
