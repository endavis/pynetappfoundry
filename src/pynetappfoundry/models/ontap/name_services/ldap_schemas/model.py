"""OntapLdapSchema information."""

from __future__ import annotations

from pydantic import Field

from pynetappfoundry.models._base import OntapModel


class OntapLdapSchemaNameMappingAccount(OntapModel):
    """OntapLdapSchemaNameMappingAccount sub-model for account."""

    unix: str = ""
    windows: str = ""


class OntapLdapSchemaNameMappingWindowsToUnix(OntapModel):
    """OntapLdapSchemaNameMappingWindowsToUnix sub-model for windows_to_unix."""

    attribute: str = ""
    no_domain_prefix: bool = False
    object_class: str = ""


class OntapLdapSchemaNameMapping(OntapModel):
    """OntapLdapSchemaNameMapping sub-model for name_mapping."""

    account: OntapLdapSchemaNameMappingAccount = Field(
        default_factory=OntapLdapSchemaNameMappingAccount
    )
    windows_to_unix: OntapLdapSchemaNameMappingWindowsToUnix = Field(
        default_factory=OntapLdapSchemaNameMappingWindowsToUnix
    )


class OntapLdapSchemaOwner(OntapModel):
    """OntapLdapSchemaOwner sub-model for owner."""

    name: str = ""
    uuid: str = ""


class OntapLdapSchemaRfc2307Attribute(OntapModel):
    """OntapLdapSchemaRfc2307Attribute sub-model for attribute."""

    gecos: str = ""
    gid_number: str = ""
    home_directory: str = ""
    login_shell: str = ""
    uid: str = ""
    uid_number: str = ""
    user_password: str = ""


class OntapLdapSchemaRfc2307Cn(OntapModel):
    """OntapLdapSchemaRfc2307Cn sub-model for cn."""

    group: str = ""
    netgroup: str = ""


class OntapLdapSchemaRfc2307Member(OntapModel):
    """OntapLdapSchemaRfc2307Member sub-model for member."""

    nis_netgroup: str = ""
    uid: str = ""


class OntapLdapSchemaRfc2307Nis(OntapModel):
    """OntapLdapSchemaRfc2307Nis sub-model for nis."""

    mapentry: str = ""
    mapname: str = ""
    netgroup: str = ""
    netgroup_triple: str = ""
    object: str = ""


class OntapLdapSchemaRfc2307Posix(OntapModel):
    """OntapLdapSchemaRfc2307Posix sub-model for posix."""

    account: str = ""
    group: str = ""


class OntapLdapSchemaRfc2307(OntapModel):
    """OntapLdapSchemaRfc2307 sub-model for rfc2307."""

    attribute: OntapLdapSchemaRfc2307Attribute = Field(
        default_factory=OntapLdapSchemaRfc2307Attribute
    )
    cn: OntapLdapSchemaRfc2307Cn = Field(default_factory=OntapLdapSchemaRfc2307Cn)
    member: OntapLdapSchemaRfc2307Member = Field(default_factory=OntapLdapSchemaRfc2307Member)
    nis: OntapLdapSchemaRfc2307Nis = Field(default_factory=OntapLdapSchemaRfc2307Nis)
    posix: OntapLdapSchemaRfc2307Posix = Field(default_factory=OntapLdapSchemaRfc2307Posix)


class OntapLdapSchemaRfc2307bis(OntapModel):
    """OntapLdapSchemaRfc2307bis sub-model for rfc2307bis."""

    enabled: bool = False
    group_of_unique_names: str = ""
    maximum_groups: int = 0
    unique_member: str = ""


class OntapLdapSchemaTemplate(OntapModel):
    """OntapLdapSchemaTemplate sub-model for template."""

    name: str = ""


class OntapLdapSchema(OntapModel):
    """OntapLdapSchema information."""

    comment: str = ""
    global_schema: bool = False
    name: str = ""
    name_mapping: OntapLdapSchemaNameMapping = Field(default_factory=OntapLdapSchemaNameMapping)
    owner: OntapLdapSchemaOwner = Field(default_factory=OntapLdapSchemaOwner)
    rfc2307: OntapLdapSchemaRfc2307 = Field(default_factory=OntapLdapSchemaRfc2307)
    rfc2307bis: OntapLdapSchemaRfc2307bis = Field(default_factory=OntapLdapSchemaRfc2307bis)
    scope: str = ""
    template: OntapLdapSchemaTemplate = Field(default_factory=OntapLdapSchemaTemplate)
