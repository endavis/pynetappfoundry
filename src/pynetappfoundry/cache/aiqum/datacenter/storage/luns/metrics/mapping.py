"""AiqumLunMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.luns.metrics.model import (
    AiqumLunMetricsSampleResponse,
)

AIQUMLUNMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumLunMetricsSampleResponse",
    model_class=AiqumLunMetricsSampleResponse,
    api_endpoint="/datacenter/storage/luns/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumLun",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="lun.key",
        ),
        FieldMapping(
            cache_attr="lun.name",
        ),
        FieldMapping(
            cache_attr="lun.uuid",
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
            cache_attr="summary.iops",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumLunMetricsSampleResponse", AIQUMLUNMETRICSSAMPLERESPONSE_MAPPING
)
