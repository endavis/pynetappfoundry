"""OntapQosWorkload type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.qos.workloads.model import OntapQosWorkload

ONTAPQOSWORKLOAD_MAPPING = TypeMapping(
    name="OntapQosWorkload",
    model_class=OntapQosWorkload,
    api_endpoint="/storage/qos/workloads?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="file",
        ),
        FieldMapping(
            cache_attr="lun",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="policy.name",
        ),
        FieldMapping(
            cache_attr="policy.uuid",
        ),
        FieldMapping(
            cache_attr="qtree",
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
        FieldMapping(
            cache_attr="volume",
        ),
        FieldMapping(
            cache_attr="wid",
            default=0,
        ),
        FieldMapping(
            cache_attr="workload_class",
        ),
    ),
)

model_registry.register_mapping("OntapQosWorkload", ONTAPQOSWORKLOAD_MAPPING)
