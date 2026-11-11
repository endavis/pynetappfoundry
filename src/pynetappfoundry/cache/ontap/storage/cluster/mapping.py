"""OntapClusterSpace type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.cluster.model import (
    OntapClusterSpace,
    OntapClusterSpaceBlockStorageMedia,
)

ONTAPCLUSTERSPACE_MAPPING = TypeMapping(
    name="OntapClusterSpace",
    model_class=OntapClusterSpace,
    api_endpoint="/storage/cluster?fields=*",
    api_type="ontap",
    response_shape="singleton",
    fields=(
        FieldMapping(
            cache_attr="block_storage.available",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.inactive_data",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.medias",
            item_model=OntapClusterSpaceBlockStorageMedia,
            default=[],
        ),
        FieldMapping(
            cache_attr="block_storage.physical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.size",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="block_storage.used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="cloud_storage.used",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency.savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots.savings",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.logical_used",
            cache_strategy="realtime",
            default=0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.ratio",
            cache_strategy="realtime",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="efficiency_without_snapshots_flexclones.savings",
            cache_strategy="realtime",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapClusterSpace", ONTAPCLUSTERSPACE_MAPPING)
