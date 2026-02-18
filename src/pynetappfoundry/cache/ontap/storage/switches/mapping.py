"""OntapStorageSwitch type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.switches.model import (
    OntapStorageSwitch,
    OntapStorageSwitchConnection,
    OntapStorageSwitchError,
    OntapStorageSwitchFan,
    OntapStorageSwitchPath,
    OntapStorageSwitchPort,
    OntapStorageSwitchPowerSupplyUnit,
    OntapStorageSwitchTemperatureSensor,
    OntapStorageSwitchVsan,
    OntapStorageSwitchZone,
)


def _transform_connections(record: dict[str, Any]) -> list[OntapStorageSwitchConnection]:
    """Transform connections into OntapStorageSwitchConnection list."""
    return [OntapStorageSwitchConnection(**item) for item in record.get("connections", [])]


def _transform_errors(record: dict[str, Any]) -> list[OntapStorageSwitchError]:
    """Transform errors into OntapStorageSwitchError list."""
    return [OntapStorageSwitchError(**item) for item in record.get("errors", [])]


def _transform_fans(record: dict[str, Any]) -> list[OntapStorageSwitchFan]:
    """Transform fans into OntapStorageSwitchFan list."""
    return [OntapStorageSwitchFan(**item) for item in record.get("fans", [])]


def _transform_paths(record: dict[str, Any]) -> list[OntapStorageSwitchPath]:
    """Transform paths into OntapStorageSwitchPath list."""
    return [OntapStorageSwitchPath(**item) for item in record.get("paths", [])]


def _transform_ports(record: dict[str, Any]) -> list[OntapStorageSwitchPort]:
    """Transform ports into OntapStorageSwitchPort list."""
    return [OntapStorageSwitchPort(**item) for item in record.get("ports", [])]


def _transform_power_supply_units(
    record: dict[str, Any],
) -> list[OntapStorageSwitchPowerSupplyUnit]:
    """Transform power_supply_units into OntapStorageSwitchPowerSupplyUnit list."""
    return [
        OntapStorageSwitchPowerSupplyUnit(**item) for item in record.get("power_supply_units", [])
    ]


def _transform_temperature_sensors(
    record: dict[str, Any],
) -> list[OntapStorageSwitchTemperatureSensor]:
    """Transform temperature_sensors into OntapStorageSwitchTemperatureSensor list."""
    return [
        OntapStorageSwitchTemperatureSensor(**item)
        for item in record.get("temperature_sensors", [])
    ]


def _transform_vsans(record: dict[str, Any]) -> list[OntapStorageSwitchVsan]:
    """Transform vsans into OntapStorageSwitchVsan list."""
    return [OntapStorageSwitchVsan(**item) for item in record.get("vsans", [])]


def _transform_zones(record: dict[str, Any]) -> list[OntapStorageSwitchZone]:
    """Transform zones into OntapStorageSwitchZone list."""
    return [OntapStorageSwitchZone(**item) for item in record.get("zones", [])]


ONTAPSTORAGESWITCH_MAPPING = TypeMapping(
    name="OntapStorageSwitch",
    model_class=OntapStorageSwitch,
    api_endpoint="/storage/switches?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="connections",
            transform=_transform_connections,
            default=[],
        ),
        FieldMapping(
            cache_attr="director_class",
            api_path="director_class",
            default=False,
        ),
        FieldMapping(
            cache_attr="domain_id",
            api_path="domain_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="errors",
            transform=_transform_errors,
            default=[],
        ),
        FieldMapping(
            cache_attr="fabric_name",
            api_path="fabric_name",
        ),
        FieldMapping(
            cache_attr="fans",
            transform=_transform_fans,
            default=[],
        ),
        FieldMapping(
            cache_attr="firmware_version",
            api_path="firmware_version",
        ),
        FieldMapping(
            cache_attr="ip_address",
            api_path="ip_address",
        ),
        FieldMapping(
            cache_attr="local",
            api_path="local",
            default=False,
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
        ),
        FieldMapping(
            cache_attr="monitored_blades",
            api_path="monitored_blades",
            default=[],
        ),
        FieldMapping(
            cache_attr="monitoring_enabled",
            api_path="monitoring_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="paths",
            transform=_transform_paths,
            default=[],
        ),
        FieldMapping(
            cache_attr="ports",
            transform=_transform_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="power_supply_units",
            transform=_transform_power_supply_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="role",
            api_path="role",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="symbolic_name",
            api_path="symbolic_name",
        ),
        FieldMapping(
            cache_attr="temperature_sensors",
            transform=_transform_temperature_sensors,
            default=[],
        ),
        FieldMapping(
            cache_attr="vendor",
            api_path="vendor",
        ),
        FieldMapping(
            cache_attr="vsans",
            transform=_transform_vsans,
            default=[],
        ),
        FieldMapping(
            cache_attr="wwn",
            api_path="wwn",
        ),
        FieldMapping(
            cache_attr="zones",
            transform=_transform_zones,
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapStorageSwitch", ONTAPSTORAGESWITCH_MAPPING)
