"""OntapIscsiCredentials information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIscsiCredentialsMask(OntapModel):
    """OntapIscsiCredentialsMask sub-model for masks."""

    initiator_address_masks_address: str = ""
    initiator_address_masks_family: str = ""
    initiator_address_masks_netmask: str = ""


class OntapIscsiCredentialsRange(OntapModel):
    """OntapIscsiCredentialsRange sub-model for ranges."""

    initiator_address_ranges_end: str = ""
    initiator_address_ranges_family: str = ""


class OntapIscsiCredentials(OntapModel):
    """OntapIscsiCredentials information."""

    authentication_type: str = ""
    chap_inbound_password: str = ""
    chap_inbound_user: str = ""
    chap_outbound_password: str = ""
    chap_outbound_user: str = ""
    initiator: str = ""
    initiator_address_masks: list[OntapIscsiCredentialsMask] = Field(default_factory=list)
    initiator_address_ranges: list[OntapIscsiCredentialsRange] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
