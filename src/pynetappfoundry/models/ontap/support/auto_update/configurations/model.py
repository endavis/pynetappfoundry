"""OntapAutoUpdateConfiguration information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapAutoUpdateConfiguration(OntapModel):
    """OntapAutoUpdateConfiguration information."""

    action: str = ""
    category: str = ""
    description_code: str = ""
    description_message: str = ""
    uuid: str = ""
