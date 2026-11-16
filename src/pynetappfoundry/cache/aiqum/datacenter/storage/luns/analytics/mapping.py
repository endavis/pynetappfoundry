"""AiqumLunAnalytics type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.storage.luns.analytics.model import AiqumLunAnalytics

AIQUMLUNANALYTICS_MAPPING = TypeMapping(
    name="AiqumLunAnalytics",
    model_class=AiqumLunAnalytics,
    api_endpoint="/datacenter/storage/luns/analytics",
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
            cache_attr="iops",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="latency",
            default=0.0,
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

model_registry.register_mapping("AiqumLunAnalytics", AIQUMLUNANALYTICS_MAPPING)
