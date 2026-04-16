"""OntapNvmeSubsystem type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nvme.subsystems.model import (
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
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="comment",
        ),
        FieldMapping(
            cache_attr="delete_on_unmap",
            default=False,
        ),
        FieldMapping(
            cache_attr="hosts",
            transform=_transform_hosts,
            default=[],
        ),
        FieldMapping(
            cache_attr="io_queue.default.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="io_queue.default.depth",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="os_type",
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="subsystem_maps",
            transform=_transform_subsystem_maps,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="target_nqn",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="vendor_uuids",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapNvmeSubsystem", ONTAPNVMESUBSYSTEM_MAPPING)
