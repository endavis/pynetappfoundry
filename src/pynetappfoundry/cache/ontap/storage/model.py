"""Storage topology container — aggregates all storage-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.ontap.cloud.targets.model import OntapCloudTarget
from pynetappfoundry.cache.ontap.cluster.schedules.model import OntapSchedule
from pynetappfoundry.cache.ontap.protocols.san.igroups.model import OntapIgroup
from pynetappfoundry.cache.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.cache.ontap.storage.flexcache.flexcaches.model import OntapFlexcache
from pynetappfoundry.cache.ontap.storage.luns.model import OntapLun
from pynetappfoundry.cache.ontap.storage.qos.policies.model import OntapQosPolicy
from pynetappfoundry.cache.ontap.storage.qtrees.model import OntapQtree
from pynetappfoundry.cache.ontap.storage.snapshot_policies.model import OntapSnapshotPolicy
from pynetappfoundry.cache.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.cache.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.cache.ontap.svm.svms.top_metrics.users.model import OntapTopMetricsSvmUser


class StorageInfo(CacheModel):
    """Storage topology information.

    Contains aggregates, SVMs, cloud targets, volumes, qtrees,
    snapshot policies, schedules, LUNs, igroups, QoS policies,
    and FlexCache volumes.
    """

    aggregates: list[OntapAggregate] = Field(default_factory=list)
    svms: list[OntapSvm] = Field(default_factory=list)
    cloud_targets: list[OntapCloudTarget] = Field(default_factory=list)
    volumes: list[OntapVolume] = Field(default_factory=list)
    qtrees: list[OntapQtree] = Field(default_factory=list)
    snapshot_policies: list[OntapSnapshotPolicy] = Field(default_factory=list)
    schedules: list[OntapSchedule] = Field(default_factory=list)
    luns: list[OntapLun] = Field(default_factory=list)
    igroups: list[OntapIgroup] = Field(default_factory=list)
    qos_policies: list[OntapQosPolicy] = Field(default_factory=list)
    flexcaches: list[OntapFlexcache] = Field(default_factory=list)
    svm_top_metrics_users: list[OntapTopMetricsSvmUser] = Field(default_factory=list)
