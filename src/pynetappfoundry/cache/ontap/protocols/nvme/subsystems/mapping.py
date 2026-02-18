"""OntapNvmeSubsystem type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.nvme.subsystems.model import (
    OntapNvmeSubsystem,
    OntapNvmeSubsystemHost,
    OntapNvmeSubsystemSubsystemMap,
)


def _transform_hosts(record: dict[str, Any]) -> list[OntapNvmeSubsystemHost]:
    """Transform hosts into OntapNvmeSubsystemHost list."""
    return [OntapNvmeSubsystemHost(**item) for item in record.get("hosts", [])]


def _transform_subsystem_maps(record: dict[str, Any]) -> list[OntapNvmeSubsystemSubsystemMap]:
    """Transform subsystem_maps into OntapNvmeSubsystemSubsystemMap list."""
    return [OntapNvmeSubsystemSubsystemMap(**item) for item in record.get("subsystem_maps", [])]


ONTAPNVMESUBSYSTEM_MAPPING = TypeMapping(
    name="OntapNvmeSubsystem",
    model_class=OntapNvmeSubsystem,
    api_endpoint="/protocols/nvme/subsystems?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="delete_on_unmap",
            api_path="delete_on_unmap",
            default=False,
        ),
        FieldMapping(
            cache_attr="hosts",
            transform=_transform_hosts,
            default=[],
        ),
        FieldMapping(
            cache_attr="io_queue_default_count",
            api_path="io_queue.default.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="io_queue_default_depth",
            api_path="io_queue.default.depth",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="os_type",
            api_path="os_type",
        ),
        FieldMapping(
            cache_attr="serial_number",
            api_path="serial_number",
        ),
        FieldMapping(
            cache_attr="subsystem_maps",
            transform=_transform_subsystem_maps,
            default=[],
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
            cache_attr="target_nqn",
            api_path="target_nqn",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="vendor_uuids",
            api_path="vendor_uuids",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapNvmeSubsystem", ONTAPNVMESUBSYSTEM_MAPPING)
