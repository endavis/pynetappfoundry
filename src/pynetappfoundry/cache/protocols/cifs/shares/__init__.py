"""Re-export CIFS share cache models."""

from __future__ import annotations

from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo

__all__ = [
    "CIFSShareInfo",
]
