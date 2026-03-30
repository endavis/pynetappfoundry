"""OntapCifsSymlinkMapping information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCifsSymlinkMapping(OntapModel):
    """OntapCifsSymlinkMapping information."""

    svm_name: str = ""
    svm_uuid: str = ""
    target_home_directory: bool = False
    target_locality: str = ""
    target_path: str = ""
    target_server: str = ""
    target_share: str = ""
    unix_path: str = ""
