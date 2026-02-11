"""Broadcast domain information — /network/ethernet/broadcast-domains."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class BroadcastDomain(CacheModel):
    """Broadcast domain configuration."""

    uuid: str = ""
    name: str = ""
    ipspace: str = ""
    mtu: int = 0
    ports: list[str] = Field(default_factory=list)
