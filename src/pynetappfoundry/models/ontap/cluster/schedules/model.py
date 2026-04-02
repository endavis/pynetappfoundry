"""OntapSchedule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapScheduleCluster(OntapModel):
    """OntapScheduleCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapScheduleCron(OntapModel):
    """OntapScheduleCron sub-model for cron."""

    days: list[int] = Field(default_factory=list)
    hours: list[int] = Field(default_factory=list)
    minutes: list[int] = Field(default_factory=list)
    months: list[int] = Field(default_factory=list)
    weekdays: list[int] = Field(default_factory=list)


class OntapScheduleSvm(OntapModel):
    """OntapScheduleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapSchedule(OntapModel):
    """OntapSchedule information."""

    cluster: OntapScheduleCluster = Field(default_factory=OntapScheduleCluster)
    cron: OntapScheduleCron = Field(default_factory=OntapScheduleCron)
    interval: str = ""
    name: str = ""
    scope: str = ""
    svm: OntapScheduleSvm = Field(default_factory=OntapScheduleSvm)
    type_: str = ""
    uuid: OntapUUID = ""
