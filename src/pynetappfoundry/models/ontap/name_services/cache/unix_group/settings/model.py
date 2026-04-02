"""OntapUnixGroupSettings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupSettingsSvm(OntapModel):
    """OntapUnixGroupSettingsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapUnixGroupSettings(OntapModel):
    """OntapUnixGroupSettings information."""

    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    propagation_enabled: bool = False
    svm: OntapUnixGroupSettingsSvm = Field(default_factory=OntapUnixGroupSettingsSvm)
    ttl: str = ""
