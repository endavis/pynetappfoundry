"""AiqumNetworkFcInterfaceAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.interfaces.analytics.model import (
    AiqumNetworkFcInterfaceAnalytics,
)

AIQUMNETWORKFCINTERFACEANALYTICS_MAPPING = TypeMapping(
    name="AiqumNetworkFcInterfaceAnalytics",
    model_class=AiqumNetworkFcInterfaceAnalytics,
    api_endpoint="/datacenter/network/fc/interfaces/analytics",
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
            cache_attr="fc_interface.key",
        ),
        FieldMapping(
            cache_attr="fc_interface.name",
        ),
        FieldMapping(
            cache_attr="fc_interface.uuid",
        ),
        FieldMapping(
            cache_attr="iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="latency",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="period",
            default=0,
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
        FieldMapping(
            cache_attr="throughput",
            default=0.0,
        ),
    ),
)

model_registry.register_mapping(
    "AiqumNetworkFcInterfaceAnalytics", AIQUMNETWORKFCINTERFACEANALYTICS_MAPPING
)
