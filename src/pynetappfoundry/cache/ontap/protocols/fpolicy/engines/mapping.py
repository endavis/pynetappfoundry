"""OntapFpolicyEngine type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.engines.model import OntapFpolicyEngine

ONTAPFPOLICYENGINE_MAPPING = TypeMapping(
    name="OntapFpolicyEngine",
    model_class=OntapFpolicyEngine,
    api_endpoint="/protocols/fpolicy/{svm.uuid}/engines?fields=*",
    api_type="ontap",
    parent_mapping="OntapSvm",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="buffer_size.recv_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="buffer_size.send_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.serial_number",
        ),
        FieldMapping(
            cache_attr="format",
        ),
        FieldMapping(
            cache_attr="keep_alive_interval",
        ),
        FieldMapping(
            cache_attr="max_server_requests",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="primary_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="request_abort_timeout",
        ),
        FieldMapping(
            cache_attr="request_cancel_timeout",
        ),
        FieldMapping(
            cache_attr="resiliency.directory_path",
        ),
        FieldMapping(
            cache_attr="resiliency.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="resiliency.retention_duration",
        ),
        FieldMapping(
            cache_attr="secondary_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="server_progress_timeout",
        ),
        FieldMapping(
            cache_attr="ssl_option",
        ),
        FieldMapping(
            cache_attr="status_request_interval",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyEngine", ONTAPFPOLICYENGINE_MAPPING)
