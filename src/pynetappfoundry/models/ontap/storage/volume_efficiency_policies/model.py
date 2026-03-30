"""OntapVolumeEfficiencyPolicy information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapVolumeEfficiencyPolicy(OntapModel):
    """OntapVolumeEfficiencyPolicy information."""

    comment: str = ""
    duration: int = 0
    enabled: bool = False
    name: str = ""
    qos_policy: str = ""
    schedule_name: str = ""
    start_threshold_percent: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    uuid: str = ""
