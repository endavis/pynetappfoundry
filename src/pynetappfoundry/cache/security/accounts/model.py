"""OntapAccount information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapAccountApplication(CacheModel):
    """OntapAccountApplication sub-model for applications."""

    applications_application: str = ""
    applications_authentication_methods: list[str] = Field(default_factory=list)
    applications_is_ldap_fastbind: bool = False
    applications_is_ns_switch_group: bool = False
    applications_second_authentication_method: str = ""


class OntapAccount(CacheModel):
    """OntapAccount information."""

    applications: list[OntapAccountApplication] = Field(default_factory=list)
    comment: str = ""
    locked: bool = False
    name: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    password: str = ""
    password_hash_algorithm: str = ""
    role_name: str = ""
    scope: str = ""
