"""OntapActiveDirectoryPreferredDc information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapActiveDirectoryPreferredDc(OntapModel):
    """OntapActiveDirectoryPreferredDc information."""

    fqdn: str = ""
    server_ip: str = ""
