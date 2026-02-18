"""OntapSnmpUser type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.support.snmp.users.model import OntapSnmpUser

ONTAPSNMPUSER_MAPPING = TypeMapping(
    name="OntapSnmpUser",
    model_class=OntapSnmpUser,
    api_endpoint="/support/snmp/users?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_method",
            api_path="authentication_method",
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="engine_id",
            api_path="engine_id",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="owner_name",
            api_path="owner.name",
        ),
        FieldMapping(
            cache_attr="owner_uuid",
            api_path="owner.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="snmpv3_authentication_password",
            api_path="snmpv3.authentication_password",
        ),
        FieldMapping(
            cache_attr="snmpv3_authentication_protocol",
            api_path="snmpv3.authentication_protocol",
        ),
        FieldMapping(
            cache_attr="snmpv3_privacy_password",
            api_path="snmpv3.privacy_password",
        ),
        FieldMapping(
            cache_attr="snmpv3_privacy_protocol",
            api_path="snmpv3.privacy_protocol",
        ),
        FieldMapping(
            cache_attr="switch_address",
            api_path="switch_address",
        ),
    ),
)

model_registry.register_mapping("OntapSnmpUser", ONTAPSNMPUSER_MAPPING)
