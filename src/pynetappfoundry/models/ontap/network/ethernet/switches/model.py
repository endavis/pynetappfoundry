"""OntapSwitch information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapSwitch(OntapModel):
    """OntapSwitch information."""

    address: str = ""
    discovered: bool = False
    model_: str = ""
    monitoring_enabled: bool = False
    monitoring_monitored: bool = False
    monitoring_reason: str = ""
    name: str = ""
    network: str = ""
    serial_number: str = ""
    snmp_user: str = ""
    snmp_version: str = ""
    version: str = ""
