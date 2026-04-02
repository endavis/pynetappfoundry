"""OntapGroupMembershipSettings information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupMembershipSettingsSvm(OntapModel):
    """OntapGroupMembershipSettingsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapGroupMembershipSettings(OntapModel):
    """OntapGroupMembershipSettings information."""

    enabled: bool = False
    svm: OntapGroupMembershipSettingsSvm = Field(default_factory=OntapGroupMembershipSettingsSvm)
    ttl: str = ""
