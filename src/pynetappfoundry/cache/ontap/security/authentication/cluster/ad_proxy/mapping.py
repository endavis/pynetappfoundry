"""OntapClusterAdProxy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.authentication.cluster.ad_proxy.model import (
    OntapClusterAdProxy,
)

ONTAPCLUSTERADPROXY_MAPPING = TypeMapping(
    name="OntapClusterAdProxy",
    model_class=OntapClusterAdProxy,
    api_endpoint="/security/authentication/cluster/ad-proxy?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapClusterAdProxy", ONTAPCLUSTERADPROXY_MAPPING)
