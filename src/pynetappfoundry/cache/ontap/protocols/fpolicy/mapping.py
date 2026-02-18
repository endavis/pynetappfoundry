"""OntapFpolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.ontap.protocols.fpolicy.model import OntapFpolicy

ONTAPFPOLICY_MAPPING = TypeMapping(
    name="OntapFpolicy",
    model_class=OntapFpolicy,
    api_endpoint="/protocols/fpolicy/{svm.uuid}?fields=*",
    api_type="ontap",
    records_path="engines",
    parent_mapping="OntapProtocolsFpolicy",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="buffer_size_recv_buffer",
            api_path="buffer_size.recv_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="buffer_size_send_buffer",
            api_path="buffer_size.send_buffer",
            default=0,
        ),
        FieldMapping(
            cache_attr="certificate_ca",
            api_path="certificate.ca",
        ),
        FieldMapping(
            cache_attr="certificate_name",
            api_path="certificate.name",
        ),
        FieldMapping(
            cache_attr="certificate_serial_number",
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
            cache_attr="resiliency_directory_path",
            api_path="resiliency.directory_path",
        ),
        FieldMapping(
            cache_attr="resiliency_enabled",
            api_path="resiliency.enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="resiliency_retention_duration",
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
            cache_attr="type_",
            api_path="type",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicy", ONTAPFPOLICY_MAPPING)
