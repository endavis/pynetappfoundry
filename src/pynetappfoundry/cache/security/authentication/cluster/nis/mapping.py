"""OntapClusterNisService type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.security.authentication.cluster.nis.model import OntapClusterNisService

ONTAPCLUSTERNISSERVICE_MAPPING = TypeMapping(
    name="OntapClusterNisService",
    model_class=OntapClusterNisService,
    api_endpoint="/security/authentication/cluster/nis?fields=*",
    api_type="ontap",
    records_path="binding_details",
    fields=(
        FieldMapping(
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="status_code",
            api_path="status.code",
        ),
        FieldMapping(
            cache_attr="status_message",
            api_path="status.message",
        ),
    ),
)

model_registry.register_mapping("OntapClusterNisService", ONTAPCLUSTERNISSERVICE_MAPPING)
