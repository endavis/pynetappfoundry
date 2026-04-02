"""OntapVolumeEfficiencyPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.volume_efficiency_policies.model import (
    OntapVolumeEfficiencyPolicy,
)

ONTAPVOLUMEEFFICIENCYPOLICY_MAPPING = TypeMapping(
    name="OntapVolumeEfficiencyPolicy",
    model_class=OntapVolumeEfficiencyPolicy,
    api_endpoint="/storage/volume-efficiency-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="comment",
            api_path="comment",
        ),
        FieldMapping(
            cache_attr="duration",
            api_path="duration",
            default=0,
        ),
        FieldMapping(
            cache_attr="enabled",
            api_path="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="qos_policy",
            api_path="qos_policy",
        ),
        FieldMapping(
            cache_attr="schedule.name",
            api_path="schedule.name",
        ),
        FieldMapping(
            cache_attr="start_threshold_percent",
            api_path="start_threshold_percent",
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
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVolumeEfficiencyPolicy", ONTAPVOLUMEEFFICIENCYPOLICY_MAPPING)
