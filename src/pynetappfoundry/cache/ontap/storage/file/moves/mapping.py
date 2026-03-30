"""OntapFileMove type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.file.moves.model import (
    OntapFileMove,
    OntapFileMoveArgument,
    OntapFileMoveDestination,
    OntapFileMoveSource,
)


def _transform_failure_arguments(record: dict[str, Any]) -> list[OntapFileMoveArgument]:
    """Transform failure.arguments into OntapFileMoveArgument list."""
    return [OntapFileMoveArgument(**item) for item in record.get("failure.arguments", [])]


def _transform_files_to_move_destinations(record: dict[str, Any]) -> list[OntapFileMoveDestination]:
    """Transform files_to_move.destinations into OntapFileMoveDestination list."""
    return [
        OntapFileMoveDestination(**item) for item in record.get("files_to_move.destinations", [])
    ]


def _transform_files_to_move_sources(record: dict[str, Any]) -> list[OntapFileMoveSource]:
    """Transform files_to_move.sources into OntapFileMoveSource list."""
    return [OntapFileMoveSource(**item) for item in record.get("files_to_move.sources", [])]


ONTAPFILEMOVE_MAPPING = TypeMapping(
    name="OntapFileMove",
    model_class=OntapFileMove,
    api_endpoint="/storage/file/moves?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cutover_time",
            api_path="cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="destination_path",
            api_path="destination.path",
        ),
        FieldMapping(
            cache_attr="destination_svm_name",
            api_path="destination.svm.name",
        ),
        FieldMapping(
            cache_attr="destination_svm_uuid",
            api_path="destination.svm.uuid",
        ),
        FieldMapping(
            cache_attr="destination_volume_name",
            api_path="destination.volume.name",
        ),
        FieldMapping(
            cache_attr="destination_volume_uuid",
            api_path="destination.volume.uuid",
        ),
        FieldMapping(
            cache_attr="elapsed_time",
            api_path="elapsed_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="failure_arguments",
            api_path="failure.arguments",
            transform=_transform_failure_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="failure_code",
            api_path="failure.code",
        ),
        FieldMapping(
            cache_attr="failure_message",
            api_path="failure.message",
        ),
        FieldMapping(
            cache_attr="files_to_move_destinations",
            api_path="files_to_move.destinations",
            transform=_transform_files_to_move_destinations,
            default=[],
        ),
        FieldMapping(
            cache_attr="files_to_move_sources",
            api_path="files_to_move.sources",
            transform=_transform_files_to_move_sources,
            default=[],
        ),
        FieldMapping(
            cache_attr="index",
            api_path="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="is_destination_ready",
            api_path="is_destination_ready",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_flexgroup",
            api_path="is_flexgroup",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_snapshot_fenced",
            api_path="is_snapshot_fenced",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_cutover_time",
            api_path="max_cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="max_throughput",
            api_path="max_throughput",
            default=0,
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
            cache_attr="reference_max_cutover_time",
            api_path="reference.max_cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="reference_path",
            api_path="reference.path",
        ),
        FieldMapping(
            cache_attr="reference_svm_name",
            api_path="reference.svm.name",
        ),
        FieldMapping(
            cache_attr="reference_svm_uuid",
            api_path="reference.svm.uuid",
        ),
        FieldMapping(
            cache_attr="reference_volume_name",
            api_path="reference.volume.name",
        ),
        FieldMapping(
            cache_attr="reference_volume_uuid",
            api_path="reference.volume.uuid",
        ),
        FieldMapping(
            cache_attr="scanner_percent",
            api_path="scanner.percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="scanner_progress",
            api_path="scanner.progress",
            default=0,
        ),
        FieldMapping(
            cache_attr="scanner_state",
            api_path="scanner.state",
        ),
        FieldMapping(
            cache_attr="scanner_total",
            api_path="scanner.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="source_path",
            api_path="source.path",
        ),
        FieldMapping(
            cache_attr="source_svm_name",
            api_path="source.svm.name",
        ),
        FieldMapping(
            cache_attr="source_svm_uuid",
            api_path="source.svm.uuid",
        ),
        FieldMapping(
            cache_attr="source_volume_name",
            api_path="source.volume.name",
        ),
        FieldMapping(
            cache_attr="source_volume_uuid",
            api_path="source.volume.uuid",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFileMove", ONTAPFILEMOVE_MAPPING)
