"""OntapFileMove type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.file.moves.model import (
    OntapFileMove,
    OntapFileMoveFailureArgument,
    OntapFileMoveFilesToMoveDestination,
    OntapFileMoveFilesToMoveSource,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_failure_arguments(record: dict[str, Any]) -> list[OntapFileMoveFailureArgument]:
    """Transform failure.arguments into OntapFileMoveFailureArgument list."""
    try:
        items = get_nested_value(record, "failure.arguments")
    except Exception:
        items = []
    return [OntapFileMoveFailureArgument(**item) for item in items]


def _transform_files_to_move_destinations(
    record: dict[str, Any],
) -> list[OntapFileMoveFilesToMoveDestination]:
    """Transform files_to_move.destinations into OntapFileMoveFilesToMoveDestination list."""
    try:
        items = get_nested_value(record, "files_to_move.destinations")
    except Exception:
        items = []
    return [OntapFileMoveFilesToMoveDestination(**item) for item in items]


def _transform_files_to_move_sources(
    record: dict[str, Any],
) -> list[OntapFileMoveFilesToMoveSource]:
    """Transform files_to_move.sources into OntapFileMoveFilesToMoveSource list."""
    try:
        items = get_nested_value(record, "files_to_move.sources")
    except Exception:
        items = []
    return [OntapFileMoveFilesToMoveSource(**item) for item in items]


ONTAPFILEMOVE_MAPPING = TypeMapping(
    name="OntapFileMove",
    model_class=OntapFileMove,
    api_endpoint="/storage/file/moves?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="destination.path",
        ),
        FieldMapping(
            cache_attr="destination.svm.name",
        ),
        FieldMapping(
            cache_attr="destination.svm.uuid",
        ),
        FieldMapping(
            cache_attr="destination.volume.name",
        ),
        FieldMapping(
            cache_attr="destination.volume.uuid",
        ),
        FieldMapping(
            cache_attr="elapsed_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="failure.arguments",
            transform=_transform_failure_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="failure.code",
        ),
        FieldMapping(
            cache_attr="failure.message",
        ),
        FieldMapping(
            cache_attr="files_to_move.destinations",
            transform=_transform_files_to_move_destinations,
            default=[],
        ),
        FieldMapping(
            cache_attr="files_to_move.sources",
            transform=_transform_files_to_move_sources,
            default=[],
        ),
        FieldMapping(
            cache_attr="index",
            default=0,
        ),
        FieldMapping(
            cache_attr="is_destination_ready",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_flexgroup",
            default=False,
        ),
        FieldMapping(
            cache_attr="is_snapshot_fenced",
            default=False,
        ),
        FieldMapping(
            cache_attr="max_cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="max_throughput",
            default=0,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="reference.max_cutover_time",
            default=0,
        ),
        FieldMapping(
            cache_attr="reference.path",
        ),
        FieldMapping(
            cache_attr="reference.svm.name",
        ),
        FieldMapping(
            cache_attr="reference.svm.uuid",
        ),
        FieldMapping(
            cache_attr="reference.volume.name",
        ),
        FieldMapping(
            cache_attr="reference.volume.uuid",
        ),
        FieldMapping(
            cache_attr="scanner.percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="scanner.progress",
            default=0,
        ),
        FieldMapping(
            cache_attr="scanner.state",
        ),
        FieldMapping(
            cache_attr="scanner.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="source.path",
        ),
        FieldMapping(
            cache_attr="source.svm.name",
        ),
        FieldMapping(
            cache_attr="source.svm.uuid",
        ),
        FieldMapping(
            cache_attr="source.volume.name",
        ),
        FieldMapping(
            cache_attr="source.volume.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFileMove", ONTAPFILEMOVE_MAPPING)
