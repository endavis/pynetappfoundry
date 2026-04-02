# ruff: noqa: E501
"""OntapPoliciesAndRulesToBeApplied information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPoliciesAndRulesToBeAppliedSvm(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicySvm(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicySvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy sub-model for access_policies."""

    create_time: str = ""
    description: str = ""
    member_rules: list[str] = Field(default_factory=list)
    name: str = ""
    sid: str = ""
    svm: OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicySvm = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicySvm
    )
    update_time: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRuleSvm(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRuleSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule sub-model for access_rules."""

    create_time: str = ""
    current_permission: str = ""
    description: str = ""
    name: str = ""
    proposed_permission: str = ""
    resource_criteria: str = ""
    svm: OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRuleSvm = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRuleSvm
    )
    update_time: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettingsBranchcache(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettingsBranchcache sub-model for branchcache."""

    hash_publication_mode: str = ""
    supported_hash_version: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettings(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettings sub-model for registry_settings."""

    branchcache: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettingsBranchcache = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettingsBranchcache
    )
    refresh_time_interval: str = ""
    refresh_time_random_offset: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventAuditSettings(
    OntapModel
):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventAuditSettings sub-model for event_audit_settings."""

    logon_type: str = ""
    object_access_type: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventLogSettings(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventLogSettings sub-model for event_log_settings."""

    max_size: int = 0
    retention_method: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsKerberos(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsKerberos sub-model for kerberos."""

    max_clock_skew: str = ""
    max_renew_age: str = ""
    max_ticket_age: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsPrivilegeRights(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsPrivilegeRights sub-model for privilege_rights."""

    change_notify_users: list[str] = Field(default_factory=list)
    security_privilege_users: list[str] = Field(default_factory=list)
    take_ownership_users: list[str] = Field(default_factory=list)


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRegistryValues(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRegistryValues sub-model for registry_values."""

    signing_required: bool = False


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRestrictAnonymous(
    OntapModel
):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRestrictAnonymous sub-model for restrict_anonymous."""

    anonymous_access_to_shares_and_named_pipes_restricted: bool = False
    combined_restriction_for_anonymous_user: str = ""
    no_enumeration_of_sam_accounts: bool = False
    no_enumeration_of_sam_accounts_and_shares: bool = False


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettings(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettings sub-model for security_settings."""

    event_audit_settings: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventAuditSettings = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventAuditSettings
    )
    event_log_settings: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventLogSettings = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsEventLogSettings
    )
    files_or_folders: list[str] = Field(default_factory=list)
    kerberos: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsKerberos = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsKerberos
    )
    privilege_rights: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsPrivilegeRights = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsPrivilegeRights
    )
    registry_values: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRegistryValues = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRegistryValues
    )
    restrict_anonymous: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRestrictAnonymous = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettingsRestrictAnonymous
    )
    restricted_groups: list[str] = Field(default_factory=list)


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSvm(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedObject(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedObject sub-model for objects."""

    central_access_policy_settings: list[str] = Field(default_factory=list)
    central_access_policy_staging_audit_type: str = ""
    enabled: bool = False
    extensions: list[str] = Field(default_factory=list)
    file_system_path: str = ""
    index: int = 0
    ldap_path: str = ""
    link: str = ""
    name: str = ""
    registry_settings: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettings = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectRegistrySettings
    )
    security_settings: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettings = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSecuritySettings
    )
    svm: OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSvm = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedObjectSvm
    )
    uuid: str = ""
    version: int = 0


class OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroupSvm(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroupSvm sub-model for svm."""

    name: str = ""
    uuid: str = ""


class OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup sub-model for restricted_groups."""

    group_name: str = ""
    link: str = ""
    members: list[str] = Field(default_factory=list)
    memberships: list[str] = Field(default_factory=list)
    policy_name: str = ""
    svm: OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroupSvm = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroupSvm
    )
    version: int = 0


class OntapPoliciesAndRulesToBeAppliedToBeApplied(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedToBeApplied sub-model for to_be_applied."""

    access_policies: list[OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessPolicy] = Field(
        default_factory=list
    )
    access_rules: list[OntapPoliciesAndRulesToBeAppliedToBeAppliedAccessRule] = Field(
        default_factory=list
    )
    objects: list[OntapPoliciesAndRulesToBeAppliedToBeAppliedObject] = Field(default_factory=list)
    restricted_groups: list[OntapPoliciesAndRulesToBeAppliedToBeAppliedRestrictedGroup] = Field(
        default_factory=list
    )


class OntapPoliciesAndRulesToBeApplied(OntapModel):
    """OntapPoliciesAndRulesToBeApplied information."""

    svm: OntapPoliciesAndRulesToBeAppliedSvm = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedSvm
    )
    to_be_applied: OntapPoliciesAndRulesToBeAppliedToBeApplied = Field(
        default_factory=OntapPoliciesAndRulesToBeAppliedToBeApplied
    )
