"""OntapIpServicePolicy type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.network.ip.service_policies.model import OntapIpServicePolicy

ONTAPIPSERVICEPOLICY_MAPPING = TypeMapping(
    name="OntapIpServicePolicy",
    model_class=OntapIpServicePolicy,
    api_endpoint="/network/ip/service-policies?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ipspace.name",
            api_path="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
            api_path="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="is_built_in",
            api_path="is_built_in",
            default=False,
        ),
        FieldMapping(
            cache_attr="name",
            api_path="name",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="services",
            api_path="services",
            default=[],
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
            cache_attr="uuid",
            api_path="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapIpServicePolicy", ONTAPIPSERVICEPOLICY_MAPPING)
