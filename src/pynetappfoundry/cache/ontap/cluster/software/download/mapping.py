"""OntapSoftwarePackageDownloadGet type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.download.model import (
    OntapSoftwarePackageDownloadGet,
)

ONTAPSOFTWAREPACKAGEDOWNLOADGET_MAPPING = TypeMapping(
    name="OntapSoftwarePackageDownloadGet",
    model_class=OntapSoftwarePackageDownloadGet,
    api_endpoint="/cluster/software/download?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="code",
            default=0,
        ),
        FieldMapping(
            cache_attr="message",
        ),
        FieldMapping(
            cache_attr="state",
        ),
    ),
)

model_registry.register_mapping(
    "OntapSoftwarePackageDownloadGet", ONTAPSOFTWAREPACKAGEDOWNLOADGET_MAPPING
)
