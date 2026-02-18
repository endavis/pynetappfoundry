"""OntapKerberosInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.nfs.kerberos.interfaces.model import (
    OntapKerberosInterface,
)

ONTAPKERBEROSINTERFACE_MAPPING = TypeMapping(
    name="OntapKerberosInterface",
    model_class=OntapKerberosInterface,
    api_endpoint="/protocols/nfs/kerberos/interfaces?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="encryption_types",
            api_path="encryption_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="force",
            api_path="force",
            default=False,
        ),
        FieldMapping(
            cache_attr="interface_ip_address",
            api_path="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface_name",
            api_path="interface.name",
        ),
        FieldMapping(
            cache_attr="interface_uuid",
            api_path="interface.uuid",
        ),
        FieldMapping(
            cache_attr="keytab_uri",
            api_path="keytab_uri",
        ),
        FieldMapping(
            cache_attr="machine_account",
            api_path="machine_account",
        ),
        FieldMapping(
            cache_attr="organizational_unit",
            api_path="organizational_unit",
        ),
        FieldMapping(
            cache_attr="password",
            api_path="password",
        ),
        FieldMapping(
            cache_attr="spn",
            api_path="spn",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="user",
            api_path="user",
        ),
    ),
)

model_registry.register_mapping("OntapKerberosInterface", ONTAPKERBEROSINTERFACE_MAPPING)
