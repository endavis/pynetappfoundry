"""OntapMetroclusterSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterSvmCluster(OntapModel):
    """OntapMetroclusterSvmCluster sub-model for cluster."""

    name: str = ""
    uuid: OntapUUID = ""


class OntapMetroclusterSvmFailedReasonArgument(OntapModel):
    """OntapMetroclusterSvmFailedReasonArgument sub-model for arguments."""

    code: str = ""
    message: str = ""


class OntapMetroclusterSvmFailedReason(OntapModel):
    """OntapMetroclusterSvmFailedReason sub-model for failed_reason."""

    arguments: list[OntapMetroclusterSvmFailedReasonArgument] = Field(default_factory=list)
    code: str = ""
    message: str = ""


class OntapMetroclusterSvmPartnerSvm(OntapModel):
    """OntapMetroclusterSvmPartnerSvm sub-model for partner_svm."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterSvmSvm(OntapModel):
    """OntapMetroclusterSvmSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapMetroclusterSvm(OntapModel):
    """OntapMetroclusterSvm information."""

    cluster: OntapMetroclusterSvmCluster = Field(default_factory=OntapMetroclusterSvmCluster)
    configuration_state: str = ""
    failed_reason: OntapMetroclusterSvmFailedReason = Field(
        default_factory=OntapMetroclusterSvmFailedReason
    )
    partner_svm: OntapMetroclusterSvmPartnerSvm = Field(
        default_factory=OntapMetroclusterSvmPartnerSvm
    )
    svm: OntapMetroclusterSvmSvm = Field(default_factory=OntapMetroclusterSvmSvm)
