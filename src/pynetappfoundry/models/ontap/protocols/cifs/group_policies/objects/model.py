# ruff: noqa: E501
"""OntapGroupPolicyObject information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapGroupPolicyObjectRegistrySettingsBranchcache(OntapModel):
    """OntapGroupPolicyObjectRegistrySettingsBranchcache sub-model for branchcache."""

    hash_publication_mode: str = ""
    supported_hash_version: str = ""


class OntapGroupPolicyObjectRegistrySettings(OntapModel):
    """OntapGroupPolicyObjectRegistrySettings sub-model for registry_settings."""

    branchcache: OntapGroupPolicyObjectRegistrySettingsBranchcache = Field(
        default_factory=OntapGroupPolicyObjectRegistrySettingsBranchcache
    )
    refresh_time_interval: str = ""
    refresh_time_random_offset: str = ""


class OntapGroupPolicyObjectSecuritySettingsEventAuditSettings(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsEventAuditSettings sub-model for event_audit_settings."""

    logon_type: str = ""
    object_access_type: str = ""


class OntapGroupPolicyObjectSecuritySettingsEventLogSettings(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsEventLogSettings sub-model for event_log_settings."""

    max_size: int = 0
    retention_method: str = ""


class OntapGroupPolicyObjectSecuritySettingsKerberos(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsKerberos sub-model for kerberos."""

    max_clock_skew: str = ""
    max_renew_age: str = ""
    max_ticket_age: str = ""


class OntapGroupPolicyObjectSecuritySettingsPrivilegeRights(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsPrivilegeRights sub-model for privilege_rights."""

    change_notify_users: list[str] = Field(default_factory=list)
    security_privilege_users: list[str] = Field(default_factory=list)
    take_ownership_users: list[str] = Field(default_factory=list)


class OntapGroupPolicyObjectSecuritySettingsRegistryValues(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsRegistryValues sub-model for registry_values."""

    signing_required: bool = False


class OntapGroupPolicyObjectSecuritySettingsRestrictAnonymous(OntapModel):
    """OntapGroupPolicyObjectSecuritySettingsRestrictAnonymous sub-model for restrict_anonymous."""

    anonymous_access_to_shares_and_named_pipes_restricted: bool = False
    combined_restriction_for_anonymous_user: str = ""
    no_enumeration_of_sam_accounts: bool = False
    no_enumeration_of_sam_accounts_and_shares: bool = False


class OntapGroupPolicyObjectSecuritySettings(OntapModel):
    """OntapGroupPolicyObjectSecuritySettings sub-model for security_settings."""

    event_audit_settings: OntapGroupPolicyObjectSecuritySettingsEventAuditSettings = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsEventAuditSettings
    )
    event_log_settings: OntapGroupPolicyObjectSecuritySettingsEventLogSettings = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsEventLogSettings
    )
    files_or_folders: list[str] = Field(default_factory=list)
    kerberos: OntapGroupPolicyObjectSecuritySettingsKerberos = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsKerberos
    )
    privilege_rights: OntapGroupPolicyObjectSecuritySettingsPrivilegeRights = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsPrivilegeRights
    )
    registry_values: OntapGroupPolicyObjectSecuritySettingsRegistryValues = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsRegistryValues
    )
    restrict_anonymous: OntapGroupPolicyObjectSecuritySettingsRestrictAnonymous = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettingsRestrictAnonymous
    )
    restricted_groups: list[str] = Field(default_factory=list)


class OntapGroupPolicyObjectSvm(OntapModel):
    """OntapGroupPolicyObjectSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapGroupPolicyObject(OntapModel):
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
    registry_settings: OntapGroupPolicyObjectRegistrySettings = Field(
        default_factory=OntapGroupPolicyObjectRegistrySettings
    )
    security_settings: OntapGroupPolicyObjectSecuritySettings = Field(
        default_factory=OntapGroupPolicyObjectSecuritySettings
    )
    svm: OntapGroupPolicyObjectSvm = Field(default_factory=OntapGroupPolicyObjectSvm)
    uuid: str = ""
    version: int = 0
