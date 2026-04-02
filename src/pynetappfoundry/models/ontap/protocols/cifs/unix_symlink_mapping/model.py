"""OntapCifsSymlinkMapping information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsSymlinkMappingSvm(OntapModel):
    """OntapCifsSymlinkMappingSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsSymlinkMappingTarget(OntapModel):
    """OntapCifsSymlinkMappingTarget sub-model for target."""

    home_directory: bool = False
    locality: str = ""
    path: str = ""
    server: str = ""
    share: str = ""


class OntapCifsSymlinkMapping(OntapModel):
    """OntapCifsSymlinkMapping information."""

    svm: OntapCifsSymlinkMappingSvm = Field(default_factory=OntapCifsSymlinkMappingSvm)
    target: OntapCifsSymlinkMappingTarget = Field(default_factory=OntapCifsSymlinkMappingTarget)
    unix_path: str = ""
