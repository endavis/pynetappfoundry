"""OntapTopMetricsSvmDirectory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.svms.top_metrics.directories.model import (
    OntapTopMetricsSvmDirectory,
)

ONTAPTOPMETRICSSVMDIRECTORY_MAPPING = TypeMapping(
    name="OntapTopMetricsSvmDirectory",
    model_class=OntapTopMetricsSvmDirectory,
    api_endpoint="/svm/svms/{svm.uuid}/top-metrics/directories?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="iops.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="junction_path",
            api_path="junction-path",
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="throughput.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapTopMetricsSvmDirectory", ONTAPTOPMETRICSSVMDIRECTORY_MAPPING)
