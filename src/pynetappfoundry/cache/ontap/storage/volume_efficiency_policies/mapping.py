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
        ),
        FieldMapping(
            cache_attr="duration",
            default=0,
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="qos_policy",
        ),
        FieldMapping(
            cache_attr="schedule.name",
        ),
        FieldMapping(
            cache_attr="start_threshold_percent",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapVolumeEfficiencyPolicy", ONTAPVOLUMEEFFICIENCYPOLICY_MAPPING)
