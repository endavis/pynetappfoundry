"""OntapEmsConfig information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapEmsConfig(OntapModel):
    """OntapEmsConfig information."""

    mail_from: str = ""
    mail_server: str = ""
    mail_server_password: str = ""
    mail_server_user: str = ""
    proxy_password: str = ""
    proxy_url: str = ""
    proxy_user: str = ""
    pubsub_enabled: bool = False
