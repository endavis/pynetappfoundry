"""OntapShelf type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.shelves.model import (
    OntapShelf,
    OntapShelfAcp,
    OntapShelfBay,
    OntapShelfCurrentSensor,
    OntapShelfDrawer,
    OntapShelfFan,
    OntapShelfFru,
    OntapShelfPath,
    OntapShelfPort,
    OntapShelfTemperatureSensor,
    OntapShelfVoltageSensor,
)


def _transform_acps(record: dict[str, Any]) -> list[OntapShelfAcp]:
    """Transform acps into OntapShelfAcp list."""
    return [OntapShelfAcp(**item) for item in record.get("acps", [])]


def _transform_bays(record: dict[str, Any]) -> list[OntapShelfBay]:
    """Transform bays into OntapShelfBay list."""
    return [OntapShelfBay(**item) for item in record.get("bays", [])]


def _transform_current_sensors(record: dict[str, Any]) -> list[OntapShelfCurrentSensor]:
    """Transform current_sensors into OntapShelfCurrentSensor list."""
    return [OntapShelfCurrentSensor(**item) for item in record.get("current_sensors", [])]


def _transform_drawers(record: dict[str, Any]) -> list[OntapShelfDrawer]:
    """Transform drawers into OntapShelfDrawer list."""
    return [OntapShelfDrawer(**item) for item in record.get("drawers", [])]


def _transform_fans(record: dict[str, Any]) -> list[OntapShelfFan]:
    """Transform fans into OntapShelfFan list."""
    return [OntapShelfFan(**item) for item in record.get("fans", [])]


def _transform_frus(record: dict[str, Any]) -> list[OntapShelfFru]:
    """Transform frus into OntapShelfFru list."""
    return [OntapShelfFru(**item) for item in record.get("frus", [])]


def _transform_paths(record: dict[str, Any]) -> list[OntapShelfPath]:
    """Transform paths into OntapShelfPath list."""
    return [OntapShelfPath(**item) for item in record.get("paths", [])]


def _transform_ports(record: dict[str, Any]) -> list[OntapShelfPort]:
    """Transform ports into OntapShelfPort list."""
    return [OntapShelfPort(**item) for item in record.get("ports", [])]


def _transform_temperature_sensors(record: dict[str, Any]) -> list[OntapShelfTemperatureSensor]:
    """Transform temperature_sensors into OntapShelfTemperatureSensor list."""
    return [OntapShelfTemperatureSensor(**item) for item in record.get("temperature_sensors", [])]


def _transform_voltage_sensors(record: dict[str, Any]) -> list[OntapShelfVoltageSensor]:
    """Transform voltage_sensors into OntapShelfVoltageSensor list."""
    return [OntapShelfVoltageSensor(**item) for item in record.get("voltage_sensors", [])]


ONTAPSHELF_MAPPING = TypeMapping(
    name="OntapShelf",
    model_class=OntapShelf,
    api_endpoint="/storage/shelves?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="acps",
            api_path="acps",
            transform=_transform_acps,
            default=[],
        ),
        FieldMapping(
            cache_attr="bays",
            api_path="bays",
            transform=_transform_bays,
            default=[],
        ),
        FieldMapping(
            cache_attr="connection_type",
            api_path="connection_type",
        ),
        FieldMapping(
            cache_attr="current_sensors",
            api_path="current_sensors",
            transform=_transform_current_sensors,
            default=[],
        ),
        FieldMapping(
            cache_attr="disk_count",
            api_path="disk_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="drawers",
            api_path="drawers",
            transform=_transform_drawers,
            default=[],
        ),
        FieldMapping(
            cache_attr="errors",
            api_path="errors",
            default=[],
        ),
        FieldMapping(
            cache_attr="fans",
            api_path="fans",
            transform=_transform_fans,
            default=[],
        ),
        FieldMapping(
            cache_attr="frus",
            api_path="frus",
            transform=_transform_frus,
            default=[],
        ),
        FieldMapping(
            cache_attr="id",
            api_path="id",
        ),
        FieldMapping(
            cache_attr="internal",
            api_path="internal",
            default=False,
        ),
        FieldMapping(
            cache_attr="local",
            api_path="local",
            default=False,
        ),
        FieldMapping(
            cache_attr="location_led",
            api_path="location_led",
        ),
        FieldMapping(
            cache_attr="manufacturer.name",
            api_path="manufacturer.name",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="module_type",
            api_path="module_type",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="paths",
            api_path="paths",
            transform=_transform_paths,
            default=[],
        ),
        FieldMapping(
            cache_attr="ports",
            api_path="ports",
            transform=_transform_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="temperature_sensors",
            api_path="temperature_sensors",
            transform=_transform_temperature_sensors,
            default=[],
        ),
        FieldMapping(
            cache_attr="uid",
            api_path="uid",
        ),
        FieldMapping(
            cache_attr="vendor.manufacturer",
            api_path="vendor.manufacturer",
        ),
        FieldMapping(
            cache_attr="vendor.name",
            api_path="vendor.name",
        ),
        FieldMapping(
            cache_attr="vendor.part_number",
            api_path="vendor.part_number",
        ),
        FieldMapping(
            cache_attr="vendor.product",
            api_path="vendor.product",
        ),
        FieldMapping(
            cache_attr="vendor.serial_number",
            api_path="vendor.serial_number",
        ),
        FieldMapping(
            cache_attr="voltage_sensors",
            api_path="voltage_sensors",
            transform=_transform_voltage_sensors,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapShelf", ONTAPSHELF_MAPPING)
