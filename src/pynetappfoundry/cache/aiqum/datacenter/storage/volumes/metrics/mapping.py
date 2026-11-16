"""AiqumVolumeMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.volumes.metrics.model import (
    AiqumVolumeMetricsSampleResponse,
)

AIQUMVOLUMEMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumVolumeMetricsSampleResponse",
    model_class=AiqumVolumeMetricsSampleResponse,
    api_endpoint="/datacenter/storage/volumes/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumVolume",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="num_samples",
            default=0,
        ),
        FieldMapping(
            cache_attr="samples",
            default=[],
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="summary.cache_miss_ratio",
        ),
        FieldMapping(
            cache_attr="summary.iops",
        ),
        FieldMapping(
            cache_attr="volume.key",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumVolumeMetricsSampleResponse", AIQUMVOLUMEMETRICSSAMPLERESPONSE_MAPPING
)
