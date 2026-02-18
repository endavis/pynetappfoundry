"""OntapAutosupportMessage information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapAutosupportMessage(CacheModel):
    """OntapAutosupportMessage information."""

    destination: str = ""
    error_code: int = 0
    error_message: str = ""
    generated_on: str = ""
    index: int = 0
    message: str = ""
    node_name: str = ""
    node_uuid: str = ""
    state: str = ""
    subject: str = ""
    type_: str = ""
    uri: str = ""
