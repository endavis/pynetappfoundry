"""OntapCifsSession type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.cifs.sessions.model import (
    OntapCifsSession,
    OntapCifsSessionVolume,
)


def _transform_volumes(record: dict[str, Any]) -> list[OntapCifsSessionVolume]:
    """Transform volumes into OntapCifsSessionVolume list."""
    return [OntapCifsSessionVolume(**item) for item in record.get("volumes", [])]


ONTAPCIFSSESSION_MAPPING = TypeMapping(
    name="OntapCifsSession",
    model_class=OntapCifsSession,
    api_endpoint="/protocols/cifs/sessions?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication",
            api_path="authentication",
        ),
        FieldMapping(
            cache_attr="client_ip",
            api_path="client_ip",
        ),
        FieldMapping(
            cache_attr="connected_duration",
            api_path="connected_duration",
        ),
        FieldMapping(
            cache_attr="connection_count",
            api_path="connection_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="connection_id",
            api_path="connection_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="continuous_availability",
            api_path="continuous_availability",
        ),
        FieldMapping(
            cache_attr="identifier",
            api_path="identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="idle_duration",
            api_path="idle_duration",
        ),
        FieldMapping(
            cache_attr="large_mtu",
            api_path="large_mtu",
            default=False,
        ),
        FieldMapping(
            cache_attr="mapped_unix_user",
            api_path="mapped_unix_user",
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
            cache_attr="open_files",
            api_path="open_files",
            default=0,
        ),
        FieldMapping(
            cache_attr="open_other",
            api_path="open_other",
            default=0,
        ),
        FieldMapping(
            cache_attr="open_shares",
            api_path="open_shares",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol",
            api_path="protocol",
        ),
        FieldMapping(
            cache_attr="server_ip",
            api_path="server_ip",
        ),
        FieldMapping(
            cache_attr="smb_encryption",
            api_path="smb_encryption",
        ),
        FieldMapping(
            cache_attr="smb_signing",
            api_path="smb_signing",
            default=False,
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
            cache_attr="user",
            api_path="user",
        ),
        FieldMapping(
            cache_attr="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCifsSession", ONTAPCIFSSESSION_MAPPING)
