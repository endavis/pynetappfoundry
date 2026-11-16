"""AiqumJob type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.management_server.jobs.model import (
    AiqumJob,
    AiqumJobJobResult,
    AiqumJobTaskReport,
)

AIQUMJOB_MAPPING = TypeMapping(
    name="AiqumJob",
    model_class=AiqumJob,
    api_endpoint="/management-server/jobs",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="complete_time",
        ),
        FieldMapping(
            cache_attr="job_results",
            item_model=AiqumJobJobResult,
            default=[],
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="parent_job_key",
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.aborted_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.completed_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.failed_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.running_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.successful_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="spawned_job_summary.total_jobs",
            default=0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="status",
        ),
        FieldMapping(
            cache_attr="submit_time",
        ),
        FieldMapping(
            cache_attr="task_reports",
            item_model=AiqumJobTaskReport,
            default=[],
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("AiqumJob", AIQUMJOB_MAPPING)
