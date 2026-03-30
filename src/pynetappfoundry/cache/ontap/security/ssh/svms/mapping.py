"""OntapSvmSshServer type mapping."""

from __future__ import annotations

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.ssh.svms.model import OntapSvmSshServer

ONTAPSVMSSHSERVER_MAPPING = TypeMapping(
    name="OntapSvmSshServer",
    model_class=OntapSvmSshServer,
    api_endpoint="/security/ssh/svms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="ciphers",
            api_path="ciphers",
            default=[],
        ),
        FieldMapping(
            cache_attr="host_key_algorithms",
            api_path="host_key_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="is_rsa_in_publickey_algorithms_enabled",
            api_path="is_rsa_in_publickey_algorithms_enabled",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_exchange_algorithms",
            api_path="key_exchange_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="mac_algorithms",
            api_path="mac_algorithms",
            default=[],
        ),
        FieldMapping(
            cache_attr="max_authentication_retry_count",
            api_path="max_authentication_retry_count",
            default=0,
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
    ),
)

model_registry.register_mapping("OntapSvmSshServer", ONTAPSVMSSHSERVER_MAPPING)
