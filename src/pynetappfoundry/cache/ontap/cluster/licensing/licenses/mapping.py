"""OntapLicensePackageResponse type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.licensing.licenses.model import (
    OntapLicensePackageResponse,
    OntapLicensePackageResponseLicense,
)


def _transform_licenses(record: dict[str, Any]) -> list[OntapLicensePackageResponseLicense]:
    """Transform licenses into OntapLicensePackageResponseLicense list."""
    return [OntapLicensePackageResponseLicense(**item) for item in record.get("licenses", [])]


ONTAPLICENSEPACKAGERESPONSE_MAPPING = TypeMapping(
    name="OntapLicensePackageResponse",
    model_class=OntapLicensePackageResponse,
    api_endpoint="/cluster/licensing/licenses?fields=*",
    api_type="ontap",
    identifier_field="name",
    fields=(
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="entitlement.action",
        ),
        FieldMapping(
            cache_attr="entitlement.risk",
        ),
        FieldMapping(
            cache_attr="keys",
            default=[],
        ),
        FieldMapping(
            cache_attr="licenses",
            transform=_transform_licenses,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="state",
        ),
    ),
)

model_registry.register_mapping("OntapLicensePackageResponse", ONTAPLICENSEPACKAGERESPONSE_MAPPING)
