"""OntapTapeDevice type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.tape_devices.model import (
    OntapTapeDevice,
    OntapTapeDeviceAlias2,
    OntapTapeDeviceDeviceName,
)


def _transform_aliases(record: dict[str, Any]) -> list[OntapTapeDeviceAlias2]:
    """Transform aliases into OntapTapeDeviceAlias2 list."""
    return [OntapTapeDeviceAlias2(**item) for item in record.get("aliases", [])]


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
            cache_attr="alias.mapping",
        ),
        FieldMapping(
            cache_attr="alias.name",
        ),
        FieldMapping(
            cache_attr="aliases",
            transform=_transform_aliases,
            default=[],
        ),
        FieldMapping(
            cache_attr="block_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="density",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="device_id",
        ),
        FieldMapping(
            cache_attr="device_names",
            transform=_transform_device_names,
            default=[],
        ),
        FieldMapping(
            cache_attr="device_state",
        ),
        FieldMapping(
            cache_attr="file_number",
            default=0,
        ),
        FieldMapping(
            cache_attr="formats",
            default=[],
        ),
        FieldMapping(
            cache_attr="interface",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="online",
            default=False,
        ),
        FieldMapping(
            cache_attr="position.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="position.operation",
        ),
        FieldMapping(
            cache_attr="reservation_type",
        ),
        FieldMapping(
            cache_attr="residual_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="storage_port.name",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="wwnn",
        ),
        FieldMapping(
            cache_attr="wwpn",
        ),
    ),
)

model_registry.register_mapping("OntapTapeDevice", ONTAPTAPEDEVICE_MAPPING)
