"""AiqumExportPolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.aiqum.datacenter.protocols.nfs.export_policies.model import (
    AiqumExportPolicy,
    AiqumExportPolicyRule,
)

AIQUMEXPORTPOLICY_MAPPING = TypeMapping(
    name="AiqumExportPolicy",
    model_class=AiqumExportPolicy,
    api_endpoint="/datacenter/protocols/nfs/export-policies",
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
            cache_attr="id",
            default=0,
        ),
        FieldMapping(
            cache_attr="key",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="rules",
            item_model=AiqumExportPolicyRule,
            default=[],
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
    ),
)

model_registry.register_mapping("AiqumExportPolicy", AIQUMEXPORTPOLICY_MAPPING)
