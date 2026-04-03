"""OntapCifsSearchPath type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.home_directory.search_paths.model import (
    OntapCifsSearchPath,
)

ONTAPCIFSSEARCHPATH_MAPPING = TypeMapping(
    name="OntapCifsSearchPath",
    model_class=OntapCifsSearchPath,
    api_endpoint="/protocols/cifs/home-directory/search-paths?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCifsSearchPath", ONTAPCIFSSEARCHPATH_MAPPING)
