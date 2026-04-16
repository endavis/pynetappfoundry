"""OntapCloudTarget type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.cloud.targets.model import OntapCloudTarget

ONTAPCLOUDTARGET_MAPPING = TypeMapping(
    name="OntapCloudTarget",
    model_class=OntapCloudTarget,
    api_endpoint="/cloud/targets?fields=*",
    api_type="ontap",
    identifier_field="uuid",
    fields=(
        FieldMapping(
            cache_attr="access_key",
        ),
        FieldMapping(
            cache_attr="authentication_type",
        ),
        FieldMapping(
            cache_attr="azure_account",
        ),
        FieldMapping(
            cache_attr="azure_msi_token",
        ),
        FieldMapping(
            cache_attr="azure_private_key",
        ),
        FieldMapping(
            cache_attr="azure_sas_token",
        ),
        FieldMapping(
            cache_attr="cap_url",
        ),
        FieldMapping(
            cache_attr="certificate_validation_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="cluster.name",
        ),
        FieldMapping(
            cache_attr="cluster.uuid",
        ),
        FieldMapping(
            cache_attr="container",
        ),
        FieldMapping(
            cache_attr="ipspace.name",
        ),
        FieldMapping(
            cache_attr="ipspace.uuid",
        ),
        FieldMapping(
            cache_attr="name",
        ),
        FieldMapping(
            cache_attr="owner",
        ),
        FieldMapping(
            cache_attr="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="provider_type",
        ),
        FieldMapping(
            cache_attr="read_latency_warning_threshold",
            default=0,
        ),
        FieldMapping(
            cache_attr="scope",
        ),
        FieldMapping(
            cache_attr="secret_password",
        ),
        FieldMapping(
            cache_attr="server",
        ),
        FieldMapping(
            cache_attr="server_side_encryption",
        ),
        FieldMapping(
            cache_attr="snapmirror_use",
        ),
        FieldMapping(
            cache_attr="ssl_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="svm.name",
        ),
        FieldMapping(
            cache_attr="svm.uuid",
        ),
        FieldMapping(
            cache_attr="url_style",
        ),
        FieldMapping(
            cache_attr="use_http_proxy",
            default=False,
        ),
        FieldMapping(
            cache_attr="used",
            default=0,
        ),
        FieldMapping(
            cache_attr="uuid",
        ),
    ),
)

model_registry.register_mapping("OntapCloudTarget", ONTAPCLOUDTARGET_MAPPING)
