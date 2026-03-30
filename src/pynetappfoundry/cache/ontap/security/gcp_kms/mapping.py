"""OntapGcpKms type mapping."""

from __future__ import annotations

from typing import Any

from pynetappfoundry.cache._registry import model_registry
from pynetappfoundry.cache.field_mapping import FieldMapping, TypeMapping
from pynetappfoundry.models.ontap.security.gcp_kms.model import (
    OntapGcpKms,
    OntapGcpKmsEkmipReachability,
)


def _transform_ekmip_reachability(record: dict[str, Any]) -> list[OntapGcpKmsEkmipReachability]:
    """Transform ekmip_reachability into OntapGcpKmsEkmipReachability list."""
    return [OntapGcpKmsEkmipReachability(**item) for item in record.get("ekmip_reachability", [])]


ONTAPGCPKMS_MAPPING = TypeMapping(
    name="OntapGcpKms",
    model_class=OntapGcpKms,
    api_endpoint="/security/gcp-kms?fields=*",
    api_type="ontap",
    fields=(
        FieldMapping(
            cache_attr="application_credentials",
            api_path="application_credentials",
        ),
        FieldMapping(
            cache_attr="caller_account",
            api_path="caller_account",
        ),
        FieldMapping(
            cache_attr="cloudkms_host",
            api_path="cloudkms_host",
        ),
        FieldMapping(
            cache_attr="ekmip_reachability",
            api_path="ekmip_reachability",
            transform=_transform_ekmip_reachability,
            default=[],
        ),
        FieldMapping(
            cache_attr="google_reachability_code",
            api_path="google_reachability.code",
        ),
        FieldMapping(
            cache_attr="google_reachability_message",
            api_path="google_reachability.message",
        ),
        FieldMapping(
            cache_attr="google_reachability_reachable",
            api_path="google_reachability.reachable",
            default=False,
        ),
        FieldMapping(
            cache_attr="key_name",
            api_path="key_name",
        ),
        FieldMapping(
            cache_attr="key_ring_location",
            api_path="key_ring_location",
        ),
        FieldMapping(
            cache_attr="key_ring_name",
            api_path="key_ring_name",
        ),
        FieldMapping(
            cache_attr="oauth_host",
            api_path="oauth_host",
        ),
        FieldMapping(
            cache_attr="oauth_url",
            api_path="oauth_url",
        ),
        FieldMapping(
            cache_attr="port",
            api_path="port",
            default=0,
        ),
        FieldMapping(
            cache_attr="privileged_account",
            api_path="privileged_account",
        ),
        FieldMapping(
            cache_attr="project_id",
            api_path="project_id",
        ),
        FieldMapping(
            cache_attr="proxy_host",
            api_path="proxy_host",
        ),
        FieldMapping(
            cache_attr="proxy_password",
            api_path="proxy_password",
        ),
        FieldMapping(
            cache_attr="proxy_port",
            api_path="proxy_port",
            default=0,
        ),
        FieldMapping(
            cache_attr="proxy_type",
            api_path="proxy_type",
        ),
        FieldMapping(
            cache_attr="proxy_username",
            api_path="proxy_username",
        ),
        FieldMapping(
            cache_attr="scope",
            api_path="scope",
        ),
        FieldMapping(
            cache_attr="state_cluster_state",
            api_path="state.cluster_state",
            default=False,
        ),
        FieldMapping(
            cache_attr="state_code",
            api_path="state.code",
        ),
        FieldMapping(
            cache_attr="state_message",
            api_path="state.message",
        ),
        FieldMapping(
            cache_attr="svm_name",
            api_path="svm.name",
        ),
        FieldMapping(
            cache_attr="svm_uuid",
            api_path="svm.uuid",
        ),
        FieldMapping(
            cache_attr="uuid",
            api_path="uuid",
        ),
        FieldMapping(
            cache_attr="verify_host",
            api_path="verify_host",
            default=False,
        ),
        FieldMapping(
            cache_attr="verify_ip",
            api_path="verify_ip",
            default=False,
        ),
    ),
)

model_registry.register_mapping("OntapGcpKms", ONTAPGCPKMS_MAPPING)
