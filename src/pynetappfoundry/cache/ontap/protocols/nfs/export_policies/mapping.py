"""OntapExportPolicy type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import (
    OntapExportPolicy,
    OntapExportPolicyRule,
)


def _transform_rules(record: dict[str, Any]) -> list[OntapExportPolicyRule]:
    """Transform rules into OntapExportPolicyRule list."""
    return [OntapExportPolicyRule(**item) for item in record.get("rules", [])]


ONTAPEXPORTPOLICY_MAPPING = TypeMapping(
    name="OntapExportPolicy",
    model_class=OntapExportPolicy,
    api_endpoint="/protocols/nfs/export-policies?fields=*",
    api_type="ontap",
    identifier_field="id",
    fields=(
        FieldMapping(
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="rules",
            transform=_transform_rules,
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

model_registry.register_mapping("OntapExportPolicy", ONTAPEXPORTPOLICY_MAPPING)
