"""OntapLoginMessages information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapLoginMessages(CacheModel):
    """OntapLoginMessages information."""

    banner: str = ""
    message: str = ""
    scope: str = ""
    show_cluster_message: bool = False
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
