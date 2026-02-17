"""OntapSvmMigrationVolume information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapSvmMigrationVolumeError(CacheModel):
    """OntapSvmMigrationVolumeError sub-model for errors."""

    errors_code: str = ""
    errors_message: str = ""


class OntapSvmMigrationVolume(CacheModel):
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
