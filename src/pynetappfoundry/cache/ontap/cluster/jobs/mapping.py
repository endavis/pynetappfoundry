"""OntapJob type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.jobs.model import OntapJob, OntapJobErrorArgument
from pynetappfoundry.utils.dict_path import get_nested_value


def _transform_error_arguments(record: dict[str, Any]) -> list[OntapJobErrorArgument]:
    """Transform error.arguments into OntapJobErrorArgument list."""
    try:
        items = get_nested_value(record, "error.arguments")
    except Exception:
        items = []
    return [OntapJobErrorArgument(**item) for item in items]


ONTAPJOB_MAPPING = TypeMapping(
    name="OntapJob",
    model_class=OntapJob,
    api_endpoint="/cluster/jobs?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="code",
            default=0,
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="error.arguments",
            transform=_transform_error_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="error.code",
        ),
        FieldMapping(
            cache_attr="error.message",
        ),
        FieldMapping(
            cache_attr="message",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="state",
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
    ),
)

model_registry.register_mapping("OntapJob", ONTAPJOB_MAPPING)
