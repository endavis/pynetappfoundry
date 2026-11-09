"""OntapFpolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.fpolicy.model import (
    OntapFpolicy,
    OntapFpolicyEngine,
    OntapFpolicyEvent,
    OntapFpolicyPersistentStore,
    OntapFpolicyPolicy,
)


def _transform_engines(record: dict[str, Any]) -> list[OntapFpolicyEngine]:
    """Transform engines into OntapFpolicyEngine list."""
    return [OntapFpolicyEngine(**item) for item in record.get("engines", [])]


def _transform_events(record: dict[str, Any]) -> list[OntapFpolicyEvent]:
    """Transform events into OntapFpolicyEvent list."""
    return [OntapFpolicyEvent(**item) for item in record.get("events", [])]


def _transform_persistent_stores(record: dict[str, Any]) -> list[OntapFpolicyPersistentStore]:
    """Transform persistent_stores into OntapFpolicyPersistentStore list."""
    return [OntapFpolicyPersistentStore(**item) for item in record.get("persistent_stores", [])]


def _transform_policies(record: dict[str, Any]) -> list[OntapFpolicyPolicy]:
    """Transform policies into OntapFpolicyPolicy list."""
    return [OntapFpolicyPolicy(**item) for item in record.get("policies", [])]


ONTAPFPOLICY_MAPPING = TypeMapping(
    name="OntapFpolicy",
    model_class=OntapFpolicy,
    api_endpoint="/protocols/fpolicy?fields=*",
    api_type="ontap",
    identifier_field="svm.uuid",
    fields=(
        FieldMapping(
            cache_attr="engines",
            transform=_transform_engines,
            default=[],
        ),
        FieldMapping(
            cache_attr="events",
            transform=_transform_events,
            default=[],
        ),
        FieldMapping(
            cache_attr="persistent_stores",
            transform=_transform_persistent_stores,
            default=[],
        ),
        FieldMapping(
            cache_attr="policies",
            transform=_transform_policies,
            default=[],
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapFpolicy", ONTAPFPOLICY_MAPPING)
