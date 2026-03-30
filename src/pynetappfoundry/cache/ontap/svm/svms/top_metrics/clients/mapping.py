"""OntapTopMetricsSvmClient type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.svm.svms.top_metrics.clients.model import OntapTopMetricsSvmClient

ONTAPTOPMETRICSSVMCLIENT_MAPPING = TypeMapping(
    name="OntapTopMetricsSvmClient",
    model_class=OntapTopMetricsSvmClient,
    api_endpoint="/svm/svms/{svm.uuid}/top-metrics/clients?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="client_ip",
            api_path="client_ip",
        ),
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
    ),
)

model_registry.register_mapping("OntapTopMetricsSvmClient", ONTAPTOPMETRICSSVMCLIENT_MAPPING)
