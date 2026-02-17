"""OntapQosOption information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapQosOption(CacheModel):
    """OntapQosOption information."""

    background_task_reserve: int = 0
