"""OntapNetbios type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.cifs.netbios.model import OntapNetbios, OntapNetbiosWinsServer


def _transform_wins_servers(record: dict[str, Any]) -> list[OntapNetbiosWinsServer]:
    """Transform wins_servers into OntapNetbiosWinsServer list."""
    return [OntapNetbiosWinsServer(**item) for item in record.get("wins_servers", [])]


ONTAPNETBIOS_MAPPING = TypeMapping(
    name="OntapNetbios",
    model_class=OntapNetbios,
    api_endpoint="/protocols/cifs/netbios?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="interfaces",
            api_path="interfaces",
            default=[],
        ),
        FieldMapping(
            cache_attr="mode",
            api_path="mode",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="name_registration_type",
            api_path="name_registration_type",
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
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="suffix",
            api_path="suffix",
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
            cache_attr="time_left",
            api_path="time_left",
            default=0,
        ),
        FieldMapping(
            cache_attr="wins_servers",
            transform=_transform_wins_servers,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapNetbios", ONTAPNETBIOS_MAPPING)
