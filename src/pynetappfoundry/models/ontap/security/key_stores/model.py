"""OntapSecurityKeystore information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSecurityKeystoreConfiguration(OntapModel):
    """OntapSecurityKeystoreConfiguration sub-model for configuration."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeystoreSvm(OntapModel):
    """OntapSecurityKeystoreSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSecurityKeystore(OntapModel):
    """OntapSecurityKeystore information."""

    configuration: OntapSecurityKeystoreConfiguration = Field(
        default_factory=OntapSecurityKeystoreConfiguration
    )
    enabled: bool = False
    location: str = ""
    scope: str = ""
    state: str = ""
    svm: OntapSecurityKeystoreSvm = Field(default_factory=OntapSecurityKeystoreSvm)
    type_: str = ""
    uuid: str = ""
