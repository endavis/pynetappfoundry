"""AiqumLicensePackage type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.cluster.licensing.licenses.model import (
    AiqumLicensePackage,
    AiqumLicensePackageLicense,
)

AIQUMLICENSEPACKAGE_MAPPING = TypeMapping(
    name="AiqumLicensePackage",
    model_class=AiqumLicensePackage,
    api_endpoint="/datacenter/cluster/licensing/licenses",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="licenses",
            item_model=AiqumLicensePackageLicense,
            default=[],
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumLicensePackage", AIQUMLICENSEPACKAGE_MAPPING)
