"""OntapNtpServer type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cluster.ntp.servers.model import OntapNtpServer

ONTAPNTPSERVER_MAPPING = TypeMapping(
    name="OntapNtpServer",
    model_class=OntapNtpServer,
    api_endpoint="/cluster/ntp/servers?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="authentication_enabled",
            api_path="authentication_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_id",
            api_path="key.id",
            default=0,
        ),
        FieldMapping(
            cache_attr="server",
            api_path="server",
        ),
        FieldMapping(
            cache_attr="version",
            api_path="version",
        ),
    ),
)

model_registry.register_mapping("OntapNtpServer", ONTAPNTPSERVER_MAPPING)
