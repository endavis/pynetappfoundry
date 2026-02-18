# ruff: noqa: E501
"""OntapGroupPolicyObject information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.cache._base import CacheModel


class OntapGroupPolicyObject(CacheModel):
    """OntapGroupPolicyObject information."""

    central_access_policy_settings: list[str] = Field(default_factory=list)
    central_access_policy_staging_audit_type: str = ""
    enabled: bool = False
    extensions: list[str] = Field(default_factory=list)
    file_system_path: str = ""
    index: int = 0
    ldap_path: str = ""
    link: str = ""
    name: str = ""
    registry_settings_branchcache_hash_publication_mode: str = ""
    registry_settings_branchcache_supported_hash_version: str = ""
    registry_settings_refresh_time_interval: str = ""
    registry_settings_refresh_time_random_offset: str = ""
    security_settings_event_audit_settings_logon_type: str = ""
    security_settings_event_audit_settings_object_access_type: str = ""
    security_settings_event_log_settings_max_size: int = 0
    security_settings_event_log_settings_retention_method: str = ""
    security_settings_files_or_folders: list[str] = Field(default_factory=list)
    security_settings_kerberos_max_clock_skew: str = ""
    security_settings_kerberos_max_renew_age: str = ""
    security_settings_kerberos_max_ticket_age: str = ""
    security_settings_privilege_rights_change_notify_users: list[str] = Field(default_factory=list)
    security_settings_privilege_rights_security_privilege_users: list[str] = Field(
        default_factory=list
    )
    security_settings_privilege_rights_take_ownership_users: list[str] = Field(default_factory=list)
    security_settings_registry_values_signing_required: bool = False
    security_settings_restrict_anonymous_anonymous_access_to_shares_and_named_pipes_restricted: bool = False
    security_settings_restrict_anonymous_combined_restriction_for_anonymous_user: str = ""
    security_settings_restrict_anonymous_no_enumeration_of_sam_accounts: bool = False
    security_settings_restrict_anonymous_no_enumeration_of_sam_accounts_and_shares: bool = False
    security_settings_restricted_groups: list[str] = Field(default_factory=list)
    svm_name: str = ""
    svm_uuid: str = ""
    uuid: str = ""
    version: int = 0
