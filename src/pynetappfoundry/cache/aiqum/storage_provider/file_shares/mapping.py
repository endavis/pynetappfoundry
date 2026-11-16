"""AiqumFileshareGetCollection type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.storage_provider.file_shares.model import (
    AiqumFileshareGetCollection,
)

AIQUMFILESHAREGETCOLLECTION_MAPPING = TypeMapping(
    name="AiqumFileshareGetCollection",
    model_class=AiqumFileshareGetCollection,
    api_endpoint="/storage-provider/file-shares",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="assigned_performance_service_level.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.key",
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.name",
        ),
        FieldMapping(
            cache_attr="assigned_performance_service_level.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="assigned_storage_efficiency_policy.key",
        ),
        FieldMapping(
            cache_attr="assigned_storage_efficiency_policy.name",
        ),
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
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.expected_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.key",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.name",
        ),
        FieldMapping(
            cache_attr="recommended_performance_service_level.peak_iops",
            default=0,
        ),
        FieldMapping(
            cache_attr="space.size",
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
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("AiqumFileshareGetCollection", AIQUMFILESHAREGETCOLLECTION_MAPPING)
