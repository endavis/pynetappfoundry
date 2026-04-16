"""DiiMonitorsGroup type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.monitors.groups.model import DiiMonitorsGroup

DIIMONITORSGROUP_MAPPING = TypeMapping(
    name="DiiMonitorsGroup",
    model_class=DiiMonitorsGroup,
    api_endpoint="/monitors/groups",
    api_type="dii",
    records_path="",
    fields=(
        FieldMapping(
            cache_attr="groupType",
        ),
        FieldMapping(
            cache_attr="created",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="monitorInfo.monitorCount",
            default=0,
        ),
        FieldMapping(
            cache_attr="monitorInfo.monitorsLink",
        ),
        FieldMapping(
            cache_attr="monitorInfo.monitors",
            default=[],
        ),
        FieldMapping(
            cache_attr="self",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="updated",
            default=0,
        ),
    ),
)

model_registry.register_mapping("DiiMonitorsGroup", DIIMONITORSGROUP_MAPPING)
