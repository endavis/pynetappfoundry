"""OntapGroupMembershipSettings information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapGroupMembershipSettings(OntapModel):
    """OntapGroupMembershipSettings information."""

    enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    ttl: str = ""
