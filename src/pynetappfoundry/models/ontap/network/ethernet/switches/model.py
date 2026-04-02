"""OntapSwitch information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSwitchMonitoring(OntapModel):
    """OntapSwitchMonitoring sub-model for monitoring."""

    enabled: bool = False
    monitored: bool = False
    reason: str = ""


class OntapSwitchSnmp(OntapModel):
    """OntapSwitchSnmp sub-model for snmp."""

    user: str = ""
    version: str = ""


class OntapSwitch(OntapModel):
    """OntapSwitch information."""

    address: str = ""
    discovered: bool = False
    model_: str = ""
    monitoring: OntapSwitchMonitoring = Field(default_factory=OntapSwitchMonitoring)
    name: str = ""
    network: str = ""
    serial_number: str = ""
    snmp: OntapSwitchSnmp = Field(default_factory=OntapSwitchSnmp)
    version: str = ""
