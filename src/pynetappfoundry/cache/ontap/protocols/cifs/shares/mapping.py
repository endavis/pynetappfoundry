"""OntapCifsShare type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.shares.model import (
    OntapCifsShare,
    OntapCifsShareAcl,
)


def _transform_acls(record: dict[str, Any]) -> list[OntapCifsShareAcl]:
    """Transform acls into OntapCifsShareAcl list."""
    return [OntapCifsShareAcl(**item) for item in record.get("acls", [])]


ONTAPCIFSSHARE_MAPPING = TypeMapping(
    name="OntapCifsShare",
    model_class=OntapCifsShare,
    api_endpoint="/protocols/cifs/shares?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="access_based_enumeration",
            default=False,
        ),
        FieldMapping(
            cache_attr="acls",
            transform=_transform_acls,
            default=[],
        ),
        FieldMapping(
            cache_attr="allow_unencrypted_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="attribute_cache",
            default=False,
        ),
        FieldMapping(
            cache_attr="browsable",
            default=False,
        ),
        FieldMapping(
            cache_attr="change_notify",
            default=False,
        ),
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="continuously_available",
            cache_strategy="realtime",
            default=False,
        ),
        FieldMapping(
            cache_attr="dir_umask",
        ),
        FieldMapping(
            cache_attr="encryption",
            default=False,
        ),
        FieldMapping(
            cache_attr="file_umask",
        ),
        FieldMapping(
            cache_attr="force_group_for_create",
        ),
        FieldMapping(
            cache_attr="home_directory",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_connections_per_share",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="namespace_caching",
            default=False,
        ),
        FieldMapping(
            cache_attr="no_strict_security",
            default=False,
        ),
        FieldMapping(
            cache_attr="offline_files",
        ),
        FieldMapping(
            cache_attr="oplocks",
            default=False,
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="show_previous_versions",
            default=False,
        ),
        FieldMapping(
            cache_attr="show_snapshot",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="unix_symlink",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
        FieldMapping(
            cache_attr="vscan_profile",
        ),
    ),
)

model_registry.register_mapping("OntapCifsShare", ONTAPCIFSSHARE_MAPPING)
