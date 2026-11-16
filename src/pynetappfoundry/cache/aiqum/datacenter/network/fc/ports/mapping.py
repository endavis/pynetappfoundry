"""AiqumFcPort type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.ports.model import AiqumFcPort

AIQUMFCPORT_MAPPING = TypeMapping(
    name="AiqumFcPort",
    model_class=AiqumFcPort,
    api_endpoint="/datacenter/network/fc/ports",
    api_type="aiqum",
    identifier_field="key",
    fields=(
        FieldMapping(
            cache_attr="cluster.key",
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="description",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="fabric.connected",
            default=False,
        ),
        FieldMapping(
            cache_attr="fabric.connected_speed",
            default=0,
        ),
        FieldMapping(
            cache_attr="fabric.switch_port",
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="node.key",
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="physical_protocol",
        ),
        FieldMapping(
            cache_attr="speed.configured",
        ),
        FieldMapping(
            cache_attr="speed.maximum",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
        FieldMapping(
            cache_attr="wwnn",
        ),
        FieldMapping(
            cache_attr="wwpn",
        ),
    ),
)

model_registry.register_mapping("AiqumFcPort", AIQUMFCPORT_MAPPING)
