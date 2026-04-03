"""OntapShadowcopySet type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.protocols.cifs.shadowcopy_sets.model import OntapShadowcopySet

ONTAPSHADOWCOPYSET_MAPPING = TypeMapping(
    name="OntapShadowcopySet",
    model_class=OntapShadowcopySet,
    api_endpoint="/protocols/cifs/shadowcopy-sets?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="keep_snapshots",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapShadowcopySet", ONTAPSHADOWCOPYSET_MAPPING)
