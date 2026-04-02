"""OntapCifsDomainPreferredDc type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.domains.preferred_domain_controllers.model import (
    OntapCifsDomainPreferredDc,
)

ONTAPCIFSDOMAINPREFERREDDC_MAPPING = TypeMapping(
    name="OntapCifsDomainPreferredDc",
    model_class=OntapCifsDomainPreferredDc,
    api_endpoint="/protocols/cifs/domains/{svm.uuid}/preferred-domain-controllers?fields=*",
    api_type="ontap",
    parent_mapping="OntapCifsDomain",
    parent_id_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="fqdn",
            api_path="fqdn",
        ),
        FieldMapping(
            cache_attr="server_ip",
            api_path="server_ip",
        ),
        FieldMapping(
            cache_attr="status.details",
            api_path="status.details",
        ),
        FieldMapping(
            cache_attr="status.reachable",
            api_path="status.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCifsDomainPreferredDc", ONTAPCIFSDOMAINPREFERREDDC_MAPPING)
