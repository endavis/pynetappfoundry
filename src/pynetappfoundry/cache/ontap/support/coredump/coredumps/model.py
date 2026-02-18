"""OntapCoredump information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapCoredump(CacheModel):
    """OntapCoredump information."""

    is_partial: bool = False
    is_saved: bool = False
    md5_data_checksum: str = ""
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    panic_time: str = ""
    size: int = 0
    type_: str = ""
