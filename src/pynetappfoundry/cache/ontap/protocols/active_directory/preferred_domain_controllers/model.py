"""OntapActiveDirectoryPreferredDc information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapActiveDirectoryPreferredDc(CacheModel):
    """OntapActiveDirectoryPreferredDc information."""

    fqdn: str = ""
    server_ip: str = ""
