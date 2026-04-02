"""OntapHostsSettings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapHostsSettingsSvm(OntapModel):
    """OntapHostsSettingsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapHostsSettings(OntapModel):
    """OntapHostsSettings information."""

    dns_ttl_enabled: bool = False
    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    svm: OntapHostsSettingsSvm = Field(default_factory=OntapHostsSettingsSvm)
    ttl: str = ""
    uuid: str = ""
