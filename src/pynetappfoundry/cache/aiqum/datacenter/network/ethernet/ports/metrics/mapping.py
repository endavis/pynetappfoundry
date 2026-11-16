"""AiqumEthernetPortMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.ethernet.ports.metrics.model import (
    AiqumEthernetPortMetricsSampleResponse,
)

AIQUMETHERNETPORTMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumEthernetPortMetricsSampleResponse",
    model_class=AiqumEthernetPortMetricsSampleResponse,
    api_endpoint="/datacenter/network/ethernet/ports/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumEthernetPort",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="ethernet_port.key",
        ),
        FieldMapping(
            cache_attr="ethernet_port.name",
        ),
        FieldMapping(
            cache_attr="ethernet_port.uuid",
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
            cache_attr="summary.bytes.received",
        ),
        FieldMapping(
            cache_attr="summary.error.received",
        ),
        FieldMapping(
            cache_attr="summary.utilization_percent",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumEthernetPortMetricsSampleResponse", AIQUMETHERNETPORTMETRICSSAMPLERESPONSE_MAPPING
)
