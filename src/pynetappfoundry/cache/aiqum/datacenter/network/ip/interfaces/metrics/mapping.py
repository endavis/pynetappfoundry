"""AiqumNetworkIpInterfaceMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.ip.interfaces.metrics.model import (
    AiqumNetworkIpInterfaceMetricsSampleResponse,
)

AIQUMNETWORKIPINTERFACEMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumNetworkIpInterfaceMetricsSampleResponse",
    model_class=AiqumNetworkIpInterfaceMetricsSampleResponse,
    api_endpoint="/datacenter/network/ip/interfaces/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumIpInterface",
    parent_id_field="key",
    fields=(
        FieldMapping(
            cache_attr="duration",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="lif.key",
        ),
        FieldMapping(
            cache_attr="lif.name",
        ),
        FieldMapping(
            cache_attr="lif.uuid",
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
            cache_attr="summary.error.received",
        ),
        FieldMapping(
            cache_attr="summary.packets.received",
        ),
        FieldMapping(
            cache_attr="summary.throughput.received",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumNetworkIpInterfaceMetricsSampleResponse",
    AIQUMNETWORKIPINTERFACEMETRICSSAMPLERESPONSE_MAPPING,
)
