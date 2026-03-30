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
            cache_attr="ad_server_address",
            api_path="ad_server.address",
        ),
        FieldMapping(
            cache_attr="ad_server_name",
            api_path="ad_server.name",
        ),
        FieldMapping(
            cache_attr="admin_server_address",
            api_path="admin_server.address",
        ),
        FieldMapping(
            cache_attr="admin_server_port",
            api_path="admin_server.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="clock_skew",
            api_path="clock_skew",
            default=0,
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="encryption_types",
            api_path="encryption_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="kdc_ip",
            api_path="kdc.ip",
        ),
        FieldMapping(
            cache_attr="kdc_port",
            api_path="kdc.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="kdc_vendor",
            api_path="kdc.vendor",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="password_server_address",
            api_path="password_server.address",
        ),
        FieldMapping(
            cache_attr="password_server_port",
            api_path="password_server.port",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapKerberosRealm", ONTAPKERBEROSREALM_MAPPING)
