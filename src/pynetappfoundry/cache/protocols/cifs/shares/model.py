"""OntapCifsShare information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapCifsShareAcl(CacheModel):
    """OntapCifsShareAcl sub-model for acls."""

    acls_permission: str = ""
    acls_type: str = ""
    acls_user_or_group: str = ""
    acls_win_sid_unix_id: str = ""


class OntapCifsShare(CacheModel):
    """OntapCifsShare information."""

    access_based_enumeration: bool = False
    acls: list[OntapCifsShareAcl] = Field(default_factory=list)
    allow_unencrypted_access: bool = False
    attribute_cache: bool = False
    browsable: bool = False
    change_notify: bool = False
    comment: str = ""
    continuously_available: bool = False
    dir_umask: str = ""
    encryption: bool = False
    file_umask: str = ""
    force_group_for_create: str = ""
    home_directory: bool = False
    max_connections_per_share: int = 0
    name: str = ""
    namespace_caching: bool = False
    no_strict_security: bool = False
    offline_files: str = ""
    oplocks: bool = False
    path: str = ""
    show_previous_versions: bool = False
    show_snapshot: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    unix_symlink: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
    vscan_profile: str = ""
