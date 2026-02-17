"""OntapAutosupport information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapAutosupport(CacheModel):
    """OntapAutosupport information."""

    component: str = ""
    corrective_action_code: str = ""
    corrective_action_message: str = ""
    destination: str = ""
    issue_code: str = ""
    issue_message: str = ""
    node_name: str = ""
    node_uuid: str = ""
