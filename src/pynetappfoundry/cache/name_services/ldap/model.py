"""OntapLdapService information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapLdapService(CacheModel):
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
    status_code: int = 0
    status_dn_message: list[str] = Field(default_factory=list)
    status_ipv4_code: int = 0
    status_ipv4_dn_messages: list[str] = Field(default_factory=list)
    status_ipv4_message: str = ""
    status_ipv4_state: str = ""
    status_ipv6_code: int = 0
    status_ipv6_dn_messages: list[str] = Field(default_factory=list)
    status_ipv6_message: str = ""
    status_ipv6_state: str = ""
    status_message: str = ""
    status_state: str = ""
    svm_name: str = ""
    svm_uuid: str = ""
    try_channel_binding: bool = False
    use_start_tls: bool = False
    user_dn: str = ""
    user_scope: str = ""
