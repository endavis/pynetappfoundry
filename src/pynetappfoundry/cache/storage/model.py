"""Storage topology container — aggregates all storage-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.cloud.targets.model import CloudTargetInfo
from pynetappfoundry.cache.cluster.schedules.model import ScheduleInfo
from pynetappfoundry.cache.protocols.san.igroups.model import IgroupInfo
from pynetappfoundry.cache.storage.aggregates.model import AggregateInfo
from pynetappfoundry.cache.storage.flexcache.model import FlexCacheInfo
from pynetappfoundry.cache.storage.luns.model import LunInfo
from pynetappfoundry.cache.storage.qos.model import QosPolicyInfo
from pynetappfoundry.cache.storage.qtrees.model import QtreeInfo
from pynetappfoundry.cache.storage.snapshot_policies.model import (
    SnapshotPolicyInfo,
)
from pynetappfoundry.cache.storage.volumes.model import VolumeInfo
from pynetappfoundry.cache.svm.model import SVMInfo


class StorageInfo(CacheModel):
    """Storage topology information.

    Contains aggregates, SVMs, cloud targets, volumes, qtrees,
    snapshot policies, schedules, LUNs, igroups, QoS policies,
    and FlexCache volumes.
    """

    aggregates: list[AggregateInfo] = Field(default_factory=list)
    svms: list[SVMInfo] = Field(default_factory=list)
    cloud_targets: list[CloudTargetInfo] = Field(default_factory=list)
    volumes: list[VolumeInfo] = Field(default_factory=list)
    qtrees: list[QtreeInfo] = Field(default_factory=list)
    snapshot_policies: list[SnapshotPolicyInfo] = Field(default_factory=list)
    schedules: list[ScheduleInfo] = Field(default_factory=list)
    luns: list[LunInfo] = Field(default_factory=list)
    igroups: list[IgroupInfo] = Field(default_factory=list)
    qos_policies: list[QosPolicyInfo] = Field(default_factory=list)
    flexcaches: list[FlexCacheInfo] = Field(default_factory=list)
