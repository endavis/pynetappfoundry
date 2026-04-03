"""OntapStoragePort type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.ports.model import OntapStoragePort

ONTAPSTORAGEPORT_MAPPING = TypeMapping(
    name="OntapStoragePort",
    model_class=OntapStoragePort,
    api_endpoint="/storage/ports?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="board_name",
        ),
        FieldMapping(
            cache_attr="cable.identifier",
        ),
        FieldMapping(
            cache_attr="cable.length",
        ),
        FieldMapping(
            cache_attr="cable.part_number",
        ),
        FieldMapping(
            cache_attr="cable.serial_number",
        ),
        FieldMapping(
            cache_attr="cable.transceiver",
        ),
        FieldMapping(
            cache_attr="cable.vendor",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="error.corrective_action",
        ),
        FieldMapping(
            cache_attr="error.message",
        ),
        FieldMapping(
            cache_attr="firmware_version",
        ),
        FieldMapping(
            cache_attr="force",
            default=False,
        ),
        FieldMapping(
            cache_attr="in_use",
            default=False,
        ),
        FieldMapping(
            cache_attr="mac_address",
        ),
        FieldMapping(
            cache_attr="mode",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="part_number",
        ),
        FieldMapping(
            cache_attr="redundant",
            default=False,
        ),
        FieldMapping(
            cache_attr="serial_number",
        ),
        FieldMapping(
            cache_attr="speed",
            default=0.0,
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="wwn",
        ),
        FieldMapping(
            cache_attr="wwpn",
        ),
    ),
)

model_registry.register_mapping("OntapStoragePort", ONTAPSTORAGEPORT_MAPPING)
