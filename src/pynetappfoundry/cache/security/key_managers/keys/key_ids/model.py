"""OntapKeyManagerKeys information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapKeyManagerKeys(CacheModel):
    """OntapKeyManagerKeys information."""

    crn: str = ""
    encryption_algorithm: str = ""
    key_id: str = ""
    key_manager: str = ""
    key_server: str = ""
    key_store: str = ""
    key_store_type: str = ""
    key_tag: str = ""
    key_type: str = ""
    key_user: str = ""
    node_name: str = ""
    node_uuid: str = ""
    policy: str = ""
    restored: bool = False
    scope: str = ""
    security_key_manager_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
