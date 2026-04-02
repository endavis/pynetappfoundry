"""OntapClusterSpace type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.cluster.model import (
    OntapClusterSpace,
    OntapClusterSpaceBlockStorageMedia,
)
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_block_storage_medias(
    record: dict[str, Any],
) -> list[OntapClusterSpaceBlockStorageMedia]:
    """Transform block_storage.medias into OntapClusterSpaceBlockStorageMedia list."""
    try:
        items = get_nested_value(record, "block_storage.medias")
    except Exception:
        items = []
    return [OntapClusterSpaceBlockStorageMedia(**item) for item in items]


ONTAPCLUSTERSPACE_MAPPING = TypeMapping(
    name="OntapClusterSpace",
    model_class=OntapClusterSpace,
    api_endpoint="/storage/cluster?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="block_storage.available",
            api_path="block_storage.available",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.inactive_data",
            api_path="block_storage.inactive_data",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.medias",
            api_path="block_storage.medias",
            transform=_transform_block_storage_medias,
            default=[],
        ),
        FieldMapping(
            cache_attr="block_storage.physical_used",
            api_path="block_storage.physical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.size",
            api_path="block_storage.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.used",
            api_path="block_storage.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="cloud_storage.used",
            api_path="cloud_storage.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency.logical_used",
            api_path="efficiency.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency.ratio",
            api_path="efficiency.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency.savings",
            api_path="efficiency.savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.logical_used",
            api_path="efficiency_without_snapshots.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.ratio",
            api_path="efficiency_without_snapshots.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.savings",
            api_path="efficiency_without_snapshots.savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.logical_used",
            api_path="efficiency_without_snapshots_flexclones.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.ratio",
            api_path="efficiency_without_snapshots_flexclones.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.savings",
            api_path="efficiency_without_snapshots_flexclones.savings",
            cache_strategy="realtime",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterSpace", ONTAPCLUSTERSPACE_MAPPING)
