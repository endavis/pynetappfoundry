"""OntapKeyManagerAuthKey information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapKeyManagerAuthKey(CacheModel):
    """OntapKeyManagerAuthKey information."""

    key_id: str = ""
    key_tag: str = ""
    passphrase: str = ""
    security_key_manager_uuid: str = ""
