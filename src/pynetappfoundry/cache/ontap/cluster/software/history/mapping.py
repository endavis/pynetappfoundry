"""OntapSoftwareHistory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.software.history.model import OntapSoftwareHistory

ONTAPSOFTWAREHISTORY_MAPPING = TypeMapping(
    name="OntapSoftwareHistory",
    model_class=OntapSoftwareHistory,
    api_endpoint="/cluster/software/history?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="end_time",
        ),
        FieldMapping(
            cache_attr="from_version",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="start_time",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="to_version",
        ),
    ),
)

model_registry.register_mapping("OntapSoftwareHistory", ONTAPSOFTWAREHISTORY_MAPPING)
