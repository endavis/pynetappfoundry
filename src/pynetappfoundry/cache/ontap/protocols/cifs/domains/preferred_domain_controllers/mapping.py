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
        ),
        FieldMapping(
            cache_attr="server_ip",
        ),
        FieldMapping(
            cache_attr="status.details",
        ),
        FieldMapping(
            cache_attr="status.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCifsDomainPreferredDc", ONTAPCIFSDOMAINPREFERREDDC_MAPPING)
