# ruff: noqa: E501
"""OntapPoliciesAndRulesToBeApplied information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapPoliciesAndRulesToBeAppliedAccessPolicy(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedAccessPolicy sub-model for access_policies."""

    to_be_applied_access_policies_create_time: str = ""
    to_be_applied_access_policies_description: str = ""
    to_be_applied_access_policies_member_rules: list[str] = Field(default_factory=list)
    to_be_applied_access_policies_name: str = ""
    to_be_applied_access_policies_sid: str = ""
    to_be_applied_access_policies_svm_name: str = ""
    to_be_applied_access_policies_svm_uuid: str = ""
    to_be_applied_access_policies_update_time: str = ""


class OntapPoliciesAndRulesToBeAppliedAccessRule(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedAccessRule sub-model for access_rules."""

    to_be_applied_access_rules_create_time: str = ""
    to_be_applied_access_rules_current_permission: str = ""
    to_be_applied_access_rules_description: str = ""
    to_be_applied_access_rules_name: str = ""
    to_be_applied_access_rules_proposed_permission: str = ""
    to_be_applied_access_rules_resource_criteria: str = ""
    to_be_applied_access_rules_svm_name: str = ""
    to_be_applied_access_rules_svm_uuid: str = ""
    to_be_applied_access_rules_update_time: str = ""


class OntapPoliciesAndRulesToBeAppliedObject(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedObject sub-model for objects."""

    to_be_applied_objects_central_access_policy_settings: list[str] = Field(default_factory=list)
    to_be_applied_objects_central_access_policy_staging_audit_type: str = ""
    to_be_applied_objects_enabled: bool = False
    to_be_applied_objects_extensions: list[str] = Field(default_factory=list)
    to_be_applied_objects_file_system_path: str = ""
    to_be_applied_objects_index: int = 0
    to_be_applied_objects_ldap_path: str = ""
    to_be_applied_objects_link: str = ""
    to_be_applied_objects_name: str = ""
    to_be_applied_objects_registry_settings_branchcache_hash_publication_mode: str = ""
    to_be_applied_objects_registry_settings_branchcache_supported_hash_version: str = ""
    to_be_applied_objects_registry_settings_refresh_time_interval: str = ""
    to_be_applied_objects_registry_settings_refresh_time_random_offset: str = ""
    to_be_applied_objects_security_settings_event_audit_settings_logon_type: str = ""
    to_be_applied_objects_security_settings_event_audit_settings_object_access_type: str = ""
    to_be_applied_objects_security_settings_event_log_settings_max_size: int = 0
    to_be_applied_objects_security_settings_event_log_settings_retention_method: str = ""
    to_be_applied_objects_security_settings_files_or_folders: list[str] = Field(
        default_factory=list
    )
    to_be_applied_objects_security_settings_kerberos_max_clock_skew: str = ""
    to_be_applied_objects_security_settings_kerberos_max_renew_age: str = ""
    to_be_applied_objects_security_settings_kerberos_max_ticket_age: str = ""
    to_be_applied_objects_security_settings_privilege_rights_change_notify_users: list[str] = Field(
        default_factory=list
    )
    to_be_applied_objects_security_settings_privilege_rights_security_privilege_users: list[str] = (
        Field(default_factory=list)
    )
    to_be_applied_objects_security_settings_privilege_rights_take_ownership_users: list[str] = (
        Field(default_factory=list)
    )
    to_be_applied_objects_security_settings_registry_values_signing_required: bool = False
    to_be_applied_objects_security_settings_restrict_anonymous_anonymous_access_to_shares_and_named_pipes_restricted: bool = False
    to_be_applied_objects_security_settings_restrict_anonymous_combined_restriction_for_anonymous_user: str = ""
    to_be_applied_objects_security_settings_restrict_anonymous_no_enumeration_of_sam_accounts: bool = False
    to_be_applied_objects_security_settings_restrict_anonymous_no_enumeration_of_sam_accounts_and_shares: bool = False
    to_be_applied_objects_security_settings_restricted_groups: list[str] = Field(
        default_factory=list
    )
    to_be_applied_objects_svm_name: str = ""
    to_be_applied_objects_svm_uuid: str = ""
    to_be_applied_objects_uuid: str = ""
    to_be_applied_objects_version: int = 0


class OntapPoliciesAndRulesToBeAppliedRestrictedGroup(OntapModel):
    """OntapPoliciesAndRulesToBeAppliedRestrictedGroup sub-model for restricted_groups."""

    to_be_applied_restricted_groups_group_name: str = ""
    to_be_applied_restricted_groups_link: str = ""
    to_be_applied_restricted_groups_members: list[str] = Field(default_factory=list)
    to_be_applied_restricted_groups_memberships: list[str] = Field(default_factory=list)
    to_be_applied_restricted_groups_policy_name: str = ""
    to_be_applied_restricted_groups_svm_name: str = ""
    to_be_applied_restricted_groups_svm_uuid: str = ""
    to_be_applied_restricted_groups_version: int = 0


class OntapPoliciesAndRulesToBeApplied(OntapModel):
    """OntapPoliciesAndRulesToBeApplied information."""

    svm_name: str = ""
    svm_uuid: str = ""
    to_be_applied_access_policies: list[OntapPoliciesAndRulesToBeAppliedAccessPolicy] = Field(
        default_factory=list
    )
    to_be_applied_access_rules: list[OntapPoliciesAndRulesToBeAppliedAccessRule] = Field(
        default_factory=list
    )
    to_be_applied_objects: list[OntapPoliciesAndRulesToBeAppliedObject] = Field(
        default_factory=list
    )
    to_be_applied_restricted_groups: list[OntapPoliciesAndRulesToBeAppliedRestrictedGroup] = Field(
        default_factory=list
    )
