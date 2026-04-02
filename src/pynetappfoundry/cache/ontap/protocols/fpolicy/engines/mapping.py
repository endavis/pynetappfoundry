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
            api_path="buffer_size.recv_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="buffer_size.send_buffer",
            api_path="buffer_size.send_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="certificate.ca",
            api_path="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate.name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate.serial_number",
            api_path="certificate.serial_number",
        ),
        FieldMapping(
            cache_attr="format",
            api_path="format",
        ),
        FieldMapping(
            cache_attr="keep_alive_interval",
            api_path="keep_alive_interval",
        ),
        FieldMapping(
            cache_attr="max_server_requests",
            api_path="max_server_requests",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="primary_servers",
            api_path="primary_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="request_abort_timeout",
            api_path="request_abort_timeout",
        ),
        FieldMapping(
            cache_attr="request_cancel_timeout",
            api_path="request_cancel_timeout",
        ),
        FieldMapping(
            cache_attr="resiliency.directory_path",
            api_path="resiliency.directory_path",
        ),
        FieldMapping(
            cache_attr="resiliency.enabled",
            api_path="resiliency.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="resiliency.retention_duration",
            api_path="resiliency.retention_duration",
        ),
        FieldMapping(
            cache_attr="secondary_servers",
            api_path="secondary_servers",
            default=[],
        ),
        FieldMapping(
            cache_attr="server_progress_timeout",
            api_path="server_progress_timeout",
        ),
        FieldMapping(
            cache_attr="ssl_option",
            api_path="ssl_option",
        ),
        FieldMapping(
            cache_attr="status_request_interval",
            api_path="status_request_interval",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicyEngine", ONTAPFPOLICYENGINE_MAPPING)
