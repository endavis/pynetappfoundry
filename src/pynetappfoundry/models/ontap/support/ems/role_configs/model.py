"""OntapEmsRoleConfigResponse information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapEmsRoleConfigResponse(OntapModel):
    """OntapEmsRoleConfigResponse information."""

    access_control_role_name: str = ""
    event_filter_name: str = ""
    limit_access_to_global_configs: bool = False
