"""OntapUnixGroupSettings information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapUnixGroupSettings(OntapModel):
    """OntapUnixGroupSettings information."""

    enabled: bool = False
    negative_cache_enabled: bool = False
    negative_ttl: str = ""
    propagation_enabled: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    ttl: str = ""
