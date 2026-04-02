"""OntapFirmwareHistory type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.firmware.history.model import OntapFirmwareHistory

ONTAPFIRMWAREHISTORY_MAPPING = TypeMapping(
    name="OntapFirmwareHistory",
    model_class=OntapFirmwareHistory,
    api_endpoint="/cluster/firmware/history?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="end_time",
            api_path="end_time",
        ),
        FieldMapping(
            cache_attr="fw_file_name",
            api_path="fw_file_name",
        ),
        FieldMapping(
            cache_attr="fw_update_state",
            api_path="fw_update_state",
        ),
        FieldMapping(
            cache_attr="job.uuid",
            api_path="job.uuid",
        ),
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="start_time",
            api_path="start_time",
        ),
        FieldMapping(
            cache_attr="update_status",
            api_path="update_status",
            default=[],
        ),
    ),
)

model_registry.register_mapping("OntapFirmwareHistory", ONTAPFIRMWAREHISTORY_MAPPING)
