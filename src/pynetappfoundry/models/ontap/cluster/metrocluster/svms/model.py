"""OntapMetroclusterSvm information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel, OntapUUID


class OntapMetroclusterSvmArgument(OntapModel):
    """OntapMetroclusterSvmArgument sub-model for arguments."""

    failed_reason_arguments_code: str = ""
    failed_reason_arguments_message: str = ""


class OntapMetroclusterSvm(OntapModel):
    """OntapMetroclusterSvm information."""

    cluster_name: str = ""
    cluster_uuid: OntapUUID = ""
    configuration_state: str = ""
    failed_reason_arguments: list[OntapMetroclusterSvmArgument] = Field(default_factory=list)
    failed_reason_code: str = ""
    failed_reason_message: str = ""
    partner_svm_name: str = ""
    partner_svm_uuid: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
