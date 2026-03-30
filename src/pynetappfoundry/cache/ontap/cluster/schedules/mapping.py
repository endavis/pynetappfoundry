"""OntapSchedule type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.schedules.model import OntapSchedule

ONTAPSCHEDULE_MAPPING = TypeMapping(
    name="OntapSchedule",
    model_class=OntapSchedule,
    api_endpoint="/cluster/schedules?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="cluster_name",
            api_path="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster_uuid",
            api_path="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="cron_days",
            api_path="cron.days",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron_hours",
            api_path="cron.hours",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron_minutes",
            api_path="cron.minutes",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron_months",
            api_path="cron.months",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron_weekdays",
            api_path="cron.weekdays",
            default=[],
        ),
        FieldMapping(
            cache_attr="interval",
            api_path="interval",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
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
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSchedule", ONTAPSCHEDULE_MAPPING)
