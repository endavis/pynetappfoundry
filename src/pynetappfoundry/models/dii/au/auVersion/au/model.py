# ruff: noqa: N815
"""DiiAuversionAu information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiAuversionAu(OntapModel):
    """DiiAuversionAu information."""

    auVersion: str = ""
    versionToBeUpgradedTo: str = ""
    isPinned: bool = False
    ip: str = ""
    auUpgradeToImageUploadedTime: int = 0
    restartRequestTime: int = 0
    upgradeOverDueMessage: str = ""
    type_: str = ""
    uuid: str = ""
    leasePeriod: int = 0
    upgradeOverDue: bool = False
    name: str = ""
    upgradeType: str = ""
    self: str = ""
    id: str = ""
    nextLeaseRenewal: int = 0
    status: str = ""
