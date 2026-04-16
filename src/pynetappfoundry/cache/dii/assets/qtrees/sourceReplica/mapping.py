"""DiiQtreereplica type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.dii.assets.qtrees.sourceReplica.model import DiiQtreereplica

DIIQTREEREPLICA_MAPPING = TypeMapping(
    name="DiiQtreereplica",
    model_class=DiiQtreereplica,
    api_endpoint="/assets/qtrees/{id}/sourceReplica",
    api_type="dii",
    fields=(
        FieldMapping(
            cache_attr="mode",
        ),
        FieldMapping(
            cache_attr="qtree",
        ),
        FieldMapping(
            cache_attr="technology",
        ),
    ),
)

model_registry.register_mapping("DiiQtreereplica", DIIQTREEREPLICA_MAPPING)
