"""OntapNvmeSubsystemMap type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.nvme.subsystem_maps.model import OntapNvmeSubsystemMap

ONTAPNVMESUBSYSTEMMAP_MAPPING = TypeMapping(
    name="OntapNvmeSubsystemMap",
    model_class=OntapNvmeSubsystemMap,
    api_endpoint="/protocols/nvme/subsystem-maps?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="anagrpid",
            requires_explicit_fetch=True,
        ),
        FieldMapping(
            cache_attr="namespace.name",
        ),
        FieldMapping(
            cache_attr="namespace.node.name",
        ),
        FieldMapping(
            cache_attr="namespace.node.uuid",
        ),
        FieldMapping(
            cache_attr="namespace.uuid",
        ),
        FieldMapping(
            cache_attr="nsid",
        ),
        FieldMapping(
            cache_attr="subsystem.name",
        ),
        FieldMapping(
            cache_attr="subsystem.uuid",
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapNvmeSubsystemMap", ONTAPNVMESUBSYSTEMMAP_MAPPING)
