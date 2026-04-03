"""OntapCifsSession type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.sessions.model import (
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
        ),
        FieldMapping(
            cache_attr="client_ip",
        ),
        FieldMapping(
            cache_attr="connected_duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="connection_count",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="connection_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="continuous_availability",
        ),
        FieldMapping(
            cache_attr="identifier",
            default=0,
        ),
        FieldMapping(
            cache_attr="idle_duration",
            cache_strategy="realtime",
        ),
        FieldMapping(
            cache_attr="large_mtu",
            default=False,
        ),
        FieldMapping(
            cache_attr="mapped_unix_user",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="open_files",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="open_other",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="open_shares",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="server_ip",
        ),
        FieldMapping(
            cache_attr="smb_encryption",
        ),
        FieldMapping(
            cache_attr="smb_signing",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="user",
        ),
        FieldMapping(
            cache_attr="volumes",
            transform=_transform_volumes,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapCifsSession", ONTAPCIFSSESSION_MAPPING)
