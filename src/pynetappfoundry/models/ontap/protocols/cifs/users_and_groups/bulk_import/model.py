"""OntapLocalCifsUsersAndGroupsImport information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsUsersAndGroupsImportDetailedStatus(OntapModel):
    """OntapLocalCifsUsersAndGroupsImportDetailedStatus sub-model for detailed_status."""

    code: str = ""
    message: str = ""


class OntapLocalCifsUsersAndGroupsImportImportUri(OntapModel):
    """OntapLocalCifsUsersAndGroupsImportImportUri sub-model for import_uri."""

    password: str = ""
    path: str = ""
    username: str = ""


class OntapLocalCifsUsersAndGroupsImportStatusUri(OntapModel):
    """OntapLocalCifsUsersAndGroupsImportStatusUri sub-model for status_uri."""

    password: str = ""
    path: str = ""
    username: str = ""


class OntapLocalCifsUsersAndGroupsImportSvm(OntapModel):
    """OntapLocalCifsUsersAndGroupsImportSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLocalCifsUsersAndGroupsImport(OntapModel):
    """OntapLocalCifsUsersAndGroupsImport information."""

    decryption_password: str = ""
    detailed_status: OntapLocalCifsUsersAndGroupsImportDetailedStatus = Field(
        default_factory=OntapLocalCifsUsersAndGroupsImportDetailedStatus
    )
    elements_ignored: int = 0
    elements_imported: int = 0
    import_uri: OntapLocalCifsUsersAndGroupsImportImportUri = Field(
        default_factory=OntapLocalCifsUsersAndGroupsImportImportUri
    )
    state: str = ""
    status_uri: OntapLocalCifsUsersAndGroupsImportStatusUri = Field(
        default_factory=OntapLocalCifsUsersAndGroupsImportStatusUri
    )
    svm: OntapLocalCifsUsersAndGroupsImportSvm = Field(
        default_factory=OntapLocalCifsUsersAndGroupsImportSvm
    )
