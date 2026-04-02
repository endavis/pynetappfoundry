"""OntapFcSwitch type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.fabrics.switches.model import (
    OntapFcSwitch,
    OntapFcSwitchPort,
)


def _transform_ports(record: dict[str, Any]) -> list[OntapFcSwitchPort]:
    """Transform ports into OntapFcSwitchPort list."""
    return [OntapFcSwitchPort(**item) for item in record.get("ports", [])]


ONTAPFCSWITCH_MAPPING = TypeMapping(
    name="OntapFcSwitch",
    model_class=OntapFcSwitch,
    api_endpoint="/network/fc/fabrics/{fabric.name}/switches?fields=*",
    api_type="ontap",
    parent_mapping="OntapFabric",
    parent_id_field="name",
    fields=(
        FieldMapping(
            cache_attr="cache.age",
            api_path="cache.age",
        ),
        FieldMapping(
            cache_attr="cache.is_current",
            api_path="cache.is_current",
            default=False,
        ),
        FieldMapping(
            cache_attr="cache.update_time",
            api_path="cache.update_time",
        ),
        FieldMapping(
            cache_attr="domain_id",
            api_path="domain_id",
            default=0,
        ),
        FieldMapping(
            cache_attr="fabric.name",
            api_path="fabric.name",
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="ports",
            api_path="ports",
            transform=_transform_ports,
            default=[],
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="release",
            api_path="release",
        ),
        FieldMapping(
            cache_attr="vendor",
            api_path="vendor",
        ),
        FieldMapping(
            cache_attr="wwn",
            api_path="wwn",
        ),
    ),
)

model_registry.register_mapping("OntapFcSwitch", ONTAPFCSWITCH_MAPPING)
