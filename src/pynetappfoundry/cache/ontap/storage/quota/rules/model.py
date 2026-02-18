"""OntapQuotaRule information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapQuotaRuleUser(CacheModel):
    """OntapQuotaRuleUser sub-model for users."""

    users_id: str = ""
    users_name: str = ""


class OntapQuotaRule(CacheModel):
    """OntapQuotaRule information."""

    files_hard_limit: int = 0
    files_soft_limit: int = 0
    group_id: str = ""
    group_name: str = ""
    qtree_id: int = 0
    qtree_name: str = ""
    space_hard_limit: int = 0
    space_soft_limit: int = 0
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    user_mapping: bool = False
    users: list[OntapQuotaRuleUser] = Field(default_factory=list)
    uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
