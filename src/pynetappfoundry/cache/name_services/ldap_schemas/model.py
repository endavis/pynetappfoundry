"""OntapLdapSchema information."""

from __future__ import annotations

from pynetappfoundry.cache._base import CacheModel


class OntapLdapSchema(CacheModel):
    """OntapLdapSchema information."""

    comment: str = ""
    global_schema: bool = False
    name: str = ""
    name_mapping_account_unix: str = ""
    name_mapping_account_windows: str = ""
    name_mapping_windows_to_unix_attribute: str = ""
    name_mapping_windows_to_unix_no_domain_prefix: bool = False
    name_mapping_windows_to_unix_object_class: str = ""
    owner_name: str = ""
    owner_uuid: str = ""
    rfc2307_attribute_gecos: str = ""
    rfc2307_attribute_gid_number: str = ""
    rfc2307_attribute_home_directory: str = ""
    rfc2307_attribute_login_shell: str = ""
    rfc2307_attribute_uid: str = ""
    rfc2307_attribute_uid_number: str = ""
    rfc2307_attribute_user_password: str = ""
    rfc2307_cn_group: str = ""
    rfc2307_cn_netgroup: str = ""
    rfc2307_member_nis_netgroup: str = ""
    rfc2307_member_uid: str = ""
    rfc2307_nis_mapentry: str = ""
    rfc2307_nis_mapname: str = ""
    rfc2307_nis_netgroup: str = ""
    rfc2307_nis_netgroup_triple: str = ""
    rfc2307_nis_object: str = ""
    rfc2307_posix_account: str = ""
    rfc2307_posix_group: str = ""
    rfc2307bis_enabled: bool = False
    rfc2307bis_group_of_unique_names: str = ""
    rfc2307bis_maximum_groups: int = 0
    rfc2307bis_unique_member: str = ""
    scope: str = ""
    template_name: str = ""
