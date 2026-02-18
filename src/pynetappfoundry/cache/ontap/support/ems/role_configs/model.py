"""OntapEmsRoleConfigResponse information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapEmsRoleConfigResponse(CacheModel):
    """OntapEmsRoleConfigResponse information."""

    access_control_role_name: str = ""
    event_filter_name: str = ""
    limit_access_to_global_configs: bool = False
