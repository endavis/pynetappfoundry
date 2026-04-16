"""OntapKerberosInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.kerberos.interfaces.model import (
    OntapKerberosInterface,
)

ONTAPKERBEROSINTERFACE_MAPPING = TypeMapping(
    name="OntapKerberosInterface",
    model_class=OntapKerberosInterface,
    api_endpoint="/protocols/nfs/kerberos/interfaces?fields=*",
    api_type="ontap",
    identifier_field="interface.uuid",
    fields=(
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="encryption_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="force",
            default=False,
        ),
        FieldMapping(
            cache_attr="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
        ),
        FieldMapping(
            cache_attr="keytab_uri",
        ),
        FieldMapping(
            cache_attr="machine_account",
        ),
        FieldMapping(
            cache_attr="organizational_unit",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="spn",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="user",
        ),
    ),
)

model_registry.register_mapping("OntapKerberosInterface", ONTAPKERBEROSINTERFACE_MAPPING)
