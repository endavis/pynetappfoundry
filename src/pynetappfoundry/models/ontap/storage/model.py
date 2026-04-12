"""Storage topology container — aggregates all storage-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel
from pynetappfoundry.models.ontap.cloud.targets.model import OntapCloudTarget
from pynetappfoundry.models.ontap.cluster.schedules.model import OntapSchedule
from pynetappfoundry.models.ontap.protocols.san.igroups.model import OntapIgroup
from pynetappfoundry.models.ontap.storage.aggregates.model import OntapAggregate
from pynetappfoundry.models.ontap.storage.flexcache.flexcaches.model import OntapFlexcache
from pynetappfoundry.models.ontap.storage.luns.model import OntapLun
from pynetappfoundry.models.ontap.storage.qos.policies.model import OntapQosPolicy
from pynetappfoundry.models.ontap.storage.qtrees.model import OntapQtree
from pynetappfoundry.models.ontap.storage.snapshot_policies.model import OntapSnapshotPolicy
from pynetappfoundry.models.ontap.storage.volumes.model import OntapVolume
from pynetappfoundry.models.ontap.svm.svms.model import OntapSvm
from pynetappfoundry.models.ontap.svm.svms.top_metrics.users.model import OntapTopMetricsSvmUser

_UNMAPPED_REASON = "Aggregate container model — not an ONTAP REST endpoint"


class StorageInfo(OntapModel):
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
