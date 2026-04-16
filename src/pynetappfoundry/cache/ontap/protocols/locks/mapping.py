"""OntapClientLock type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.locks.model import OntapClientLock

ONTAPCLIENTLOCK_MAPPING = TypeMapping(
    name="OntapClientLock",
    model_class=OntapClientLock,
    api_endpoint="/protocols/locks?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="byte_lock.exclusive",
            default=False,
        ),
        FieldMapping(
            cache_attr="byte_lock.length",
            default=0,
        ),
        FieldMapping(
            cache_attr="byte_lock.mandatory",
            default=False,
        ),
        FieldMapping(
            cache_attr="byte_lock.offset",
            default=0,
        ),
        FieldMapping(
            cache_attr="byte_lock.soft",
            default=False,
        ),
        FieldMapping(
            cache_attr="byte_lock.super",
            default=False,
        ),
        FieldMapping(
            cache_attr="client_address",
        ),
        FieldMapping(
            cache_attr="constituent",
            default=False,
        ),
        FieldMapping(
            cache_attr="delegation",
        ),
        FieldMapping(
            cache_attr="interface.ip.address",
        ),
        FieldMapping(
            cache_attr="interface.name",
        ),
        FieldMapping(
            cache_attr="interface.uuid",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="oplock_level",
        ),
        FieldMapping(
            cache_attr="owner_id",
        ),
        FieldMapping(
            cache_attr="path",
        ),
        FieldMapping(
            cache_attr="protocol",
        ),
        FieldMapping(
            cache_attr="share_lock.mode",
        ),
        FieldMapping(
            cache_attr="share_lock.soft",
            default=False,
        ),
        FieldMapping(
            cache_attr="smb.connect_state",
        ),
        FieldMapping(
            cache_attr="smb.open_group_id",
        ),
        FieldMapping(
            cache_attr="smb.open_type",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="type_",
            api_path="type",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="volume.name",
        ),
        FieldMapping(
            cache_attr="volume.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapClientLock", ONTAPCLIENTLOCK_MAPPING)
