"""OntapClusterSpace type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.cluster.model import (
    OntapClusterSpace,
    OntapClusterSpaceMedia,
)


def _transform_block_storage_medias(record: dict[str, Any]) -> list[OntapClusterSpaceMedia]:
    """Transform block_storage.medias into OntapClusterSpaceMedia list."""
    return [OntapClusterSpaceMedia(**item) for item in record.get("block_storage.medias", [])]


ONTAPCLUSTERSPACE_MAPPING = TypeMapping(
    name="OntapClusterSpace",
    model_class=OntapClusterSpace,
    api_endpoint="/storage/cluster?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="block_storage_available",
            api_path="block_storage.available",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage_inactive_data",
            api_path="block_storage.inactive_data",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage_medias",
            api_path="block_storage.medias",
            transform=_transform_block_storage_medias,
            default=[],
        ),
        FieldMapping(
            cache_attr="block_storage_physical_used",
            api_path="block_storage.physical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage_size",
            api_path="block_storage.size",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage_used",
            api_path="block_storage.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="cloud_storage_used",
            api_path="cloud_storage.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_logical_used",
            api_path="efficiency.logical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_ratio",
            api_path="efficiency.ratio",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_savings",
            api_path="efficiency.savings",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_logical_used",
            api_path="efficiency_without_snapshots.logical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_ratio",
            api_path="efficiency_without_snapshots.ratio",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_savings",
            api_path="efficiency_without_snapshots.savings",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones_logical_used",
            api_path="efficiency_without_snapshots_flexclones.logical_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones_ratio",
            api_path="efficiency_without_snapshots_flexclones.ratio",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones_savings",
            api_path="efficiency_without_snapshots_flexclones.savings",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterSpace", ONTAPCLUSTERSPACE_MAPPING)
