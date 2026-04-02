"""OntapLunAttribute information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLunAttributeLun(OntapModel):
    """OntapLunAttributeLun sub-model for lun."""

    uuid: str = ""


class OntapLunAttribute(OntapModel):
    """OntapLunAttribute information."""

    lun: OntapLunAttributeLun = Field(default_factory=OntapLunAttributeLun)
    name: str = ""
    value: str = ""
