"""OntapSensors information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapSensorsNode(OntapModel):
    """OntapSensorsNode sub-model for node."""

    name: str = ""
    uuid: str = ""


class OntapSensors(OntapModel):
    """OntapSensors information."""

    critical_high_threshold: int = 0
    critical_low_threshold: int = 0
    discrete_state: str = ""
    discrete_value: str = ""
    index: int = 0
    name: str = ""
    node: OntapSensorsNode = Field(default_factory=OntapSensorsNode)
    threshold_state: str = ""
    type_: str = ""
    value: int = 0
    value_units: str = ""
    warning_high_threshold: int = 0
    warning_low_threshold: int = 0
