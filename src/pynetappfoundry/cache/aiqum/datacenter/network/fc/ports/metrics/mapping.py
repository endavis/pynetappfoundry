"""AiqumFcPortMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.ports.metrics.model import (
    AiqumFcPortMetricsSampleResponse,
)

AIQUMFCPORTMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumFcPortMetricsSampleResponse",
    model_class=AiqumFcPortMetricsSampleResponse,
    api_endpoint="/datacenter/network/fc/ports/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumFcPort",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="fc_port.key",
        ),
        FieldMapping(
            cache_attr="fc_port.name",
        ),
        FieldMapping(
            cache_attr="fc_port.uuid",
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
            cache_attr="summary.throughput",
        ),
        FieldMapping(
            cache_attr="summary.utilization_percent",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumFcPortMetricsSampleResponse", AIQUMFCPORTMETRICSSAMPLERESPONSE_MAPPING
)
