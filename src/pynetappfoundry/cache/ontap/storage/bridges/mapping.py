"""OntapStorageBridge type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.bridges.model import (
    OntapStorageBridge,
    OntapStorageBridgeArgument,
    OntapStorageBridgeError,
    OntapStorageBridgeFcPort,
    OntapStorageBridgePath,
    OntapStorageBridgePowerSupplyUnit,
    OntapStorageBridgeSasPort,
)


def _transform_errors(record: dict[str, Any]) -> list[OntapStorageBridgeError]:
    """Transform errors into OntapStorageBridgeError list."""
    return [OntapStorageBridgeError(**item) for item in record.get("errors", [])]


def _transform_fc_ports(record: dict[str, Any]) -> list[OntapStorageBridgeFcPort]:
    """Transform fc_ports into OntapStorageBridgeFcPort list."""
    return [OntapStorageBridgeFcPort(**item) for item in record.get("fc_ports", [])]


def _transform_last_reboot_reason_arguments(
    record: dict[str, Any],
) -> list[OntapStorageBridgeArgument]:
    """Transform last_reboot.reason.arguments into OntapStorageBridgeArgument list."""
    return [
        OntapStorageBridgeArgument(**item)
        for item in record.get("last_reboot.reason.arguments", [])
    ]


def _transform_paths(record: dict[str, Any]) -> list[OntapStorageBridgePath]:
    """Transform paths into OntapStorageBridgePath list."""
    return [OntapStorageBridgePath(**item) for item in record.get("paths", [])]


def _transform_power_supply_units(
    record: dict[str, Any],
) -> list[OntapStorageBridgePowerSupplyUnit]:
    """Transform power_supply_units into OntapStorageBridgePowerSupplyUnit list."""
    return [
        OntapStorageBridgePowerSupplyUnit(**item) for item in record.get("power_supply_units", [])
    ]


def _transform_sas_ports(record: dict[str, Any]) -> list[OntapStorageBridgeSasPort]:
    """Transform sas_ports into OntapStorageBridgeSasPort list."""
    return [OntapStorageBridgeSasPort(**item) for item in record.get("sas_ports", [])]


ONTAPSTORAGEBRIDGE_MAPPING = TypeMapping(
    name="OntapStorageBridge",
    model_class=OntapStorageBridge,
    api_endpoint="/storage/bridges?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="chassis_throughput_state",
            api_path="chassis_throughput_state",
        ),
        FieldMapping(
            cache_attr="dram_single_bit_error_count",
            api_path="dram_single_bit_error_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="errors",
            api_path="errors",
            transform=_transform_errors,
            default=[],
        ),
        FieldMapping(
            cache_attr="fc_ports",
            api_path="fc_ports",
            transform=_transform_fc_ports,
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
            cache_attr="last_reboot_reason_arguments",
            api_path="last_reboot.reason.arguments",
            transform=_transform_last_reboot_reason_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="last_reboot_reason_code",
            api_path="last_reboot.reason.code",
        ),
        FieldMapping(
            cache_attr="last_reboot_reason_message",
            api_path="last_reboot.reason.message",
        ),
        FieldMapping(
            cache_attr="last_reboot_time",
            api_path="last_reboot.time",
        ),
        FieldMapping(
            cache_attr="managed_by",
            api_path="managed_by",
        ),
        FieldMapping(
            cache_attr="model_",
            api_path="model",
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
            api_path="paths",
            transform=_transform_paths,
            default=[],
        ),
        FieldMapping(
            cache_attr="power_supply_units",
            api_path="power_supply_units",
            transform=_transform_power_supply_units,
            default=[],
        ),
        FieldMapping(
            cache_attr="sas_ports",
            api_path="sas_ports",
            transform=_transform_sas_ports,
            default=[],
        ),
        FieldMapping(
            cache_attr="security_enabled",
            api_path="security_enabled",
            default=False,
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
            cache_attr="symbolic_name",
            api_path="symbolic_name",
        ),
        FieldMapping(
            cache_attr="temperature_sensor_maximum",
            api_path="temperature_sensor.maximum",
            default=0,
        ),
        FieldMapping(
            cache_attr="temperature_sensor_minimum",
            api_path="temperature_sensor.minimum",
            default=0,
        ),
        FieldMapping(
            cache_attr="temperature_sensor_name",
            api_path="temperature_sensor.name",
        ),
        FieldMapping(
            cache_attr="temperature_sensor_reading",
            api_path="temperature_sensor.reading",
            default=0,
        ),
        FieldMapping(
            cache_attr="temperature_sensor_state",
            api_path="temperature_sensor.state",
        ),
        FieldMapping(
            cache_attr="vendor",
            api_path="vendor",
        ),
        FieldMapping(
            cache_attr="wwn",
            api_path="wwn",
        ),
    ),
)

model_registry.register_mapping("OntapStorageBridge", ONTAPSTORAGEBRIDGE_MAPPING)
