"""OntapTopMetricsClient type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.volumes.top_metrics.clients.model import (
    OntapTopMetricsClient,
)

ONTAPTOPMETRICSCLIENT_MAPPING = TypeMapping(
    name="OntapTopMetricsClient",
    model_class=OntapTopMetricsClient,
    api_endpoint="/storage/volumes/{volume.uuid}/top-metrics/clients?fields=*",
    api_type="ontap",
    parent_mapping="OntapVolume",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="client_ip",
            api_path="client_ip",
        ),
        FieldMapping(
            cache_attr="iops.error.lower_bound",
            api_path="iops.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.error.upper_bound",
            api_path="iops.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.read",
            api_path="iops.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="iops.write",
            api_path="iops.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="throughput.error.lower_bound",
            api_path="throughput.error.lower_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.error.upper_bound",
            api_path="throughput.error.upper_bound",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.read",
            api_path="throughput.read",
            default=0,
        ),
        FieldMapping(
            cache_attr="throughput.write",
            api_path="throughput.write",
            default=0,
        ),
        FieldMapping(
            cache_attr="volume.name",
            api_path="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
            api_path="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapTopMetricsClient", ONTAPTOPMETRICSCLIENT_MAPPING)
