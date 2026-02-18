"""OntapFcSwitch information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapFcSwitchPort(CacheModel):
    """OntapFcSwitchPort sub-model for ports."""

    ports_attached_device_port_id: str = ""
    ports_attached_device_wwpn: str = ""
    ports_slot: str = ""
    ports_state: str = ""
    ports_type: str = ""
    ports_wwpn: str = ""


class OntapFcSwitch(CacheModel):
    """OntapFcSwitch information."""

    cache_age: str = ""
    cache_is_current: bool = False
    cache_update_time: str = ""
    domain_id: int = 0
    fabric_name: str = ""
    name: str = ""
    ports: list[OntapFcSwitchPort] = Field(default_factory=list)
    release: str = ""
    vendor: str = ""
    wwn: str = ""
