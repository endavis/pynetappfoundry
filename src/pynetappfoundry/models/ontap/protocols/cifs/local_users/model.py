"""OntapLocalCifsUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsUserMembership(OntapModel):
    """OntapLocalCifsUserMembership sub-model for membership."""

    membership_name: str = ""
    membership_sid: str = ""


class OntapLocalCifsUser(OntapModel):
    """OntapLocalCifsUser information."""

    account_disabled: bool = False
    description: str = ""
    full_name: str = ""
    membership: list[OntapLocalCifsUserMembership] = Field(default_factory=list)
    name: str = ""
    password: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
