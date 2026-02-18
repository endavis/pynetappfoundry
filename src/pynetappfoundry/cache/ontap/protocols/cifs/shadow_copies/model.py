"""OntapShadowcopy information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapShadowcopy(CacheModel):
    """OntapShadowcopy information."""

    client_uuid: str = ""
    destination_dir: str = ""
    files: list[str] = Field(default_factory=list)
    shadowcopy_set_uuid: str = ""
    share_name: str = ""
    source_dir: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    volume_name: str = ""
    volume_uuid: str = ""
    with_content: bool = False
