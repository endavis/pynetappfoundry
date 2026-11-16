"""AiqumFcPortAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.ports.analytics.model import (
    AiqumFcPortAnalytics,
)

AIQUMFCPORTANALYTICS_MAPPING = TypeMapping(
    name="AiqumFcPortAnalytics",
    model_class=AiqumFcPortAnalytics,
    api_endpoint="/datacenter/network/fc/ports/analytics",
    api_type="aiqum",
    fields=(
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
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
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="period",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="utilization_percent",
            default=0.0,
        ),
    ),
)

model_registry.register_mapping("AiqumFcPortAnalytics", AIQUMFCPORTANALYTICS_MAPPING)
