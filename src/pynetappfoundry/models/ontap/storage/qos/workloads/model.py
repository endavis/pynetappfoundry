"""OntapQosWorkload information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQosWorkloadPolicy(OntapModel):
    """OntapQosWorkloadPolicy sub-model for policy."""

    name: str = ""
    uuid: str = ""


class OntapQosWorkloadSvm(OntapModel):
    """OntapQosWorkloadSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapQosWorkload(OntapModel):
    """OntapQosWorkload information."""

    file: str = ""
    lun: str = ""
    name: str = ""
    policy: OntapQosWorkloadPolicy = Field(default_factory=OntapQosWorkloadPolicy)
    qtree: str = ""
    svm: OntapQosWorkloadSvm = Field(default_factory=OntapQosWorkloadSvm)
    uuid: str = ""
    volume: str = ""
    wid: int = 0
    workload_class: str = ""
