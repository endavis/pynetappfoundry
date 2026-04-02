"""OntapUnixUserSettings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixUserSettingsSvm(OntapModel):
    """OntapUnixUserSettingsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUnixUserSettings(OntapModel):
    """OntapUnixUserSettings information."""

    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    propagation_enabled: bool = False
    svm: OntapUnixUserSettingsSvm = Field(default_factory=OntapUnixUserSettingsSvm)
    ttl: str = ""
