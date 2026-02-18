"""OntapIpsec information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapIpsec(CacheModel):
    """OntapIpsec information."""

    enabled: bool = False
    offload_enabled: bool = False
    replay_window: int = 0
