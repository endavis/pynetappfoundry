"""OntapCifsOpenFile information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCifsOpenFile(CacheModel):
    """OntapCifsOpenFile information."""

    connection_count: int = 0
    connection_identifier: int = 0
    continuously_available: str = ""
    identifier: int = 0
    node_name: str = ""
    node_uuid: str = ""
    open_mode: str = ""
    path: str = ""
    range_locks_count: int = 0
    session_identifier: int = 0
    share_mode: str = ""
    share_name: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
