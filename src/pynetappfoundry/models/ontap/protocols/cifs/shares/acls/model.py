"""OntapCifsShareAcl information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapCifsShareAcl(OntapModel):
    """OntapCifsShareAcl information."""

    permission: str = ""
    share: str = ""
    sid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    type_: str = ""
    unix_id: int = 0
    user_or_group: str = ""
