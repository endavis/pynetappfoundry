"""OntapAutoUpdateInfo information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutoUpdateInfoEula(OntapModel):
    """OntapAutoUpdateInfoEula sub-model for eula."""

    accepted: bool = False
    accepted_ip_address: str = ""
    accepted_timestamp: str = ""
    user_id_accepted: str = ""


class OntapAutoUpdateInfo(OntapModel):
    """OntapAutoUpdateInfo information."""

    enabled: bool = False
    eula: OntapAutoUpdateInfoEula = Field(default_factory=OntapAutoUpdateInfoEula)
