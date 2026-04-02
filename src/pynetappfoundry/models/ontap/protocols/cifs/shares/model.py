"""OntapCifsShare information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsShareAcl(OntapModel):
    """OntapCifsShareAcl sub-model for acls."""

    permission: str = ""
    type_: str = ""
    user_or_group: str = ""
    win_sid_unix_id: str = ""


class OntapCifsShareSvm(OntapModel):
    """OntapCifsShareSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsShareVolume(OntapModel):
    """OntapCifsShareVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapCifsShare(OntapModel):
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
    svm: OntapCifsShareSvm = Field(default_factory=OntapCifsShareSvm)
    unix_symlink: str = ""
    volume: OntapCifsShareVolume = Field(default_factory=OntapCifsShareVolume)
    vscan_profile: str = ""
