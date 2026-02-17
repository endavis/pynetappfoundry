# ruff: noqa: E501
"""OntapSnapmirrorTransfer type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.snapmirror.relationships.transfers.model import (
    OntapSnapmirrorTransfer,
    OntapSnapmirrorTransferConsistencyGroupVolume,
    OntapSnapmirrorTransferFile,
)


def _transform_files(record: dict[str, Any]) -> list[OntapSnapmirrorTransferFile]:
    """Transform files into OntapSnapmirrorTransferFile list."""
    return [OntapSnapmirrorTransferFile(**item) for item in record.get("files", [])]


def _transform_relationship_destination_consistency_group_volumes(
    record: dict[str, Any],
) -> list[OntapSnapmirrorTransferConsistencyGroupVolume]:
    """Transform relationship.destination.consistency_group_volumes into OntapSnapmirrorTransferConsistencyGroupVolume list."""
    return [
        OntapSnapmirrorTransferConsistencyGroupVolume(**item)
        for item in record.get("relationship.destination.consistency_group_volumes", [])
    ]


ONTAPSNAPMIRRORTRANSFER_MAPPING = TypeMapping(
    name="OntapSnapmirrorTransfer",
    model_class=OntapSnapmirrorTransfer,
    api_endpoint="/snapmirror/relationships/{relationship.uuid}/transfers?fields=*",
    api_type="ontap",
    parent_mapping="OntapSnapmirrorRelationship",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="bytes_transferred",
            api_path="bytes_transferred",
            default=0,
        ),
        FieldMapping(
            cache_attr="checkpoint_size",
            api_path="checkpoint_size",
            default=0,
        ),
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="error_info_code",
            api_path="error_info.code",
            default=0,
        ),
        FieldMapping(
            cache_attr="error_info_message",
            api_path="error_info.message",
        ),
        FieldMapping(
            cache_attr="files",
            transform=_transform_files,
            default=[],
        ),
        FieldMapping(
            cache_attr="last_updated_time",
            api_path="last_updated_time",
        ),
        FieldMapping(
            cache_attr="network_compression_ratio",
            api_path="network_compression_ratio",
        ),
        FieldMapping(
            cache_attr="on_demand_attrs",
            api_path="on_demand_attrs",
        ),
        FieldMapping(
            cache_attr="options",
            api_path="options",
            default=[],
        ),
        FieldMapping(
            cache_attr="relationship_destination_cluster_name",
            api_path="relationship.destination.cluster.name",
        ),
        FieldMapping(
            cache_attr="relationship_destination_cluster_uuid",
            api_path="relationship.destination.cluster.uuid",
        ),
        FieldMapping(
            cache_attr="relationship_destination_consistency_group_volumes",
            transform=_transform_relationship_destination_consistency_group_volumes,
            default=[],
        ),
        FieldMapping(
            cache_attr="relationship_destination_ipspace",
            api_path="relationship.destination.ipspace",
        ),
        FieldMapping(
            cache_attr="relationship_destination_luns_name",
            api_path="relationship.destination.luns.name",
        ),
        FieldMapping(
            cache_attr="relationship_destination_luns_uuid",
            api_path="relationship.destination.luns.uuid",
        ),
        FieldMapping(
            cache_attr="relationship_destination_path",
            api_path="relationship.destination.path",
        ),
        FieldMapping(
            cache_attr="relationship_destination_svm_name",
            api_path="relationship.destination.svm.name",
        ),
        FieldMapping(
            cache_attr="relationship_destination_svm_uuid",
            api_path="relationship.destination.svm.uuid",
        ),
        FieldMapping(
            cache_attr="relationship_restore",
            api_path="relationship.restore",
            default=False,
        ),
        FieldMapping(
            cache_attr="relationship_uuid",
            api_path="relationship.uuid",
        ),
        FieldMapping(
            cache_attr="snapshot",
            api_path="snapshot",
        ),
        FieldMapping(
            cache_attr="source_snapshot",
            api_path="source_snapshot",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
        ),
        FieldMapping(
            cache_attr="storage_efficiency_enabled",
            api_path="storage_efficiency_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="throttle",
            api_path="throttle",
            default=0,
        ),
        FieldMapping(
            cache_attr="total_duration",
            api_path="total_duration",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSnapmirrorTransfer", ONTAPSNAPMIRRORTRANSFER_MAPPING)
