"""OntapLdapService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLdapServiceStatusIpv4(OntapModel):
    """OntapLdapServiceStatusIpv4 sub-model for ipv4."""

    code: int = 0
    dn_messages: list[str] = Field(default_factory=list)
    message: str = ""
    state: str = ""


class OntapLdapServiceStatusIpv6(OntapModel):
    """OntapLdapServiceStatusIpv6 sub-model for ipv6."""

    code: int = 0
    dn_messages: list[str] = Field(default_factory=list)
    message: str = ""
    state: str = ""


class OntapLdapServiceStatus(OntapModel):
    """OntapLdapServiceStatus sub-model for status."""

    code: int = 0
    dn_message: list[str] = Field(default_factory=list)
    ipv4: OntapLdapServiceStatusIpv4 = Field(default_factory=OntapLdapServiceStatusIpv4)
    ipv4_state: str = ""
    ipv6: OntapLdapServiceStatusIpv6 = Field(default_factory=OntapLdapServiceStatusIpv6)
    ipv6_state: str = ""
    message: str = ""
    state: str = ""


class OntapLdapServiceSvm(OntapModel):
    """OntapLdapServiceSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapLdapService(OntapModel):
    """OntapLdapService information."""

    ad_domain: str = ""
    base_dn: str = ""
    base_scope: str = ""
    bind_as_cifs_server: bool = False
    bind_dn: str = ""
    bind_password: str = ""
    group_dn: str = ""
    group_membership_filter: str = ""
    group_scope: str = ""
    is_netgroup_byhost_enabled: bool = False
    is_owner: bool = False
    ldaps_enabled: bool = False
    min_bind_level: str = ""
    netgroup_byhost_dn: str = ""
    netgroup_byhost_scope: str = ""
    netgroup_dn: str = ""
    netgroup_scope: str = ""
    port: int = 0
    preferred_ad_servers: list[str] = Field(default_factory=list)
    query_timeout: int = 0
    referral_enabled: bool = False
    restrict_discovery_to_site: bool = False
    schema_: str = ""
    servers: list[str] = Field(default_factory=list)
    session_security: str = ""
    skip_config_validation: bool = False
    status: OntapLdapServiceStatus = Field(default_factory=OntapLdapServiceStatus)
    svm: OntapLdapServiceSvm = Field(default_factory=OntapLdapServiceSvm)
    try_channel_binding: bool = False
    use_start_tls: bool = False
    user_dn: str = ""
    user_scope: str = ""
