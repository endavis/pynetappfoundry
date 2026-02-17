"""OntapLocalCifsUsersAndGroupsImport type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.cifs.users_and_groups.bulk_import.model import (
    OntapLocalCifsUsersAndGroupsImport,
)

ONTAPLOCALCIFSUSERSANDGROUPSIMPORT_MAPPING = TypeMapping(
    name="OntapLocalCifsUsersAndGroupsImport",
    model_class=OntapLocalCifsUsersAndGroupsImport,
    api_endpoint="/protocols/cifs/users-and-groups/bulk-import/{svm.uuid}?fields=*",
    api_type="ontap",
    parent_mapping="OntapProtocolsCifsUsersAndGroupsBulkImport",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="decryption_password",
            api_path="decryption_password",
        ),
        FieldMapping(
            cache_attr="detailed_status_code",
            api_path="detailed_status.code",
        ),
        FieldMapping(
            cache_attr="detailed_status_message",
            api_path="detailed_status.message",
        ),
        FieldMapping(
            cache_attr="elements_ignored",
            api_path="elements_ignored",
            default=0,
        ),
        FieldMapping(
            cache_attr="elements_imported",
            api_path="elements_imported",
            default=0,
        ),
        FieldMapping(
            cache_attr="import_uri_password",
            api_path="import_uri.password",
        ),
        FieldMapping(
            cache_attr="import_uri_path",
            api_path="import_uri.path",
        ),
        FieldMapping(
            cache_attr="import_uri_username",
            api_path="import_uri.username",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="status_uri_password",
            api_path="status_uri.password",
        ),
        FieldMapping(
            cache_attr="status_uri_path",
            api_path="status_uri.path",
        ),
        FieldMapping(
            cache_attr="status_uri_username",
            api_path="status_uri.username",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapLocalCifsUsersAndGroupsImport", ONTAPLOCALCIFSUSERSANDGROUPSIMPORT_MAPPING
)
