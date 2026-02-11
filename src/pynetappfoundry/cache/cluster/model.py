"""Core cluster identity information — /cluster."""

from __future__ import annotations

from pydantic import field_validator

from pynetappfoundry.cache._base import CacheModel


class ClusterInfo(CacheModel):
    """Core cluster identity information.

    Contains cluster name, UUID, and version from ONTAP.
    """

    cluster_name: str = ""
    cluster_uuid: str = ""
    ontap_version: str = ""
    model: str = ""
    contact: str = ""
    location: str = ""
    is_ha: bool = False

    @field_validator("model", mode="before")
    @classmethod
    def coerce_model_to_str(cls, v: object) -> str:
        """Coerce model field to string (API sometimes returns int)."""
        return str(v) if v is not None else ""
