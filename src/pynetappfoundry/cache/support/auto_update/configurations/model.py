"""OntapAutoUpdateConfiguration information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapAutoUpdateConfiguration(CacheModel):
    """OntapAutoUpdateConfiguration information."""

    action: str = ""
    category: str = ""
    description_code: str = ""
    description_message: str = ""
    uuid: str = ""
