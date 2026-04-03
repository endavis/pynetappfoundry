"""OntapLoginMessages type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.login.messages.model import OntapLoginMessages

ONTAPLOGINMESSAGES_MAPPING = TypeMapping(
    name="OntapLoginMessages",
    model_class=OntapLoginMessages,
    api_endpoint="/security/login/messages?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="banner",
        ),
        FieldMapping(
            cache_attr="message",
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="show_cluster_message",
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

model_registry.register_mapping("OntapLoginMessages", ONTAPLOGINMESSAGES_MAPPING)
