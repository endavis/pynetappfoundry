"""OntapFileDirectorySecurity type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.file_security.permissions.model import (
    OntapFileDirectorySecurity,
    OntapFileDirectorySecurityAcl,
)


def _transform_acls(record: dict[str, Any]) -> list[OntapFileDirectorySecurityAcl]:
    """Transform acls into OntapFileDirectorySecurityAcl list."""
    return [OntapFileDirectorySecurityAcl(**item) for item in record.get("acls", [])]


ONTAPFILEDIRECTORYSECURITY_MAPPING = TypeMapping(
    name="OntapFileDirectorySecurity",
    model_class=OntapFileDirectorySecurity,
    api_endpoint="/protocols/file-security/permissions/{svm.uuid}/{path}?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="access_control",
        ),
        FieldMapping(
            cache_attr="acls",
            transform=_transform_acls,
            default=[],
        ),
        FieldMapping(
            cache_attr="control_flags",
        ),
        FieldMapping(
            cache_attr="dos_attributes",
        ),
        FieldMapping(
            cache_attr="effective_style",
        ),
        FieldMapping(
            cache_attr="group",
        ),
        FieldMapping(
            cache_attr="group_id",
        ),
        FieldMapping(
            cache_attr="ignore_paths",
            default=[],
        ),
        FieldMapping(
            cache_attr="inode",
            default=0,
        ),
        FieldMapping(
            cache_attr="mode_bits",
            default=0,
        ),
        FieldMapping(
            cache_attr="owner",
        ),
        FieldMapping(
            cache_attr="propagation_mode",
        ),
        FieldMapping(
            cache_attr="security_style",
        ),
        FieldMapping(
            cache_attr="text_dos_attr",
        ),
        FieldMapping(
            cache_attr="text_mode_bits",
        ),
        FieldMapping(
            cache_attr="user_id",
        ),
    ),
)

model_registry.register_mapping("OntapFileDirectorySecurity", ONTAPFILEDIRECTORYSECURITY_MAPPING)
