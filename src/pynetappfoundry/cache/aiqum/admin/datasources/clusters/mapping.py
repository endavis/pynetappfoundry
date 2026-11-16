"""AiqumDatasource type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.admin.datasources.clusters.model import AiqumDatasource

AIQUMDATASOURCE_MAPPING = TypeMapping(
    name="AiqumDatasource",
    model_class=AiqumDatasource,
    api_endpoint="/admin/datasources/clusters",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="address",
        ),
        FieldMapping(
            cache_attr="cluster_health_status",
        ),
        FieldMapping(
            cache_attr="cluster_object_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="is_metro_cluster",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="maintenance_window.end_time",
        ),
        FieldMapping(
            cache_attr="maintenance_window.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="maintenance_window.start_time",
        ),
        FieldMapping(
            cache_attr="managed_workload_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="mutual_tls_status",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="operation.end_time",
        ),
        FieldMapping(
            cache_attr="operation.last_failure_time",
        ),
        FieldMapping(
            cache_attr="operation.last_success_time",
        ),
        FieldMapping(
            cache_attr="operation.start_time",
        ),
        FieldMapping(
            cache_attr="operation.state",
        ),
        FieldMapping(
            cache_attr="operation.type_",
            api_path="operation.type",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="raw_capacity",
            default=0,
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="status_message",
        ),
        FieldMapping(
            cache_attr="username",
        ),
    ),
)

model_registry.register_mapping("AiqumDatasource", AIQUMDATASOURCE_MAPPING)
