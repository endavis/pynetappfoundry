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
            api_path="code",
            default=0,
        ),
        FieldMapping(
            cache_attr="description",
            api_path="description",
        ),
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="error.arguments",
            api_path="error.arguments",
            transform=_transform_error_arguments,
            default=[],
        ),
        FieldMapping(
            cache_attr="error.code",
            api_path="error.code",
        ),
        FieldMapping(
            cache_attr="error.message",
            api_path="error.message",
        ),
        FieldMapping(
            cache_attr="message",
            api_path="message",
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="start_time",
            api_path="start_time",
        ),
        FieldMapping(
            cache_attr="state",
            api_path="state",
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
    ),
)

model_registry.register_mapping("OntapJob", ONTAPJOB_MAPPING)
