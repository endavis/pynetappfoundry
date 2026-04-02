"""OntapVolumeEfficiencyPolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapVolumeEfficiencyPolicySchedule(OntapModel):
    """OntapVolumeEfficiencyPolicySchedule sub-model for schedule."""

    name: str = ""


class OntapVolumeEfficiencyPolicySvm(OntapModel):
    """OntapVolumeEfficiencyPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapVolumeEfficiencyPolicy(OntapModel):
    """OntapVolumeEfficiencyPolicy information."""

    comment: str = ""
    duration: int = 0
    enabled: bool = False
    name: str = ""
    qos_policy: str = ""
    schedule: OntapVolumeEfficiencyPolicySchedule = Field(
        default_factory=OntapVolumeEfficiencyPolicySchedule
    )
    start_threshold_percent: int = 0
    svm: OntapVolumeEfficiencyPolicySvm = Field(default_factory=OntapVolumeEfficiencyPolicySvm)
    type_: str = ""
    uuid: str = ""
