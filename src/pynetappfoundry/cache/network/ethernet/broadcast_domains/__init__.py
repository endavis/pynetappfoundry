"""Re-export network ethernet broadcast domain cache models."""

from __future__ import annotations

from pynetappfoundry.cache.network.ethernet.broadcast_domains.mapping import (
    BROADCAST_DOMAIN_MAPPING,
)
from pynetappfoundry.cache.network.ethernet.broadcast_domains.model import (
    BroadcastDomain,
)

__all__ = [
    "BROADCAST_DOMAIN_MAPPING",
    "BroadcastDomain",
]
