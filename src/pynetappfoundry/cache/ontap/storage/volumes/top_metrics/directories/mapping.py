"""OntapTopMetricsDirectory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.storage.volumes.top_metrics.directories.model import (
    OntapTopMetricsDirectory,
)

ONTAPTOPMETRICSDIRECTORY_MAPPING = TypeMapping(
    name="OntapTopMetricsDirectory",
    model_class=OntapTopMetricsDirectory,
    api_endpoint="/storage/volumes/{volume.uuid}/top-metrics/directories?fields=*",
    api_type="ontap",
    parent_mapping="OntapVolume",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="iops_error_lower_bound",
            api_path="iops.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_error_upper_bound",
            api_path="iops.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_read",
            api_path="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops_write",
            api_path="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="non_recursive_bytes_used",
            api_path="non_recursive_bytes_used",
            default=0,
        ),
        FieldMapping(
            cache_attr="path",
            api_path="path",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="throughput_error_lower_bound",
            api_path="throughput.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_error_upper_bound",
            api_path="throughput.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput_write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume_name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume_uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapTopMetricsDirectory", ONTAPTOPMETRICSDIRECTORY_MAPPING)
