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
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="cron.days",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron.hours",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron.minutes",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron.months",
            default=[],
        ),
        FieldMapping(
            cache_attr="cron.weekdays",
            default=[],
        ),
        FieldMapping(
            cache_attr="interval",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="scope",
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

model_registry.register_mapping("OntapSchedule", ONTAPSCHEDULE_MAPPING)
