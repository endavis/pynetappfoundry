"""OntapFileDirectorySecurity type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.file_security.permissions.model import (
    OntapFileDirectorySecurity,
)

ONTAPFILEDIRECTORYSECURITY_MAPPING = TypeMapping(
    name="OntapFileDirectorySecurity",
    model_class=OntapFileDirectorySecurity,
    api_endpoint="/protocols/file-security/permissions/{svm.uuid}/{path}?fields=*",
    api_type="ontap",
    records_path="acls",
    fields=(
        FieldMapping(
            cache_attr="access",
        ),
        FieldMapping(
            cache_attr="access_control",
        ),
        FieldMapping(
            cache_attr="advanced_rights.append_data",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.delete",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.delete_child",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.execute_file",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.full_control",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.read_attr",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.read_data",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.read_ea",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.read_perm",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.synchronize",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.write_attr",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.write_data",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.write_ea",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.write_owner",
            default=False,
        ),
        FieldMapping(
            cache_attr="advanced_rights.write_perm",
            default=False,
        ),
        FieldMapping(
            cache_attr="apply_to.files",
            default=False,
        ),
        FieldMapping(
            cache_attr="apply_to.sub_folders",
            default=False,
        ),
        FieldMapping(
            cache_attr="apply_to.this_folder",
            default=False,
        ),
        FieldMapping(
            cache_attr="inherited",
            default=False,
        ),
        FieldMapping(
            cache_attr="rights",
        ),
        FieldMapping(
            cache_attr="user",
        ),
    ),
)

model_registry.register_mapping("OntapFileDirectorySecurity", ONTAPFILEDIRECTORYSECURITY_MAPPING)
