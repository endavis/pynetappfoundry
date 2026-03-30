"""OntapSoftwarePackage type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.packages.model import OntapSoftwarePackage

ONTAPSOFTWAREPACKAGE_MAPPING = TypeMapping(
    name="OntapSoftwarePackage",
    model_class=OntapSoftwarePackage,
    api_endpoint="/cluster/software/packages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="create_time",
            api_path="create_time",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwarePackage", ONTAPSOFTWAREPACKAGE_MAPPING)
