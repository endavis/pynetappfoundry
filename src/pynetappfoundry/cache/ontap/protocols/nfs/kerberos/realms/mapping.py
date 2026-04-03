"""OntapKerberosRealm type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.kerberos.realms.model import OntapKerberosRealm

ONTAPKERBEROSREALM_MAPPING = TypeMapping(
    name="OntapKerberosRealm",
    model_class=OntapKerberosRealm,
    api_endpoint="/protocols/nfs/kerberos/realms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ad_server.address",
        ),
        FieldMapping(
            cache_attr="ad_server.name",
        ),
        FieldMapping(
            cache_attr="admin_server.address",
        ),
        FieldMapping(
            cache_attr="admin_server.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="clock_skew",
            default=0,
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="encryption_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="kdc.ip",
        ),
        FieldMapping(
            cache_attr="kdc.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="kdc.vendor",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="password_server.address",
        ),
        FieldMapping(
            cache_attr="password_server.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapKerberosRealm", ONTAPKERBEROSREALM_MAPPING)
