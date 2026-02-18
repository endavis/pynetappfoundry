"""OntapSensors information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapSensors(CacheModel):
    """OntapSensors information."""

    critical_high_threshold: int = 0
    critical_low_threshold: int = 0
    discrete_state: str = ""
    discrete_value: str = ""
    index: int = 0
    name: str = ""
    node_name: str = ""
    node_uuid: str = ""
    threshold_state: str = ""
    type_: str = ""
    value: int = 0
    value_units: str = ""
    warning_high_threshold: int = 0
    warning_low_threshold: int = 0
