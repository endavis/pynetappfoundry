"""OntapEmsConfig information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapEmsConfig(CacheModel):
    """OntapEmsConfig information."""

    mail_from: str = ""
    mail_server: str = ""
    mail_server_password: str = ""
    mail_server_user: str = ""
    proxy_password: str = ""
    proxy_url: str = ""
    proxy_user: str = ""
    pubsub_enabled: bool = False
