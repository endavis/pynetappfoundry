"""OntapSoftwareHistory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.software.history.model import OntapSoftwareHistory
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

ONTAPSOFTWAREHISTORY_MAPPING = TypeMapping(
    name="OntapSoftwareHistory",
    model_class=OntapSoftwareHistory,
    api_endpoint="/cluster/software/history?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="from_version",
            api_path="from_version",
        ),
        FieldMapping(
            cache_attr="node_name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node_uuid",
            api_path="node.uuid",
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
            cache_attr="to_version",
            api_path="to_version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwareHistory", ONTAPSOFTWAREHISTORY_MAPPING)
