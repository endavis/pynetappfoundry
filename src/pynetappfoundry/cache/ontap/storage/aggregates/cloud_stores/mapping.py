"""OntapCloudStore type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.aggregates.cloud_stores.model import OntapCloudStore

ONTAPCLOUDSTORE_MAPPING = TypeMapping(
    name="OntapCloudStore",
    model_class=OntapCloudStore,
    api_endpoint="/storage/aggregates/{aggregate.uuid}/cloud-stores?fields=*",
    api_type="ontap",
    parent_mapping="OntapAggregate",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="aggregate.name",
        ),
        FieldMapping(
            cache_attr="availability",
        ),
        FieldMapping(
            cache_attr="availability_at_partner",
        ),
        FieldMapping(
            cache_attr="mirror_degraded",
            default=False,
        ),
        FieldMapping(
            cache_attr="primary",
            default=False,
        ),
        FieldMapping(
            cache_attr="resync_progress",
            api_path="resync-progress",
            default=0,
        ),
        FieldMapping(
            cache_attr="target.name",
        ),
        FieldMapping(
            cache_attr="target.uuid",
        ),
        FieldMapping(
            cache_attr="unavailable_reason.message",
        ),
        FieldMapping(
            cache_attr="unreclaimed_space_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="used",
            default=0,
        ),
    ),
)

model_registry.register_mapping("OntapCloudStore", ONTAPCLOUDSTORE_MAPPING)
