"""OntapSplitLoad information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSplitLoad(OntapModel):
    """OntapSplitLoad information."""

    load_allowable: int = 0
    load_current: int = 0
    load_maximum: int = 0
    load_token_reserved: int = 0
    node_name: str = ""
    node_uuid: str = ""
