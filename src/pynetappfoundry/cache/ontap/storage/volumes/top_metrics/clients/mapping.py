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
        ),
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

model_registry.register_mapping("OntapTopMetricsClient", ONTAPTOPMETRICSCLIENT_MAPPING)
