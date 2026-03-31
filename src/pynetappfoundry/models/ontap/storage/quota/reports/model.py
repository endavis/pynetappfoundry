"""OntapQuotaReport information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQuotaReportUser(OntapModel):
    """OntapQuotaReportUser sub-model for users."""

    id: str = ""
    name: str = ""


class OntapQuotaReport(OntapModel):
    """OntapQuotaReport information."""

    files_hard_limit: int = 0
    files_soft_limit: int = 0
    files_used_hard_limit_percent: int = 0
    files_used_soft_limit_percent: int = 0
    files_used_total: int = 0
    group_id: str = ""
    group_name: str = ""
    index: int = 0
    qtree_id: int = 0
    qtree_name: str = ""
    space_hard_limit: int = 0
    space_soft_limit: int = 0
    space_used_hard_limit_percent: int = 0
    space_used_soft_limit_percent: int = 0
    space_used_total: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    users: list[OntapQuotaReportUser] = Field(default_factory=list)
    volume_name: str = ""
    volume_uuid: str = ""
