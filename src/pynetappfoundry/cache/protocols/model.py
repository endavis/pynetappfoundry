"""Protocols configuration container — aggregates all protocol-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.protocols.cifs.services.model import CIFSServiceInfo
from pynetappfoundry.cache.protocols.cifs.shares.model import CIFSShareInfo
from pynetappfoundry.cache.protocols.nfs.export_policies.model import (
    ExportPolicyInfo,
)
from pynetappfoundry.cache.protocols.nfs.services.model import NFSServiceInfo
from pynetappfoundry.cache.protocols.s3.buckets.model import S3BucketInfo


class ProtocolsInfo(CacheModel):
    """Protocol configuration information.

    Contains NFS export policies, CIFS shares, NFS/CIFS services,
    S3 buckets, and protocol-related data.
    """

    nfs_export_policies: list[ExportPolicyInfo] = Field(default_factory=list)
    cifs_shares: list[CIFSShareInfo] = Field(default_factory=list)
    nfs_services: list[NFSServiceInfo] = Field(default_factory=list)
    cifs_services: list[CIFSServiceInfo] = Field(default_factory=list)
    s3_buckets: list[S3BucketInfo] = Field(default_factory=list)
