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
    fields=(
        FieldMapping(
            cache_attr="node.name",
            api_path="node.name",
        ),
        FieldMapping(
            cache_attr="node.uuid",
            api_path="node.uuid",
        ),
        FieldMapping(
            cache_attr="time",
            api_path="time",
        ),
    ),
)

model_registry.register_mapping(
    "OntapSnaplockComplianceClock", ONTAPSNAPLOCKCOMPLIANCECLOCK_MAPPING
)
