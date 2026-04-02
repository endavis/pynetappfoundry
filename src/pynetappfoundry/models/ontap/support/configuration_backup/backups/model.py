"""OntapConfigurationBackupFile information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapConfigurationBackupFileBackupNode(OntapModel):
    """OntapConfigurationBackupFileBackupNode sub-model for backup_nodes."""

    name: str = ""


class OntapConfigurationBackupFileNode(OntapModel):
    """OntapConfigurationBackupFileNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapConfigurationBackupFile(OntapModel):
    """OntapConfigurationBackupFile information."""

    auto: bool = False
    backup_nodes: list[OntapConfigurationBackupFileBackupNode] = Field(default_factory=list)
    download_link: str = ""
    name: str = ""
    node: OntapConfigurationBackupFileNode = Field(default_factory=OntapConfigurationBackupFileNode)
    size: int = 0
    time: str = ""
    type_: str = ""
    version: str = ""
