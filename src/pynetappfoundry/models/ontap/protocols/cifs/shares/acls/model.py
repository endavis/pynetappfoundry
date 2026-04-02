"""OntapCifsShareAcl information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapCifsShareAclSvm(OntapModel):
    """OntapCifsShareAclSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapCifsShareAcl(OntapModel):
    """OntapCifsShareAcl information."""

    permission: str = ""
    share: str = ""
    sid: str = ""
    svm: OntapCifsShareAclSvm = Field(default_factory=OntapCifsShareAclSvm)
    type_: str = ""
    unix_id: int = 0
    user_or_group: str = ""
