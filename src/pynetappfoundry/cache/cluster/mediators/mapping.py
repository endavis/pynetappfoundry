"""Mediator type mapping definition for the declarative field mapping framework.

Defines MEDIATOR_MAPPING which maps ONTAP REST API mediator data to
MediatorInfo cache model attributes.
"""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.cluster.mediators.model import MediatorInfo
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping

MEDIATOR_MAPPING = TypeMapping(
    name="Mediator",
    model_class=MediatorInfo,
    api_endpoint="/cluster/mediators?fields=*",
    cli_command="",
    id_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="mediator_address",
            api_path="ip_address",
        ),
        FieldMapping(
            cache_attr="mediator_uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="mediator_port",
            api_path="port",
            default=0,
        ),
    ),
)

model_registry.register_mapping("Mediator", MEDIATOR_MAPPING)
