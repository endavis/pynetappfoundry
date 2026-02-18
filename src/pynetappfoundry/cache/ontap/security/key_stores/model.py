"""OntapSecurityKeystore information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSecurityKeystore(CacheModel):
    """OntapSecurityKeystore information."""

    configuration_name: str = ""
    configuration_uuid: str = ""
    enabled: bool = False
    location: str = ""
    scope: str = ""
    state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: str = ""
