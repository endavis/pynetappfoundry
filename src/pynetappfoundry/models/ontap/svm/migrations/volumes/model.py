"""OntapSvmMigrationVolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmMigrationVolumeError(OntapModel):
    """OntapSvmMigrationVolumeError sub-model for errors."""

    code: str = ""
    message: str = ""


class OntapSvmMigrationVolumeNode(OntapModel):
    """OntapSvmMigrationVolumeNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationVolumeSvm(OntapModel):
    """OntapSvmMigrationVolumeSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationVolumeVolume(OntapModel):
    """OntapSvmMigrationVolumeVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapSvmMigrationVolume(OntapModel):
    """OntapSvmMigrationVolume information."""

    errors: list[OntapSvmMigrationVolumeError] = Field(default_factory=list)
    healthy: bool = False
    node: OntapSvmMigrationVolumeNode = Field(default_factory=OntapSvmMigrationVolumeNode)
    svm: OntapSvmMigrationVolumeSvm = Field(default_factory=OntapSvmMigrationVolumeSvm)
    transfer_state: str = ""
    volume: OntapSvmMigrationVolumeVolume = Field(default_factory=OntapSvmMigrationVolumeVolume)
