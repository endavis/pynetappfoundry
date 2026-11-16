"""AiqumSvmMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.svm.svms.metrics.model import (
    AiqumSvmMetricsSampleResponse,
)

AIQUMSVMMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumSvmMetricsSampleResponse",
    model_class=AiqumSvmMetricsSampleResponse,
    api_endpoint="/datacenter/svm/svms/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumSvm",
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
            cache_attr="summary.iops",
        ),
        FieldMapping(
            cache_attr="summary.latency",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumSvmMetricsSampleResponse", AIQUMSVMMETRICSSAMPLERESPONSE_MAPPING
)
