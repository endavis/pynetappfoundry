"""OntapConfigurationBackup information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapConfigurationBackup(OntapModel):
    """OntapConfigurationBackup information."""

    password: str = ""
    url: str = ""
    username: str = ""
    validate_certificate: bool = False
