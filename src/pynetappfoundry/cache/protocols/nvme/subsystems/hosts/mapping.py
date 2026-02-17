"""OntapNvmeSubsystemHost type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.cache.protocols.nvme.subsystems.hosts.model import (
    OntapNvmeSubsystemHost,
    OntapNvmeSubsystemHostRecord,
)


def _transform_records(record: dict[str, Any]) -> list[OntapNvmeSubsystemHostRecord]:
    """Transform records into OntapNvmeSubsystemHostRecord list."""
    return [OntapNvmeSubsystemHostRecord(**item) for item in record.get("records", [])]


ONTAPNVMESUBSYSTEMHOST_MAPPING = TypeMapping(
    name="OntapNvmeSubsystemHost",
    model_class=OntapNvmeSubsystemHost,
    api_endpoint="/protocols/nvme/subsystems/{subsystem.uuid}/hosts?fields=*",
    api_type="ontap",
    parent_mapping="OntapNvmeSubsystem",
    parent_id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="dh_hmac_chap_controller_secret_key",
            api_path="dh_hmac_chap.controller_secret_key",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap_group_size",
            api_path="dh_hmac_chap.group_size",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap_hash_function",
            api_path="dh_hmac_chap.hash_function",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap_host_secret_key",
            api_path="dh_hmac_chap.host_secret_key",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap_mode",
            api_path="dh_hmac_chap.mode",
        ),
        FieldMapping(
            cache_attr="io_queue_count",
            api_path="io_queue.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="io_queue_depth",
            api_path="io_queue.depth",
            default=0,
        ),
        FieldMapping(
            cache_attr="nqn",
            api_path="nqn",
        ),
        FieldMapping(
            cache_attr="priority",
            api_path="priority",
        ),
        FieldMapping(
            cache_attr="records",
            transform=_transform_records,
            default=[],
        ),
        FieldMapping(
            cache_attr="subsystem_name",
            api_path="subsystem.name",
        ),
        FieldMapping(
            cache_attr="subsystem_uuid",
            api_path="subsystem.uuid",
        ),
        FieldMapping(
            cache_attr="tls_configured_psk",
            api_path="tls.configured_psk",
        ),
        FieldMapping(
            cache_attr="tls_key_type",
            api_path="tls.key_type",
        ),
    ),
)

model_registry.register_mapping("OntapNvmeSubsystemHost", ONTAPNVMESUBSYSTEMHOST_MAPPING)
