"""OntapLocalCifsUser information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLocalCifsUserMembership(CacheModel):
    """OntapLocalCifsUserMembership sub-model for membership."""

    membership_name: str = ""
    membership_sid: str = ""


class OntapLocalCifsUser(CacheModel):
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
