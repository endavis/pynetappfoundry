"""OntapNvmeSubsystemController type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nvme.subsystem_controllers.model import (
    OntapNvmeSubsystemController,
)

ONTAPNVMESUBSYSTEMCONTROLLER_MAPPING = TypeMapping(
    name="OntapNvmeSubsystemController",
    model_class=OntapNvmeSubsystemController,
    api_endpoint="/protocols/nvme/subsystem-controllers?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="admin_queue.depth",
            default=0,
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap.group_size",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap.hash_function",
        ),
        FieldMapping(
            cache_attr="dh_hmac_chap.mode",
        ),
        FieldMapping(
            cache_attr="digest.data",
            default=False,
        ),
        FieldMapping(
            cache_attr="digest.header",
            default=False,
        ),
        FieldMapping(
            cache_attr="host.id",
        ),
        FieldMapping(
            cache_attr="host.nqn",
        ),
        FieldMapping(
            cache_attr="host.transport_address",
        ),
        FieldMapping(
            cache_attr="id",
        ),
        FieldMapping(
            cache_attr="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.transport_address",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
        ),
        FieldMapping(
            cache_attr="io_queue.count",
            default=0,
        ),
        FieldMapping(
            cache_attr="io_queue.depth",
            default=[],
        ),
        FieldMapping(
            cache_attr="keep_alive_timeout",
            default=0,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="subsystem.name",
        ),
        FieldMapping(
            cache_attr="subsystem.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="tls.cipher",
        ),
        FieldMapping(
            cache_attr="tls.key_type",
        ),
        FieldMapping(
            cache_attr="tls.psk_identity",
        ),
        FieldMapping(
            cache_attr="transport_protocol",
        ),
    ),
)

model_registry.register_mapping(
    "OntapNvmeSubsystemController", ONTAPNVMESUBSYSTEMCONTROLLER_MAPPING
)
