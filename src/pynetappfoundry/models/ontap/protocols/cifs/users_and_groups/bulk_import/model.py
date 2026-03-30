"""OntapLocalCifsUsersAndGroupsImport information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapLocalCifsUsersAndGroupsImport(OntapModel):
    """OntapLocalCifsUsersAndGroupsImport information."""

    decryption_password: str = ""
    detailed_status_code: str = ""
    detailed_status_message: str = ""
    elements_ignored: int = 0
    elements_imported: int = 0
    import_uri_password: str = ""
    import_uri_path: str = ""
    import_uri_username: str = ""
    state: str = ""
    status_uri_password: str = ""
    status_uri_path: str = ""
    status_uri_username: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
