"""OntapAntiRansomwareSuspect information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class OntapAntiRansomwareSuspect(OntapModel):
    """OntapAntiRansomwareSuspect information."""

    file_format: str = ""
    file_name: str = ""
    file_path: str = ""
    file_reason: str = ""
    file_suspect_time: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
