"""OntapCifsOpenFile type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.cifs.session.files.model import OntapCifsOpenFile

ONTAPCIFSOPENFILE_MAPPING = TypeMapping(
    name="OntapCifsOpenFile",
    model_class=OntapCifsOpenFile,
    api_endpoint="/protocols/cifs/session/files?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="connection_count",
            api_path="connection.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="connection_identifier",
            api_path="connection.identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="continuously_available",
            api_path="continuously_available",
        ),
        FieldMapping(
            cache_attr="identifier",
            api_path="identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="open_mode",
            api_path="open_mode",
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="range_locks_count",
            api_path="range_locks_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="session_identifier",
            api_path="session.identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="share_mode",
            api_path="share.mode",
        ),
        FieldMapping(
            cache_attr="share_name",
            api_path="share.name",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCifsOpenFile", ONTAPCIFSOPENFILE_MAPPING)
