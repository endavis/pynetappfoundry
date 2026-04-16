"""OntapSnaplockComplianceClock type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.storage.snaplock.compliance_clocks.model import (
    OntapSnaplockComplianceClock,
)

ONTAPSNAPLOCKCOMPLIANCECLOCK_MAPPING = TypeMapping(
    name="OntapSnaplockComplianceClock",
    model_class=OntapSnaplockComplianceClock,
    api_endpoint="/storage/snaplock/compliance-clocks?fields=*",
    api_type="ontap",
    identifier_field="node.uuid",
    fields=(
        FieldMapping(
            cache_attr="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
        ),
        FieldMapping(
            cache_attr="time",
        ),
    ),
)

model_registry.register_mapping(
    "OntapSnaplockComplianceClock", ONTAPSNAPLOCKCOMPLIANCECLOCK_MAPPING
)
