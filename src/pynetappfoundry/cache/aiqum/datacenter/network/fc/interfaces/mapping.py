"""AiqumFcInterface type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.network.fc.interfaces.model import AiqumFcInterface

AIQUMFCINTERFACE_MAPPING = TypeMapping(
    name="AiqumFcInterface",
    model_class=AiqumFcInterface,
    api_endpoint="/datacenter/network/fc/interfaces",
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
            cache_attr="data_protocol",
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="location.home_node.key",
        ),
        FieldMapping(
            cache_attr="location.home_node.name",
        ),
        FieldMapping(
            cache_attr="location.home_node.uuid",
        ),
        FieldMapping(
            cache_attr="location.home_port.key",
        ),
        FieldMapping(
            cache_attr="location.home_port.name",
        ),
        FieldMapping(
            cache_attr="location.home_port.node.name",
        ),
        FieldMapping(
            cache_attr="location.home_port.uuid",
        ),
        FieldMapping(
            cache_attr="location.is_home",
            default=False,
        ),
        FieldMapping(
            cache_attr="location.port.key",
        ),
        FieldMapping(
            cache_attr="location.port.name",
        ),
        FieldMapping(
            cache_attr="location.port.node.name",
        ),
        FieldMapping(
            cache_attr="location.port.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="state",
        ),
        FieldMapping(
            cache_attr="svm.key",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
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

model_registry.register_mapping("AiqumFcInterface", AIQUMFCINTERFACE_MAPPING)
