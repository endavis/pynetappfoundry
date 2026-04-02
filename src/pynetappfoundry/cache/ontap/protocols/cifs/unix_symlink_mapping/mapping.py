"""OntapCifsSymlinkMapping type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.unix_symlink_mapping.model import (
    OntapCifsSymlinkMapping,
)

ONTAPCIFSSYMLINKMAPPING_MAPPING = TypeMapping(
    name="OntapCifsSymlinkMapping",
    model_class=OntapCifsSymlinkMapping,
    api_endpoint="/protocols/cifs/unix-symlink-mapping?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target.home_directory",
            api_path="target.home_directory",
            default=False,
        ),
        FieldMapping(
            cache_attr="target.locality",
            api_path="target.locality",
        ),
        FieldMapping(
            cache_attr="target.path",
            api_path="target.path",
        ),
        FieldMapping(
            cache_attr="target.server",
            api_path="target.server",
        ),
        FieldMapping(
            cache_attr="target.share",
            api_path="target.share",
        ),
        FieldMapping(
            cache_attr="unix_path",
            api_path="unix_path",
        ),
    ),
)

model_registry.register_mapping("OntapCifsSymlinkMapping", ONTAPCIFSSYMLINKMAPPING_MAPPING)
