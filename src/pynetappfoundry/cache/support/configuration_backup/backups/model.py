"""OntapConfigurationBackupFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapConfigurationBackupFileBackupNode(CacheModel):
    """OntapConfigurationBackupFileBackupNode sub-model for backup_nodes."""

    backup_nodes_name: str = ""


class OntapConfigurationBackupFile(CacheModel):
    """OntapConfigurationBackupFile information."""

    auto: bool = False
    backup_nodes: list[OntapConfigurationBackupFileBackupNode] = Field(default_factory=list)
    download_link: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    size: int = 0
    time: str = ""
    type_: str = ""
    version: str = ""
