"""OntapLicenseManagerResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.licensing.license_managers.model import (
    OntapLicenseManagerResponse,
)

ONTAPLICENSEMANAGERRESPONSE_MAPPING = TypeMapping(
    name="OntapLicenseManagerResponse",
    model_class=OntapLicenseManagerResponse,
    api_endpoint="/cluster/licensing/license-managers?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="default",
            default=False,
        ),
        FieldMapping(
            cache_attr="uri.host",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapLicenseManagerResponse", ONTAPLICENSEMANAGERRESPONSE_MAPPING)
