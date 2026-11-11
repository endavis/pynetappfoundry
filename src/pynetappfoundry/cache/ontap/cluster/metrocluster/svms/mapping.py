"""OntapMetroclusterSvm type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.metrocluster.svms.model import (
    OntapMetroclusterSvm,
    OntapMetroclusterSvmFailedReasonArgument,
)

ONTAPMETROCLUSTERSVM_MAPPING = TypeMapping(
    name="OntapMetroclusterSvm",
    model_class=OntapMetroclusterSvm,
    api_endpoint="/cluster/metrocluster/svms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="configuration_state",
        ),
        FieldMapping(
            cache_attr="failed_reason.arguments",
            item_model=OntapMetroclusterSvmFailedReasonArgument,
            default=[],
        ),
        FieldMapping(
            cache_attr="failed_reason.code",
        ),
        FieldMapping(
            cache_attr="failed_reason.message",
        ),
        FieldMapping(
            cache_attr="partner_svm.name",
        ),
        FieldMapping(
            cache_attr="partner_svm.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapMetroclusterSvm", ONTAPMETROCLUSTERSVM_MAPPING)
