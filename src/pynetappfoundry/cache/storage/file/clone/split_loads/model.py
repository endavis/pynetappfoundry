"""OntapSplitLoad information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSplitLoad(CacheModel):
    """OntapSplitLoad information."""

    load_allowable: int = 0
    load_current: int = 0
    load_maximum: int = 0
    load_token_reserved: int = 0
    node_name: str = ""
    node_uuid: str = ""
