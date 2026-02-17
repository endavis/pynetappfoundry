"""OntapQosWorkload information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapQosWorkload(CacheModel):
    """OntapQosWorkload information."""

    file: str = ""
    lun: str = ""
    name: str = ""
    policy_name: str = ""
    policy_uuid: str = ""
    qtree: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    volume: str = ""
    wid: int = 0
    workload_class: str = ""
