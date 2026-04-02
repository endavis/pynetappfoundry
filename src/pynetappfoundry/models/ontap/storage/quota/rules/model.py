"""OntapQuotaRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapQuotaRuleFiles(OntapModel):
    """OntapQuotaRuleFiles sub-model for files."""

    hard_limit: int = 0
    soft_limit: int = 0


class OntapQuotaRuleGroup(OntapModel):
    """OntapQuotaRuleGroup sub-model for group."""

    id: str = ""
    name: str = ""


class OntapQuotaRuleQtree(OntapModel):
    """OntapQuotaRuleQtree sub-model for qtree."""

    id: int = 0
    name: str = ""


class OntapQuotaRuleSpace(OntapModel):
    """OntapQuotaRuleSpace sub-model for space."""

    hard_limit: int = 0
    soft_limit: int = 0


class OntapQuotaRuleSvm(OntapModel):
    """OntapQuotaRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapQuotaRuleUser(OntapModel):
    """OntapQuotaRuleUser sub-model for users."""

    id: str = ""
    name: str = ""


class OntapQuotaRuleVolume(OntapModel):
    """OntapQuotaRuleVolume sub-model for volume."""

    name: str = ""
    uuid: str = ""


class OntapQuotaRule(OntapModel):
    """OntapQuotaRule information."""

    files: OntapQuotaRuleFiles = Field(default_factory=OntapQuotaRuleFiles)
    group: OntapQuotaRuleGroup = Field(default_factory=OntapQuotaRuleGroup)
    qtree: OntapQuotaRuleQtree = Field(default_factory=OntapQuotaRuleQtree)
    space: OntapQuotaRuleSpace = Field(default_factory=OntapQuotaRuleSpace)
    svm: OntapQuotaRuleSvm = Field(default_factory=OntapQuotaRuleSvm)
    type_: str = ""
    user_mapping: bool = False
    users: list[OntapQuotaRuleUser] = Field(default_factory=list)
    uuid: str = ""
    volume: OntapQuotaRuleVolume = Field(default_factory=OntapQuotaRuleVolume)
