"""OntapIpsec information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapIpsec(OntapModel):
    """OntapIpsec information."""

    enabled: bool = False
    offload_enabled: bool = False
    replay_window: int = 0
