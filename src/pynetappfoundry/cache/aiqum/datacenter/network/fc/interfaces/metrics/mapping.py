"""AiqumNetworkFcInterfaceMetricsSampleResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.interfaces.metrics.model import (
    AiqumNetworkFcInterfaceMetricsSampleResponse,
)

AIQUMNETWORKFCINTERFACEMETRICSSAMPLERESPONSE_MAPPING = TypeMapping(
    name="AiqumNetworkFcInterfaceMetricsSampleResponse",
    model_class=AiqumNetworkFcInterfaceMetricsSampleResponse,
    api_endpoint="/datacenter/network/fc/interfaces/{key}/metrics",
    api_type="aiqum",
    response_shape="singleton",
    parent_mapping="AiqumFcInterface",
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
            cache_attr="summary.iops",
        ),
    ),
)

model_registry.register_mapping(
    "AiqumNetworkFcInterfaceMetricsSampleResponse",
    AIQUMNETWORKFCINTERFACEMETRICSSAMPLERESPONSE_MAPPING,
)
