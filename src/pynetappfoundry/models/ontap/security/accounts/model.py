"""OntapAccount information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAccountApplication(OntapModel):
    """OntapAccountApplication sub-model for applications."""

    application: str = ""
    authentication_methods: list[str] = Field(default_factory=list)
    is_ldap_fastbind: bool = False
    is_ns_switch_group: bool = False
    second_authentication_method: str = ""


class OntapAccountOwner(OntapModel):
    """OntapAccountOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapAccountRole(OntapModel):
    """OntapAccountRole sub-model for role."""

    name: str = ""


class OntapAccount(OntapModel):
    """OntapAccount information."""

    applications: list[OntapAccountApplication] = Field(default_factory=list)
    comment: str = ""
    locked: bool = False
    name: str = ""
    owner: OntapAccountOwner = Field(default_factory=OntapAccountOwner)
    password: str = ""
    password_hash_algorithm: str = ""
    role: OntapAccountRole = Field(default_factory=OntapAccountRole)
    scope: str = ""
