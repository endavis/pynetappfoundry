"""OntapIscsiCredentials information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapIscsiCredentialsChapInbound(OntapModel):
    """OntapIscsiCredentialsChapInbound sub-model for inbound."""

    password: str = ""
    user: str = ""


class OntapIscsiCredentialsChapOutbound(OntapModel):
    """OntapIscsiCredentialsChapOutbound sub-model for outbound."""

    password: str = ""
    user: str = ""


class OntapIscsiCredentialsChap(OntapModel):
    """OntapIscsiCredentialsChap sub-model for chap."""

    inbound: OntapIscsiCredentialsChapInbound = Field(
        default_factory=OntapIscsiCredentialsChapInbound
    )
    outbound: OntapIscsiCredentialsChapOutbound = Field(
        default_factory=OntapIscsiCredentialsChapOutbound
    )


class OntapIscsiCredentialsInitiatorAddressMask(OntapModel):
    """OntapIscsiCredentialsInitiatorAddressMask sub-model for masks."""

    address: str = ""
    family: str = ""
    netmask: str = ""


class OntapIscsiCredentialsInitiatorAddressRange(OntapModel):
    """OntapIscsiCredentialsInitiatorAddressRange sub-model for ranges."""

    end: str = ""
    family: str = ""


class OntapIscsiCredentialsInitiatorAddress(OntapModel):
    """OntapIscsiCredentialsInitiatorAddress sub-model for initiator_address."""

    masks: list[OntapIscsiCredentialsInitiatorAddressMask] = Field(default_factory=list)
    ranges: list[OntapIscsiCredentialsInitiatorAddressRange] = Field(default_factory=list)


class OntapIscsiCredentialsSvm(OntapModel):
    """OntapIscsiCredentialsSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapIscsiCredentials(OntapModel):
    """OntapIscsiCredentials information."""

    authentication_type: str = ""
    chap: OntapIscsiCredentialsChap = Field(default_factory=OntapIscsiCredentialsChap)
    initiator: str = ""
    initiator_address: OntapIscsiCredentialsInitiatorAddress = Field(
        default_factory=OntapIscsiCredentialsInitiatorAddress
    )
    svm: OntapIscsiCredentialsSvm = Field(default_factory=OntapIscsiCredentialsSvm)
