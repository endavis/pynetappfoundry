"""Re-export network IP interface cache models."""

from __future__ import annotations

from pynetappfoundry.cache.network.ip.interfaces.mapping import NETWORK_LIF_MAPPING
from pynetappfoundry.cache.network.ip.interfaces.model import NetworkLIF

__all__ = [
    "NETWORK_LIF_MAPPING",
    "NetworkLIF",
]
