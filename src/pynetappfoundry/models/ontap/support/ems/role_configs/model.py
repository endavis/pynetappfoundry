"""OntapEmsRoleConfigResponse information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapEmsRoleConfigResponseAccessControlRole(OntapModel):
    """OntapEmsRoleConfigResponseAccessControlRole sub-model for access_control_role."""

    name: str = ""


class OntapEmsRoleConfigResponseEventFilter(OntapModel):
    """OntapEmsRoleConfigResponseEventFilter sub-model for event_filter."""

    name: str = ""


class OntapEmsRoleConfigResponse(OntapModel):
    """OntapEmsRoleConfigResponse information."""

    access_control_role: OntapEmsRoleConfigResponseAccessControlRole = Field(
        default_factory=OntapEmsRoleConfigResponseAccessControlRole
    )
    event_filter: OntapEmsRoleConfigResponseEventFilter = Field(
        default_factory=OntapEmsRoleConfigResponseEventFilter
    )
    limit_access_to_global_configs: bool = False
