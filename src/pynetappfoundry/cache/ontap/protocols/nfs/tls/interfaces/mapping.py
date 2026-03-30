"""OntapNfsTlsInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.tls.interfaces.model import OntapNfsTlsInterface

ONTAPNFSTLSINTERFACE_MAPPING = TypeMapping(
    name="OntapNfsTlsInterface",
    model_class=OntapNfsTlsInterface,
    api_endpoint="/protocols/nfs/tls/interfaces?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="certificate_name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate_uuid",
            api_path="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
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
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNfsTlsInterface", ONTAPNFSTLSINTERFACE_MAPPING)
