"""OntapFcSwitch information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcSwitchPort(OntapModel):
    """OntapFcSwitchPort sub-model for ports."""

    attached_device_port_id: str = ""
    attached_device_wwpn: str = ""
    slot: str = ""
    state: str = ""
    type: str = ""
    wwpn: str = ""


class OntapFcSwitch(OntapModel):
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
