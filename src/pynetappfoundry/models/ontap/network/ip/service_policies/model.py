"""OntapIpServicePolicy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIpServicePolicyIpspace(OntapModel):
    """OntapIpServicePolicyIpspace sub-model for ipspace."""

    name: str = ""
    uuid: str = ""


class OntapIpServicePolicySvm(OntapModel):
    """OntapIpServicePolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIpServicePolicy(OntapModel):
    """OntapIpServicePolicy information."""

    ipspace: OntapIpServicePolicyIpspace = Field(default_factory=OntapIpServicePolicyIpspace)
    is_built_in: bool = False
    name: str = ""
    scope: str = ""
    services: list[str] = Field(default_factory=list)
    svm: OntapIpServicePolicySvm = Field(default_factory=OntapIpServicePolicySvm)
    uuid: str = ""
