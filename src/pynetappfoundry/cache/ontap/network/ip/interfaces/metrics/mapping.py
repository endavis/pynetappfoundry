"""OntapInterfaceMetricsResponse type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.network.ip.interfaces.metrics.model import (
    OntapInterfaceMetricsResponse,
)

ONTAPINTERFACEMETRICSRESPONSE_MAPPING = TypeMapping(
    name="OntapInterfaceMetricsResponse",
    model_class=OntapInterfaceMetricsResponse,
    api_endpoint="/network/ip/interfaces/{uuid}/metrics?fields=*",
    api_type="ontap",
    parent_mapping="OntapIpInterface",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="duration",
            api_path="duration",
        ),
        FieldMapping(
            cache_attr="status",
            api_path="status",
        ),
        FieldMapping(
            cache_attr="throughput_read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_total",
            api_path="throughput.total",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="timestamp",
            api_path="timestamp",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping(
    "OntapInterfaceMetricsResponse", ONTAPINTERFACEMETRICSRESPONSE_MAPPING
)
