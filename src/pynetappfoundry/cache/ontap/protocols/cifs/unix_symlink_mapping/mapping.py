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
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target.home_directory",
            default=False,
        ),
        FieldMapping(
            cache_attr="target.locality",
        ),
        FieldMapping(
            cache_attr="target.path",
        ),
        FieldMapping(
            cache_attr="target.server",
        ),
        FieldMapping(
            cache_attr="target.share",
        ),
        FieldMapping(
            cache_attr="unix_path",
        ),
    ),
)

model_registry.register_mapping("OntapCifsSymlinkMapping", ONTAPCIFSSYMLINKMAPPING_MAPPING)
