"""OntapAutoUpdateConfiguration information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapAutoUpdateConfigurationDescription(OntapModel):
    """OntapAutoUpdateConfigurationDescription sub-model for description."""

    code: str = ""
    message: str = ""


class OntapAutoUpdateConfiguration(OntapModel):
    """OntapAutoUpdateConfiguration information."""

    action: str = ""
    category: str = ""
    description: OntapAutoUpdateConfigurationDescription = Field(
        default_factory=OntapAutoUpdateConfigurationDescription
    )
    uuid: str = ""
