"""OntapKeyManagerAuthKey information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapKeyManagerAuthKey(OntapModel):
    """OntapKeyManagerAuthKey information."""

    key_id: str = ""
    key_tag: str = ""
    passphrase: str = ""
    security_key_manager_uuid: str = ""
