"""Mediator information — /cluster/mediators."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class MediatorInfo(CacheModel):
    """ONTAP Mediator configuration for cloud HA.

    Populated from the ``/cluster/mediators`` REST API endpoint.
    """

    mediator_address: str = ""
    mediator_uuid: str = ""
    mediator_port: int = 0
