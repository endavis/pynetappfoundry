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
            cache_attr="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.uuid",
        ),
        FieldMapping(
            cache_attr="enabled",
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
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNfsTlsInterface", ONTAPNFSTLSINTERFACE_MAPPING)
