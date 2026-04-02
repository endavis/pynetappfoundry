"""OntapWwpnAlias type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.fc.wwpn_aliases.model import OntapWwpnAlias

ONTAPWWPNALIAS_MAPPING = TypeMapping(
    name="OntapWwpnAlias",
    model_class=OntapWwpnAlias,
    api_endpoint="/network/fc/wwpn-aliases?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="alias",
            api_path="alias",
        ),
        FieldMapping(
            cache_attr="svm.name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="wwpn",
            api_path="wwpn",
        ),
    ),
)

model_registry.register_mapping("OntapWwpnAlias", ONTAPWWPNALIAS_MAPPING)
