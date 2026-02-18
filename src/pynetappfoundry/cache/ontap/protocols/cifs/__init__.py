"""Re-export CIFS cache models from sub-packages."""

from __future__ import annotations

from pynetappfoundry.cache.ontap.protocols.cifs.services import OntapCifsService
from pynetappfoundry.cache.ontap.protocols.cifs.shares import OntapCifsShare

__all__ = [
    "OntapCifsService",
    "OntapCifsShare",
]
