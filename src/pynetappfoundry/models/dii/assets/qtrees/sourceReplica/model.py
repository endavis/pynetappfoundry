"""DiiQtreereplica information."""

from __future__ import annotations

from pynetappfoundry.models._base import OntapModel


class DiiQtreereplica(OntapModel):
    """DiiQtreereplica information."""

    mode: str = ""
    qtree: str = ""
    technology: str = ""
