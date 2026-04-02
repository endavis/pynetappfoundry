"""OntapFabric information."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapFabricCache(OntapModel):
    """OntapFabricCache sub-model for cache."""

    age: str = ""
    is_current: bool = False
    update_time: str = ""


class OntapFabricZoneset(OntapModel):
    """OntapFabricZoneset sub-model for zoneset."""

    name: str = ""


class OntapFabric(OntapModel):
    """OntapFabric information."""

    cache: OntapFabricCache = Field(default_factory=OntapFabricCache)
    connections: list[dict[str, Any]] = Field(default_factory=list)
    name: str = ""
    zoneset: OntapFabricZoneset = Field(default_factory=OntapFabricZoneset)
