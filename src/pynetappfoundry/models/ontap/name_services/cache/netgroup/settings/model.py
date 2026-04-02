"""OntapNetgroupsSettings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapNetgroupsSettingsSvm(OntapModel):
    """OntapNetgroupsSettingsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapNetgroupsSettings(OntapModel):
    """OntapNetgroupsSettings information."""

    enabled: bool = False
    negative_cache_enabled_byhost: bool = False
    negative_ttl_byhost: str = ""
    svm: OntapNetgroupsSettingsSvm = Field(default_factory=OntapNetgroupsSettingsSvm)
    ttl_byhost: str = ""
    ttl_for_members: str = ""
