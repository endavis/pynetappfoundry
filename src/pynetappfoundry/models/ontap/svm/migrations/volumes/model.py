"""OntapSvmMigrationVolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSvmMigrationVolumeError(OntapModel):
    """OntapSvmMigrationVolumeError sub-model for errors."""

    errors_code: str = ""
    errors_message: str = ""


class OntapSvmMigrationVolume(OntapModel):
    """OntapSvmMigrationVolume information."""

    errors: list[OntapSvmMigrationVolumeError] = Field(default_factory=list)
    healthy: bool = False
    node_name: str = ""
    node_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    transfer_state: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
