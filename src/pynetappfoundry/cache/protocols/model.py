"""Protocols configuration container — aggregates all protocol-related models."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel
from pynetappfoundry.cache.protocols.cifs.services.model import OntapCifsService
from pynetappfoundry.cache.protocols.cifs.shares.model import OntapCifsShare
from pynetappfoundry.cache.protocols.nfs.export_policies.model import OntapExportPolicy
from pynetappfoundry.cache.protocols.nfs.services.model import OntapNfsService
from pynetappfoundry.cache.protocols.s3.buckets.model import OntapS3Bucket


class ProtocolsInfo(CacheModel):
    """Protocol configuration information.

    Contains NFS export policies, CIFS shares, NFS/CIFS services,
    S3 buckets, and protocol-related data.
    """

    nfs_export_policies: list[OntapExportPolicy] = Field(default_factory=list)
    cifs_shares: list[OntapCifsShare] = Field(default_factory=list)
    nfs_services: list[OntapNfsService] = Field(default_factory=list)
    cifs_services: list[OntapCifsService] = Field(default_factory=list)
    s3_buckets: list[OntapS3Bucket] = Field(default_factory=list)
