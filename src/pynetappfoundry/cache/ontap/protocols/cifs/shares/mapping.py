"""OntapCifsShare type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.shares.model import (
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
            api_path="access_based_enumeration",
            default=False,
        ),
        FieldMapping(
            cache_attr="acls",
            api_path="acls",
            transform=_transform_acls,
            default=[],
        ),
        FieldMapping(
            cache_attr="allow_unencrypted_access",
            api_path="allow_unencrypted_access",
            default=False,
        ),
        FieldMapping(
            cache_attr="attribute_cache",
            api_path="attribute_cache",
            default=False,
        ),
        FieldMapping(
            cache_attr="browsable",
            api_path="browsable",
            default=False,
        ),
        FieldMapping(
            cache_attr="change_notify",
            api_path="change_notify",
            default=False,
        ),
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="continuously_available",
            api_path="continuously_available",
            default=False,
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="dir_umask",
            api_path="dir_umask",
        ),
        FieldMapping(
            cache_attr="encryption",
            api_path="encryption",
            default=False,
        ),
        FieldMapping(
            cache_attr="file_umask",
            api_path="file_umask",
        ),
        FieldMapping(
            cache_attr="force_group_for_create",
            api_path="force_group_for_create",
        ),
        FieldMapping(
            cache_attr="home_directory",
            api_path="home_directory",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_connections_per_share",
            api_path="max_connections_per_share",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="namespace_caching",
            api_path="namespace_caching",
            default=False,
        ),
        FieldMapping(
            cache_attr="no_strict_security",
            api_path="no_strict_security",
            default=False,
        ),
        FieldMapping(
            cache_attr="offline_files",
            api_path="offline_files",
        ),
        FieldMapping(
            cache_attr="oplocks",
            api_path="oplocks",
            default=False,
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="show_previous_versions",
            api_path="show_previous_versions",
            default=False,
        ),
        FieldMapping(
            cache_attr="show_snapshot",
            api_path="show_snapshot",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="unix_symlink",
            api_path="unix_symlink",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
        FieldMapping(
            cache_attr="vscan_profile",
            api_path="vscan_profile",
        ),
    ),
)

model_registry.register_mapping("OntapCifsShare", ONTAPCIFSSHARE_MAPPING)
