"""OntapTapeDevice type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.tape_devices.model import (
    OntapTapeDevice,
    OntapTapeDeviceAlias,
    OntapTapeDeviceDeviceName,
)


def _transform_aliases(record: dict[str, Any]) -> list[OntapTapeDeviceAlias]:
    """Transform aliases into OntapTapeDeviceAlias list."""
    return [OntapTapeDeviceAlias(**item) for item in record.get("aliases", [])]


def _transform_device_names(record: dict[str, Any]) -> list[OntapTapeDeviceDeviceName]:
    """Transform device_names into OntapTapeDeviceDeviceName list."""
    return [OntapTapeDeviceDeviceName(**item) for item in record.get("device_names", [])]


ONTAPTAPEDEVICE_MAPPING = TypeMapping(
    name="OntapTapeDevice",
    model_class=OntapTapeDevice,
    api_endpoint="/storage/tape-devices?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="alias_mapping",
            api_path="alias.mapping",
        ),
        FieldMapping(
            cache_attr="alias_name",
            api_path="alias.name",
        ),
        FieldMapping(
            cache_attr="aliases",
            transform=_transform_aliases,
            default=[],
        ),
        FieldMapping(
            cache_attr="block_number",
            api_path="block_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="density",
            api_path="density",
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="device_id",
            api_path="device_id",
        ),
        FieldMapping(
            cache_attr="device_names",
            transform=_transform_device_names,
            default=[],
        ),
        FieldMapping(
            cache_attr="device_state",
            api_path="device_state",
        ),
        FieldMapping(
            cache_attr="file_number",
            api_path="file_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="formats",
            api_path="formats",
            default=[],
        ),
        FieldMapping(
            cache_attr="interface",
            api_path="interface",
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
            cache_attr="online",
            api_path="online",
            default=False,
        ),
        FieldMapping(
            cache_attr="position_count",
            api_path="position.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="position_operation",
            api_path="position.operation",
        ),
        FieldMapping(
            cache_attr="reservation_type",
            api_path="reservation_type",
        ),
        FieldMapping(
            cache_attr="residual_count",
            api_path="residual_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="storage_port_name",
            api_path="storage_port.name",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="wwnn",
            api_path="wwnn",
        ),
        FieldMapping(
            cache_attr="wwpn",
            api_path="wwpn",
        ),
    ),
)

model_registry.register_mapping("OntapTapeDevice", ONTAPTAPEDEVICE_MAPPING)
