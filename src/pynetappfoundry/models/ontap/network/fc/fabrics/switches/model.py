"""OntapFcSwitch information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFcSwitchCache(OntapModel):
    """OntapFcSwitchCache sub-model for cache."""

    age: str = ""
    is_current: bool = False
    update_time: str = ""


class OntapFcSwitchFabric(OntapModel):
    """OntapFcSwitchFabric sub-model for fabric."""

    name: str = ""


class OntapFcSwitchPortAttachedDevice(OntapModel):
    """OntapFcSwitchPortAttachedDevice sub-model for attached_device."""

    port_id: str = ""
    wwpn: str = ""


class OntapFcSwitchPort(OntapModel):
    """OntapFcSwitchPort sub-model for ports."""

    attached_device: OntapFcSwitchPortAttachedDevice = Field(
        default_factory=OntapFcSwitchPortAttachedDevice
    )
    slot: str = ""
    state: str = ""
    type_: str = ""
    wwpn: str = ""


class OntapFcSwitch(OntapModel):
    """OntapFcSwitch information."""

    cache: OntapFcSwitchCache = Field(default_factory=OntapFcSwitchCache)
    domain_id: int = 0
    fabric: OntapFcSwitchFabric = Field(default_factory=OntapFcSwitchFabric)
    name: str = ""
    ports: list[OntapFcSwitchPort] = Field(default_factory=list)
    release: str = ""
    vendor: str = ""
    wwn: str = ""
