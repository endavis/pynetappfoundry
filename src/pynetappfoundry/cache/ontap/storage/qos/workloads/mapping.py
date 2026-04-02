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
            api_path="file",
        ),
        FieldMapping(
            cache_attr="lun",
            api_path="lun",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="policy.name",
            api_path="policy.name",
        ),
        FieldMapping(
            cache_attr="policy.uuid",
            api_path="policy.uuid",
        ),
        FieldMapping(
            cache_attr="qtree",
            api_path="qtree",
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
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="volume",
            api_path="volume",
        ),
        FieldMapping(
            cache_attr="wid",
            api_path="wid",
            default=0,
        ),
        FieldMapping(
            cache_attr="workload_class",
            api_path="workload_class",
        ),
    ),
)

model_registry.register_mapping("OntapQosWorkload", ONTAPQOSWORKLOAD_MAPPING)
