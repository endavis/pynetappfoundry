"""OntapConfigurationBackup information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapConfigurationBackup(CacheModel):
    """OntapConfigurationBackup information."""

    password: str = ""
    url: str = ""
    username: str = ""
    validate_certificate: bool = False
