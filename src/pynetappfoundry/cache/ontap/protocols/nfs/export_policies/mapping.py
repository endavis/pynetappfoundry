"""OntapExportPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nfs.export_policies.model import (
    OntapExportPolicy,
    OntapExportPolicyRule,
)

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
            item_model=OntapExportPolicyRule,
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
