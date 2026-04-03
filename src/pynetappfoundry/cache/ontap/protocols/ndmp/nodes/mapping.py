"""OntapNdmpNode type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.ndmp.nodes.model import OntapNdmpNode

ONTAPNDMPNODE_MAPPING = TypeMapping(
    name="OntapNdmpNode",
    model_class=OntapNdmpNode,
    api_endpoint="/protocols/ndmp/nodes?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_types",
            default=[],
        ),
        FieldMapping(
            cache_attr="enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="password",
        ),
        FieldMapping(
            cache_attr="user",
        ),
    ),
)

model_registry.register_mapping("OntapNdmpNode", ONTAPNDMPNODE_MAPPING)
